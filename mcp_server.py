"""
FastMCP server exposing a Brave web search tool over stdio.
"""
import os
import sys

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("web-search")


@mcp.tool()
def web_search(query: str) -> str:
    """
    Search the internet for current information, news, and facts.

    Args:
        query: The search query string.
    """
    try:
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": os.getenv("BRAVE_SEARCH_API_KEY", ""),
        }
        params = {"q": query, "count": 5}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()

        formatted_results = []
        if "web" in results and "results" in results["web"]:
            items = results["web"]["results"]
        elif "web" in results:
            items = results["web"]
        else:
            items = []

        for item in items[:5]:
            if not isinstance(item, dict):
                continue
            formatted_results.append(
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('url', 'N/A')}\n"
                f"Description: {item.get('description', 'N/A')}\n"
            )

        return "\n---\n".join(formatted_results) if formatted_results else "No results found"
    except Exception as e:
        return f"Error performing web search: {str(e)}"


if __name__ == "__main__":
    # stdio is the MCP wire protocol — never print to stdout.
    print("Starting web-search MCP server (stdio)...", file=sys.stderr)
    mcp.run(transport="stdio")
