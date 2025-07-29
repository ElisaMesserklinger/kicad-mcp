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
        Extract all net names and their corresponding net codes from the loaded PCB.

        This function loads the specified KiCad PCB file and retrieves a list of all nets 
        along with their associated codes. It also gathers detailed information about 
        each pad, including position, net connection, and footprint metadata.

        Args:
            project_path (str): Absolute path to the KiCad `.kicad_pcb` file.

        Returns:
            dict
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
            "error": " Extracting Netlist"
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
    def track_routes(project_path: str, routes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Route multiple tracks with the given properties.

        This function places PCB tracks between multiple start and end points or pads on a specified layer, 
        using the provided width and assigning each to the specified net.

        Args:
            routes (list): A list of route dictionaries. Each route should have:
                - start (dict): Start coordinates or pad position (e.g., {"x": float, "y": float}).
                - end (dict): End coordinates or pad position (e.g., {"x": float, "y": float}).
                - layer (str): PCB layer to draw the track on (e.g., "F.Cu", "B.Cu").
                - width (float): Width of the track in millimeters.
                - net (str): Name of the net to associate with the track (must exist on the board).

        Returns:
            dict: Result object containing success status, routing metadata for all routes, and any errors.
        """
       
        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            return {"success": False, "error": error_msg}

        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path


        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            return {"success": False, "error": error_msg}
        
        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path
        
        results = []  
        
        try:
            logging.info("Starting routing operation...")

            # Route each track
            result = kicad_subprocess.track_pcb_routes(pcb_path, routes)

            # Log and append the result
            if result.get("success"):
                logging.info(f"Routes placed successfully: {routes}")
            else:
                logging.error(f"Failed to place routes: {routes}")
                
                return(result or {
                    "success": False,
                    "error": "Failed to place track",
                    "routes": result
                })
            
            return {
                "success": True,
                "message": "Routing operation completed",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Route placement timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error during placing routes: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
        

        #"C:/Users/messeel/KiCadProjects/KiCad\\hw_PB238_uiws_mainboard_test\\PB238_uiws_mainboard.kicad_pro"
        #"{"success": false, "message": "Exception occurred during routing", "error": "BoardManager.trace_routes() got an unexpected keyword argument 'start'"}