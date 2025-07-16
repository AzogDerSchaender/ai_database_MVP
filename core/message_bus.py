"""
Async pub/sub message bus for multi-agent communication.

This module implements a high-performance message bus with:
- Async pub/sub messaging
- Priority queue implementation
- Dead letter queue handling
- Message persistence for debugging
- Guaranteed delivery with retry logic
"""

import asyncio
import json
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import heapq
import pickle
import os
from pathlib import Path

# import structlog
from asyncio import Queue, PriorityQueue

from core.message_types import (
    StandardMessage,
    MessageStatus,
    MessagePriority,
    MessageValidator,
    ErrorMessage,
    create_message,
)

# logger = structlog.get_logger(__name__)


class MessageBusError(Exception):
    """Base exception for message bus errors."""

    pass


class DeliveryError(MessageBusError):
    """Raised when message delivery fails."""

    pass


class QueueOverflowError(MessageBusError):
    """Raised when queue capacity is exceeded."""

    pass


class MessageCorruptionError(MessageBusError):
    """Raised when message is corrupted."""

    pass


class MessageSubscription:
    """Represents a subscription to message topics."""

    def __init__(
        self,
        subscriber_id: str,
        callback: Callable,
        topics: Optional[Set[str]] = None,
        message_types: Optional[Set[str]] = None,
        priority_threshold: Optional[MessagePriority] = None,
    ):
        self.subscriber_id = subscriber_id
        self.callback = callback
        self.topics = topics or set()
        self.message_types = message_types or set()
        self.priority_threshold = priority_threshold
        self.is_active = True
        self.message_count = 0
        self.error_count = 0
        self.last_message_time: Optional[datetime] = None

    def matches(self, message: StandardMessage) -> bool:
        """Check if message matches subscription criteria."""
        if not self.is_active:
            return False

        # Check priority threshold
        if self.priority_threshold and message.priority > self.priority_threshold:
            return False

        # Check message type
        if self.message_types:
            # Convert enum to its value for comparison
            message_type_value = (
                message.type.value if hasattr(message.type, "value") else str(message.type)
            )
            if message_type_value not in self.message_types:
                return False

        # Check topics (in metadata)
        if self.topics:
            message_topics = message.metadata.get("topics", [])
            if not any(topic in message_topics for topic in self.topics):
                return False

        return True


class PersistentQueue:
    """Queue with optional persistence to disk."""

    def __init__(self, name: str, max_size: int = 10000, persist_path: Optional[Path] = None):
        self.name = name
        self.max_size = max_size
        self.persist_path = persist_path
        self._queue: List[Tuple[float, float, StandardMessage]] = []
        self._lock = asyncio.Lock()

        # Load persisted messages if path exists
        if persist_path and persist_path.exists():
            self._load_from_disk()

    async def put(self, message: StandardMessage) -> None:
        """Add message to queue with priority ordering."""
        async with self._lock:
            if len(self._queue) >= self.max_size:
                raise QueueOverflowError(f"Queue {self.name} is at capacity ({self.max_size})")

            # Use negative priority for min heap (lower priority value = higher priority)
            priority_value = float(
                message.priority if isinstance(message.priority, int) else message.priority.value
            )
            timestamp = time.time()
            heapq.heappush(self._queue, (priority_value, timestamp, message))

            # Persist if enabled
            if self.persist_path:
                await self._persist_to_disk()

    async def get(self) -> Optional[StandardMessage]:
        """Get highest priority message from queue."""
        async with self._lock:
            if not self._queue:
                return None

            _, _, message = heapq.heappop(self._queue)

            # Persist updated queue if enabled
            if self.persist_path:
                await self._persist_to_disk()

            return message

    async def peek(self) -> Optional[StandardMessage]:
        """Peek at highest priority message without removing."""
        async with self._lock:
            if not self._queue:
                return None
            return self._queue[0][2]

    async def size(self) -> int:
        """Get current queue size."""
        async with self._lock:
            return len(self._queue)

    async def clear(self) -> None:
        """Clear all messages from queue."""
        async with self._lock:
            self._queue.clear()
            if self.persist_path and self.persist_path.exists():
                self.persist_path.unlink()

    async def _persist_to_disk(self) -> None:
        """Persist queue to disk."""
        if not self.persist_path:
            return

        try:
            # Create directory if needed
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)

            # Serialize messages
            data = [(p, t, m.model_dump()) for p, t, m in self._queue]

            # Write atomically
            temp_path = self.persist_path.with_suffix(".tmp")
            with open(temp_path, "wb") as f:
                pickle.dump(data, f)
            temp_path.replace(self.persist_path)

        except Exception as e:
            # logger.error(f"Failed to persist queue {self.name}: {str(e)}")
            pass

    def _load_from_disk(self) -> None:
        """Load queue from disk."""
        if not self.persist_path or not self.persist_path.exists():
            return

        try:
            with open(self.persist_path, "rb") as f:
                data = pickle.load(f)

            # Reconstruct messages
            self._queue = []
            for priority, timestamp, msg_data in data:
                try:
                    message = create_message(msg_data)
                    heapq.heappush(self._queue, (priority, timestamp, message))
                except Exception as e:
                    # logger.error(f"Failed to restore message: {str(e)}")
                    pass

        except Exception as e:
            # logger.error(f"Failed to load queue {self.name} from disk: {str(e)}")
            pass


class MessageBus:
    """
    High-performance async message bus for agent communication.

    Features:
    - Async pub/sub with topic and type filtering
    - Priority queue processing
    - Dead letter queue for failed messages
    - Message persistence and replay
    - Delivery guarantees with retry logic
    """

    def __init__(
        self,
        max_queue_size: int = 10000,
        max_dead_letter_size: int = 1000,
        persistence_dir: Optional[Path] = None,
        enable_persistence: bool = True,
    ):
        # Configuration
        self.max_queue_size = max_queue_size
        self.max_dead_letter_size = max_dead_letter_size
        self.persistence_dir = persistence_dir or Path("data/message_bus")
        self.enable_persistence = enable_persistence

        # Message queues
        self.main_queue = PersistentQueue(
            "main",
            max_queue_size,
            self.persistence_dir / "main_queue.pkl" if enable_persistence else None,
        )
        self.dead_letter_queue = PersistentQueue(
            "dead_letter",
            max_dead_letter_size,
            self.persistence_dir / "dlq.pkl" if enable_persistence else None,
        )

        # Subscriptions
        self.subscriptions: Dict[str, MessageSubscription] = {}
        self._subscription_lock = asyncio.Lock()

        # Metrics
        self.metrics = {
            "messages_published": 0,
            "messages_delivered": 0,
            "messages_failed": 0,
            "messages_dlq": 0,
            "delivery_errors": 0,
            "queue_overflows": 0,
            "avg_latency_ms": 0.0,
            "throughput_per_sec": 0.0,
        }
        self._latency_samples: deque = deque(maxlen=1000)
        self._throughput_window: deque = deque(maxlen=60)  # 1 minute window

        # Processing state
        self._running = False
        self._process_task: Optional[asyncio.Task] = None

        # Persistence
        if enable_persistence:
            self.persistence_dir.mkdir(parents=True, exist_ok=True)

    async def start(self) -> None:
        """Start the message bus processing."""
        if self._running:
            return

        self._running = True
        self._process_task = asyncio.create_task(self._process_messages())
        # logger.info("Message bus started")

    async def stop(self) -> None:
        """Stop the message bus processing."""
        self._running = False

        if self._process_task:
            self._process_task.cancel()
            try:
                await self._process_task
            except asyncio.CancelledError:
                pass

        # Persist final state
        await self._persist_metrics()

        # logger.info("Message bus stopped")

    async def publish(self, message: StandardMessage, validate: bool = True) -> None:
        """
        Publish a message to the bus.

        Args:
            message: Message to publish
            validate: Whether to validate message before publishing

        Raises:
            MessageCorruptionError: If message validation fails
            QueueOverflowError: If queue is full
        """
        start_time = time.time()

        try:
            # Validate message if requested
            if validate:
                errors = MessageValidator.validate_message(message)
                if errors:
                    raise MessageCorruptionError(f"Message validation failed: {', '.join(errors)}")

            # Add to queue
            await self.main_queue.put(message)

            # Update metrics
            self.metrics["messages_published"] += 1
            self._throughput_window.append(time.time())

            # Log
            # logger.debug(
            #     "Message published",
            #     message_id=message.id,
            #     type=str(message.type),
            #     priority=message.priority,
            # )

        except QueueOverflowError:
            self.metrics["queue_overflows"] += 1
            raise

        except Exception as e:
            # logger.error(f"Failed to publish message: {str(e)}", message_id=message.id)
            raise

        finally:
            # Record latency
            latency_ms = (time.time() - start_time) * 1000
            self._latency_samples.append(latency_ms)

    async def subscribe(
        self,
        subscriber_id: str,
        callback: Callable[[StandardMessage], None],
        topics: Optional[List[str]] = None,
        message_types: Optional[List[str]] = None,
        priority_threshold: Optional[MessagePriority] = None,
    ) -> None:
        """
        Subscribe to messages.

        Args:
            subscriber_id: Unique subscriber identifier
            callback: Async callback function to handle messages
            topics: List of topics to subscribe to (None = all)
            message_types: List of message types to receive (None = all)
            priority_threshold: Only receive messages at or above this priority
        """
        async with self._subscription_lock:
            subscription = MessageSubscription(
                subscriber_id=subscriber_id,
                callback=callback,
                topics=set(topics) if topics else None,
                message_types=set(message_types) if message_types else None,
                priority_threshold=priority_threshold,
            )

            self.subscriptions[subscriber_id] = subscription

            # logger.info(
            #     "Subscriber registered",
            #     subscriber_id=subscriber_id,
            #     topics=topics,
            #     message_types=message_types,
            # )

    async def unsubscribe(self, subscriber_id: str) -> None:
        """Unsubscribe from messages."""
        async with self._subscription_lock:
            if subscriber_id in self.subscriptions:
                self.subscriptions[subscriber_id].is_active = False
                del self.subscriptions[subscriber_id]
                # logger.info("Subscriber unregistered", subscriber_id=subscriber_id)

    async def _process_messages(self) -> None:
        """Main message processing loop."""
        # logger.info("Message processing started")

        while self._running:
            try:
                # Get next message
                message = await self.main_queue.get()

                if message is None:
                    # No messages, wait a bit
                    await asyncio.sleep(0.001)  # 1ms
                    continue

                # Check if expired
                if message.is_expired():
                    # logger.warning("Message expired", message_id=message.id)
                    await self._send_to_dlq(message, "expired")
                    continue

                # Process message
                await self._deliver_message(message)

                # Update throughput metric
                self._update_throughput()

            except Exception as e:
                # logger.error(f"Error in message processing loop: {str(e)}")
                await asyncio.sleep(0.1)  # Back off on error

    async def _deliver_message(self, message: StandardMessage) -> None:
        """Deliver message to matching subscribers."""
        start_time = time.time()
        delivered_count = 0

        # Find matching subscribers
        matching_subs = []
        async with self._subscription_lock:
            for sub in self.subscriptions.values():
                if sub.matches(message):
                    matching_subs.append(sub)

        # If no subscribers and message has specific recipient, it's an error
        if not matching_subs and message.recipient:
            await self._handle_delivery_failure(
                message, f"No subscriber found for recipient: {message.recipient}"
            )
            return

        # Deliver to each matching subscriber
        delivery_tasks = []
        for sub in matching_subs:
            task = asyncio.create_task(self._deliver_to_subscriber(message, sub))
            delivery_tasks.append(task)

        # Wait for all deliveries
        if delivery_tasks:
            results = await asyncio.gather(*delivery_tasks, return_exceptions=True)

            # Count successful deliveries
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    # logger.error(
                    #     f"Delivery failed to {matching_subs[i].subscriber_id}: {str(result)}"
                    # )
                    pass
                else:
                    delivered_count += 1

        # Update metrics
        if delivered_count > 0:
            self.metrics["messages_delivered"] += delivered_count
            latency_ms = (time.time() - start_time) * 1000
            self._latency_samples.append(latency_ms)
            self._update_avg_latency()
        else:
            # No successful deliveries
            await self._handle_delivery_failure(message, "No successful deliveries")

    async def _deliver_to_subscriber(
        self, message: StandardMessage, subscription: MessageSubscription
    ) -> None:
        """Deliver message to a single subscriber."""
        try:
            # Call the callback
            if asyncio.iscoroutinefunction(subscription.callback):
                await subscription.callback(message)
            else:
                # Run sync callback in executor
                await asyncio.get_event_loop().run_in_executor(None, subscription.callback, message)

            # Update subscription metrics
            subscription.message_count += 1
            subscription.last_message_time = datetime.now(timezone.utc)

        except Exception as e:
            subscription.error_count += 1
            raise DeliveryError(f"Callback error: {str(e)}")

    async def _handle_delivery_failure(self, message: StandardMessage, reason: str) -> None:
        """Handle failed message delivery."""
        self.metrics["messages_failed"] += 1

        # Check if we should retry
        if message.should_retry():
            message.increment_retry()
            # logger.warning(
            #     f"Retrying message delivery (attempt {message.retry_count})",
            #     message_id=message.id,
            #     reason=reason,
            # )

            # Re-queue with slight delay
            await asyncio.sleep(0.1 * message.retry_count)  # Exponential backoff
            await self.main_queue.put(message)
        else:
            # Max retries exceeded, send to DLQ
            await self._send_to_dlq(message, reason)

    async def _send_to_dlq(self, message: StandardMessage, reason: str) -> None:
        """Send message to dead letter queue."""
        try:
            # Add failure metadata
            message.metadata["dlq_reason"] = reason
            message.metadata["dlq_timestamp"] = datetime.now(timezone.utc).isoformat()

            await self.dead_letter_queue.put(message)
            self.metrics["messages_dlq"] += 1

            # logger.error("Message sent to DLQ", message_id=message.id, reason=reason)

        except QueueOverflowError:
            # logger.critical("Dead letter queue full, message lost!", message_id=message.id)
            pass

    def _update_avg_latency(self) -> None:
        """Update average latency metric."""
        if self._latency_samples:
            self.metrics["avg_latency_ms"] = sum(self._latency_samples) / len(self._latency_samples)

    def _update_throughput(self) -> None:
        """Update throughput metric."""
        now = time.time()
        # Remove old entries (older than 1 second)
        cutoff = now - 1.0
        while self._throughput_window and self._throughput_window[0] < cutoff:
            self._throughput_window.popleft()

        self.metrics["throughput_per_sec"] = len(self._throughput_window)

    async def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        metrics = self.metrics.copy()

        # Add queue sizes
        metrics["main_queue_size"] = await self.main_queue.size()
        metrics["dlq_size"] = await self.dead_letter_queue.size()

        # Add subscription info
        async with self._subscription_lock:
            metrics["active_subscriptions"] = len(self.subscriptions)

        return metrics

    async def _persist_metrics(self) -> None:
        """Persist metrics to disk."""
        if not self.enable_persistence:
            return

        try:
            metrics_file = self.persistence_dir / "metrics.json"
            with open(metrics_file, "w") as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            # logger.error(f"Failed to persist metrics: {str(e)}")
            pass

    async def replay_dlq(self, limit: Optional[int] = None) -> int:
        """
        Replay messages from dead letter queue.

        Args:
            limit: Maximum number of messages to replay (None = all)

        Returns:
            Number of messages replayed
        """
        count = 0

        while True:
            if limit and count >= limit:
                break

            message = await self.dead_letter_queue.get()
            if message is None:
                break

            # Reset retry count
            message.retry_count = 0
            message.metadata.pop("dlq_reason", None)
            message.metadata.pop("dlq_timestamp", None)

            # Re-publish
            await self.publish(message, validate=False)
            count += 1

        # logger.info(f"Replayed {count} messages from DLQ")
        return count


# Singleton instance
_message_bus: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """Get the singleton message bus instance."""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus()
    return _message_bus


async def initialize_message_bus(**kwargs) -> MessageBus:
    """Initialize and start the message bus."""
    global _message_bus
    _message_bus = MessageBus(**kwargs)
    await _message_bus.start()
    return _message_bus
