"""ResearchPilot-MCP: MCP Server for Research Paper Interaction."""

from fastmcp import FastMCP

from src.tools.paper_tools import mcp as paper_mcp
from src.tools.pdf_tools import mcp as pdf_mcp
from src.tools.search_tools import mcp as search_mcp
from src.tools.compare_tools import mcp as compare_mcp
from src.tools.citation_tools import mcp as citation_mcp
from src.tools.summary_tools import mcp as summary_mcp
from src.tools.review_tools import mcp as review_mcp


# Main MCP server
mcp = FastMCP(
    name="ResearchPilot-MCP"
)


# Mount individual MCP modules
mcp.mount(paper_mcp)
mcp.mount(pdf_mcp)
mcp.mount(search_mcp)
mcp.mount(compare_mcp)
mcp.mount(citation_mcp)
mcp.mount(summary_mcp)
mcp.mount(review_mcp)


if __name__ == "__main__":
    mcp.run()