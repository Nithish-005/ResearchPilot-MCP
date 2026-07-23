"""Example usage of ResearchPilot-MCP services.

This demonstrates how to use the services directly (without MCP)
for programmatic access to research papers.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.paper_service import PaperService
from src.services.pdf_service import PDFService
from src.services.search_service import SearchService
from src.services.summary_service import SummaryService
from src.services.compare_service import CompareService
from src.services.citation_service import CitationService


# Configure the papers directory
PAPERS_DIR = Path.home() / "research_papers"


def example_list_papers():
    """List all available papers."""
    print("=" * 60)
    print("EXAMPLE: List Papers")
    print("=" * 60)

    service = PaperService(PAPERS_DIR)
    papers = service.list_papers()

    if not papers:
        print("No papers found. Add PDFs to:", PAPERS_DIR)
        return

    print(f"Found {len(papers)} papers:\n")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper.title}")
        print(f"   File: {paper.filename}")
        print(f"   Pages: {paper.page_count}")
        print(f"   Size: {paper.file_size_kb} KB\n")


def example_read_pdf(filename: str):
    """Read content from a specific paper."""
    print("=" * 60)
    print(f"EXAMPLE: Read PDF - {filename}")
    print("=" * 60)

    service = PDFService(PAPERS_DIR)
    result = service.read_pdf(filename, start_page=0, max_pages=2)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"Title: {result['filename']}")
    print(f"Total pages: {result['total_pages']}")
    print(f"Pages read: {result['pages_read']}")
    print(f"\nContent preview:\n{result['content'][:500]}...")


def example_search_papers(keyword: str):
    """Search for a keyword across all papers."""
    print("=" * 60)
    print(f"EXAMPLE: Search for '{keyword}'")
    print("=" * 60)

    service = SearchService(PAPERS_DIR)
    results = service.search_keyword(keyword)

    print(f"Found {len(results)} matches:\n")
    for result in results[:5]:
        print(f"- {result['filename']} (page {result['page']})")
        print(f"  Snippet: {result['snippet'][:100]}...\n")


def example_summarize_paper(filename: str):
    """Summarize a specific paper."""
    print("=" * 60)
    print(f"EXAMPLE: Summarize - {filename}")
    print("=" * 60)

    service = SummaryService(PAPERS_DIR)
    summary = service.summarize_paper(filename)

    if "error" in summary:
        print(f"Error: {summary['error']}")
        return

    print(f"Title: {summary['title']}")
    print(f"Authors: {summary['authors']}")
    print(f"Pages: {summary['page_count']}")
    print(f"\nSections found: {', '.join(summary['sections_found'])}")
    print(f"\nSummary:\n{summary['summary']}")

    if summary.get("key_findings"):
        print(f"\nKey Findings:")
        for finding in summary["key_findings"]:
            print(f"  - {finding[:100]}...")


def example_compare_papers(filenames: list):
    """Compare multiple papers."""
    print("=" * 60)
    print(f"EXAMPLE: Compare Papers")
    print("=" * 60)

    service = CompareService(PAPERS_DIR)
    comparison = service.compare_papers(filenames)

    if "error" in comparison:
        print(f"Error: {comparison['error']}")
        return

    print(comparison["summary"])

    if comparison.get("common_keywords"):
        print(f"\nCommon keywords: {', '.join(comparison['common_keywords'])}")


def example_generate_citation(filename: str):
    """Generate citations for a paper."""
    print("=" * 60)
    print(f"EXAMPLE: Generate Citations - {filename}")
    print("=" * 60)

    service = CitationService(PAPERS_DIR)

    ieee = service.generate_ieee_citation(filename)
    if "error" not in ieee:
        print(f"IEEE: {ieee['ieee_citation']}")

    apa = service.generate_apa_citation(filename)
    if "error" not in apa:
        print(f"\nAPA: {apa['apa_citation']}")

    bibtex = service.generate_bibtex(filename)
    if "error" not in bibtex:
        print(f"\nBibTeX:\n{bibtex['bibtex']}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("ResearchPilot-MCP - Service Examples")
    print("=" * 60)

    if not PAPERS_DIR.exists():
        print(f"\nPapers directory not found: {PAPERS_DIR}")
        print("Please create it and add some PDF research papers.")
        return

    example_list_papers()

    service = PaperService(PAPERS_DIR)
    papers = service.list_papers()

    if papers:
        first_paper = papers[0].filename

        example_read_pdf(first_paper)
        example_summarize_paper(first_paper)
        example_generate_citation(first_paper)

        if len(papers) >= 2:
            example_compare_papers([papers[0].filename, papers[1].filename])

        example_search_papers("neural")

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
