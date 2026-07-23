"""Search service - business logic for searching paper content."""

import re
from pathlib import Path
from typing import List, Tuple

import fitz


class SearchService:
    """Service for searching within PDF papers."""

    def __init__(self, papers_directory: Path) -> None:
        """Initialize with the papers directory path."""
        self.papers_directory = papers_directory

    def search_keyword(self, keyword: str, case_sensitive: bool = False) -> List[dict]:
        """
        Search for a keyword across all papers.

        Args:
            keyword: The keyword/phrase to search for
            case_sensitive: Whether to match case exactly

        Returns:
            List of matches with filename, page number, and snippet
        """
        results = []
        search_pattern = keyword if case_sensitive else keyword.lower()

        if not self.papers_directory.exists():
            return results

        for filepath in self.papers_directory.glob("*.pdf"):
            try:
                doc = fitz.open(str(filepath))
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    search_text = text if case_sensitive else text.lower()

                    if search_pattern in search_text:
                        matches = self._extract_snippets(text, keyword, case_sensitive)
                        for match_text, match_start in matches:
                            results.append(
                                {
                                    "filename": filepath.name,
                                    "page": page_num + 1,
                                    "snippet": match_text,
                                    "position": match_start,
                                }
                            )
                doc.close()
            except Exception:
                continue

        return results

    def _extract_snippets(
        self, text: str, keyword: str, case_sensitive: bool, context_chars: int = 150
    ) -> List[Tuple[str, int]]:
        """
        Extract snippets around keyword matches.

        Args:
            text: Full text to search in
            keyword: Keyword to find
            case_sensitive: Whether search is case-sensitive
            context_chars: Number of characters to include around match

        Returns:
            List of (snippet, position) tuples
        """
        snippets = []
        search_text = text if case_sensitive else text.lower()
        search_keyword = keyword if case_sensitive else keyword.lower()

        start = 0
        while True:
            pos = search_text.find(search_keyword, start)
            if pos == -1:
                break

            snippet_start = max(0, pos - context_chars)
            snippet_end = min(len(text), pos + len(keyword) + context_chars)

            snippet = text[snippet_start:snippet_end]
            if snippet_start > 0:
                snippet = "..." + snippet
            if snippet_end < len(text):
                snippet = snippet + "..."

            snippets.append((snippet.strip(), pos))
            start = pos + 1

        return snippets

    def search_multiple_keywords(
        self, keywords: List[str], match_all: bool = False
    ) -> List[dict]:
        """
        Search for multiple keywords across all papers.

        Args:
            keywords: List of keywords to search for
            match_all: If True, only return matches containing all keywords

        Returns:
            List of matches with filename, page number, and matched keywords
        """
        results = []

        if not self.papers_directory.exists():
            return results

        for filepath in self.papers_directory.glob("*.pdf"):
            try:
                doc = fitz.open(str(filepath))
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    text_lower = text.lower()

                    found_keywords = [kw for kw in keywords if kw.lower() in text_lower]

                    if found_keywords and not match_all:
                        results.append(
                            {
                                "filename": filepath.name,
                                "page": page_num + 1,
                                "matched_keywords": found_keywords,
                                "snippet": self._get_first_snippet(text, keywords),
                            }
                        )
                    elif match_all and len(found_keywords) == len(keywords):
                        results.append(
                            {
                                "filename": filepath.name,
                                "page": page_num + 1,
                                "matched_keywords": found_keywords,
                                "snippet": self._get_first_snippet(text, keywords),
                            }
                        )
                doc.close()
            except Exception:
                continue

        return results

    def _get_first_snippet(self, text: str, keywords: List[str]) -> str:
        """Get a snippet around the first matched keyword."""
        text_lower = text.lower()
        first_pos = len(text)

        for kw in keywords:
            pos = text_lower.find(kw.lower())
            if pos != -1 and pos < first_pos:
                first_pos = pos

        if first_pos == len(text):
            return text[:200] + "..."

        start = max(0, first_pos - 100)
        end = min(len(text), first_pos + 200)
        snippet = text[start:end]

        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet
