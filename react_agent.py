"""
LangChain ReAct Agent with Web Search Tool
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import requests
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define Web Search Tool
def web_search(query: str) -> str:
    """
    Search the web using a simple search API.
    Args:
        query: The search query string
    Returns:
        Search results as a string
    """
    try:
        # Using DuckDuckGo API for search (no API key required)
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": os.getenv("BRAVE_SEARCH_API_KEY", "")
        }
        params = {
            "q": query,
            "count": 5
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        
        # Format results
        formatted_results = []
        if "web" in results:
            for item in results["web"][:5]:
                formatted_results.append(
                    f"Title: {item.get('title', 'N/A')}\n"
                    f"URL: {item.get('url', 'N/A')}\n"
                    f"Description: {item.get('description', 'N/A')}\n"
                )
        
        return "\n---\n".join(formatted_results) if formatted_results else "No results found"
    
    except Exception as e:
        return f"Error performing web search: {str(e)}"


# Create tools list
tools = [
    Tool(
        name="WebSearch",
        func=web_search,
        description="Useful for searching the internet for current information, news, and facts. Input should be a search query string."
    )
]

# Get the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")

# Create the ReAct agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=["\nObservation:"]
)

# Create the agent executor with max_iterations=5
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)


def run_agent(query: str) -> str:
    """
    Run the ReAct agent with a given query.
    
    Args:
        query: The user query to process
        
    Returns:
        The agent's final response
    """
    try:
        result = agent_executor.invoke({"input": query})
        return result.get("output", "No response generated")
    except Exception as e:
        return f"Error executing agent: {str(e)}"


if __name__ == "__main__":
    # Example usage
    query = "What are the latest developments in AI?"
    print(f"Query: {query}\n")
    response = run_agent(query)
    print(f"\nFinal Response:\n{response}")
