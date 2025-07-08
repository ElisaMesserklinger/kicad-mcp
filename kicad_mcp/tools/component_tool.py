import sys
import os
import logging
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# KiCad Python Path hinzufügen
sys.path.insert(0, "c:/Users/messeel/AppData/Local/Programs/KiCad/9.0/bin")


try:
    import pcbnew
    KICAD_AVAILABLE = True
except ImportError:
    KICAD_AVAILABLE = False
    logger.warning("KiCad Python API not available")


#board that should be added 
current_board = None
current_project_path = None


def register_component_tools(mcp: FastMCP) -> None:
    """Register component placement tools using direct pcbnew API."""

    @mcp.tool()
    def load_pcb_board(project_path: str) -> Dict[str, Any]:
        """Load a KiCad PCB board for component operations.
        
        Args:
            project_path: Path to the .kicad_pro file
            
        Returns:
            Dict with success status and board information
        """
        global current_board, current_project_path

        if not KICAD_AVAILABLE:
            return {
                "success": False,
                "message": "KiCad Python API not available",
                "error": "pcbnew module could not be imported"
            }
        
        try:
            # .kicad_pro → .kicad_pcb 
            if project_path.endswith('.kicad_pro'):
                pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
            else:
                pcb_path = project_path
            
            if not os.path.exists(pcb_path):
                return {
                    "success": False,
                    "message": f"PCB file not found: {pcb_path}"
                }
            
            # load current board
            current_board = pcbnew.LoadBoard(pcb_path)
            current_project_path = project_path

            #get all foodprints in pcb file
            footprints = list(current_board.GetFootprints())

        



    