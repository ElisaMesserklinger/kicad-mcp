import os
import logging
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv


from kicad_mcp.utils.create_foodprint_utils import find_pdfs, analyze_pdfs

from kicad_mcp.config import KICAD_USER_DIR, ADDITIONAL_SEARCH_PATHS, DATASHEET_PATH
load_dotenv()


def register_pdf_tools(mcp: FastMCP) -> None:
    """Register PDF file management tools with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """

    @mcp.tool()
    def list_pdfs() -> List[Dict[str, Any]]:
        """Find and list all PDF files in configured search directories."""
        logging.info("Executing list_pdfs tool...")
        pdfs = find_pdfs()
        logging.info(f"list_pdfs tool returning {len(pdfs)} PDF files.")
        return pdfs
    
    @mcp.tool()
    def analyze_pdf_url(pdf_url: str, prompt: str) -> List[Dict[str, Any]]:
        """
        Analyze a single PDF from a URL using Claude with a given prompt.
        
        Args:
            pdf_url: A public URL pointing to a PDF file.
            prompt: A question or instruction for Claude to apply to the PDF.
        
        Returns:
            Claude's analysis of the document or error if failed.
        """
        logging.info(f"Executing analyze_pdf_url tool on: {pdf_url}")
        result = analyze_pdfs(pdf_url, prompt)
        return result