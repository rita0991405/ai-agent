# LangChain ReAct Agent with Web Search

A Python-based ReAct (Reasoning + Acting) agent using LangChain that can search the web and answer questions.

## Features

- **ReAct Agent**: Reasoning and Acting framework for intelligent decision-making
- **Web Search Tool**: Integrated web search capability
- **Max Iterations**: Limited to 5 iterations to prevent infinite loops
- **OpenAI Integration**: Uses GPT-4 for reasoning

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/rita0991405/ai-agent.git
cd ai-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

### Basic Example
```python
from react_agent import run_agent

query = "What are the latest developments in AI?"
response = run_agent(query)
print(response)
```

### Run from Command Line
```bash
python react_agent.py
```

## How It Works

1. **Observation**: The agent observes the input query
2. **Thought**: It reasons about what needs to be done
3. **Action**: It decides to use the WebSearch tool if needed
4. **Result**: It processes the search results
5. **Final Answer**: It generates a comprehensive response

The agent stops after 5 iterations maximum or when it determines the answer is complete.

## Configuration

- **Max Iterations**: Change `max_iterations=5` in `react_agent.py` to adjust
- **Model**: Currently uses GPT-4, modify in `ChatOpenAI(model="gpt-4")`
- **Temperature**: Set to 0 for deterministic behavior, adjust as needed

## Architecture

```
agent_executor
├── ReAct Agent
│   ├── LLM (GPT-4)
│   ├── Tools
│   │   └── WebSearch Tool
│   └── Prompt (from LangChain Hub)
└── Max Iterations: 5
```

## Error Handling

- Gracefully handles parsing errors
- Returns error messages if API calls fail
- Catches timeout exceptions in web search

## Future Enhancements

- Add more tools (Calculator, Wikipedia, Custom APIs)
- Implement memory/conversation history
- Add response caching
- Support for different LLM models

## License

MIT
