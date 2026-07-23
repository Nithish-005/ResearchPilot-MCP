"""PDF service - business logic for PDF reading and parsing."""

from pathlib import Path
from typing import Optional

import fitz


class PDFService:
    """Service for reading and extracting content from PDF files."""

    def __init__(self, papers_directory: Path) -> None:
        """Initialize with the papers directory path."""
        self.papers_directory = papers_directory

    def read_pdf(self, filename: str, start_page: int = 0, max_pages: int = 10) -> dict:
        """
        Read content from a PDF file.

        Args:
            filename: Name of the PDF file (not full path)
            start_page: Page to start reading from (0-indexed)
            max_pages: Maximum number of pages to read

        Returns:
            Dictionary with extracted text and metadata
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))
            total_pages = len(doc)

            text_parts = []
            for page_num in range(start_page, min(start_page + max_pages, total_pages)):
                page = doc[page_num]
                text_parts.append(f"--- Page {page_num + 1} ---\n{page.get_text()}")

            doc.close()

            return {
                "filename": filename,
                "total_pages": total_pages,
                "pages_read": min(max_pages, total_pages - start_page),
                "content": "\n\n".join(text_parts),
            }
        except Exception as e:
            return {"error": str(e)}

    def extract_page(self, filename: str, page_number: int) -> Optional[str]:
        """
        Extract text from a specific page.

        Args:
            filename: Name of the PDF file
            page_number: Page number (1-indexed for user friendliness)

        Returns:
            Extracted text or None if page doesn't exist
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return None

        try:
            doc = fitz.open(str(filepath))
            if page_number < 1 or page_number > len(doc):
                doc.close()
                return None

            page = doc[page_number - 1]
            text = page.get_text()
            doc.close()
            return text
        except Exception:
            return None

    def extract_abstract(self, filename: str) -> Optional[str]:
        """
        Extract abstract from a PDF.

        Heuristic: Look for "Abstract" section at the beginning.

        Args:
            filename: Name of the PDF file

        Returns:
            Extracted abstract or None if not found
        """
        text = self.extract_page(filename, 1)
        if not text:
            return None

        text_lower = text.lower()

        if "abstract" in text_lower:
            lines = text.split("\n")
            abstract_start = -1
            for i, line in enumerate(lines):
                if "abstract" in line.lower():
                    abstract_start = i
                    break

            if abstract_start >= 0:
                abstract_lines = lines[abstract_start + 1 :]
                abstract_text = " ".join(
                    line.strip() for line in abstract_lines if line.strip()
                )

                for end_marker in [
                    "1. introduction",
                    "i. introduction",
                    "keywords",
                    "index terms",
                ]:
                    if end_marker in abstract_text.lower():
                        abstract_text = abstract_text.split(end_marker)[0]

                return abstract_text.strip()

        return None
