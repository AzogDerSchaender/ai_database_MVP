"""
Message types and schemas for multi-agent communication system.

This module defines all message types used in the system including:
- Base message classes
- Agent-specific request/response types
- Error and status messages
- Context sharing messages
- Validation schemas using Pydantic
"""

import enum
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from dataclasses import field

from pydantic import BaseModel, Field, field_validator, ConfigDict

# import structlog

# logger = structlog.get_logger(__name__)


class MessagePriority(enum.IntEnum):
    """Message priority levels for queue ordering."""

    CRITICAL = 1  # System-critical messages
    HIGH = 2  # Important agent communications
    NORMAL = 3  # Standard operations
    LOW = 4  # Background tasks
    DEFERRED = 5  # Can be delayed


class MessageStatus(enum.Enum):
    """Message lifecycle status."""

    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"
    DEAD_LETTER = "dead_letter"


class MessageType(enum.Enum):
    """Types of messages in the system."""

    AGENT_REQUEST = "agent_request"
    AGENT_RESPONSE = "agent_response"
    ERROR = "error"
    STATUS = "status"
    CONTEXT = "context"
    HEARTBEAT = "heartbeat"
    CONTROL = "control"


class StandardMessage(BaseModel):
    """
    Base message class for all inter-agent communication.

    Attributes:
        id: Unique message identifier
        type: Message type enumeration
        sender: Sender agent/component ID
        recipient: Target agent/component ID (None for broadcast)
        timestamp: Message creation timestamp
        priority: Message priority for queue ordering
        ttl: Time-to-live in seconds (None = no expiry)
        correlation_id: ID for tracking related messages
        metadata: Additional message metadata
        retry_count: Number of delivery attempts
        max_retries: Maximum retry attempts allowed
    """

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    sender: str
    recipient: Optional[str] = None  # None = broadcast
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    priority: MessagePriority = MessagePriority.NORMAL
    ttl: Optional[int] = Field(default=300, ge=0)  # 5 minutes default
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(cls, v):
        """Ensure metadata doesn't exceed size limits."""
        # Serialize to check size
        serialized = json.dumps(v)
        if len(serialized.encode("utf-8")) > 512:  # 512 bytes limit
            raise ValueError("Metadata exceeds 512 bytes limit")
        return v

    def is_expired(self) -> bool:
        """Check if message has expired based on TTL."""
        if self.ttl is None:
            return False
        elapsed = (datetime.now(timezone.utc) - self.timestamp).total_seconds()
        return elapsed > self.ttl

    def should_retry(self) -> bool:
        """Check if message should be retried."""
        return self.retry_count < self.max_retries

    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return self.model_dump()

    def serialize(self) -> bytes:
        """Serialize message to bytes for persistence."""
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> "StandardMessage":
        """Deserialize message from bytes."""
        return cls.model_validate_json(data)

    def get_size_bytes(self) -> int:
        """Get message size in bytes."""
        return len(self.serialize())


class AgentRequest(StandardMessage):
    """
    Request message from one agent to another.

    Attributes:
        action: Requested action/operation
        payload: Request data payload
        requires_response: Whether a response is expected
        timeout: Response timeout in seconds
    """

    type: MessageType = MessageType.AGENT_REQUEST
    action: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    requires_response: bool = True
    timeout: int = Field(default=30, ge=1)  # 30 seconds default

    @field_validator("action")
    @classmethod
    def validate_action(cls, v):
        """Validate action is not empty."""
        if not v or not v.strip():
            raise ValueError("Action cannot be empty")
        return v.strip()


class AgentResponse(StandardMessage):
    """
    Response message from agent.

    Attributes:
        request_id: ID of the original request
        status_code: Response status code (HTTP-style)
        result: Response data
        error: Error details if failed
        processing_time_ms: Time taken to process request
    """

    type: MessageType = MessageType.AGENT_RESPONSE
    request_id: str
    status_code: int = Field(ge=100, le=599)
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    processing_time_ms: Optional[float] = None

    @field_validator("status_code")
    @classmethod
    def validate_status_code(cls, v):
        """Ensure valid HTTP-style status code."""
        if v < 100 or v > 599:
            raise ValueError(f"Invalid status code: {v}")
        return v

    @property
    def is_success(self) -> bool:
        """Check if response indicates success."""
        return 200 <= self.status_code < 300

    @property
    def is_error(self) -> bool:
        """Check if response indicates error."""
        return self.status_code >= 400


class ErrorMessage(StandardMessage):
    """
    Error message for system errors and failures.

    Attributes:
        error_code: Specific error code
        error_type: Type/category of error
        error_message: Human-readable error message
        stack_trace: Optional stack trace for debugging
        context: Additional error context
        recoverable: Whether error is recoverable
    """

    type: MessageType = MessageType.ERROR
    error_code: str
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    recoverable: bool = True

    @field_validator("error_message")
    @classmethod
    def validate_error_message(cls, v):
        """Ensure error message is not empty."""
        if not v or not v.strip():
            raise ValueError("Error message cannot be empty")
        return v.strip()

    @field_validator("stack_trace")
    @classmethod
    def sanitize_stack_trace(cls, v):
        """Remove sensitive information from stack trace."""
        if v is None:
            return v
        # Remove file paths that might reveal system structure
        import re

        # Keep only relative paths and line numbers
        sanitized = re.sub(r"(/[^/\s]+)+/", "", v)
        return sanitized


class StatusMessage(StandardMessage):
    """
    Status update message for monitoring and health checks.

    Attributes:
        status: Current status
        component: Component reporting status
        health_score: Health score (0-100)
        metrics: Performance/health metrics
        details: Additional status details
    """

    type: MessageType = MessageType.STATUS
    status: str
    component: str
    health_score: float = Field(ge=0, le=100)
    metrics: Dict[str, Union[int, float]] = Field(default_factory=dict)
    details: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("health_score")
    @classmethod
    def validate_health_score(cls, v):
        """Ensure health score is in valid range."""
        if v < 0 or v > 100:
            raise ValueError(f"Health score must be 0-100, got {v}")
        return v


class ContextMessage(StandardMessage):
    """
    Context sharing message for state synchronization.

    Attributes:
        context_type: Type of context being shared
        context_data: The context data
        version: Context version for consistency
        merge_strategy: How to merge with existing context
        expires_at: When context expires
    """

    type: MessageType = MessageType.CONTEXT
    context_type: str
    context_data: Dict[str, Any]
    version: int = Field(ge=1)
    merge_strategy: str = "replace"  # replace, merge, append
    expires_at: Optional[datetime] = None

    @field_validator("merge_strategy")
    @classmethod
    def validate_merge_strategy(cls, v):
        """Validate merge strategy."""
        valid_strategies = {"replace", "merge", "append"}
        if v not in valid_strategies:
            raise ValueError(f"Invalid merge strategy: {v}")
        return v

    @field_validator("context_data")
    @classmethod
    def validate_context_size(cls, v):
        """Ensure context data doesn't exceed limits."""
        serialized = json.dumps(v)
        if len(serialized.encode("utf-8")) > 10240:  # 10KB limit
            raise ValueError("Context data exceeds 10KB limit")
        return v

    def is_valid(self) -> bool:
        """Check if context is still valid."""
        if self.expires_at is None:
            return True
        return datetime.now(timezone.utc) < self.expires_at


# Message validation schemas
class MessageValidator:
    """Validates messages for correctness and security."""

    @staticmethod
    def validate_message(message: StandardMessage) -> List[str]:
        """
        Validate a message and return list of validation errors.

        Args:
            message: Message to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Check message size
        try:
            size = message.get_size_bytes()
            if size > 1024:  # 1KB limit
                errors.append(f"Message size {size} bytes exceeds 1KB limit")
        except Exception as e:
            errors.append(f"Failed to calculate message size: {str(e)}")

        # Check expiry
        if message.is_expired():
            errors.append("Message has expired")

        # Validate sender/recipient
        if not message.sender:
            errors.append("Message must have a sender")

        # Type-specific validation
        if isinstance(message, AgentRequest):
            if message.requires_response and not message.recipient:
                errors.append("Request requiring response must have specific recipient")

        elif isinstance(message, AgentResponse):
            if not message.request_id:
                errors.append("Response must reference a request ID")

        elif isinstance(message, ErrorMessage):
            if not message.error_code:
                errors.append("Error message must have error code")

        return errors

    @staticmethod
    def is_valid(message: StandardMessage) -> bool:
        """Check if message is valid."""
        return len(MessageValidator.validate_message(message)) == 0


# Type definitions for better IDE support
MessageUnion = Union[AgentRequest, AgentResponse, ErrorMessage, StatusMessage, ContextMessage]


# Factory function for creating messages from dict
def create_message(data: Dict[str, Any]) -> StandardMessage:
    """
    Create appropriate message instance from dictionary data.

    Args:
        data: Message data dictionary

    Returns:
        Appropriate message instance

    Raises:
        ValueError: If message type is invalid
    """
    msg_type = data.get("type")
    if msg_type is None:
        raise ValueError("Message type is required")

    type_map = {
        MessageType.AGENT_REQUEST.value: AgentRequest,
        MessageType.AGENT_RESPONSE.value: AgentResponse,
        MessageType.ERROR.value: ErrorMessage,
        MessageType.STATUS.value: StatusMessage,
        MessageType.CONTEXT.value: ContextMessage,
    }

    message_class = type_map.get(msg_type)
    if not message_class:
        raise ValueError(f"Unknown message type: {msg_type}")

    return message_class(**data)
