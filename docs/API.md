# API Documentation

## Azure MCP Server API Reference

### Core Classes and Functions

#### `run()` - Main Server Function

**Signature:**
```python
async def run() -> None
```

**Description:**
Main asynchronous function that orchestrates the entire MCP server operation.

**Flow:**
1. Initialize Azure OpenAI client with authentication
2. Configure MCP server parameters
3. Establish stdio connection to MCP server
4. Initialize MCP client session
5. Discover and list available tools
6. Start interactive conversation loop
7. Handle tool calls and responses

**Error Handling:**
- Catches and logs connection errors
- Handles authentication failures
- Manages tool execution errors
- Gracefully handles user interruptions (Ctrl+C)

#### Configuration Components

##### Azure OpenAI Client Setup
```python
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT, 
    api_version="2024-04-01-preview", 
    azure_ad_token_provider=token_provider
)
```

**Parameters:**
- `azure_endpoint`: Azure OpenAI resource endpoint
- `api_version`: API version for Azure OpenAI
- `azure_ad_token_provider`: Azure AD token provider for authentication

##### MCP Server Parameters
```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@azure/mcp@latest", "server", "start"],
    env=None
)
```

**Parameters:**
- `command`: Command to execute MCP server
- `args`: Arguments for MCP server startup
- `env`: Environment variables (None uses current environment)

### Tool Management

#### Tool Discovery
```python
tools = await session.list_tools()
for tool in tools.tools:
    print(tool.name)
```

**Returns:**
- List of available MCP tools
- Each tool contains: name, description, inputSchema

#### Tool Formatting for Azure OpenAI
```python
available_tools = [{
    "type": "function",
    "function": {
        "name": tool.name,
        "description": tool.description,
        "parameters": tool.inputSchema
    }
} for tool in tools.tools]
```

#### Tool Execution
```python
result = await session.call_tool(tool_call.function.name, function_args)
```

**Parameters:**
- `tool_call.function.name`: Name of the tool to execute
- `function_args`: Parsed JSON arguments for the tool

**Returns:**
- Tool execution result with content

### Conversation Management

#### Message Structure
```python
messages = [
    {"role": "user", "content": user_input},
    {"role": "assistant", "content": ai_response},
    {"role": "tool", "name": tool_name, "content": tool_result}
]
```

#### Azure OpenAI API Call
```python
response = client.chat.completions.create(
    model=AZURE_OPENAI_MODEL,
    messages=messages,
    tools=available_tools
)
```

#### Tool Call Handling
```python
if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        function_args = json.loads(tool_call.function.arguments)
        result = await session.call_tool(tool_call.function.name, function_args)
        
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": result.content,
        })
```

### Authentication

#### Azure Credential Setup
```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)
```

**Authentication Methods (in order of precedence):**
1. Environment variables
2. Managed Identity
3. Visual Studio Code
4. Azure CLI
5. Azure PowerShell
6. Interactive browser

### Environment Variables

#### Required Variables
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4
```

#### Loading Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
```

### Error Handling Patterns

#### Connection Errors
```python
try:
    async with stdio_client(server_params) as (read, write):
        # ... server operations
except Exception as e:
    logger.error(f"Failed to connect to MCP server: {e}")
```

#### Tool Execution Errors
```python
try:
    result = await session.call_tool(tool_name, args)
except Exception as e:
    logger.error(f"Tool execution failed: {e}")
    # Continue conversation with error message
```

#### API Call Errors
```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"An error occurred: {e}")
    continue  # Continue conversation loop
```

### Async Context Managers

#### Stdio Client Context
```python
async with stdio_client(server_params) as (read, write):
    # read, write are stream objects for MCP communication
```

#### Client Session Context
```python
async with ClientSession(read, write) as session:
    await session.initialize()
    # session is ready for tool discovery and execution
```

### Response Processing

#### Message Processing
```python
response_message = response.choices[0].message
messages.append(response_message)
```

#### Tool Call Extraction
```python
if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        # Process each tool call
```

### Logging Configuration

```python
import logging

logger = logging.getLogger(__name__)
```

**Recommended logging levels:**
- `DEBUG`: Detailed information for debugging
- `INFO`: General information about program execution
- `WARNING`: Warning messages
- `ERROR`: Error messages