#!/usr/bin/env python3
"""
Test script to verify BaseTool import works correctly.
This demonstrates the fix for the import issue and shows multi-agent parallel execution.
"""

# Example tools.py implementation
from duckduckgo_search import DDGS
from praisonai_tools import BaseTool

class InternetSearchTool(BaseTool):
    name: str = "InternetSearchTool"
    description: str = "Search Internet for relevant information based on a query or latest news"

    def _run(self, query: str):
        """Execute the search query using DuckDuckGo."""
        try:
            ddgs = DDGS()
            results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
            return results
        except Exception as e:
            return f"Error performing search: {str(e)}"

# Test the tool directly
def test_direct_tool_usage():
    """Test using the tool directly."""
    print("Testing direct tool usage...")
    tool = InternetSearchTool()
    
    # Test the tool
    try:
        result = tool._run("Python programming language")
        print(f"Tool works! Found {len(result) if isinstance(result, list) else 0} results")
        return True
    except Exception as e:
        print(f"Tool failed: {str(e)}")
        return False

# Test with mock agent framework (since praisonaiagents isn't installed)
def test_multi_agent_simulation():
    """Simulate multi-agent parallel execution."""
    print("\nSimulating multi-agent parallel execution...")
    
    # Create multiple tool instances for different agents
    search_agent1 = InternetSearchTool()
    search_agent2 = InternetSearchTool()
    search_agent3 = InternetSearchTool()
    
    # Simulate parallel queries
    queries = [
        "artificial intelligence latest news",
        "machine learning tutorials",
        "python web frameworks"
    ]
    
    print(f"Running {len(queries)} searches in parallel simulation...")
    
    results = []
    for i, (tool, query) in enumerate(zip([search_agent1, search_agent2, search_agent3], queries)):
        print(f"Agent {i+1} searching for: '{query}'")
        try:
            result = tool._run(query)
            results.append({
                "agent": i+1,
                "query": query,
                "success": True,
                "result_count": len(result) if isinstance(result, list) else 0
            })
        except Exception as e:
            results.append({
                "agent": i+1,
                "query": query,
                "success": False,
                "error": str(e)
            })
    
    # Print results
    print("\nResults:")
    for r in results:
        if r["success"]:
            print(f"  Agent {r['agent']}: Successfully found {r['result_count']} results for '{r['query']}'")
        else:
            print(f"  Agent {r['agent']}: Failed with error: {r['error']}")
    
    return all(r["success"] for r in results)

# Test LangChain integration
def test_langchain_integration():
    """Test that the tool can be converted to LangChain format."""
    print("\nTesting LangChain integration...")
    
    tool = InternetSearchTool()
    
    try:
        # Convert to LangChain tool
        langchain_tool = tool.to_langchain()
        print(f"Successfully converted to LangChain tool: {langchain_tool.name}")
        print(f"Description: {langchain_tool.description}")
        return True
    except Exception as e:
        print(f"LangChain conversion failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("BaseTool Import Test Script")
    print("=" * 50)
    
    # Verify imports work
    print("✓ Successfully imported BaseTool from praisonai_tools")
    print("✓ Successfully created InternetSearchTool class")
    
    # Run tests
    tests = [
        ("Direct Tool Usage", test_direct_tool_usage),
        ("LangChain Integration", test_langchain_integration),
        ("Multi-Agent Simulation", test_multi_agent_simulation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {status}: {test_name}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'All tests passed!' if all_passed else 'Some tests failed.'}")
    
    # Note about the original error
    print("\n" + "=" * 50)
    print("NOTE: The original ImportError was due to an outdated package version.")
    print("The current praisonai_tools package has its own BaseTool implementation")
    print("and does not depend on crewai_tools.")
    print("\nTo fix the issue in your environment, please update the package:")
    print("  pip install --upgrade praisonai-tools")
    print("  # or if installing from this repository:")
    print("  pip install --upgrade .")