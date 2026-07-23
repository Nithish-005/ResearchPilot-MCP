"""Compare tools - MCP tools for comparing papers."""

from typing import List

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.compare_service import CompareService

mcp = FastMCP("ResearchPilot-Compare")


def _create_service() -> CompareService:
    """Create a CompareService instance."""
    return CompareService(PAPERS_DIRECTORY)


@mcp.tool()
def compare_papers(filenames: List[str]) -> dict:
    """
    Compare multiple research papers side by side.

    Extracts metadata and finds common keywords across papers.

    Args:
        filenames: List of PDF filenames to compare (e.g., ["paper1.pdf", "paper2.pdf"])

    Returns:
        Dictionary with comparison results
    """
    service = _create_service()
    return service.compare_papers(filenames)


@mcp.tool()
def find_similar_papers(filename: str, max_results: int = 5) -> dict:
    """
    Find papers similar to a given paper.

    Uses keyword overlap to determine similarity.

    Args:
        filename: Reference paper filename
        max_results: Maximum number of similar papers to return

    Returns:
        Dictionary with similar papers and similarity scores
    """
    service = _create_service()
    similar = service.find_similar_papers(filename, max_results)

    return {"reference_paper": filename, "similar_papers": similar}
