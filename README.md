# Azure MCP Server

A Python-based Model Context Protocol (MCP) server that integrates Azure OpenAI with Azure MCP tools to provide intelligent conversational AI capabilities with access to Azure services.

## Overview

This project creates a bridge between Azure OpenAI and Azure MCP tools, enabling AI conversations that can dynamically call Azure services through MCP tool integration. The server handles tool calls, manages conversation context, and provides a seamless chat interface.

## Features

- **Azure OpenAI Integration**: Uses Azure OpenAI GPT models for conversational AI
- **MCP Tool Support**: Connects to Azure MCP server for tool execution
- **Authentication**: Leverages Azure Identity for secure authentication
- **Async Architecture**: Built with asyncio for efficient concurrent operations
- **Interactive Chat**: Command-line interface for real-time conversations
- **Error Handling**: Comprehensive error handling and logging

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Azure MCP       │───▶│  Azure OpenAI   │
│                 │    │  Server          │    │  Service        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   MCP Tools      │    │  AI Response    │
                       │   (Azure Services)│    │                 │
                       └──────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.10 or higher (required for MCP package)
- Node.js and npm (for Azure MCP server)
- Azure OpenAI resource
- Azure CLI (for authentication)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd azuremcpserver
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies (for MCP server):**
   ```bash
   # Node.js will be used automatically via npx
   # Ensure you have Node.js installed
   node --version
   npm --version
   ```

## Configuration

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables:**
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_MODEL=gpt-4
   ```

3. **Authenticate with Azure:**
   ```bash
   az login
   ```

## Usage

### Running the Server

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
python src/mcp_server/azure_mcp_server.py
```

### Interactive Chat

Once running, the server will:

1. Initialize Azure OpenAI client
2. Connect to Azure MCP server
3. List available tools
4. Start interactive chat loop

Example interaction:
```
Available tools:
- azure_storage_list
- azure_keyvault_get
- azure_vm_status

Prompt: List all storage accounts in my subscription
AI: I'll help you list the storage accounts. Let me use the Azure storage tool...

[Tool execution and response]
```

## Project Structure

```
azuremcpserver/
├── src/
│   └── mcp_server/
│       ├── azure_mcp_server.py      # Main server implementation
│       └── test_azure_mcp_server.py # Unit tests
├── requirements.txt                  # Python dependencies
├── .env.example                     # Environment template
├── .env                            # Environment variables (create this)
├── README.md                       # This file
└── docs/                          # Additional documentation
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest src/mcp_server/test_azure_mcp_server.py -v

# Run with coverage
python -m pytest src/mcp_server/test_azure_mcp_server.py -v --cov=src/mcp_server/

# Run specific test
python -m pytest src/mcp_server/test_azure_mcp_server.py::test_run_initialization -v
```

### Code Style

The project follows Python best practices:
- Type hints where applicable
- Async/await for asynchronous operations
- Comprehensive error handling
- Logging for debugging and monitoring

## API Reference

### Main Functions

#### `run()`
Main async function that orchestrates the MCP server operation.

**Functionality:**
- Initializes Azure OpenAI client
- Connects to MCP server via stdio
- Manages conversation loop
- Handles tool calls and responses

#### Key Components

- **Azure OpenAI Client**: Handles AI model interactions
- **MCP Client Session**: Manages MCP server communication
- **Tool Management**: Discovers and executes available tools
- **Conversation Loop**: Maintains chat context and history

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError for 'azure'**
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

2. **MCP package requires Python 3.10+**
   - Install Python 3.10 or higher
   - Create new virtual environment with correct Python version

3. **npx command not found**
   - Install Node.js: `brew install node` (macOS) or equivalent
   - Verify installation: `npx --version`

4. **Azure authentication errors**
   - Run `az login` to authenticate
   - Verify Azure CLI is installed and configured

### Debug Mode

Enable detailed logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Azure OpenAI and MCP documentation