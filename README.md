# ResearchPilot-MCP

An MCP Server that gives AI agents the ability to interact with research papers stored locally. Instead of loading every PDF into the LLM context, the AI agent calls MCP tools that read, search, compare, summarize, and analyze research papers.

## Features

- **List Papers** - Discover available research papers
- **Read PDFs** - Extract text content from any page
- **Search Keywords** - Find papers containing specific terms
- **Summarize Papers** - Generate paper summaries and key findings
- **Compare Papers** - Analyze multiple papers side by side
- **Generate Citations** - Create IEEE, APA, and BibTeX citations
- **Build Literature Reviews** - Synthesize findings across papers

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI Agent (MCP Client)                    │
│                  Claude Desktop, Cursor, VS Code, etc.          │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                        MCP Protocol (JSON-RPC)
                                │
┌──────────────────────────────▼──────────────────────────────────┐
│                     ResearchPilot-MCP Server                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Tool Registry                           │ │
│  │  list_papers | read_pdf | search_keyword | summarize_paper  │ │
│  │  compare_papers | generate_ieee_citation | build_liter...   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌──────────────────────────▼──────────────────────────────┐   │
│  │                    Tool Routers                           │   │
│  │  paper_tools | pdf_tools | search_tools | summary_tools  │   │
│  │  compare_tools | citation_tools | review_tools            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────▼──────────────────────────────┐   │
│  │                   Services Layer                          │   │
│  │  PaperService | PDFService | SearchService              │   │
│  │  SummaryService | CompareService | CitationService       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
└──────────────────────────────▼──────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   PDF Files           │
                    │   ~/research_papers/  │
                    └───────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Install Dependencies

```bash
cd ResearchPilot-MCP
pip install -e .
```

This installs the package in editable mode, so you can edit code and see changes immediately.

### Install Dependencies for Development

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Configure Your Papers Directory

By default, the server looks for papers in `~/research_papers`. Create this directory:

```bash
# Linux/Mac
mkdir -p ~/research_papers

# Windows
mkdir %USERPROFILE%\research_papers
```

Copy your PDF research papers into this folder.

### 2. Run the Server

```bash
python -m src.server
```

The server will start and listen for MCP client connections via stdio.

### 3. Configure MCP Client

Add to your MCP client configuration:

**Claude Desktop (claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "researchpilot": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/ResearchPilot-MCP"
    }
  }
}
```

## Available Tools

### Paper Management

| Tool | Description |
|------|-------------|
| `list_papers` | List all available research papers |
| `read_pdf` | Read content from a specific page range |
| `extract_abstract` | Extract the abstract from a paper |
| `get_page` | Get text from a specific page |

### Search

| Tool | Description |
|------|-------------|
| `search_keyword` | Search for a keyword across all papers |
| `search_multiple_keywords` | Search for multiple keywords |
| `count_keyword_occurrences` | Count keyword frequency across papers |

### Analysis

| Tool | Description |
|------|-------------|
| `summarize_paper` | Generate a summary of a paper |
| `get_paper_overview` | Get quick paper overview |
| `extract_key_findings` | Extract key findings from a paper |
| `compare_papers` | Compare multiple papers side by side |
| `find_similar_papers` | Find papers similar to a given paper |

### Citations

| Tool | Description |
|------|-------------|
| `generate_ieee_citation` | Generate IEEE format citation |
| `generate_apa_citation` | Generate APA format citation |
| `generate_bibtex` | Generate BibTeX entry |

### Literature Review

| Tool | Description |
|------|-------------|
| `build_literature_review` | Build a literature review for a topic |
| `get_papers_by_keyword` | Find papers matching a keyword |

## Project Structure

```
ResearchPilot-MCP/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── server.py              # Main MCP server entry point
│   │
│   ├── tools/                 # MCP tool definitions
│   │   ├── __init__.py
│   │   ├── paper_tools.py     # list_papers
│   │   ├── pdf_tools.py       # read_pdf, extract_abstract
│   │   ├── search_tools.py    # search_keyword
│   │   ├── summary_tools.py   # summarize_paper
│   │   ├── compare_tools.py   # compare_papers
│   │   ├── citation_tools.py   # generate_ieee_citation
│   │   └── review_tools.py     # build_literature_review
│   │
│   └── services/              # Business logic (framework-agnostic)
│       ├── __init__.py
│       ├── paper_service.py   # Paper listing and metadata
│       ├── pdf_service.py     # PDF reading and parsing
│       ├── search_service.py  # Keyword search
│       ├── summary_service.py # Summarization logic
│       ├── compare_service.py # Paper comparison
│       └── citation_service.py # Citation generation
│
├── tests/                     # Test suite
├── docs/                      # Documentation
├── examples/                  # Example usage
│
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
├── README.md                  # This file
└── LICENSE                   # MIT License
```

## Development

### Run Tests

```bash
cd ResearchPilot-MCP
pytest tests/ -v
```

### Code Formatting

```bash
ruff format src/
```

### Linting

```bash
ruff check src/
```

## How MCP Works

### Request Flow

1. **AI Agent** decides it needs information from research papers
2. **AI Agent** sends a JSON-RPC request via MCP protocol
3. **MCP Server** (this project) receives the request
4. **Tool Router** finds the matching `@mcp.tool()` decorated function
5. **Service Layer** executes the business logic
6. **PDF files** are read from disk
7. **Result** is converted to JSON and returned
8. **AI Agent** receives the structured data

### Example: AI calls `list_papers()`

```python
# 1. AI sends:
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_papers",
    "arguments": {}
  }
}

# 2. Server responds:
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "filename": "attention_is_all_you_need.pdf",
        "filepath": "/home/user/research_papers/attention_is_all_you_need.pdf",
        "title": "Attention Is All You Need",
        "page_count": 15,
        "file_size_kb": 245.32
      }
    ]
  }
}
```

## License

MIT License - see LICENSE file for details.