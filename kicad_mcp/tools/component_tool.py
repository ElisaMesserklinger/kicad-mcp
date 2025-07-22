import sys
import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP, Context
import subprocess


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kicad_mcp.log'),  # Also log to file
    ]
)

logger = logging.getLogger(__name__)

from kicad_mcp.utils.kicad_bridge import KiCadBridge

try:
    kicad_subprocess = KiCadBridge()
    logger.info("KiCadBridge initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize KiCadBridge: {e}")
    kicad_subprocess = None

def register_component_tools(mcp: FastMCP) -> None:
    """Register component placement tools using direct pcbnew API."""
    
    @mcp.tool()
    async def load_pcb_board(project_path: str, ctx: Context) -> Dict[str, Any]:
        """Load a KiCad PCB board for component operations.
        
        Args:
            project_path: Path to the .kicad_pro file
            
        Returns:
            Dict with success status and board information
        """
    
    
        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            ctx.error(error_msg)
            return {"success": False, "error": error_msg}
        
        ctx.info(f"Loading PCB board from {project_path}")
        await ctx.report_progress(10, 100)
        
        # Log the exact path being used
        ctx.info(f"Absolute path: {os.path.abspath(project_path)}")
        ctx.info(f"Path exists: {os.path.exists(project_path)}")
        logger.debug(f"Absolute path: {os.path.abspath(project_path)}")
        logger.debug(f"Path exists: {os.path.exists(project_path)}")


        # Check if corresponding PCB file exists
        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
            ctx.info(f"PCB file path: {pcb_path}")
            ctx.info(f"PCB file exists: {os.path.exists(pcb_path)}")
        else:
            pcb_path = project_path
      
        try:
            # Add timeout handling and better error reporting
            ctx.info("Starting board load operation...")
            logger.info("Starting board load operation...")
            
            result = kicad_subprocess.load_board(pcb_path)

            await ctx.report_progress(100, 100)
            
            if result.get("success"):
                ctx.info("Board loaded successfully")
                logger.info("Board loaded successfully")
                ctx.info(f"Board info: {result.get('board_info', {})}")
            else:
                error_msg = result.get("error", "Failed to load board")
                ctx.error(f"Board load failed: {error_msg}")
                logger.error("Board failed to load")
            
            return result or {
            "success": False,
            "error": "Load Board Failed with an unkown error"
        }
            
        except asyncio.TimeoutError:
            error_msg = "Board load operation timed out"
            ctx.error(error_msg)
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error during board load: {str(e)}"
            ctx.error(error_msg)
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    
    @mcp.tool()
    async def place_component(
        project_path: str,
        component_id: str,
        position: Dict[str, Any],
        library: str,
        reference: Optional[str] = None,
        value: Optional[str] = None,
        rotation: float = 0,
        layer: str = "F.Cu",
        output_path: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """Place a component on the PCB (load -> place -> save in one operation).
        
        Args:
            project_path: Path to the .kicad_pro file
            component_id: Component/footprint ID (e.g., "R_0805_2012Metric")
            position: Position dict with x, y coordinates in mm
            reference: Optional reference designator (e.g., "R1")
            value: Optional component value (e.g., "1k")
            rotation: Rotation in degrees (default: 0)
            layer: Layer name (default: "F.Cu")
            library: Optional library name (e.g., "Resistor_SMD")
            output_path: Optional output path for saving
            
        Returns:
            Dict with success status and component info
        """

        
        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            ctx.error(error_msg)
            return {"success": False, "error": error_msg}
       
        if ctx:
            ctx.info(f"Placing component {component_id} at {position}")
            await ctx.report_progress(10, 100)

        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        
        try:
            
            result = kicad_subprocess.place_component(
                project_path=pcb_path,
                component_id=component_id,
                position=position,
                library=library,
                reference=reference,
                value=value,
                rotation=rotation,
                layer=layer,
                output_path=output_path
            )
            
                    
            if ctx:
                await ctx.report_progress(100, 100)
                if result.get("success"):
                    comp_ref = result.get("component", {}).get("reference", "Unknown")
                    ctx.info(f"Component {comp_ref} placed and saved successfully")
                else:
                    ctx.error(f"Component placement failed: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error placing component: {str(e)}"
            if ctx:
                ctx.error(error_msg)
            return {"success": False, "error": error_msg}
        
    @mcp.tool()
    async def move_component(
    project_path: str,
    reference: str,
    position: Dict[str, Any],
    rotation: Optional[float] = None,
    ctx: Context = None
    ) -> Dict[str, Any]:
        """Move a component to a new position on the PCB.
        
        Args:
            project_path: Path to the .kicad_pro file
            reference: Reference designator of the component (e.g., 'R5', 'C1', 'U3')
            position: Position dict with x, y coordinates in mm
            rotation: Optional new rotation in degrees (default: no rotation change)
            
        Returns:
            Dict with success status and component info
        """

        # Check if KiCadBridge is available
        if kicad_subprocess is None:
            error_msg = "KiCadBridge not initialized"
            ctx.error(error_msg)
            return {"success": False, "error": error_msg}
        
        if ctx:
            ctx.info(f"Moving component {reference} to {position}")
            logger.debug("Ready to move component:")
            await ctx.report_progress(10, 100)
        
        # Convert project path to PCB path
        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path
        
        # Log the operation
        ctx.info(f"Moving component {reference} to position {position}")
        logger.info(f"Moving component {reference} to position {position}")
        
        try:
            # Validate position dictionary
            if not isinstance(position, dict):
                raise ValueError("Position must be a dictionary")
            
            required_keys = ['x', 'y']
            for key in required_keys:
                if key not in position:
                    raise ValueError(f"Position dictionary missing required key: {key}")
            
            # Validate coordinates
            if not isinstance(position['x'], (int, float)):
                raise ValueError("X coordinate must be a number")
            if not isinstance(position['y'], (int, float)):
                raise ValueError("Y coordinate must be a number")
            
            # Validate rotation if provided
            if rotation is not None and not isinstance(rotation, (int, float)):
                raise ValueError("Rotation must be a number")
            
            # Call the KiCad bridge to move the component
            result = kicad_subprocess.move_component(
                project_path=pcb_path,
                reference=reference,
                position=position,
                rotation=rotation
            )
            
            if ctx:
                await ctx.report_progress(100, 100)
                if result.get("success"):
                    ctx.info(f"Component {reference} moved successfully")
                else:
                    ctx.error(f"Component move failed: {result.get('error')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error moving component {reference}: {str(e)}"
            if ctx:
                ctx.error(error_msg)
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "reference": reference}

