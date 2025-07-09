

import sys
import json
import os
from pathlib import Path

# Project Path Setup
project_root = Path("c:/Git/kicad-mcp/kicad_mcp/utils")
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent))  # Add parent directory too


try:
    import pcbnew
    KICAD_AVAILABLE = True
except ImportError:
    KICAD_AVAILABLE = False


# Import separate utils
try:
    from utils.set_components_utils import ComponentManager
    from utils.board_utils import BoardManager
    UTILS_AVAILABLE = True
except ImportError as e:
    print(json.dumps({"success": False, "error": f"Utils import failed: {{str(e)}}"}, indent=2))
    UTILS_AVAILABLE = False

# Global instances
if UTILS_AVAILABLE:
    board_manager = BoardManager()
    component_manager = ComponentManager()

# DIRECT EXECUTION
if __name__ == "__main__":
    try:
        if not UTILS_AVAILABLE:
            print(json.dumps({"success": False, "error": "Utils not available"}))
            sys.exit(1)
            
        method_name = sys.argv[1]
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        
        if method_name == "load_board":
            result = board_manager.load_board(params["project_path"])
            if result["success"]:
                component_manager.set_board(board_manager.get_board())
            print(json.dumps(result))
        
        elif method_name == "place_component_full":
            project_path = params["project_path"]
            
            # Step 1: Load board
            print("DEBUG: Loading board...", file=sys.stderr)
            load_result = board_manager.load_board(project_path)
            if not load_result["success"]:
                print(json.dumps(load_result))
                sys.exit(1)
            
            # Set board in component manager
            component_manager.set_board(board_manager.get_board())
            print("DEBUG: Board loaded successfully", file=sys.stderr)
            
            # Step 2: Place component
            print("DEBUG: Placing component...", file=sys.stderr)
            footprint = component_manager.create_footprint(
                component_id=params["component_id"],
                position=params["position"],
                reference=params.get("reference"),
                value=params.get("value"),
                rotation=params.get("rotation", 0),
                layer=params.get("layer", "F.Cu"),
                library=params.get("library")
            )
            component_info = component_manager.place_footprint(footprint)
            print("DEBUG: Component placed successfully", file=sys.stderr)
            
            # Step 3: Save board
            print("DEBUG: Saving board...", file=sys.stderr)
            save_result = board_manager.save_board(params.get("output_path"))
            if not save_result["success"]:
                print(json.dumps(save_result))
                sys.exit(1)
            
            print("DEBUG: Board saved successfully", file=sys.stderr)
            
            # Return combined result
            result = {
                "success": True,
                "message": f"Component placed and saved: {{params['component_id']}}",
                "component": {
                    "reference": component_info.reference,
                    "value": component_info.value,
                    "footprint": component_info.footprint,
                    "position": component_info.position,
                    "rotation": component_info.rotation,
                    "layer": component_info.layer,
                },
                "board_info": load_result.get("board_info", {}),
                "save_info": save_result
            }
            print(json.dumps(result))
        
        elif method_name == "save_board":
            result = board_manager.save_board(params.get("output_path"))
            print(json.dumps(result))
        
        else:
            print(json.dumps({"success": False, "error": f"Unknown method: {method_name}"}))
            
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
