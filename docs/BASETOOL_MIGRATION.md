# BaseTool Migration Guide

## Issue: ImportError with crewai_tools

If you're encountering the following error:

```python
ImportError: cannot import name 'BaseTool' from 'crewai_tools'
```

This indicates you have an outdated version of `praisonai_tools` that was attempting to import from `crewai_tools`.

## Solution

The current version of `praisonai_tools` includes its own `BaseTool` implementation and no longer depends on `crewai_tools`.

### Quick Fix

1. **Update the package:**
   ```bash
   pip install --upgrade praisonai-tools
   ```

2. **Or install from this repository:**
   ```bash
   git clone https://github.com/MervinPraison/PraisonAI-Tools.git
   cd PraisonAI-Tools
   pip install .
   ```

### Using the Correct Import

The correct import statement is:

```python
from praisonai_tools import BaseTool
```

### Example Usage

```python
from duckduckgo_search import DDGS
from praisonai_tools import BaseTool

class InternetSearchTool(BaseTool):
    name: str = "InternetSearchTool"
    description: str = "Search Internet for relevant information based on a query or latest news"

    def _run(self, query: str):
        ddgs = DDGS()
        results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
        return results
```

### Multi-Agent Usage with PraisonAI Agents

```python
from praisonaiagents import Agent, PraisonAIAgents

# Create an agent with your custom tool
agent = Agent(
    name="Internet Search Agent",
    tools=[InternetSearchTool],
    instructions="""
    You are an agent that can search the internet for relevant information based on a query or latest news.
    """
)

# Run the agent
result = PraisonAIAgents(agents=[agent], verbose=10).start()
print(result)
```

## What Changed?

1. **Independent Implementation**: `praisonai_tools` now has its own `BaseTool` class
2. **No CrewAI Dependency**: The package no longer imports from or depends on `crewai_tools`
3. **LangChain Integration**: Tools can be converted to LangChain format using `tool.to_langchain()`
4. **Modern Python**: Uses Pydantic v2 for the main implementation

## Features of the New BaseTool

- **Abstract Base Class**: Inherit from `BaseTool` and implement the `_run` method
- **Automatic Schema Generation**: Automatically generates argument schemas from method signatures
- **Tool Decorator**: Use `@tool` decorator to quickly create tools from functions
- **LangChain Compatible**: Convert any tool to LangChain's `StructuredTool` format
- **Caching Support**: Built-in support for result caching

## Troubleshooting

If you still encounter issues after updating:

1. **Check your installation:**
   ```bash
   pip show praisonai-tools
   ```

2. **Verify the import works:**
   ```python
   from praisonai_tools import BaseTool
   print("Import successful!")
   ```

3. **Clear pip cache if needed:**
   ```bash
   pip cache purge
   pip install --no-cache-dir praisonai-tools
   ```

## Additional Resources

- [Test script](../test_basetool_fix.py) - Demonstrates the working implementation
- [Example tools](../example.py) - Shows various tool usage patterns
- [Base tool implementation](../praisonai_tools/tools/base_tool.py) - The source code for reference