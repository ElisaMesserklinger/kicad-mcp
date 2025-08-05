import os
import logging
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Any, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kicad-mcp.log'),
    ]
)

from kicad_mcp.utils.create_foodprint_symbol_utils import *

def register_footprint_symbol_tools(mcp: FastMCP) -> None:
    """
    Register a set of tools for handling KiCad library management and PDF handling 
    with the FastMCP server instance.

    These tools include:
        - Listing PDF files from configured paths
        - Saving KiCad footprints and symbols to libraries
        - Adding those libraries to the global KiCad configuration
        - Validating the structure of symbols and footprints

    Args:
        mcp: The FastMCP server instance where tools are being registered.
    """

    @mcp.tool()
    def list_pdfs() -> List[Dict[str, Any]]:
        """
        Tool: List all PDF files from configured search directories.

        Searches for PDF files recursively in the paths defined in the project configuration.
        
        Returns:
            A list of dictionaries with PDF metadata (e.g. file name, path).
        """

        logging.info("Executing list_pdfs tool...")
        return find_pdfs()

    @mcp.tool()
    def save_footprint_mod(mod_data: str, footprint_name: str, lib_name: str) -> Dict[str, Any]:
        """
        Tool: Save a footprint (.kicad_mod) file into a KiCad footprint library.

        Args:
            mod_data: The raw text content of the .kicad_mod file (S-expression format).
            footprint_name: The name for the new footprint.
            lib_name: The target KiCad library name where the footprint will be saved.

        Returns:
            A dictionary with a success flag: { "success": True } or { "success": False }
        """

        return save_kicad_footprint(mod_data, footprint_name, lib_name)


    @mcp.tool()
    def add_footprint_to_Lib(lib_name: str, description: str) -> Dict[str, Any]:
        """
        Tool: Add a footprint library to the global KiCad footprint table.

        This registers the library so KiCad can access it globally.

        Args:
            lib_path: Path to the footprint library directory.
            lib_name: Name of the library.
            description: Description for the library entry.

        Returns:
            A dictionary with success flag and optionally the path:
            e.g. { "success": True, "Path": lib_path }
        """

        type = "footprint" #differentiate between footprint and symbol

        return save_kicad_footprint_symbol_to_table(lib_name, description, type)
    

    @mcp.tool()
    def save_symbol(file_data: str, symbol_name: str, lib_name: str) -> Dict[str, Any]:
        """
        Tool: Save a symbol (.kicad_sym) into a KiCad symbol library.

        Args:
            file_data: The full content of the symbol in KiCad S-expression format.
            symbol_name: The name of the symbol to save.
            lib_name: The name of the symbol library to save into.

        Returns:
            A dictionary with a success flag.
        """
        return save_kicad_symbol(file_data, symbol_name, lib_name)

    @mcp.tool()
    def add_symbol_to_Lib(lib_name: str, description: str) -> Dict[str, Any]:
        """
        Tool: Add a symbol library to the global KiCad symbol table.

        Registers the symbol library so it can be used across projects.

        Args:
            lib_path: Path to the symbol library file (.kicad_sym).
            lib_name: Name of the symbol library.
            description: Description of the library.

        Returns:
            A dictionary with success flag and library path if successful.
        """

        type = "symbol" #differentiate between footprint and symbol

        return save_kicad_footprint_symbol_to_table(lib_name, description, type)
    
    
    
    @mcp.tool()
    def validate_symbol_structure(symbol_content: str) -> Dict[str, Any]:
        """
        Tool: Validate the structure of a KiCad symbol.

        This function parses the symbol file content and checks it against KiCad standards.
        Useful for catching formatting or semantic errors before saving.

        Args:
            symbol_content: The raw S-expression content of the symbol.

        Returns:
            A dictionary containing validation status and any errors or warnings.
            
        """
        return validate_kicad_symbol(symbol_content)
    

    @mcp.tool()
    def validate_footprint_structure(footprint_content: str) -> Dict[str, Any]:
        """
        Tool: Validate the structure of a KiCad footprint.

        Parses the footprint data and checks its structure for correctness.

        Args:
            footprint_content: The full content of a .kicad_mod file as a string.

        Returns:
            A dictionary with validation results.
        """
        return validate_kicad_footprint(footprint_content)
    

    @mcp.tool()
    def edit_footprint_symbol_files(content: str, filename: str, filetype: str) -> Dict[str, Any]:
        """
        Overwrites the content of a specific footprint or symbol file with new content.

        Parameters:
            content (str): The new content to write to the file.
            filename (str): The relative path (from a predefined base directory) to the target file.

        Returns:
            Dict[str, Any]: A dictionary indicating the success or failure of the operation, 
                            including a message and optionally an error detail.
        """

        return accessFiles(content, filename, filetype)
    

    @mcp.tool()
    def get_content(filename: str, filetype: str) -> Dict[str, Any]:
        """
        Retrieves the content of a specified file based on its filename and type.
        
        Parameters:
            filename (str): The name of the file (without extension).
            filetype (str): The type of the file, e.g., "symbol" or "footprint".
            
        Returns:
            Dict[str, Any]: A dictionary containing the success status and either
                            the file content or an error message.
        """
        return readFileContent(filename, filetype)
    
    @mcp.tool()
    def make_pdf_smaller(input_pdf_path: str, output_dir: str, pages_per_split: int, filename: str) -> Dict[str, Any]:
        """
        Split a PDF file into smaller chunks.
        
        Args:
            input_pdf_path (str): Path to the input PDF file
            output_dir (str): Directory where split files will be saved
            pages_per_split (int): Number of pages per split file
            
        Returns:
            Dict
        """
        return split_pdf(input_pdf_path, output_dir, pages_per_split, filename)

