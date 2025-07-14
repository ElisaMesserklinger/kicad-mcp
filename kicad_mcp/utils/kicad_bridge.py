import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import threading
import logging


logging.basicConfig(filename="C:/Git/kicad-mcp/mcp_sunprocess.log", level=logging.DEBUG)

class KiCadBridge:
    """Bridge between MCP server and KiCad Python environment."""
    
    def __init__(self):
        self.kicad_python = self._find_kicad_python()
        self.script_path = self._create_subprocess_script()
    
    def _find_kicad_python(self) -> str:
        """Find KiCad Python executable."""
        paths = [
            "C:/Program Files/KiCad/9.0/bin/python.exe",
            "C:/Users/messeel/AppData/Local/Programs/KiCad/9.0/bin/python.exe"
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError("KiCad Python not found")
    
    def _create_subprocess_script(self) -> str:
        """Create the subprocess script that uses your existing files."""
        
        # Get current directory
        current_dir = Path(__file__).parent #import for later imports
        
        # Create subprocess script
        script_content = '''

import sys
import json
from pathlib import Path
import logging
import threading
import os

sys.stdout.flush()

# Project Path Setup
project_root = Path("{project_root}")
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent))  # Add parent directory too

logging.basicConfig(filename="C:\Git\kicad-mcp\mcp_sunprocess.log", level=logging.DEBUG)


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
    print(json.dumps({{"success": False, "error": f"Utils import failed: {{str(e)}}"}}, indent=2))
    UTILS_AVAILABLE = False

# Global instances
if UTILS_AVAILABLE:
    board_manager = BoardManager()
    component_manager = ComponentManager()

# DIRECT EXECUTION
if __name__ == "__main__":
    try:
        if not UTILS_AVAILABLE:
            print(json.dumps({{"success": False, "error": "Utils not available"}}))
            sys.exit(1)
            
        method_name = sys.argv[1]
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {{}}
        
        if method_name == "load_board":
            result = board_manager.load_board(params["project_path"])
            if result["success"]:
                logging.debug("Successfully loaded board in subprocess")
                component_manager.set_board(board_manager.get_board())
                logging.debug("TEST")
                logging.debug(json.dumps(result))

            print(json.dumps(result))
           
        
        elif method_name == "place_component_full":
            project_path = params["project_path"]
            
            # Step 1: Load board
            logging.debug("DEBUG: Loading board...")
            load_result = board_manager.load_board(project_path)
            if not load_result["success"]:
                print(json.dumps(load_result))
                sys.exit(1)
            
            # Set board in component manager
            component_manager.set_board(board_manager.get_board())
            logging.debug("DEBUG: Board loaded successfully")
            
            # Step 2: Place component
            logging.debug("DEBUG: Placing component...")
            footprint = component_manager.create_footprint(
                component_id=params["component_id"],
                position=params["position"],
                library=params["library"],
                reference=params.get("reference"),
                value=params.get("value"),
                rotation=params.get("rotation", 0),
                layer=params.get("layer", "F.Cu"),
            )
            component_info = component_manager.place_footprint(footprint)
            logging.debug("DEBUG: Component placed successfully")
            
            # Step 3: Save board
            logging.debug("DEBUG: Saving board...")
            save_result = board_manager.save_board(params.get("output_path"))
            if not save_result["success"]:
                print(json.dumps(save_result))
                sys.exit(1)
            
            logging.debug("DEBUG: Board saved successfully")
            
            # Return combined result
            result = {{
                "success": True,
                "message": f"Component placed and saved: {{params['component_id']}}",
                "component": {{
                    "reference": component_info.reference,
                    "value": component_info.value,
                    "footprint": component_info.footprint,
                    "position": component_info.position,
                    "rotation": component_info.rotation,
                    "layer": component_info.layer,
                }},
                "board_info": load_result.get("board_info", {{}}),
                "save_info": save_result
            }}
            logging.debug(json.dumps(result))
            print(json.dumps(result))

        elif method_name == "move_component":
            project_path = params["project_path"]
            reference = params.get("reference")
            position = params["position"]
            rotation = params.get("rotation")
            
            # Step 1: Load board
            logging.debug("DEBUG: Loading board for move operation...")
            load_result = board_manager.load_board(project_path)
            if not load_result["success"]:
                print(json.dumps(load_result))
                sys.exit(1)
            
            # Set board in component manager
            component_manager.set_board(board_manager.get_board())
            logging.debug("DEBUG: Board loaded successfully")
            
            # Step 2: Move component
            logging.debug("DEBUG: Moving component ...")
            try:
                move_result = component_manager.move_component(
                    reference=reference,
                    position=position,
                    rotation=rotation
                )
                
                logging.debug(move_result.reference)    
                logging.debug("DEBUG: Component moved successfully")
                
                # Step 3: Save board
                logging.debug("DEBUG: Saving board...")
                save_result = board_manager.save_board()
                if not save_result["success"]:
                    print(json.dumps(save_result))
                    sys.exit(1)
                
                logging.debug("DEBUG: Board saved successfully")
                
                # Return combined result
                result = {{
                    "success": True,
                    "message": "Component moved successfully",
                    "component": {{
                        "reference": reference,
                        "position": position,
                        "rotation": rotation
                    }},
                    "board_info": load_result.get("board_info", {{}}),
                    "save_info": save_result
                }}
                logging.debug(json.dumps(result))
                print(json.dumps(result))
                
            except Exception as e:
                error_result = {{
                    "success": False,
                    "error": f"Failed to move component: {{str(e)}}"
                }}
                logging.error(json.dumps(error_result))
                print(json.dumps(error_result))
        
        else:
            print(json.dumps({{"success": False, "error": f"Unknown method: {{method_name}}"}}))
            
    except Exception as e:
        print(json.dumps({{"success": False, "error": str(e)}}))
'''

        # FORMAT the script with the actual project root path
        # Convert to forward slashes to avoid escape sequence issues
        project_root_path = str(current_dir).replace('\\', '/')
        formatted_script = script_content.format(project_root=project_root_path)
    


        # Save script
        script_path = current_dir / "kicad_script_subprocess.py"
        script_path.write_text(formatted_script)
        return str(script_path)
    

    def _run_subprocess(self, method_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run subprocess with method and parameters."""
        logging.debug("Before Calling Subprocess")
        logging.debug(f"Method: {method_name}")
        logging.debug(f"Params: {params}")
        
        try:             
            result = subprocess.run([
                self.kicad_python, 
                self.script_path, 
                method_name, 
                json.dumps(params)],

                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL, 
                timeout=60
            )

            logging.debug(f"Subprocess return code: {result.returncode}")
            logging.debug(f"Subprocess stdout: {result.stdout}")
            logging.debug(f"Subprocess stderr: {result.stderr}")
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Subprocess failed with return code {result.returncode}",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            
            # Parse the JSON output
            try:
                logging.debug("Try to parse JSON loads")
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Failed to parse subprocess output: {str(e)}",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            
        except subprocess.TimeoutExpired:
            logging.error("Subprocess timeout")
            return {"success": False, "error": "Command timeout after 60 seconds"}
        except Exception as e:
            logging.error(f"Subprocess error: {str(e)}")
            return {"success": False, "error": f"Subprocess execution failed: {str(e)}"}
        
    

    #functions that are called by tools
    def load_board(self, project_path: str) -> Dict[str, Any]:
        logging.debug("Called Load Board with Tool")
        logging.debug("Project Path")
        return self._run_subprocess("load_board", {"project_path": project_path})
    
    def place_component(self, project_path: str, component_id: str, position: Dict[str, Any],  library: str, 
                       reference: Optional[str] = None, value: Optional[str] = None,
                       rotation: float = 0, layer: str = "F.Cu", 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Place a single component (load -> place -> save)."""
        return self._run_subprocess("place_component_full", {
            "project_path": project_path,
            "component_id": component_id,
            "position": position,
            "library": library,
            "reference": reference,
            "value": value,
            "rotation": rotation,
            "layer": layer,
            "output_path": output_path
        })
    

    def move_component(self, project_path: str, reference: str, position: Dict[str, Any], 
                      rotation: Optional[float] = None) -> Dict[str, Any]:
        """Move a component to a new position (load -> move -> save)."""
        return self._run_subprocess("move_component", {
            "project_path": project_path,
            "reference": reference,
            "position": position,
            "rotation": rotation
        })
    

    





