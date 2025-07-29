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
            unrouted_pad_count = 0

        
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

                    if pad.GetNetname() is None:
                        unrouted_pad_count += 1

            return {
                "success": True,
                "net_info": net_info,
                "pad_info" : pad_info,
                "unrouted pads": unrouted_pad_count
            }

        except Exception as e:
            return {
                "success": False,
                "message": "Failed to extract net list and pad info",
                "error": str(e)
            }

    def trace_routes(self, start: dict, end: dict, width: float, net: str, layer: Optional[str] = "F.Cu",) -> Dict[str, Any]:
        """Route a trace between two points or pads"""

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }
        
        try:
            #check if net exists
            target_net = self._find_net_by_name(net)
            if not target_net:
                return {
                    "success": False,
                    "message": f"Net '{net}' not found"
                }
            
            #Get layer ID
            layer_id = self.board.GetLayerID(layer)
            if layer_id < 0:
                return {
                    "success": False,
                    "message": "Invalid layer",
                    "errorDetails": f"Layer '{layer}' does not exist"
                }
            
            # Parse positions
            start_pos = self._parse_position(start)
            end_pos = self._parse_position(end)
            
            if not start_pos or not end_pos:
                return {
                    "success": False,
                    "message": "Invalid start or end position"
                }
            
            
            # Convert width from mm to nanometers
            track_width = int(width * 1000000)
            
            # Create single track
            track = pcbnew.PCB_TRACK(self.board)
            track.SetStart(start_pos)
            track.SetEnd(end_pos)
            track.SetWidth(track_width)
            track.SetLayer(layer_id)
            track.SetNet(target_net)
            
            # Add track to board
            self.board.Add(track)
            
            # Calculate track length
            dx = end_pos.x - start_pos.x
            dy = end_pos.y - start_pos.y
            length_mm = ((dx*dx + dy*dy) ** 0.5) / 1000000.0
            
            return {
                "success": True,
                "message": "Track created successfully",
                "track_info": {
                    "start": {"x": start_pos.x / 1000000.0, "y": start_pos.y / 1000000.0},
                    "end": {"x": end_pos.x / 1000000.0, "y": end_pos.y / 1000000.0},
                    "width_mm": width,
                    "length_mm": round(length_mm, 3),
                    "net": net,
                    "layer": layer
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to create track",
                "error": str(e)
            }
                
        
    def _find_net_by_name(self, net_name: str) -> Optional[pcbnew.NETINFO_ITEM]:
        """Find a net by name"""
        netinfo = self.board.GetNetInfo()
        for net_code in range(netinfo.GetNetCount()):
            net_obj = netinfo.GetNetItem(net_code)
            if net_obj and net_obj.GetNetname() == net_name:
                return net_obj
        return None
    

    def _parse_position(self, pos_dict: dict) -> Optional[pcbnew.VECTOR2I]:
        """Parse position from dictionary to KiCad coordinates"""
        try:
            if "pad" in pos_dict:
                # Find pad by reference (e.g., "R1.1")
                #TODO is this even necessary
                pad = self._find_pad(pos_dict["pad"])
                if pad:
                    return pad.GetPosition()
            elif "x" in pos_dict and "y" in pos_dict:
                # Convert mm coordinates to nanometers
                x_nm = int(pos_dict["x"] * 1000000)
                y_nm = int(pos_dict["y"] * 1000000)
                return pcbnew.VECTOR2I(x_nm, y_nm)
            
            return None
        except Exception:
            return None
        
    #TODO: don't know if that is needed too 
    def _find_pad(self, pad_ref: str) -> Optional[pcbnew.PAD]:
        """Find a pad by reference (format: 'R1.1' for component R1, pad 1)"""
        try:
            parts = pad_ref.split('.')
            if len(parts) != 2:
                return None
            
            component_ref, pad_number = parts
            
            for footprint in self.board.GetFootprints():
                if footprint.GetReference() == component_ref:
                    for pad in footprint.Pads():
                        if pad.GetNumber() == pad_number:
                            return pad
            
            return None
        except Exception:
            return None