"""Example MCP client for testing the server.

This shows how to call the MCP server tools programmatically.
"""

import json
import subprocess
import sys


def call_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Call an MCP tool via the server.

    This simulates how an MCP client would call a tool.
    """
    print(f"Calling tool: {tool_name}")
    print(f"Arguments: {arguments}")
    print("-" * 40)


def main():
    """Show available tools and how to call them."""
    print("=" * 60)
    print("ResearchPilot-MCP - Tool Reference")
    print("=" * 60)

    tools = [
        {
            "name": "list_papers",
            "description": "List all available research papers",
            "arguments": {},
        },
        {
            "name": "read_pdf",
            "description": "Read content from a PDF file",
            "arguments": {"filename": "paper.pdf", "start_page": 0, "max_pages": 10},
        },
        {
            "name": "extract_abstract",
            "description": "Extract abstract from a paper",
            "arguments": {"filename": "paper.pdf"},
        },
        {
            "name": "search_keyword",
            "description": "Search for a keyword in all papers",
            "arguments": {"keyword": "neural network"},
        },
        {
            "name": "summarize_paper",
            "description": "Generate a summary of a paper",
            "arguments": {"filename": "paper.pdf", "max_length": 500},
        },
        {
            "name": "compare_papers",
            "description": "Compare multiple papers",
            "arguments": {"filenames": ["paper1.pdf", "paper2.pdf"]},
        },
        {
            "name": "generate_ieee_citation",
            "description": "Generate IEEE citation",
            "arguments": {"filename": "paper.pdf", "authors": "Smith, J."},
        },
        {
            "name": "generate_bibtex",
            "description": "Generate BibTeX entry",
            "arguments": {"filename": "paper.pdf"},
        },
        {
            "name": "build_literature_review",
            "description": "Build a literature review",
            "arguments": {"topic": "machine learning", "max_papers": 5},
        },
        {
            "name": "find_similar_papers",
            "description": "Find papers similar to a given paper",
            "arguments": {"filename": "paper.pdf", "max_results": 5},
        },
    ]

    print("\nAvailable Tools:\n")
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   {tool['description']}")
        if tool["arguments"]:
            print(f"   Arguments: {json.dumps(tool['arguments'], indent=2)}")
        print()

    print("\nTo run the MCP server:")
    print("  python -m src.server")
    print("\nTo test with fastmcp CLI (if installed):")
    print("  fastmcp dev src/server.py")
    print("\nTo run examples:")
    print("  python examples/example_usage.py")


if __name__ == "__main__":
    main()
