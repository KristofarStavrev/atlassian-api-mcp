import os
import requests
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

CONFLUENCE_BASE_URL = os.environ.get("CONFLUENCE_BASE_URL")
if not CONFLUENCE_BASE_URL:
    raise ValueError("CONFLUENCE_BASE_URL environment variable is not set")

mcp = FastMCP("Confluence MCP Server")


def get_confluence_credentials():
    """Extract and validate Confluence credentials from request headers."""
    headers = get_http_headers()
    email = headers.get("x-atlassian-email")
    api_token = headers.get("x-atlassian-api-token")

    if not email:
        raise ValueError("Missing required header: x-atlassian-email")
    if not api_token:
        raise ValueError("Missing required header: x-atlassian-api-token")

    return email, api_token


@mcp.tool()
def fetch_confluence_page(page_id: str) -> str:
    """
    Fetch the full text content of a Confluence page.
    Use this when the user wants to read, summarize, or ask questions about
    a specific Confluence page. The page_id is the numeric ID found in the 
    page URL, e.g. for '.../wiki/spaces/TEAM/pages/123456789/Page+Title' 
    the page_id is '123456789'.
    """

    email, api_token = get_confluence_credentials()

    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.view"
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(email, api_token),
        headers={"Accept": "application/json"}
    )

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise ValueError(f"Confluence API error: {e.response.status_code}")

    data = resp.json()
    html_content = data.get("body", {}).get("view", {}).get("value", "")
    # Convert HTML to plain text
    text_content = BeautifulSoup(html_content, "html.parser").get_text()
    return text_content


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
