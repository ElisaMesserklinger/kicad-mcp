"""
Analysis and validation tools for KiCad projects.
"""
import os
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP, Context, Image
import logging
import asyncio


from kicad_mcp.utils.file_utils import get_project_files
from kicad_mcp.utils.kicad_bridge import KiCadBridge


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kicad-mcp.log'),
    ]
)

try:
    kicad_subprocess = KiCadBridge()
    logging.info("KiCadBridge initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize KiCadBridge: {e}")
    kicad_subprocess = None



def register_analysis_tools(mcp: FastMCP) -> None:
    """Register analysis and validation tools with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.tool()
    def validate_project(project_path: str) -> Dict[str, Any]:
        """Basic validation of a KiCad project."""
        if not os.path.exists(project_path):
            return {"valid": False, "error": f"Project not found: {project_path}"}
        
        issues = []
        files = get_project_files(project_path)
        
        # Check for essential files
        if "pcb" not in files:
            issues.append("Missing PCB layout file")
        
        if "schematic" not in files:
            issues.append("Missing schematic file")
        
        # Validate project file
        try:
            with open(project_path, 'r') as f:
                import json
                json.load(f)
        except json.JSONDecodeError:
            issues.append("Invalid project file format (JSON parsing error)")
        except Exception as e:
            issues.append(f"Error reading project file: {str(e)}")
        
        return {
            "valid": len(issues) == 0,
            "path": project_path,
            "issues": issues if issues else None,
            "files_found": list(files.keys())
        }


        
    @mcp.tool()
    def pcb_basicInfo(project_path: str) -> Dict[str, Any]:

        """
        Tool: Extract basic information about the PCB.

        Retrieves bounding box, filename, and net count from the KiCad PCB layout.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary containing board metadata or an error message.
            
        """

        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err

        pcb_path = resolve_pcb_path(project_path)


        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_basic_info(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}

    @mcp.tool()
    def pcb_designRules(project_path: str) -> Dict[str, Any]:

        """
        Tool: Extract design rule parameters from the PCB.

        Retrieves settings like minimum clearance, via size, and drill size.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary containing design rules or an error message.
        """

        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err

        pcb_path = resolve_pcb_path(project_path)



        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_designRules(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}

        
    @mcp.tool()
    def pcb_layers(project_path: str) -> Dict[str, Any]:

        """
        Tool: Extract information about active layers in the PCB.

        Gathers names and types of all enabled layers in the design.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary listing enabled PCB layers or an error message.
        """

        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err

        pcb_path = resolve_pcb_path(project_path)



        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_layers(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}

        
    @mcp.tool()
    def pcb_tracks_vias(project_path: str) -> Dict[str, Any]:

        """
        Tool: Extract all tracks and vias from the PCB layout.

        Differentiates between routed tracks and via connections.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary with lists of tracks and vias or an error message.
        """
        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err

        pcb_path = resolve_pcb_path(project_path)


        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_track_vias(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}

        
    @mcp.tool()
    def pcb_pads(project_path: str) -> Dict[str, Any]:

        """
        Tool: Extract pad and footprint data from the PCB.

        Collects information about each component, including pad geometry, position, and net connections.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary with components and their associated pads or an error message.
        """

        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err

        pcb_path = resolve_pcb_path(project_path)


        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_pads(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}

        
    @mcp.tool()
    def pcb_zones(project_path: str) -> Dict[str, Any]:
        """
        Tool: Extract copper zones from the PCB.

        Includes zone geometry, layer, thermal relief settings, and associated net.

        Args:
            project_path (str): Path to the KiCad project or PCB file.

        Returns:
            dict: Dictionary with list of zone me
            tadata or an error message.
        """
        # Check if KiCadBridge is available
        if (err := ensure_kicad_ready()):
            return err
        
        pcb_path = resolve_pcb_path(project_path)

        try:
            logging.info("Starting extracting information...")

            result = kicad_subprocess.extract_zones(pcb_path)

            if result.get("success"):
                    logging.info(f"Info extracted successfully")
            else:
                logging.error(f"Failed to extract info")
                    
                return(result or {
                    "success": False,
                    "error": "Failed to extract info",
                    "routes": result
                })
                
            return {
                "success": True,
                "message": "Info extracted",
                "routes": result
            }

        except asyncio.TimeoutError:
            error_msg = "Info extraction timed out"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Unexpected error during info extraction: {str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
        

    def ensure_kicad_ready() -> Optional[Dict[str, Any]]:
        """Check if KiCadBridge is available."""
        if kicad_subprocess is None:
            return {"success": False, "error": "KiCadBridge not initialized"}
        return None
    
    def resolve_pcb_path(project_path: str) -> str:
        """Convert .kicad_pro to .kicad_pcb if needed."""
        return project_path.replace(".kicad_pro", ".kicad_pcb") if project_path.endswith(".kicad_pro") else project_path
