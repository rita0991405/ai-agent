# LangGraph ReAct Agent with FastMCP Web Search

A Python ReAct agent built with **LangGraph**. Tools are served by a local **FastMCP** server over stdio, and loaded into the agent via **langchain-mcp-adapters**.

## Features

- **LangGraph ReAct Agent**: Tool-calling loop with `recursion_limit=5`
- **FastMCP Server**: Exposes `web_search` as an MCP tool (`mcp_server.py`)
- **Brave Search**: Current web results for the agent
- **OpenAI Integration**: Uses GPT-4 for reasoning

## Architecture

```
react_agent.py
├── LangGraph create_react_agent
│   ├── LLM (GPT-4)
│   └── tools from MultiServerMCPClient
└── spawns (stdio) → mcp_server.py
                      └── FastMCP tool: web_search → Brave API
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/rita0991405/ai-agent.git
cd ai-agent
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY`: Get from [OpenAI](https://platform.openai.com/api-keys)
- `BRAVE_SEARCH_API_KEY`: Get from [Brave Search](https://api.search.brave.com/)

## Usage

### Run the agent from the command line
```bash
python react_agent.py
```

### Call from Python
```python
from react_agent import run_agent

query = "What are the latest developments in AI?"
response = run_agent(query)
print(response)
```

### Run the MCP server alone (stdio)
Usually the agent starts this for you. To launch manually:
```bash
python mcp_server.py
```
Do not print application text to stdout while using stdio transport.

## How It Works

1. The agent process connects to the FastMCP server over stdio.
2. MCP tools (currently `web_search`) are loaded as LangChain tools.
3. LangGraph's ReAct agent decides whether to call tools.
4. Tool results are fed back into the model until a final answer is produced.
5. The loop stops when the answer is complete or `recursion_limit=5` is hit.

## Configuration

- **Recursion limit**: Change `MAX_RECURSION` in `react_agent.py`
- **Model**: Change `model="gpt-4"` in `_build_llm()`
- **Temperature**: Set to `0` for deterministic behavior

## Project layout

| File | Role |
|------|------|
| `react_agent.py` | LangGraph agent + MCP client |
| `mcp_server.py` | FastMCP stdio server (`web_search`) |
| `.env` | API keys (not committed) |
| `requirements.txt` | Python dependencies |

## License

MIT
