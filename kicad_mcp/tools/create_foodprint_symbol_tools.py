import os
import logging
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from pathlib import Path


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_sunprocess.log'),
        logging.StreamHandler()

    ]
)

from kicad_mcp.utils.create_foodprint_symbol_utils import *


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
    def save_footprint_mod(mod_data: str, footprint_name: str, lib_name: str) -> Dict[str, Any]:
        """
        Save the generated foodprint in Library
        """

        if not save_kicad_footprint(mod_data, footprint_name, lib_name):
            return {"success": False}
        else:
            return {"success": True}


    @mcp.tool()
    def add_footprint_to_Lib(lib_path: str, lib_name: str, description: str) -> Dict[str, Any]:
        """
        Save the generated foodprint in global Footprint Table
        """

        type = "footprint"

        if not save_kicad_footprint_symbol_to_table(lib_name, description, type):
            return {"success": False}
        else:
            return {"success": True, "Path": lib_path}

    @mcp.tool()
    def save_symbol(file_data: str, symbol_name: str, lib_name: str) -> Dict[str, Any]:
        """
        Save the generated symbol in Library
        """

        if not save_kicad_symbol(file_data, symbol_name, lib_name):
            return {"success": False}
        else:
            return {"success": True}
        

    @mcp.tool()
    def add_symbol_to_Lib(lib_path: str, lib_name: str, description: str) -> Dict[str, Any]:
        """
        Save the generated symbol in global symbol Table
        """

        type = "symbol"

        if not save_kicad_footprint_symbol_to_table(lib_name, description, type):
            return {"success": False}
        else:
            return {"success": True, "Path": lib_path}
        
    
    
    
    @mcp.tool()
    def validate_symbol_structure(symbol_content: str) -> Dict[str, Any]:
        """
        Check Structure of Symbol
        """
        result = validate_kicad_symbol(symbol_content)
        return result
    

    @mcp.tool()
    def validate_footprint_structure(footprint_content: str) -> Dict[str, Any]:
        """
        Check Structure of Footprint
        """
        result = validate_kicad_footprint(footprint_content)
        return result


    # not helpful because of Claudes Rate Limits
    '''
    @mcp.tool()
    def analyze_pdf(pdf_data: str) -> List[Dict[str, Any]]:
        """
        Analyze a single PDF from Claude input.
        
        Args:
            pdf_url: A public URL pointing to a PDF file.
            prompt: A question or instruction for Claude to apply to the PDF.
        
        Returns:
            Claude's analysis of the document or error if failed.
        """
        logging.info("Executing analyze_pdf_url tool")

        return
    '''