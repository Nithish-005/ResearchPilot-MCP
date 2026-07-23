"""Summary tools - MCP tools for summarizing papers."""

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.summary_service import SummaryService

mcp = FastMCP("ResearchPilot-Summary")


def _create_service() -> SummaryService:
    """Create a SummaryService instance."""
    return SummaryService(PAPERS_DIRECTORY)


@mcp.tool()
def summarize_paper(filename: str, max_length: int = 500) -> dict:
    """
    Generate a summary of a research paper.

    Extracts the abstract, introduction, and conclusion sections,
    then generates an overview.

    Args:
        filename: Name of the PDF file
        max_length: Maximum character length of summary

    Returns:
        Dictionary with paper info and generated summary
    """
    service = _create_service()
    return service.summarize_paper(filename, max_length)


@mcp.tool()
def get_paper_overview(filename: str) -> dict:
    """
    Get a quick overview of a paper without full summary.

    Args:
        filename: Name of the PDF file

    Returns:
        Dictionary with paper metadata and first paragraph
    """
    service = _create_service()
    return service.get_paper_overview(filename)


@mcp.tool()
def extract_key_findings(filename: str) -> dict:
    """
    Extract key findings from a research paper.

    Looks for sentences containing common research indicators like
    "we find that", "our results show", "we propose", etc.

    Args:
        filename: Name of the PDF file

    Returns:
        Dictionary with extracted findings
    """
    service = _create_service()
    summary = service.summarize_paper(filename)

    if "error" in summary:
        return summary

    return {
        "filename": filename,
        "title": summary.get("title", ""),
        "key_findings": summary.get("key_findings", []),
    }
