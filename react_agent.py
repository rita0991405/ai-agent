"""
LangGraph ReAct Agent that calls tools via a FastMCP stdio server.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
MCP_SERVER_PATH = PROJECT_ROOT / "mcp_server.py"
PYTHON_EXECUTABLE = sys.executable

MAX_RECURSION = 5


def _build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def _build_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "web-search": {
                "transport": "stdio",
                "command": PYTHON_EXECUTABLE,
                "args": [str(MCP_SERVER_PATH)],
                "cwd": str(PROJECT_ROOT),
                "env": {
                    **os.environ,
                    "BRAVE_SEARCH_API_KEY": os.getenv("BRAVE_SEARCH_API_KEY", ""),
                },
            }
        }
    )


async def run_agent_async(query: str) -> str:
    """
    Run the LangGraph ReAct agent with MCP tools.

    Args:
        query: The user query to process.

    Returns:
        The agent's final response text.
    """
    try:
        client = _build_mcp_client()
        tools = await client.get_tools()
        agent = create_react_agent(_build_llm(), tools)

        result = await agent.ainvoke(
            {"messages": [("user", query)]},
            config={"recursion_limit": MAX_RECURSION},
        )

        messages = result.get("messages", [])
        if not messages:
            return "No response generated"

        last = messages[-1]
        content = getattr(last, "content", None)
        if content is None and isinstance(last, dict):
            content = last.get("content")
        return content if content else "No response generated"
    except Exception as e:
        return f"Error executing agent: {str(e)}"


def run_agent(query: str) -> str:
    """Synchronous wrapper around the async LangGraph agent."""
    return asyncio.run(run_agent_async(query))


if __name__ == "__main__":
    query = "What are the latest developments in AI?"
    print(f"Query: {query}\n")
    response = run_agent(query)
    print(f"\nFinal Response:\n{response}")
