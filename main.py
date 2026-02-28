from fastmcp import FastMCP
import os
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

ATLASSIAN_EMAIL = os.environ.get("ATLASSIAN_EMAIL")
ATLASSIAN_API_TOKEN = os.environ.get("ATLASSIAN_API_TOKEN")
CONFLUENCE_BASE_URL = os.environ.get("CONFLUENCE_BASE_URL")

mcp = FastMCP("Confluence MCP Server")


@mcp.tool()
def fetch_confluence_page(page_id: str) -> str:
    """Fetch a Confluence page by page ID and return its content as plain text."""

    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.view"
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN),
        headers={"Accept": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json()
    html_content = data.get("body", {}).get("view", {}).get("value", "")
    # Convert HTML to plain text
    text_content = BeautifulSoup(html_content, "html.parser").get_text()
    return text_content


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
