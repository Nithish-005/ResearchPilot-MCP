"""Citation service - business logic for generating citations."""

from pathlib import Path
from typing import Optional
import datetime

import fitz


class CitationService:
    """Service for generating citations in various formats."""

    def __init__(self, papers_directory: Path) -> None:
        """Initialize with the papers directory path."""
        self.papers_directory = papers_directory

    def generate_ieee_citation(
        self, filename: str, authors: Optional[str] = None
    ) -> dict:
        """
        Generate an IEEE format citation for a paper.

        IEEE format: [Authors]. "[Title]". [Journal], [Volume], [Issue], [Pages], [Year].

        Args:
            filename: Name of the PDF file
            authors: Author names (if known, otherwise extracted from metadata)

        Returns:
            Dictionary with citation details and formatted string
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))
            metadata = doc.metadata

            title = metadata.get("title", "").strip() or self._title_from_filename(
                filename
            )

            if not authors:
                authors = metadata.get("author", "").strip() or "Unknown Author"

            year = metadata.get("creationDate", "")
            if year:
                try:
                    dt = datetime.datetime.fromisoformat(
                        year.replace("D:", "").split("+")[0]
                    )
                    year = str(dt.year)
                except Exception:
                    year = "n.d."
            else:
                year = "n.d."

            subject = metadata.get("subject", "").strip()
            if subject:
                journal_info = f"{subject}"
            else:
                journal_info = "arXiv preprint"

            doc.close()

            citation_text = f'{authors}. "{title}". {journal_info}, {year}.'

            return {
                "filename": filename,
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal_info,
                "ieee_citation": citation_text,
            }
        except Exception as e:
            return {"error": str(e)}

    def _title_from_filename(self, filename: str) -> str:
        """Convert filename to a readable title."""
        name = Path(filename).stem
        name = name.replace("_", " ").replace("-", " ")
        words = name.split()
        return " ".join(word.capitalize() for word in words)

    def generate_apa_citation(
        self, filename: str, authors: Optional[str] = None
    ) -> dict:
        """
        Generate an APA format citation for a paper.

        APA format: Author, A. A. (Year). Title. Journal, Volume(Issue), Pages.

        Args:
            filename: Name of the PDF file
            authors: Author names (if known)

        Returns:
            Dictionary with citation details and formatted string
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))
            metadata = doc.metadata

            title = metadata.get("title", "").strip() or self._title_from_filename(
                filename
            )

            if not authors:
                authors = metadata.get("author", "").strip() or "Unknown Author"

            year = "n.d."
            if metadata.get("creationDate"):
                try:
                    dt = datetime.datetime.fromisoformat(
                        metadata.get("creationDate", "").replace("D:", "").split("+")[0]
                    )
                    year = str(dt.year)
                except Exception:
                    pass

            doc.close()

            apa_citation = f"{authors} ({year}). {title}."

            return {
                "filename": filename,
                "title": title,
                "authors": authors,
                "year": year,
                "apa_citation": apa_citation,
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_bibtex(self, filename: str, authors: Optional[str] = None) -> dict:
        """
        Generate a BibTeX entry for a paper.

        Args:
            filename: Name of the PDF file
            authors: Author names (if known)

        Returns:
            Dictionary with BibTeX entry
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))
            metadata = doc.metadata

            title = metadata.get("title", "").strip() or self._title_from_filename(
                filename
            )

            if not authors:
                authors = metadata.get("author", "").strip() or "Unknown Author"

            year = "2024"
            if metadata.get("creationDate"):
                try:
                    dt = datetime.datetime.fromisoformat(
                        metadata.get("creationDate", "").replace("D:", "").split("+")[0]
                    )
                    year = str(dt.year)
                except Exception:
                    pass

            doc.close()

            cite_key = self._generate_cite_key(title, authors)

            bibtex = f"""@{metadata.get("type", "article")}{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  year = {{{year}}},
  filename = {{{filename}}}
}}"""

            return {"filename": filename, "cite_key": cite_key, "bibtex": bibtex}
        except Exception as e:
            return {"error": str(e)}

    def _generate_cite_key(self, title: str, authors: str) -> str:
        """Generate a BibTeX citation key from title and authors."""
        first_author = authors.split(",")[0].split("&")[0].strip()
        last_name = first_author.split()[-1] if first_author else "unknown"
        year = datetime.datetime.now().year
        title_word = title.split()[0].lower() if title else "paper"
        return f"{last_name}{year}{title_word}"
