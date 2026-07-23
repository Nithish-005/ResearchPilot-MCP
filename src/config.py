"""Configuration for ResearchPilot-MCP."""

from pathlib import Path


# Base directory where research papers are stored
# Default: ~/research_papers in user's home directory
PAPERS_DIRECTORY = Path.home() / "research_papers"

# Maximum number of papers to return in a single list
MAX_PAPERS_PER_LIST = 100

# PDF text extraction
PDF_EXTRACT_LENGTH = 5000  # Characters to extract for preview
