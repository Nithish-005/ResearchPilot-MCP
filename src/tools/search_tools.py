"""Search tools - MCP tools for searching within papers."""

from typing import List

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.search_service import SearchService

mcp = FastMCP("ResearchPilot-Search")


def _create_service() -> SearchService:
    """Create a SearchService instance."""
    return SearchService(PAPERS_DIRECTORY)


@mcp.tool()
def search_keyword(keyword: str, case_sensitive: bool = False) -> dict:
    """
    Search for a keyword across all papers in the research directory.

    Scans through all PDFs and finds matches with surrounding text snippets.

    Args:
        keyword: The keyword or phrase to search for
        case_sensitive: Whether to match case exactly (default: False)

    Returns:
        Dictionary with search results including filename, page, and snippets
    """
    service = _create_service()
    results = service.search_keyword(keyword, case_sensitive)

    return {"keyword": keyword, "total_matches": len(results), "results": results}


@mcp.tool()
def search_multiple_keywords(keywords: List[str], match_all: bool = False) -> dict:
    """
    Search for multiple keywords across all papers.

    Args:
        keywords: List of keywords to search for
        match_all: If True, only return results containing ALL keywords

    Returns:
        Dictionary with search results
    """
    service = _create_service()
    results = service.search_multiple_keywords(keywords, match_all)

    return {
        "keywords": keywords,
        "match_all": match_all,
        "total_matches": len(results),
        "results": results,
    }


@mcp.tool()
def count_keyword_occurrences(keyword: str) -> dict:
    """
    Count how many times a keyword appears across all papers.

    Args:
        keyword: The keyword to count

    Returns:
        Dictionary with per-paper and total counts
    """
    service = _create_service()
    results = service.search_keyword(keyword, case_sensitive=False)

    paper_counts = {}
    for result in results:
        filename = result["filename"]
        paper_counts[filename] = paper_counts.get(filename, 0) + 1

    return {
        "keyword": keyword,
        "total_occurrences": len(results),
        "papers_with_keyword": len(paper_counts),
        "per_paper_counts": paper_counts,
    }
