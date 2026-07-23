"""Summary service - business logic for summarizing papers."""

from pathlib import Path
from typing import Optional

import fitz


class SummaryService:
    """Service for generating summaries of research papers."""

    def __init__(self, papers_directory: Path) -> None:
        """Initialize with the papers directory path."""
        self.papers_directory = papers_directory

    def summarize_paper(self, filename: str, max_length: int = 500) -> dict:
        """
        Generate a summary of a paper.

        Extracts key sections and generates an overview.

        Args:
            filename: Name of the PDF file
            max_length: Maximum character length of summary

        Returns:
            Dictionary with summary and metadata
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))

            title = doc.metadata.get("title", "").strip()
            if not title:
                title = self._title_from_filename(filename)

            authors = doc.metadata.get("author", "").strip() or "Unknown"

            full_text = ""
            for page in doc:
                full_text += page.get_text()

            doc.close()

            sections = self._extract_sections(full_text)

            summary = self._generate_summary(sections, full_text, max_length)

            return {
                "filename": filename,
                "title": title,
                "authors": authors,
                "page_count": len(doc) if not filepath.exists() else 0,
                "sections_found": list(sections.keys()),
                "summary": summary,
                "key_findings": self._extract_key_findings(full_text),
            }
        except Exception as e:
            return {"error": str(e)}

    def _title_from_filename(self, filename: str) -> str:
        """Convert filename to a readable title."""
        name = Path(filename).stem
        name = name.replace("_", " ").replace("-", " ")
        return name.title()

    def _extract_sections(self, text: str) -> dict:
        """Extract major sections from the paper text."""
        sections = {}

        section_markers = {
            "abstract": ["abstract"],
            "introduction": ["1. introduction", "i. introduction", "introduction"],
            "methods": ["2. related work", "2. background", "methods", "methodology"],
            "results": ["3. experiments", "3. evaluation", "results", "experiments"],
            "conclusion": ["4. conclusion", "conclusion", "conclusions"],
        }

        lines = text.split("\n")
        current_section = "other"
        current_content = []

        for line in lines:
            line_lower = line.lower().strip()

            found_section = None
            for section_name, markers in section_markers.items():
                if any(marker in line_lower for marker in markers):
                    if current_content or current_section != "other":
                        sections[current_section] = "\n".join(current_content[:50])
                    current_section = section_name
                    current_content = []
                    found_section = True
                    break

            if not found_section:
                current_content.append(line)

        if current_content:
            if current_section not in sections:
                sections[current_section] = "\n".join(current_content[:50])

        return sections

    def _generate_summary(self, sections: dict, full_text: str, max_length: int) -> str:
        """Generate a summary from paper sections."""
        summary_parts = []

        if "abstract" in sections and sections["abstract"]:
            abstract = sections["abstract"].strip()
            if abstract:
                summary_parts.append(f"Abstract: {abstract[:300]}")

        if "introduction" in sections and sections["introduction"]:
            intro = sections["introduction"].strip()
            if intro:
                summary_parts.append(f"Introduction: {intro[:200]}")

        if "conclusion" in sections and sections["conclusion"]:
            conclusion = sections["conclusion"].strip()
            if conclusion:
                summary_parts.append(f"Conclusion: {conclusion[:200]}")

        if not summary_parts:
            first_para = (
                full_text.split("\n\n")[0] if "\n\n" in full_text else full_text[:500]
            )
            summary_parts.append(f"Overview: {first_para[:400]}")

        summary = "\n\n".join(summary_parts)

        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary

    def _extract_key_findings(self, text: str) -> list:
        """Extract potential key findings from the text."""
        findings = []

        indicator_phrases = [
            "we find that",
            "our results show",
            "we demonstrate",
            "we propose",
            "we introduce",
            "significant improvement",
            "outperforms",
            "state-of-the-art",
            "achieves",
            "results indicate",
        ]

        text_lower = text.lower()
        sentences = text.split(".")

        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            for phrase in indicator_phrases:
                if phrase in sentence_lower and len(sentence) > 50:
                    finding = sentence.strip()
                    if finding and len(finding) < 300:
                        findings.append(finding)
                    break

        return findings[:5]

    def get_paper_overview(self, filename: str) -> dict:
        """
        Get a quick overview of a paper without full summary.

        Args:
            filename: Name of the PDF file

        Returns:
            Dictionary with paper overview
        """
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return {"error": f"File not found: {filename}"}

        try:
            doc = fitz.open(str(filepath))

            title = doc.metadata.get("title", "").strip()
            if not title:
                title = self._title_from_filename(filename)

            authors = doc.metadata.get("author", "").strip() or "Unknown"
            subject = doc.metadata.get("subject", "").strip()

            first_page_text = doc[0].get_text() if len(doc) > 0 else ""
            first_para = (
                first_page_text.split("\n\n")[0]
                if "\n\n" in first_page_text
                else first_page_text[:500]
            )

            doc.close()

            return {
                "filename": filename,
                "title": title,
                "authors": authors,
                "page_count": len(doc),
                "journal": subject or "Not specified",
                "first_paragraph": first_para[:500],
            }
        except Exception as e:
            return {"error": str(e)}
