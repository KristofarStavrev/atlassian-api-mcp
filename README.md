# Atlassian API MCP

A PoC for an MCP (Model Context Protocol) server for accessing Atlassian Confluence resources via API. This server enables AI assistants and other MCP clients to fetch and read Confluence pages programmatically.

## Features

- Fetch and read Confluence page content
- HTML to plain text conversion
- HTTP-based authentication using Atlassian API tokens
- FastMCP-based server implementation

## Requirements

- Python 3.10 or higher
- Atlassian Confluence instance with API access
- Atlassian API token

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd atlassian-api-mcp
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variable:

```
CONFLUENCE_BASE_URL=https://company.atlassian.net/wiki
```

Replace `company.atlassian.net` with your Atlassian instance URL.

### Authentication

The server uses HTTP header-based authentication with Atlassian API tokens. Credentials are passed via request headers rather than stored on the server.

**Required Headers:**
- `x-atlassian-email`: Your Atlassian account email
- `x-atlassian-api-token`: Your Atlassian API token

## Getting Started

### Starting the Server

```bash
poetry run python main.py
```

The server will start on `http://0.0.0.0:8000/mcp`

### Obtaining an Atlassian API Token

1. Log in to your Atlassian account
2. Visit https://id.atlassian.com/manage-profile/security/api-tokens
3. Click "Create API token"
4. Copy the generated token (you can only view it once)

## Available Tools

### fetch_confluence_page

Fetches the full text content of a Confluence page.

**Parameters:**
- `page_id` (string): The numeric page ID from the Confluence page URL
  - Example: For URL `.../wiki/spaces/TEAM/pages/123456789/Page+Title`, the page_id is `123456789`

**Returns:** Plain text content of the page

**Example:**
```python
fetch_confluence_page("123456789")
```

## Integration Examples

### MCP Inspector (Testing)

Test the server functionality using the MCP Inspector tool:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

### Gemini CLI Integration

Add the server to your Gemini CLI configuration in `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "atlassian-api-mcp": {
      "httpUrl": "http://<your-server-ip>:8000/mcp",
      "headers": {
        "x-atlassian-email": "user@company.com",
        "x-atlassian-api-token": "your-api-token"
      }
    }
  }
}
```

**Security Note:** Using environment variables in your configuration is recommended over hardcoding credentials:

```json
{
  "mcpServers": {
    "atlassian-api-mcp": {
      "httpUrl": "http://<your-server-ip>:8000/mcp",
      "headers": {
        "x-atlassian-email": "${ATLASSIAN_EMAIL}",
        "x-atlassian-api-token": "${ATLASSIAN_API_TOKEN}"
      }
    }
  }
}
```

## Dependencies

- **fastmcp** (^3.0.2): Model Context Protocol server framework
- **beautifulsoup4** (^4.14.3): HTML parsing and text extraction
- **requests** (^2.32.5): HTTP client for API communication
- **python-dotenv** (^0.9.9): Environment variable management

## License

See LICENSE file for details.
