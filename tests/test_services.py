"""Tests for ResearchPilot-MCP."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.paper_service import PaperService, PaperInfo
from src.services.pdf_service import PDFService
from src.services.search_service import SearchService
from src.services.citation_service import CitationService
from src.services.compare_service import CompareService
from src.services.summary_service import SummaryService


class TestPaperService:
    """Tests for PaperService."""

    def test_paper_info_dataclass(self):
        """Test that PaperInfo dataclass works correctly."""
        paper = PaperInfo(
            filename="test.pdf",
            filepath=Path("/tmp/test.pdf"),
            title="Test Paper",
            page_count=10,
            file_size_kb=123.45,
        )

        assert paper.filename == "test.pdf"
        assert paper.title == "Test Paper"
        assert paper.page_count == 10
        assert paper.file_size_kb == 123.45

    def test_list_papers_empty_directory(self, tmp_path):
        """Test listing papers in empty directory."""
        service = PaperService(tmp_path)
        papers = service.list_papers()

        assert papers == []

    def test_list_papers_nonexistent_directory(self):
        """Test listing papers when directory doesn't exist."""
        service = PaperService(Path("/nonexistent/path"))
        papers = service.list_papers()

        assert papers == []


class TestSearchService:
    """Tests for SearchService."""

    def test_search_service_initialization(self, tmp_path):
        """Test that SearchService initializes correctly."""
        service = SearchService(tmp_path)

        assert service.papers_directory == tmp_path

    def test_search_keyword_empty_results(self, tmp_path):
        """Test searching in empty directory returns empty results."""
        service = SearchService(tmp_path)
        results = service.search_keyword("test")

        assert results == []


class TestCitationService:
    """Tests for CitationService."""

    def test_citation_service_initialization(self, tmp_path):
        """Test that CitationService initializes correctly."""
        service = CitationService(tmp_path)

        assert service.papers_directory == tmp_path

    def test_generate_ieee_citation_file_not_found(self, tmp_path):
        """Test IEEE citation for nonexistent file."""
        service = CitationService(tmp_path)
        result = service.generate_ieee_citation("nonexistent.pdf")

        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_generate_bibtex_file_not_found(self, tmp_path):
        """Test BibTeX generation for nonexistent file."""
        service = CitationService(tmp_path)
        result = service.generate_bibtex("nonexistent.pdf")

        assert "error" in result

    def test_title_from_filename(self, tmp_path):
        """Test title extraction from filename."""
        service = CitationService(tmp_path)

        title = service._title_from_filename("attention_is_all_you_need.pdf")
        assert title == "Attention Is All You Need"

        title = service._title_from_filename("BERT-Pre-training.pdf")
        assert title == "BERT Pre Training"


class TestCompareService:
    """Tests for CompareService."""

    def test_compare_papers_insufficient_papers(self, tmp_path):
        """Test comparing less than 2 papers."""
        service = CompareService(tmp_path)
        result = service.compare_papers(["only_one.pdf"])

        assert "error" in result

    def test_find_similar_papers_file_not_found(self, tmp_path):
        """Test finding similar papers when reference doesn't exist."""
        service = CompareService(tmp_path)
        result = service.find_similar_papers("nonexistent.pdf")

        assert len(result) == 1
        assert "error" in result[0]


class TestSummaryService:
    """Tests for SummaryService."""

    def test_summarize_paper_file_not_found(self, tmp_path):
        """Test summarizing nonexistent file."""
        service = SummaryService(tmp_path)
        result = service.summarize_paper("nonexistent.pdf")

        assert "error" in result

    def test_get_paper_overview_file_not_found(self, tmp_path):
        """Test getting overview of nonexistent file."""
        service = SummaryService(tmp_path)
        result = service.get_paper_overview("nonexistent.pdf")

        assert "error" in result


class TestConfig:
    """Tests for configuration."""

    def test_config_imports(self):
        """Test that config module imports correctly."""
        from src.config import PAPERS_DIRECTORY, MAX_PAPERS_PER_LIST, PDF_EXTRACT_LENGTH

        assert PAPERS_DIRECTORY is not None
        assert MAX_PAPERS_PER_LIST == 100
        assert PDF_EXTRACT_LENGTH == 5000
