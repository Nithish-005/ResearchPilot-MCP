"""Citation tools - MCP tools for generating citations."""

from typing import Optional

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.citation_service import CitationService

mcp = FastMCP("ResearchPilot-Citation")


def _create_service() -> CitationService:
    """Create a CitationService instance."""
    return CitationService(PAPERS_DIRECTORY)


@mcp.tool()
def generate_ieee_citation(filename: str, authors: Optional[str] = None) -> dict:
    """
    Generate an IEEE format citation for a paper.

    IEEE format: Authors. "Title". Journal, Year.

    Args:
        filename: Name of the PDF file
        authors: Author names (optional, will try to extract from PDF metadata)

    Returns:
        Dictionary with citation details and formatted IEEE citation
    """
    service = _create_service()
    return service.generate_ieee_citation(filename, authors)


@mcp.tool()
def generate_apa_citation(filename: str, authors: Optional[str] = None) -> dict:
    """
    Generate an APA format citation for a paper.

    APA format: Author (Year). Title.

    Args:
        filename: Name of the PDF file
        authors: Author names (optional, will try to extract from PDF metadata)

    Returns:
        Dictionary with citation details and formatted APA citation
    """
    service = _create_service()
    return service.generate_apa_citation(filename, authors)


@mcp.tool()
def generate_bibtex(filename: str, authors: Optional[str] = None) -> dict:
    """
    Generate a BibTeX entry for a paper.

    Args:
        filename: Name of the PDF file
        authors: Author names (optional, will try to extract from PDF metadata)

    Returns:
        Dictionary with BibTeX cite key and entry
    """
    service = _create_service()
    return service.generate_bibtex(filename, authors)
