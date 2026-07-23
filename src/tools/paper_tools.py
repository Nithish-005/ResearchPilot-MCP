"""Paper tools - MCP tools for paper management."""

from pathlib import Path

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.paper_service import PaperService, PaperInfo

# Create a FastMCP instance for tools in this module
mcp = FastMCP("ResearchPilot-Papers")


def _create_service() -> PaperService:
    """Create a PaperService instance with configured directory."""
    return PaperService(PAPERS_DIRECTORY)


@mcp.tool()
def list_papers() -> list[dict]:
    """
    List all available research papers in the papers directory.

    This tool scans the configured research papers folder and returns
    information about all PDF files found, including:
    - Filename
    - File path
    - Extracted or inferred title
    - Number of pages
    - File size

    Returns:
        A list of dictionaries with paper information.
        Empty list if no papers found or directory doesn't exist.
    """
    service = _create_service()
    papers = service.list_papers()

    return [
        {
            "filename": p.filename,
            "filepath": str(p.filepath),
            "title": p.title or p.filename,
            "page_count": p.page_count,
            "file_size_kb": p.file_size_kb,
        }
        for p in papers
    ]
