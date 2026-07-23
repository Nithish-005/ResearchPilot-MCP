# ResearchPilot-MCP 🚀

**An MCP server that enables AI agents to interact with local academic PDFs** – list, read, search, summarize, compare, cite and even generate literature reviews without ever loading the whole document into the LLM context.

---

## Features

- 📄 **List Papers** – discover every PDF in the configured directory.  
- 📖 **Read PDF** – fetch raw text from any page range.  
- 🧾 **Extract Abstract** – quick abstract extraction from the first page.  
- 🔎 **Keyword Search** – find occurrences across all papers with snippets.  
- 📊 **Summarize Paper** – generate concise over‑views and key‑finding extraction.  
- 🤝 **Compare Papers** – side‑by‑side metadata, keyword overlap & similarity scores.  
- 📚 **Citation Generation** – IEEE, APA and BibTeX entries from PDF metadata.  
- 📑 **Literature Review Builder** – synthesize a structured markdown review for a given topic.  
- ⚡ **MCP‑compatible** – works with Claude Desktop, Cursor, VS Code, OpenCode, Cline, etc.

---

## Architecture Overview

```mermaid
flowchart TD
    A[User (Human)] --> B[AI Client (Claude, Cursor, VS Code, …)]
    B --> C[MCP Protocol (JSON‑RPC over STDIO)]
    C --> D[FastMCP Server]
    D --> E[Tool Router (src/tools/)]
    E --> F[Service Layer (src/services/)]
    F --> G[External Resources]
    G -->|PDF files| H[~/research_papers]
```

*The **Tool Router** maps a requested tool name to a Python function.  
The **Service Layer** contains all business logic (PDF parsing, searching, summarization, etc.).*

---

## Project Structure

```
ResearchPilot-MCP/
│
├── src/
│   ├── __init__.py
│   ├── config.py                # configuration constants
│   ├── server.py                # FastMCP entry point
│   ├── tools/                   # MCP‑exposed tools (decorated with @mcp.tool())
│   │   ├── __init__.py
│   │   ├── paper_tools.py       # list_papers()
│   │   ├── pdf_tools.py         # read_pdf, extract_abstract, get_page
│   │   ├── search_tools.py      # search_keyword, search_multiple_keywords, count_keyword_occurrences
│   │   ├── summary_tools.py     # summarize_paper, get_paper_overview, extract_key_findings
│   │   ├── compare_tools.py     # compare_papers, find_similar_papers
│   │   ├── citation_tools.py    # generate_ieee_citation, generate_apa_citation, generate_bibtex
│   │   └── review_tools.py      # build_literature_review, get_papers_by_keyword
│   └── services/                # Pure‑Python business logic (framework‑agnostic)
│       ├── __init__.py
│       ├── paper_service.py
│       ├── pdf_service.py
│       ├── search_service.py
│       ├── summary_service.py
│       ├── compare_service.py
│       └── citation_service.py
│
├── tests/                       # PyTest suite
│   ├── __init__.py
│   └── test_services.py
│
├── examples/
│   ├── example_usage.py          # End‑to‑end demo script
│   └── mcp_tool_reference.py    # Quick reference of all tools
│
├── .env.example                 # Example environment file
├── .gitignore
├── LICENSE                      # MIT License (see LICENSE file)
├── pyproject.toml
├── requirements.txt
└── README.md
```

*Each `src/tools/*.py` file only contains a thin wrapper that forwards calls to a service method. All heavy lifting lives in the corresponding `src/services/*.py` module.*

---

## Installation Guide

### Prerequisites

| Item | Minimum version |
|------|-----------------|
| **Python** | 3.10+ |
| **Git** | any recent version |
| **Virtual‑env tool** | `venv` (built‑in) or `conda` |

### Steps

```bash
# 1️⃣ Clone the repo
git clone https://github.com/yourusername/ResearchPilot-MCP.git
cd ResearchPilot-MCP

# 2️⃣ Create a virtual environment
python -m venv venv

# 3️⃣ Activate it
#   • Linux / macOS
source venv/bin/activate
#   • Windows PowerShell
.\venv\Scripts\Activate.ps1

# 4️⃣ Install dependencies
pip install -r requirements.txt
```

> **Tip:** For development you may prefer editable mode: `pip install -e .[dev]`.

### Configure the papers folder

The server expects PDFs in `~/research_papers` (see `src/config.py`). Create the folder and drop a few PDFs:

```bash
mkdir ~/research_papers   # macOS / Linux
# Windows PowerShell
New-Item -ItemType Directory -Path "$HOME\research_papers"
```

You can change the location by editing `PAPERS_DIRECTORY` in `src/config.py`.

---

## Running the MCP Server

```bash
python -m src.server
```

**What happens internally**

1. **FastMCP** creates a server instance and registers every tool from `src/tools/`.  
2. The server starts **STDIO transport** – it reads JSON‑RPC requests from `stdin` and writes responses to `stdout`.  
3. An AI client sends a request like `{"method":"list_papers","params":{}}`.  
4. FastMCP routes the call to the matching `@mcp.tool()` function, which invokes the service layer.  
5. The result is serialized back to JSON and sent to the client.

Press **Ctrl‑C** to stop the server.

---

## MCP Inspector Testing (FastMCP CLI)

FastMCP ships a tiny inspector that lets you call tools interactively.

```bash
# Install the inspector (if you haven't already)
pip install fastmcp   # the package already contains the CLI

# Run the inspector against your server
fastmcp dev src/server.py
```

You’ll see a prompt where you can type tool names, e.g.:

```
> list_papers
> read_pdf filename="mypaper.pdf" start_page=0 max_pages=5
```

**Troubleshooting**

*Error:* `ModuleNotFoundError: No module named 'src'`  
*Fix:* Ensure you are executing the command from the repository root **or** set `PYTHONPATH`:

```bash
# macOS / Linux
export PYTHONPATH=$(pwd)

# Windows PowerShell
$env:PYTHONPATH = (Get-Location).Path
```

---

## Connecting MCP with AI Clients

### 1️⃣ Claude Desktop (example)

Create (or edit) `claude_desktop_config.json` in the Claude config folder:

```json
{
  "mcpServers": {
    "researchpilot": {
      "command": "python",
      "args": [
        "-m",
        "src.server"
      ],
      "cwd": "/absolute/path/to/ResearchPilot-MCP"
    }
  }
}
```

After restarting Claude Desktop, you can ask:

> “Show me the list of available papers.”

Claude will call `list_papers` via the MCP server.

### 2️⃣ Cursor IDE

1. Open **Settings → Extensions → MCP**.  
2. Add a new server entry:

```json
{
  "name": "researchpilot",
  "command": "python",
  "args": ["-m", "src.server"],
  "cwd": "/absolute/path/to/ResearchPilot-MCP"
}
```

3. Save and restart Cursor. All tools become available in the Command Palette.

### 3️⃣ Generic MCP‑compatible Clients

All MCP clients speak the same JSON‑RPC over STDIO.  
Start the server (`python -m src.server`) and configure the client to run the same command (`python -m src.server`).  
If the client allows custom environment variables, point `PAPERS_DIRECTORY` to a different folder.

---

## Demo

> **[TODO]** Add screenshots or a short screencast showing:
> - The CLI inspector in action.
> - Claude Desktop issuing a `list_papers` request.
> - A snippet of a generated literature review.

---

## Roadmap

- ✅ Release v0.1.0 (initial feature set)  
- ⏳ Add SQLite metadata store for faster indexing.  
- ⏳ Integrate FAISS / Chroma for semantic similarity search.  
- ⏳ Provide optional OpenAI / Ollama summarization back‑ends.  
- ⏳ Publish a Docker image for one‑click deployment.

---

## Contributing

We welcome contributions! See **CONTRIBUTING.md** for the full workflow.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Badges

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/protocol-MCP-orange)](https://github.com/Model-Context-Protocol)
[![FastMCP](https://img.shields.io/badge/FastMCP-🦊-lightgrey)](https://github.com/Model-Context-Protocol/fastmcp)
