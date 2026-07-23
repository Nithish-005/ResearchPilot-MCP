"""Paper service - business logic for paper management."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import fitz


@dataclass
class PaperInfo:
    """
    Information about a research paper.

    This is a data container - it just holds information.
    No methods, just data attributes.
    """

    filename: str
    filepath: Path
    title: Optional[str] = None
    page_count: int = 0
    file_size_kb: float = 0.0


class PaperService:
    """
    Service for managing research papers.

    This class contains all the business logic for:
    - Finding papers in the filesystem
    - Reading PDF metadata
    - Listing available papers
    """

    def __init__(self, papers_directory: Path) -> None:
        """
        Initialize the paper service.

        Args:
            papers_directory: Path to the folder containing PDFs
        """
        self.papers_directory = papers_directory

    def list_papers(self) -> List[PaperInfo]:
        """
        List all PDF files in the papers directory.

        Returns:
            List of PaperInfo objects for each found PDF
        """
        papers: List[PaperInfo] = []

        if not self.papers_directory.exists():
            return papers

        for filepath in self.papers_directory.glob("*.pdf"):
            paper_info = self._read_paper_info(filepath)
            papers.append(paper_info)

        return sorted(papers, key=lambda p: p.filename)

    def _read_paper_info(self, filepath: Path) -> PaperInfo:
        """
        Read metadata from a single PDF file.

        This is a private method (starts with _) - it's internal
        to the service and not exposed as a tool.

        Args:
            filepath: Path to the PDF file

        Returns:
            PaperInfo with metadata from the PDF
        """
        filename = filepath.name
        file_size_kb = filepath.stat().st_size / 1024

        title = None
        page_count = 0

        try:
            doc = fitz.open(str(filepath))
            page_count = len(doc)
            title = self._extract_title(doc, filename)
            doc.close()
        except Exception:
            pass

        return PaperInfo(
            filename=filename,
            filepath=filepath,
            title=title,
            page_count=page_count,
            file_size_kb=round(file_size_kb, 2),
        )

    def _extract_title(self, doc: fitz.Document, filename: str) -> str:
        """
        Extract title from PDF metadata or filename.

        Tries these sources in order:
        1. PDF metadata title field
        2. Fallback to filename without extension

        Args:
            doc: PyMuPDF document object
            filename: Original filename

        Returns:
            Extracted or derived title
        """
        if doc.metadata:
            title = doc.metadata.get("title", "").strip()
            if title:
                return title

        return Path(filename).stem.replace("_", " ").replace("-", " ").title()
