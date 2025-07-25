import os
import logging
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncio



logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kicad-mcp.log'),
    ]
)

from kicad_mcp.utils.kicad_bridge import KiCadBridge

from kicad_mcp.config import KICAD_USER_DIR, ADDITIONAL_SEARCH_PATHS, DATASHEET_PATH

try:
    kicad_subprocess = KiCadBridge()
    logging.info("KiCadBridge initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize KiCadBridge: {e}")
    kicad_subprocess = None

def register_routing_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def get_nets(project_path: str):
        
        """
        Route a track with the given properties.

        Args:
            start (dict): Start point or pad.
            end (dict): End point or pad.
            layer (str): Layer to route on.
            width (float): Track width.
            net (str): Net name.
        """

        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            return {"success": False, "error": error_msg}

        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path

        try:
            logging.info("Starting load net operation...")
            
            result = kicad_subprocess.get_net_pcb(pcb_path)
            
            if result.get("success"):
                logging.info("Nets extracted successfully")
            else:
                error_msg = result.get("error", "Failed to extract net")
                logging.error("Failed to extract net")
            
            return result or {
            "success": False,
            "error": "Load Board Failed with an unkown error"
        }
            
        except asyncio.TimeoutError:
            error_msg = "Net extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error during loading nets: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}




    @mcp.tool()
    def track_routes(project_path: str, start: dict, end: dict, layer: str, width: float, net: str):
        return 0





