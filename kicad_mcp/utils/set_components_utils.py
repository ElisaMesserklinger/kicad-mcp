"""
Component-related utility functions for KiCad operations.
"""
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


@dataclass
class ComponentInfo:
    """Data class for component information."""
    reference: str
    value: str
    footprint: str
    position: Dict[str, Any]
    rotation: float
    layer: str

class ComponentManager:
    """Utility class for KiCad component operations."""

    def __init__(self, board: Optional['pcbnew.BOARD'] = None):
        self.board = board
    
    def set_board(self, board: 'pcbnew.BOARD') -> None:
        """Set the current board."""
        self.board = board

    def get_board(self):
        return self.board

    def convert_position_to_nanometers(self, position: Dict[str, Any]) -> Tuple[int, int]:
        """Convert position from mm/inch to nanometers.
        
        Args:
            position: Dict with x, y, unit
            
        Returns:
            Tuple of (x_nm, y_nm)
        """
        unit = position.get("unit", "mm")
        scale = 1000000 if unit == "mm" else 25400000  # mm or inch to nm
        x_nm = int(position["x"] * scale)
        y_nm = int(position["y"] * scale)
        return x_nm, y_nm
    
    def convert_position_from_nanometers(self, x_nm: int, y_nm: int, unit: str = "mm") -> Dict[str, Any]:
        """Convert position from nanometers to mm/inch.
        
        Args:
            x_nm: X coordinate in nanometers
            y_nm: Y coordinate in nanometers  
            unit: Target unit (mm or inch)
            
        Returns:
            Dict with x, y, unit
        """
        scale = 1000000 if unit == "mm" else 25400000
        return {
            "x": x_nm / scale,
            "y": y_nm / scale,
            "unit": unit
        }
    
    def create_footprint(self, component_id: str, position: Dict[str, Any], library: str,
                        reference: Optional[str] = None, value: Optional[str] = None,
                        rotation: float = 0,  layer: str = "F.Cu") -> 'pcbnew.FOOTPRINT':
        """Create a new footprint with the specified parameters.
        
        Args:
            component_id: Component/footprint identifier
            position: Position dict with x, y, unit
            reference: Optional reference designator
            value: Optional component value
            rotation: Rotation in degrees
            layer: Layer name
            
        Returns:
            Created footprint object
            
        Raises:
            ValueError: If board is not set or invalid parameters
        """
        if not self.board:
            raise ValueError("Board not set")
                
        # Create footprint
        footprint = pcbnew.FOOTPRINT(self.board)

         # Parse component ID and set footprint ID
        if library:
            library_name = library
            footprint_name = component_id
        
        # Set footprint ID
        footprint.SetFPID(pcbnew.LIB_ID(component_id, library_name))

        # Set position
        x_nm, y_nm = self.convert_position_to_nanometers(position)
        footprint.SetPosition(pcbnew.VECTOR2I(x_nm, y_nm))
        
        # Set reference
        if reference:
            footprint.SetReference(reference)
        else:
            footprint.SetReference(self.generate_next_reference())
        
        # Set value
        if value:
            footprint.SetValue(value)
        else:
            footprint.SetValue(footprint_name)
        
        # Set rotation
        footprint.SetOrientation(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
        
        # Set layer
        layer_id = self.board.GetLayerID(layer)
        if layer_id >= 0:
            footprint.SetLayer(layer_id)
        else:
            logger.warning(f"Layer {layer} not found, using F.Cu")
            footprint.SetLayer(self.board.GetLayerID("F.Cu"))
        
        return footprint

    def generate_next_reference(self, prefix: str = "U") -> str:
        """Generate next available reference designator.
        
        Args:
            prefix: Reference prefix (e.g., 'U', 'R', 'C')
            
        Returns:
            Next available reference (e.g., 'U1', 'U2', etc.)
        """
        if not self.board:
            return f"{prefix}1"
        
        existing_refs = [fp.GetReference() for fp in self.board.GetFootprints()]
        counter = 1
        
        #if reference already exists skip it 
        while f"{prefix}{counter}" in existing_refs:
            counter += 1
        
        return f"{prefix}{counter}"

    def place_footprint(self, footprint: 'pcbnew.FOOTPRINT') -> ComponentInfo:
        """Place footprint on the board and return component info.
        
        Args:
            footprint: Footprint to place
            
        Returns:
            ComponentInfo with placed component details
        """
        if not self.board:
            raise ValueError("Board not set")
        
        # Add to board
        self.board.Add(footprint)
        
        # Get final position
        pos = footprint.GetPosition()
        position = self.convert_position_from_nanometers(pos.x, pos.y, "mm")
        
        return ComponentInfo(
            reference=footprint.GetReference(),
            value=footprint.GetValue(),
            footprint=str(footprint.GetFPID().GetLibItemName()),
            position=position,
            rotation=float(footprint.GetOrientation().AsDegrees()),
            layer=self.board.GetLayerName(footprint.GetLayer())
        )
    
    def find_component(self, reference: str) -> Optional['pcbnew.FOOTPRINT']:
        """Find component by reference.
        
        Args:
            reference: Component reference (e.g., 'R1')
            
        Returns:
            Footprint object or None if not found
        """
        if not self.board:
            return None
        
        return self.board.FindFootprintByReference(reference)
    

    def move_component(self, reference: str, position: Dict[str, Any], 
                      rotation: Optional[float] = None) -> ComponentInfo:
        """Move existing component to new position.
        
        Args:
            reference: Component reference
            position: New position dict
            rotation: Optional new rotation
            
        Returns:
            ComponentInfo with updated component details
            
        Raises:
            ValueError: If component not found
        """
        footprint = self.find_component(reference)
        if not footprint:
            raise ValueError(f"Component {reference} not found")
        
        # Set new position
        x_nm, y_nm = self.convert_position_to_nanometers(position)
        footprint.SetPosition(pcbnew.VECTOR2I(x_nm, y_nm))
        
        # Set rotation if provided
        if rotation is not None:
            footprint.SetOrientation(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
        
        # Return updated info
        pos = footprint.GetPosition()
        final_position = self.convert_position_from_nanometers(pos.x, pos.y, position.get("unit", "mm"))
        
        return ComponentInfo(
            reference=reference,
            value=footprint.GetValue(),
            footprint=str(footprint.GetFPID().GetLibItemName()),
            position=final_position,
            rotation=float(footprint.GetOrientation().AsDegrees()),
            layer=self.board.GetLayerName(footprint.GetLayer())
        )
    