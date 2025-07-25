"""
Board-related utility functions for KiCad operations.
"""
import os
import sys
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

logging.basicConfig(filename="C:\Git\kicad-mcp\mcp_sunprocess.log", level=logging.DEBUG)

try:
    import pcbnew
    PCBNEW_AVAILABLE = True
except ImportError:
    PCBNEW_AVAILABLE = False
    pcbnew = None

class BoardManager:
    """Utility class for KiCad board operations."""
    
    def __init__(self):
        self.board = None
        self.project_path = None

    
    def load_board(self, project_path: str) -> Dict[str, Any]:
        """Load a KiCad PCB board.
        
        Args:
            project_path: Path to .kicad_pro file
            
        Returns:
            Dict with load result and board info
        """

        logging.debug(project_path)
        
        # Convert .kicad_pro to .kicad_pcb
        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path
        

        logging.debug(pcb_path)
        if not os.path.exists(pcb_path):
            return {
                "success": False,
                "message": f"PCB file not found: {pcb_path}"
            }
        
        try:
            

            try:
                self.board = pcbnew.LoadBoard(pcb_path)
            except Exception as e:
                return {"success": False, "error": f"Failed to load board: {str(e)}"}

            self.project_path = project_path
            
            return {
                "success": True,
                "message": f"Board loaded successfully: {pcb_path}",
                "board_info": {
                    "pcb_path": pcb_path,
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to load board",
                "error": str(e)
            }
        
    def save_board(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Save the current board.
        
        Args:
            output_path: Optional path to save to
            
        Returns:
            Dict with save result
        """
        if not self.board:
            return {
                "success": False,
                "message": "No board loaded"
            }
        
        try:
            save_path = output_path or self.board.GetFileName()
            self.board.Save(save_path)
            
            return {
                "success": True,
                "message": f"Board saved to: {save_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to save board",
                "error": str(e)
            }
    
    def get_board(self) -> Optional['pcbnew.BOARD']:
        """Get current board object."""
        return self.board
    
    def is_board_loaded(self) -> bool:
        """Check if board is loaded."""
        return self.board is not None
    
    def get_net_list(self) -> Dict[str, Any]:
        """Return a dictionary of net names and their corresponding net codes."""

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }

        try:
            net_info = {}
            pad_info = []

        
            # Get all nets from the board
            netinfo = self.board.GetNetInfo()
            
            for net_code in range(netinfo.GetNetCount()):
                net = netinfo.GetNetItem(net_code)
                if net:
                    net_name = net.GetNetname()
                    net_info[net_name] = net_code

            # Get all pads from all footprints
            for footprint in self.board.GetFootprints():
                footprint_ref = footprint.GetReference()
                footprint_value = footprint.GetValue()
                footprint_pos = footprint.GetPosition()
                
                for pad in footprint.Pads():
                    pad_data = {
                        "footprint_reference": footprint_ref,
                        "footprint_value": footprint_value,
                        "footprint_position": {
                            "x": footprint_pos.x / 1000000.0,  # Convert from nanometers to mm
                            "y": footprint_pos.y / 1000000.0
                        },
                        "pad_number": pad.GetNumber(),
                        "pad_name": pad.GetPadName(),
                        "net_name": pad.GetNetname(),
                        "net_code": pad.GetNetCode(),
                        "position": {
                            "x": pad.GetPosition().x / 1000000.0, 
                            "y": pad.GetPosition().y / 1000000.0
                        },
                        "size": {
                            "x": pad.GetSize().x / 1000000.0, 
                            "y": pad.GetSize().y / 1000000.0
                        },
                        "shape": pad.GetShape(),
                        #"layer_set": pad.GetLayerSet().Seq(),
                        "drill_size": {
                            "x": pad.GetDrillSize().x / 1000000.0,  
                            "y": pad.GetDrillSize().y / 1000000.0
                        } if pad.GetDrillSize().x > 0 else None,
                        "pad_type": pad.GetAttribute()  # PAD_ATTRIB (e.g., THT, SMD, NPTH, etc.)
                    }
                    
                    pad_info.append(pad_data)

            return {
                "success": True,
                "net_info": net_info,
                "pad_info" : pad_info
            }

        except Exception as e:
            return {
                "success": False,
                "message": "Failed to extract net list and pad info",
                "error": str(e)
            }
