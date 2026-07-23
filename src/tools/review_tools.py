"""Literature review tools - MCP tools for building literature reviews."""

from pathlib import Path
from typing import List, Optional

from fastmcp import FastMCP

from src.config import PAPERS_DIRECTORY
from src.services.paper_service import PaperService
from src.services.summary_service import SummaryService
from src.services.compare_service import CompareService

mcp = FastMCP("ResearchPilot-LiteratureReview")


def _create_paper_service() -> PaperService:
    """Create a PaperService instance."""
    return PaperService(PAPERS_DIRECTORY)


def _create_summary_service() -> SummaryService:
    """Create a SummaryService instance."""
    return SummaryService(PAPERS_DIRECTORY)


def _create_compare_service() -> CompareService:
    """Create a CompareService instance."""
    return CompareService(PAPERS_DIRECTORY)


@mcp.tool()
def build_literature_review(topic: str, max_papers: int = 10) -> dict:
    """
    Build a literature review for a given topic.

    Analyzes papers containing the topic keyword and generates
    a structured literature review with summaries and comparisons.

    Args:
        topic: The research topic to focus on
        max_papers: Maximum number of papers to include (default: 10)

    Returns:
        Dictionary with literature review sections and paper analyses
    """
    paper_service = _create_paper_service()
    summary_service = _create_summary_service()

    all_papers = paper_service.list_papers()

    if not all_papers:
        return {
            "topic": topic,
            "error": "No papers found in research directory",
            "papers_analyzed": 0,
        }

    matching_papers = []
    topic_lower = topic.lower()

    for paper in all_papers:
        title_lower = (paper.title or "").lower()
        filename_lower = paper.filename.lower()

        if topic_lower in title_lower or topic_lower in filename_lower:
            matching_papers.append(paper)

    if not matching_papers:
        matching_papers = all_papers[:max_papers]
    else:
        matching_papers = matching_papers[:max_papers]

    paper_analyses = []
    for paper in matching_papers:
        summary = summary_service.summarize_paper(paper.filename)
        paper_analyses.append(
            {
                "filename": paper.filename,
                "title": paper.title or paper.filename,
                "authors": summary.get("authors", "Unknown"),
                "page_count": paper.page_count,
                "summary": summary.get("summary", "Could not generate summary"),
                "key_findings": summary.get("key_findings", [])[:3],
            }
        )

    review_sections = [
        f"## Literature Review: {topic}",
        f"\n### Overview\nThis literature review synthesizes findings from {len(paper_analyses)} research papers on {topic}.",
        "\n### Papers Analyzed\n",
    ]

    for i, analysis in enumerate(paper_analyses, 1):
        review_sections.append(f"\n#### {i}. {analysis['title']}")
        review_sections.append(f"**Authors:** {analysis['authors']}")
        review_sections.append(f"**Pages:** {analysis['page_count']}")
        review_sections.append(f"**Summary:** {analysis['summary'][:300]}...")
        if analysis["key_findings"]:
            review_sections.append(f"**Key Findings:**")
            for finding in analysis["key_findings"]:
                review_sections.append(f"- {finding[:150]}")

    if len(paper_analyses) >= 2:
        review_sections.append("\n### Comparative Analysis")
        review_sections.append(
            "\nThe papers in this review share several common themes:"
        )

        all_keywords = []
        for analysis in paper_analyses:
            if analysis.get("key_findings"):
                for finding in analysis["key_findings"]:
                    words = finding.lower().split()
                    all_keywords.extend([w for w in words if len(w) > 5])

        common_themes = list(set(all_keywords[:20]))
        if common_themes:
            review_sections.append(
                f"- Common terminology: {', '.join(common_themes[:10])}"
            )

    review_sections.append(
        f"\n### Conclusion\nThis review examined {len(paper_analyses)} papers on {topic}."
    )
    review_sections.append(
        "The papers provide insights into various aspects of the topic,"
    )
    review_sections.append(
        "including methodologies, findings, and potential applications."
    )

    return {
        "topic": topic,
        "papers_analyzed": len(paper_analyses),
        "papers": paper_analyses,
        "literature_review": "\n".join(review_sections),
    }


@mcp.tool()
def get_papers_by_keyword(keyword: str) -> dict:
    """
    Get all papers that mention a specific keyword.

    Args:
        keyword: Keyword to search for in titles

    Returns:
        Dictionary with matching papers
    """
    paper_service = _create_paper_service()
    all_papers = paper_service.list_papers()

    keyword_lower = keyword.lower()
    matching = []

    for paper in all_papers:
        title = paper.title or ""
        if keyword_lower in title.lower() or keyword_lower in paper.filename.lower():
            matching.append(
                {
                    "filename": paper.filename,
                    "title": title,
                    "page_count": paper.page_count,
                }
            )

    return {"keyword": keyword, "matching_papers": matching, "count": len(matching)}
