"""PDF tools - MCP tools for reading and extracting from PDFs."""

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.pdf_service import PDFService

mcp = FastMCP("ResearchPilot-PDF")


def _create_service() -> PDFService:
    """Create a PDFService instance."""
    return PDFService(PAPERS_DIRECTORY)


@mcp.tool()
def read_pdf(filename: str, start_page: int = 0, max_pages: int = 10) -> dict:
    """
    Read content from a PDF file.

    Extracts text from specified pages of a research paper.

    Args:
        filename: Name of the PDF file (e.g., "paper.pdf")
        start_page: Page number to start reading from (0-indexed)
        max_pages: Maximum number of pages to read (default: 10)

    Returns:
        Dictionary with filename, page count, and extracted text content
    """
    service = _create_service()
    return service.read_pdf(filename, start_page, max_pages)


@mcp.tool()
def extract_abstract(filename: str) -> dict:
    """
    Extract the abstract from a PDF file.

    Searches for an "Abstract" section at the beginning of the paper.

    Args:
        filename: Name of the PDF file

    Returns:
        Dictionary with filename and extracted abstract (if found)
    """
    service = _create_service()
    abstract = service.extract_abstract(filename)

    return {"filename": filename, "abstract": abstract, "found": abstract is not None}


@mcp.tool()
def get_page(filename: str, page_number: int) -> dict:
    """
    Get text from a specific page in a PDF.

    Args:
        filename: Name of the PDF file
        page_number: Page number (1-indexed, so 1 = first page)

    Returns:
        Dictionary with page number and text content
    """
    service = _create_service()
    text = service.extract_page(filename, page_number)

    return {
        "filename": filename,
        "page_number": page_number,
        "text": text,
        "found": text is not None,
    }
