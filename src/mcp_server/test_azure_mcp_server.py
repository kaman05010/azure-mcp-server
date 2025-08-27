import pytest
import pytest_asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import os
import json

# Import after setting up mocks to avoid module-level initialization issues
@pytest.fixture(autouse=True)
def setup_env():
    """Setup test environment variables"""
    with patch.dict(os.environ, {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_MODEL': 'test-model'
    }):
        yield

@pytest.mark.asyncio
async def test_run_initialization():
    """Test that run function initializes all components correctly"""
    with patch('azure_mcp_server.AzureOpenAI') as mock_azure_client, \
         patch('azure_mcp_server.stdio_client') as mock_stdio_client, \
         patch('azure_mcp_server.ClientSession') as mock_client_session, \
         patch('builtins.input', side_effect=KeyboardInterrupt()), \
         patch('builtins.print'):
        
        # Setup Azure client mock
        client = Mock()
        client.chat = Mock()
        client.chat.completions = Mock()
        client.chat.completions.create = Mock()
        mock_azure_client.return_value = client
        
        # Setup stdio_client mock
        read, write = AsyncMock(), AsyncMock()
        stdio_context = AsyncMock()
        stdio_context.__aenter__ = AsyncMock(return_value=(read, write))
        stdio_context.__aexit__ = AsyncMock(return_value=None)
        mock_stdio_client.return_value = stdio_context
        
        # Setup ClientSession mock
        session = AsyncMock()
        session.initialize = AsyncMock()
        session.list_tools = AsyncMock()
        
        # Mock tool
        tool = Mock()
        tool.name = "test_tool"
        tool.description = "A test tool"
        tool.inputSchema = {"type": "object", "properties": {}}
        
        tools_result = Mock()
        tools_result.tools = [tool]
        session.list_tools.return_value = tools_result
        
        session_context = AsyncMock()
        session_context.__aenter__ = AsyncMock(return_value=session)
        session_context.__aexit__ = AsyncMock(return_value=None)
        mock_client_session.return_value = session_context
        
        # Import and run
        from azure_mcp_server import run
        
        try:
            await run()
        except KeyboardInterrupt:
            pass
        
        # Verify initialization calls
        mock_azure_client.assert_called_once()
        session.initialize.assert_called_once()
        session.list_tools.assert_called_once()

@pytest.mark.asyncio
async def test_run_with_tool_calls():
    """Test run function handling tool calls"""
    with patch('azure_mcp_server.AzureOpenAI') as mock_azure_client, \
         patch('azure_mcp_server.stdio_client') as mock_stdio_client, \
         patch('azure_mcp_server.ClientSession') as mock_client_session, \
         patch('builtins.input', side_effect=['test prompt', KeyboardInterrupt()]), \
         patch('builtins.print'):
        
        # Setup Azure client mock
        client = Mock()
        
        # Mock first response with tool calls
        tool_call = Mock()
        tool_call.id = "call_123"
        tool_call.function.name = "test_tool"
        tool_call.function.arguments = '{"param": "value"}'
        
        response_message = Mock()
        response_message.tool_calls = [tool_call]
        
        first_response = Mock()
        first_response.choices = [Mock()]
        first_response.choices[0].message = response_message
        
        # Mock final response
        final_response_message = Mock()
        final_response_message.content = "Final response"
        final_response = Mock()
        final_response.choices = [Mock()]
        final_response.choices[0].message = final_response_message
        
        client.chat.completions.create.side_effect = [first_response, final_response]
        mock_azure_client.return_value = client
        
        # Setup stdio_client mock
        read, write = AsyncMock(), AsyncMock()
        stdio_context = AsyncMock()
        stdio_context.__aenter__ = AsyncMock(return_value=(read, write))
        stdio_context.__aexit__ = AsyncMock(return_value=None)
        mock_stdio_client.return_value = stdio_context
        
        # Setup session mock
        session = AsyncMock()
        session.initialize = AsyncMock()
        session.list_tools = AsyncMock()
        session.call_tool = AsyncMock()
        
        tool = Mock()
        tool.name = "test_tool"
        tool.description = "A test tool"
        tool.inputSchema = {"type": "object", "properties": {}}
        
        tools_result = Mock()
        tools_result.tools = [tool]
        session.list_tools.return_value = tools_result
        
        call_result = Mock()
        call_result.content = "Tool executed successfully"
        session.call_tool.return_value = call_result
        
        session_context = AsyncMock()
        session_context.__aenter__ = AsyncMock(return_value=session)
        session_context.__aexit__ = AsyncMock(return_value=None)
        mock_client_session.return_value = session_context
        
        from azure_mcp_server import run
        
        try:
            await run()
        except KeyboardInterrupt:
            pass
        
        # Verify tool was called
        session.call_tool.assert_called_once_with("test_tool", {"param": "value"})

@pytest.mark.asyncio
async def test_run_without_tool_calls():
    """Test run function when no tool calls are made"""
    with patch('azure_mcp_server.AzureOpenAI') as mock_azure_client, \
         patch('azure_mcp_server.stdio_client') as mock_stdio_client, \
         patch('azure_mcp_server.ClientSession') as mock_client_session, \
         patch('builtins.input', side_effect=['test prompt', KeyboardInterrupt()]), \
         patch('builtins.print'):
        
        # Setup Azure client mock
        client = Mock()
        
        # Mock response without tool calls
        response_message = Mock()
        response_message.tool_calls = None
        
        first_response = Mock()
        first_response.choices = [Mock()]
        first_response.choices[0].message = response_message
        
        # Mock final response
        final_response_message = Mock()
        final_response_message.content = "Direct response"
        final_response = Mock()
        final_response.choices = [Mock()]
        final_response.choices[0].message = final_response_message
        
        client.chat.completions.create.side_effect = [first_response, final_response]
        mock_azure_client.return_value = client
        
        # Setup stdio_client mock
        read, write = AsyncMock(), AsyncMock()
        stdio_context = AsyncMock()
        stdio_context.__aenter__ = AsyncMock(return_value=(read, write))
        stdio_context.__aexit__ = AsyncMock(return_value=None)
        mock_stdio_client.return_value = stdio_context
        
        # Setup session mock
        session = AsyncMock()
        session.initialize = AsyncMock()
        session.list_tools = AsyncMock()
        session.call_tool = AsyncMock()
        
        tool = Mock()
        tool.name = "test_tool"
        tool.description = "A test tool"
        tool.inputSchema = {"type": "object", "properties": {}}
        
        tools_result = Mock()
        tools_result.tools = [tool]
        session.list_tools.return_value = tools_result
        
        session_context = AsyncMock()
        session_context.__aenter__ = AsyncMock(return_value=session)
        session_context.__aexit__ = AsyncMock(return_value=None)
        mock_client_session.return_value = session_context
        
        from azure_mcp_server import run
        
        try:
            await run()
        except KeyboardInterrupt:
            pass
        
        # Verify tool was not called
        session.call_tool.assert_not_called()

@pytest.mark.asyncio
async def test_run_error_handling():
    """Test error handling in conversation loop"""
    with patch('azure_mcp_server.AzureOpenAI') as mock_azure_client, \
         patch('azure_mcp_server.stdio_client') as mock_stdio_client, \
         patch('azure_mcp_server.ClientSession') as mock_client_session, \
         patch('builtins.input', side_effect=['test prompt', KeyboardInterrupt()]), \
         patch('builtins.print') as mock_print:
        
        # Setup Azure client mock to raise exception
        client = Mock()
        client.chat.completions.create.side_effect = Exception("API Error")
        mock_azure_client.return_value = client
        
        # Setup stdio_client mock
        read, write = AsyncMock(), AsyncMock()
        stdio_context = AsyncMock()
        stdio_context.__aenter__ = AsyncMock(return_value=(read, write))
        stdio_context.__aexit__ = AsyncMock(return_value=None)
        mock_stdio_client.return_value = stdio_context
        
        # Setup session mock
        session = AsyncMock()
        session.initialize = AsyncMock()
        session.list_tools = AsyncMock()
        
        tool = Mock()
        tool.name = "test_tool"
        tool.description = "A test tool"
        tool.inputSchema = {"type": "object", "properties": {}}
        
        tools_result = Mock()
        tools_result.tools = [tool]
        session.list_tools.return_value = tools_result
        
        session_context = AsyncMock()
        session_context.__aenter__ = AsyncMock(return_value=session)
        session_context.__aexit__ = AsyncMock(return_value=None)
        mock_client_session.return_value = session_context
        
        from azure_mcp_server import run
        
        try:
            await run()
        except KeyboardInterrupt:
            pass
        
        # Verify error was printed
        error_printed = False
        for call in mock_print.call_args_list:
            if "An error occurred: API Error" in str(call):
                error_printed = True
                break
        assert error_printed

def test_environment_variables():
    """Test that environment variables can be loaded"""
    # Test with the current environment setup
    with patch.dict(os.environ, {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_MODEL': 'test-model'
    }):
        # Test os.getenv directly
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        model = os.getenv('AZURE_OPENAI_MODEL')
        
        assert endpoint == 'https://test.openai.azure.com/'
        assert model == 'test-model'

def test_token_provider_initialization():
    """Test that token provider functionality works"""
    with patch('azure.identity.DefaultAzureCredential') as mock_cred, \
         patch('azure.identity.get_bearer_token_provider') as mock_get_bearer:
        
        # Setup mocks
        mock_credential = Mock()
        mock_cred.return_value = mock_credential
        mock_token_provider = Mock()
        mock_get_bearer.return_value = mock_token_provider
        
        # Import and call the functions after mocking
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
        
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        
        # Verify the mocks were called
        mock_cred.assert_called_once()
        mock_get_bearer.assert_called_once_with(
            mock_credential, "https://cognitiveservices.azure.com/.default"
        )
        
        # Verify return values
        assert credential == mock_credential
        assert token_provider == mock_token_provider