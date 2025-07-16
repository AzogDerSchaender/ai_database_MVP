# Shared Global Context

#### General Resources
- [Python Documentation](https://docs.python.org/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)
- [OWASP Security Guidelines](https://owasp.org/)
- [Python Packaging User Guide](https://packaging.python.org/)


#### Common Patterns
##### Agent Pattern
```python
class MyAgent(BaseAgent):
    async def initialize(self) -> None:
        await super().initialize()

    async def process_message(self, message: Message) -> Response:
        # Your logic here
        return Response(data={})
```

##### API Endpoint Pattern
```python
@router.post('/endpoint', response_model=ResponseModel)
async def endpoint(request: RequestModel) -> ResponseModel:
    # Validate and process
    return ResponseModel()
```

##### Async Service Pattern
```python
class Service:
    async def process(self, data):
        # Business logic
        return data
```
