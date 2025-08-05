"""
Board-related utility functions for KiCad operations.
"""
import os
import sys
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

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
        if not os.path.exists(project_path):
            return {
                "success": False,
                "message": f"PCB file not found: {project_path}"
            }
        
        try:

            try:
                self.board = pcbnew.LoadBoard(project_path)
            except Exception as e:
                return {"success": False, "error": f"Failed to load board: {str(e)}"}

            self.project_path = project_path
            
            return {
                "success": True,
                "message": f"Board loaded successfully: {project_path}",
                "board_info": {
                    "pcb_path": project_path,
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

        
            # Get all nets from the board
            netinfo = self.board.GetNetInfo()
            
            for net_code in range(netinfo.GetNetCount()):
                net = netinfo.GetNetItem(net_code)
                if net:
                    net_name = net.GetNetname()
                    net_info[net_name] = net_code
                   
            return {
                "success": True,
                "net_info": net_info,
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
                pad = self._find_pad(pos_dict["pad"])
                if pad:
                    return pad.GetPosition()
            elif "x" in pos_dict and "y" in pos_dict:
                # Convert mm  to nanometers
                x_nm = int(pos_dict["x"] * 1000000)
                y_nm = int(pos_dict["y"] * 1000000)
                return pcbnew.VECTOR2I(x_nm, y_nm)
            
            return None
        except Exception:
            return None
        
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

    def basic_board_info(self):
        """
        get basic board info
        """

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }
        
        try:
            bbox = self.board.GetBoundingBox()
            return {
                "success": True,
                "data": {
                    "filename": self.board.GetFileName(),
                    "bounding_box": {
                        "x": bbox.GetX() / 1e6,
                        "y": bbox.GetY() / 1e6,
                        "width": bbox.GetWidth() / 1e6,
                        "height": bbox.GetHeight() / 1e6
                    },
                    "net_count": self.board.GetNetCount()
                }
            }
        except Exception as e:
            logging.warning(f"Could not extract board info: {str(e)}")
            return {"success": False, "message": str(e)}

    def get_design_rules(self):
        """
        get design info of pcb board
        """

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }
        
        try:
            design_settings = self.board.GetDesignSettings()
            return {
                "success": True,
                "data": {
                    "smallest_clearance": design_settings.GetSmallestClearanceValue() / 1e6,
                    "custom_via_size": design_settings.GetCustomViaSize() / 1e6,
                    "custom_via_drill": design_settings.GetCustomViaDrill() / 1e6
                }
            }
        except Exception as e:
            logging.warning(f"Could not extract design rules: {str(e)}")
            return {"success": False, "message": str(e)}


    def get_layers(self):

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }

        layers = []

        try:
            layers = {}
            for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
                if self.board.IsLayerEnabled(layer_id):
                    layers[layer_id] = {
                        "name": self.board.GetLayerName(layer_id),
                        "type": self.board.GetLayerType(layer_id)
                    }
            return {"success": True, "data": layers}
        
        except Exception as e:
            logging.warning(f"Could not extract layer info: {str(e)}")
            return {"success": False, "message": str(e)}


    def get_footprints_pads(self):
        """
        Get Pads of pcb Layout
        """

        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }

        try:
            net_to_pads = {}
            for pad in self.board.GetPads():
                net = pad.GetNet()
                if net:
                    netname = net.GetNetname()
                    net_to_pads.setdefault(netname, []).append(pad)

            components = []

            for footprint in self.board.GetFootprints():
                try:
                    pos = footprint.GetPosition()
                    component = {
                        "reference": footprint.GetReference(),
                        "value": footprint.GetValue(),
                        "footprint_id": str(footprint.GetFPID()),
                        "position": {"x": pos.x / 1e6, "y": pos.y / 1e6},
                        "layer": footprint.GetLayer(),
                        "layer_name": self.board.GetLayerName(footprint.GetLayer()),
                        "pads": []
                    }

                    for pad in footprint.Pads():
                        pad_pos = pad.GetPosition()
                        pad_size = pad.GetSize()
                        pad_net = pad.GetNet()
                        netname = pad_net.GetNetname() if pad_net else None

                        connected = []
                        if netname and netname in net_to_pads:
                            for other_pad in net_to_pads[netname]:
                                if other_pad != pad:
                                    connected.append({
                                        "pad_number": other_pad.GetNumber(),
                                        "net_name": netname
                                    })

                        pad_info = {
                            "number": pad.GetNumber(),
                            "position": {"x": pad_pos.x / 1e6, "y": pad_pos.y / 1e6},
                            "size": {"x": pad_size.x / 1e6, "y": pad_size.y / 1e6},
                            "shape": pad.GetShape(),
                            "drill_size": pad.GetDrillSize().x / 1e6,
                            "net_name": pad.GetNetname(),
                            "net_code": pad.GetNetCode(),
                            "connected_items": connected
                        }

                        component["pads"].append(pad_info)
                    components.append(component)

                except Exception as e:
                    logging.warning(f"Component error: {str(e)}")
                    components.append({"error": str(e)})

            return {"success": True, "data": {"components": components}}

        except Exception as e:
            logging.warning(f"General components error: {str(e)}")
            return {"success": False, "message": str(e)}

    def get_tracks_vias(self):
        """
        Get tracks and vias of pcb Layout
        """
        if not self.board:
            return {
                "success": False,
                "message": "Board not loaded"
            }


        try:
            tracks = []
            vias = []

            for item in self.board.GetTracks():
                if isinstance(item, pcbnew.PCB_VIA):
                    pos = item.GetPosition()
                    vias.append({
                        "position": {"x": pos.x / 1e6, "y": pos.y / 1e6},
                        "drill": item.GetDrillValue() / 1e6,
                        "net_name": item.GetNetname(),
                    })
                else:
                    start = item.GetStart()
                    end = item.GetEnd()
                    tracks.append({
                        "start": {"x": start.x / 1e6, "y": start.y / 1e6},
                        "end": {"x": end.x / 1e6, "y": end.y / 1e6},
                        "length": item.GetLength() / 1e6,
                        "net_name": item.GetNetname(),
                    })

            return {
                "success": True,
                "data": {
                    "tracks": tracks,
                    "vias": vias
                }
            }
        except Exception as e:
            logging.warning(f"Could not extract tracks/vias: {str(e)}")
            return {"success": False, "message": str(e)}


    def get_zones(self):
        """
        Get Zones of pcb layout
        """
        if not self.board:
            return {"success": False, "message": "Board not loaded"}

        try:
            zones = []
            for zone in self.board.Zones():
                try:
                    zone_info = {
                        "net_name": zone.GetNetname(),
                        "net_code": zone.GetNetCode(),
                        "layer": zone.GetLayer(),
                        "layer_name": self.board.GetLayerName(zone.GetLayer()),
                        "area": zone.GetArea() / 1e6,
                        "min_thickness": zone.GetMinThickness() / 1e6,
                        "thermal_relief_gap": zone.GetThermalReliefGap() / 1e6,
                        "thermal_relief_copper_bridge": zone.GetThermalReliefSpokeWidth() / 1e6,
                        "zone_name": zone.GetZoneName() if hasattr(zone, 'GetZoneName') else ""
                    }
                    zones.append(zone_info)
                except Exception as zerr:
                    logging.warning(f"Zone error: {str(zerr)}")
                    zones.append({"error": str(zerr)})

            return {"success": True, "data": zones}
        except Exception as e:
            logging.warning(f"General zone error: {str(e)}")
            return {"success": False, "message": str(e)}