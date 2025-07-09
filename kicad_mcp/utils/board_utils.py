"""
Board-related utility functions for KiCad operations.
"""
import os
import sys
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

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
        
        # Convert .kicad_pro to .kicad_pcb
        if project_path.endswith('.kicad_pro'):
            pcb_path = project_path.replace('.kicad_pro', '.kicad_pcb')
        else:
            pcb_path = project_path
        
        if not os.path.exists(pcb_path):
            return {
                "success": False,
                "message": f"PCB file not found: {pcb_path}"
            }
        
        try:
            self.board = pcbnew.LoadBoard(pcb_path)
            self.project_path = project_path
            
            # Get board info
            footprints = list(self.board.GetFootprints())
            
            
            return {
                "success": True,
                "message": f"Board loaded successfully: {pcb_path}",
                "board_info": {
                    "pcb_path": pcb_path,
                    "footprint_count": len(footprints),
                    "layer_count": self.board.GetCopperLayerCount(),
                    "board_name": self.board.GetFileName()
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