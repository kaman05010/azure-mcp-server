# Development Guide

## Setting Up Development Environment

### Prerequisites
- Python 3.10+
- Node.js 16+
- Azure CLI
- Git

### Initial Setup

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd azuremcpserver
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

3. **Azure authentication:**
   ```bash
   az login
   ```

## Code Structure

### Main Components

#### `azure_mcp_server.py`
- **Purpose**: Main server implementation
- **Key Functions**: 
  - `run()`: Main async orchestrator
  - Authentication setup
  - MCP client management
  - Conversation loop

#### `test_azure_mcp_server.py`
- **Purpose**: Comprehensive unit tests
- **Coverage**: All major functionality
- **Mocking**: Azure services, MCP server, user input

### Design Patterns

#### Async Context Managers
```python
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Operations within context
```

#### Error Handling Strategy
```python
try:
    # Risky operation
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    # Handle gracefully
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Continue or raise as appropriate
```

## Testing Strategy

### Test Structure
- **Unit tests**: Individual component testing
- **Integration tests**: MCP server interaction testing
- **Mock testing**: Azure services and external dependencies

### Running Tests

```bash
# All tests
python -m pytest src/mcp_server/test_azure_mcp_server.py -v

# Specific test
python -m pytest src/mcp_server/test_azure_mcp_server.py::test_run_initialization -v

# With coverage
python -m pytest --cov=src/mcp_server/ --cov-report=html
```

### Test Categories

#### 1. Initialization Tests
```python
@pytest.mark.asyncio
async def test_run_initialization():
    # Test component initialization
    # Verify Azure client creation
    # Confirm MCP session setup
```

#### 2. Tool Interaction Tests
```python
@pytest.mark.asyncio
async def test_run_with_tool_calls():
    # Test tool discovery
    # Test tool execution
    # Verify response handling
```

#### 3. Error Handling Tests
```python
@pytest.mark.asyncio
async def test_run_error_handling():
    # Test connection failures
    # Test API errors
    # Test graceful degradation
```

### Mocking Strategies

#### Azure OpenAI Client
```python
with patch('azure_mcp_server.AzureOpenAI') as mock_client:
    client = Mock()
    client.chat.completions.create.return_value = mock_response
    mock_client.return_value = client
```

#### MCP Server Connection
```python
with patch('azure_mcp_server.stdio_client') as mock_stdio:
    mock_stdio.return_value.__aenter__ = AsyncMock(return_value=(read, write))
```

## Code Quality Standards

### Style Guidelines
- **PEP 8**: Follow Python style guide
- **Type hints**: Use where beneficial
- **Docstrings**: Document public functions
- **Async/await**: Consistent async patterns

### Code Review Checklist

#### Functionality
- [ ] Does the code solve the intended problem?
- [ ] Are edge cases handled appropriately?
- [ ] Is error handling comprehensive?

#### Quality
- [ ] Is the code readable and well-structured?
- [ ] Are there appropriate comments/docstrings?
- [ ] Are variables and functions well-named?

#### Testing
- [ ] Are there adequate unit tests?
- [ ] Do tests cover error scenarios?
- [ ] Are mocks appropriate and realistic?

#### Performance
- [ ] Are async operations properly awaited?
- [ ] Are resources properly cleaned up?
- [ ] Is memory usage reasonable?

## Adding New Features

### 1. New Tool Support

To add support for additional Azure MCP tools:

```python
# Tool will be automatically discovered via MCP
# No code changes needed in most cases
# Tools are dynamically loaded from MCP server
```

### 2. Enhanced Error Handling

```python
# Add specific exception handling
try:
    result = await operation()
except SpecificAzureException as e:
    # Handle Azure-specific errors
    logger.error(f"Azure error: {e}")
except MCPException as e:
    # Handle MCP-specific errors
    logger.error(f"MCP error: {e}")
```

### 3. Additional Authentication Methods

```python
# Add custom credential providers
if custom_auth_enabled:
    credential = CustomCredential()
else:
    credential = DefaultAzureCredential()
```

## Debugging

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Common Debug Points

1. **Azure Authentication Issues**
   ```bash
   az account show  # Verify login
   az account list  # Check available subscriptions
   ```

2. **MCP Server Connection**
   ```bash
   npx @azure/mcp@latest server start  # Test MCP server manually
   ```

3. **Environment Variables**
   ```python
   print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
   print(f"Model: {os.getenv('AZURE_OPENAI_MODEL')}")
   ```

### Performance Monitoring

#### Memory Usage
```python
import psutil
import os

process = psutil.Process(os.getpid())
memory_info = process.memory_info()
print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
```

#### Async Performance
```python
import asyncio
import time

start_time = time.time()
await async_operation()
duration = time.time() - start_time
logger.info(f"Operation took {duration:.2f} seconds")
```

## Release Process

### Version Management
1. Update version in `setup.py` or `pyproject.toml`
2. Update `CHANGELOG.md`
3. Tag release: `git tag v1.0.0`
4. Push tags: `git push --tags`

### Pre-release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Dependencies updated
- [ ] Security scan completed
- [ ] Performance benchmarks run

### Deployment
1. **Development**: Direct run from source
2. **Staging**: Docker container deployment
3. **Production**: Azure Container Instances or similar

## Contributing

### Pull Request Process
1. Fork repository
2. Create feature branch: `git checkout -b feature-name`
3. Implement changes with tests
4. Run full test suite
5. Update documentation
6. Submit PR with clear description

### Code Review Process
1. Automated checks (CI/CD)
2. Peer review
3. Maintainer review
4. Merge approval

## Resources

### Documentation
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Azure OpenAI Documentation](https://docs.microsoft.com/azure/ai-services/openai/)
- [Azure Identity Documentation](https://docs.microsoft.com/python/api/overview/azure/identity-readme)

### Tools
- **IDE**: VS Code with Python extension
- **Testing**: pytest, pytest-asyncio
- **Linting**: flake8, black
- **Type checking**: mypy