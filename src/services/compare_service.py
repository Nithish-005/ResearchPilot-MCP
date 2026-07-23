"""Compare service - business logic for comparing papers."""

from pathlib import Path
from typing import List, Dict, Optional

import fitz


class CompareService:
    """Service for comparing multiple research papers."""

    def __init__(self, papers_directory: Path) -> None:
        """Initialize with the papers directory path."""
        self.papers_directory = papers_directory

    def compare_papers(self, filenames: List[str]) -> dict:
        """
        Compare multiple papers and return analysis.

        Args:
            filenames: List of PDF filenames to compare

        Returns:
            Dictionary with comparison results
        """
        if len(filenames) < 2:
            return {"error": "At least 2 papers required for comparison"}

        papers_data = []

        for filename in filenames:
            paper_info = self._read_paper_info(filename)
            if paper_info:
                papers_data.append(paper_info)
            else:
                papers_data.append(
                    {"filename": filename, "error": "Could not read paper"}
                )

        if len(papers_data) < 2:
            return {"error": "Not enough valid papers to compare"}

        comparison = {
            "papers_count": len(papers_data),
            "papers": papers_data,
            "summary": self._generate_comparison_summary(papers_data),
            "common_keywords": self._find_common_keywords(papers_data),
        }

        return comparison

    def _read_paper_info(self, filename: str) -> Optional[Dict]:
        """Read information from a single paper."""
        filepath = self.papers_directory / filename

        if not filepath.exists():
            return None

        try:
            doc = fitz.open(str(filepath))

            title = doc.metadata.get("title", "").strip()
            if not title:
                title = self._title_from_filename(filename)

            authors = doc.metadata.get("author", "").strip() or "Unknown"

            keywords = self._extract_keywords(doc)

            full_text = ""
            for page in doc:
                full_text += page.get_text()

            doc.close()

            return {
                "filename": filename,
                "title": title,
                "authors": authors,
                "page_count": len(doc) if not filepath.exists() else 0,
                "keywords": keywords[:10],
                "word_count": len(full_text.split()),
                "text_preview": full_text[:500] if full_text else "",
            }
        except Exception:
            return None

    def _title_from_filename(self, filename: str) -> str:
        """Convert filename to a readable title."""
        name = Path(filename).stem
        name = name.replace("_", " ").replace("-", " ")
        words = name.split()
        return " ".join(word.capitalize() for word in words)

    def _extract_keywords(self, doc: fitz.Document) -> List[str]:
        """Extract keywords from PDF metadata or first page."""
        keywords = []

        if doc.metadata.get("keywords"):
            keywords = [k.strip() for k in doc.metadata.get("keywords").split(",")]

        if not keywords and len(doc) > 0:
            first_page_text = doc[0].get_text().lower()
            academic_keywords = [
                "neural",
                "network",
                "learning",
                "model",
                "training",
                "data",
                "algorithm",
                "performance",
                "accuracy",
                "system",
                "method",
                "approach",
                "result",
                "experiment",
                "evaluation",
                "analysis",
            ]
            found = [kw for kw in academic_keywords if kw in first_page_text]
            keywords = found[:5]

        return keywords

    def _generate_comparison_summary(self, papers_data: List[Dict]) -> str:
        """Generate a text summary comparing the papers."""
        if not papers_data:
            return "No papers to compare."

        pages = [p.get("page_count", 0) for p in papers_data if "error" not in p]
        words = [p.get("word_count", 0) for p in papers_data if "error" not in p]

        summary_parts = [f"Comparing {len(papers_data)} papers:"]

        for i, paper in enumerate(papers_data, 1):
            if "error" in paper:
                summary_parts.append(f"  {i}. {paper['filename']} - Error reading")
            else:
                summary_parts.append(
                    f"  {i}. {paper['title'][:50]}... "
                    f"({paper['page_count']} pages, {paper.get('word_count', 0)} words)"
                )

        if pages:
            summary_parts.append(
                f"\nTotal pages: {sum(pages)}, Average: {sum(pages) // len(pages)} pages/paper"
            )

        return "\n".join(summary_parts)

    def _find_common_keywords(self, papers_data: List[Dict]) -> List[str]:
        """Find keywords that appear in multiple papers."""
        keyword_sets = []

        for paper in papers_data:
            if "error" not in paper and paper.get("keywords"):
                kw_set = set(kw.lower() for kw in paper["keywords"])
                keyword_sets.append(kw_set)

        if len(keyword_sets) < 2:
            return []

        common = keyword_sets[0]
        for kw_set in keyword_sets[1:]:
            common = common.intersection(kw_set)

        return list(common)[:10]

    def find_similar_papers(self, filename: str, max_results: int = 5) -> List[dict]:
        """
        Find papers similar to the given paper.

        Currently uses simple keyword overlap. Later can use embeddings.

        Args:
            filename: Reference paper filename
            max_results: Maximum number of similar papers to return

        Returns:
            List of similar papers with similarity scores
        """
        target_paper = self._read_paper_info(filename)
        if not target_paper:
            return [{"error": f"Could not read paper: {filename}"}]

        target_keywords = set(kw.lower() for kw in target_paper.get("keywords", []))
        if not target_keywords:
            words = target_paper.get("text_preview", "").lower().split()
            target_keywords = set(w for w in words if len(w) > 5)

        results = []

        for filepath in self.papers_directory.glob("*.pdf"):
            if filepath.name == filename:
                continue

            other_paper = self._read_paper_info(filepath.name)
            if not other_paper:
                continue

            other_keywords = set(kw.lower() for kw in other_paper.get("keywords", []))
            if not other_keywords:
                other_keywords = set(
                    w
                    for w in other_paper.get("text_preview", "").lower().split()
                    if len(w) > 5
                )

            intersection = target_keywords.intersection(other_keywords)
            union = target_keywords.union(other_keywords)

            if union:
                similarity = len(intersection) / len(union)
            else:
                similarity = 0

            if similarity > 0:
                results.append(
                    {
                        "filename": filepath.name,
                        "title": other_paper.get("title", ""),
                        "similarity_score": round(similarity, 3),
                        "common_keywords": list(intersection)[:5],
                    }
                )

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:max_results]
