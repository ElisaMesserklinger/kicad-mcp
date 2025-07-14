'''
# Test-Script erstellen:
# test_kicad_subprocess.py
from kicad_mcp.utils.kicad_bridge import KiCadBridge

kicad = KiCadBridge()

# Einfachster Test
print("Testing KiCad subprocess...")
result = kicad.place_component("C:/Users/messeel/KiCadProjects/KiCad/hw_PB244_flameoff_testload-main/hw_PB244_flameoff_testload-main/hw_PB244_flameoff_testload.kicad_pro", {
    "x": 100.0,      # X coordinate in mm
    "y": 50.0,       # Y coordinate in mm
    "units": "mm"    # Units (optional, default is mm)
})
print(f"Result: {result}")


#C:/Users/messeel/KiCadProjects/KiCad\\hw_PB244_flameoff_testload-main\\hw_PB244_flameoff_testload-main\\hw_PB244_flameoff_testload.kicad_pro
'''
import anthropic
from typing import List, Dict, Any
import os

from kicad_mcp.utils.kicad_bridge import KiCadBridge

def test_place_component_workflow():
    """Test the complete workflow: load board -> place component -> save board."""
    
    # Initialize KiCad bridge
    kicad = KiCadBridge()
    
    # Step 1: Load board first
    print("Step 1: Loading board...")
    project_path = "C:/Users/messeel/KiCadProjects/KiCad/hw_PB244_flameoff_testload-main/hw_PB244_flameoff_testload-main/hw_PB244_flameoff_testload.kicad_pro"
    
    load_result = kicad.load_board(project_path)
    print(f"Load result: {load_result}")
    
    if not load_result.get("success"):
        print("❌ Board loading failed, cannot continue")
        return False
    
    print("✅ Board loaded successfully!")
    
    # Step 2: Place a component
    print("\nStep 2: Placing component...")
    
    # Simple component placement
    place_result = kicad.place_component(
        project_path=project_path,
        component_id="R_0805_2012Metric",
        position={"x": 25.0, "y": 15.0},
        reference="R1",
        value="1k",
        library="Resistor_SMD" 
    )

    place_capacitor = kicad.place_component(
    project_path=project_path,
    component_id="C_0805_2012Metric",
    position={"x": 30.0, "y": 15.0},
    reference="C1",
    value="100nF",
    library="Capacitor_SMD"
)
    
    print(f"Place result: {place_result}")
    print(f"Place result: {place_capacitor}")


    
    if not place_result.get("success"):
        print("❌ Component placement failed")
        return False
    
    if not place_capacitor.get("success"):
        print("❌ Component placement failed")
        return False
    
    print("✅ Component placed successfully!")
    
    # Step 3: Save the board
    print("\nStep 3: Saving board...")
    
    save_result = kicad.save_board()
    print(f"Save result: {save_result}")
    
    if not save_result.get("success"):
        print("❌ Board saving failed")
        return False
    
    print("✅ Board saved successfully!")
    
    return True


def test_simplified_place_component():
    """Test the simplified place_component method."""
    
    kicad = KiCadBridge()
    
    project_path = "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro"
    
    print("Testing simplified place_component (load -> place -> save)...")
    
    # Single method call does everything
    result = kicad.place_component(
        project_path=project_path,
        component_id="R_0805_2012Metric",
        position={"x": 100.0, "y": 200.0},
        reference="R_SIMPLE",
        value="1k",
        rotation=0,
        layer="F.Cu",
        library="Resistor_SMD" 

    )

    
    
    print(f"Result: {result}")

    
    if result.get("success"):
        print("✅ Simplified approach works!")
        print(f"Component placed: {result.get('component', {})}")
        print(f"Board info: {result.get('board_info', {})}")
        print(f"Save info: {result.get('save_info', {})}")
    else:
        print("❌ Simplified approach failed")
        print(f"Error: {result.get('error')}")
    
    return result



def test_load_board():
    kicad = KiCadBridge()
    
    project_path = "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro"

    load_result = kicad.load_board(project_path)
    print(f"Load result: {load_result}")
    
    if not load_result.get("success"):
        print("❌ Board loading failed, cannot continue")
        return False
    

def test_move_component():
    kicad = KiCadBridge()
    project_path = "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro"
    result = kicad.move_component(
        project_path=project_path,
        position={"x": 232.0, "y": 150.0},
        reference="C2",
        rotation=0,
    )

    print(f"Load result: {result}")
    
    if not result.get("success"):
        print("❌ Board loading failed, cannot continue")
        return False

def analyze_pdfs(pdf_url: str, prompt: str) -> List[Dict[str, Any]]:
    """
    Analyze a list of PDFs using Claude (Anthropic) via URL-based document references.

    Args:
        pdf_urls: publicly accessible PDF URL.
        prompt: Custom prompt/question to ask Claude about each PDF.

    Returns:
        List of analysis results per PDF (as Claude's structured response).
    """
    client = anthropic.Anthropic()
    results = []

    try:
            message = client.messages.create(
                model="claude-sonnet-4-20250514",  #change to other models
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "url",
                                    "url": pdf_url
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
            )
            results.append({
                "url": pdf_url,
                "response": message.content
            })
    except Exception as e:
            results.append({
                "url": pdf_url,
                "error": str(e)
            })

    return results






#test_place_component_workflow()


#test_simplified_place_component()

#test_move_component()

#"path": "C:/Users/messeel/KiCadProjects/KiCad\\test1\\test1.kicad_pro",
#C:/Users/messeel/KiCadProjects/KiCad\\test\\test.kicad_pro

#test_load_board()

#"C:/Program Files/KiCad/9.0/bin/python.exe" kicad_script_subprocess.py load_board "{\"project_path\": "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro\"}"

#"C:/Users/messeel/AppData/Local/Programs/KiCad/9.0/bin/python.exe" "C:\Git\kicad-mcp\kicad_mcp\utils\kicad_script_subprocess.py load_board" "{"project_path": "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro"}

pdf_url = "https://www.ti.com/lit/ds/symlink/lm7321.pdf"  # Replace with actual URL
prompt = "What are the key specifications and features of this component?"
    
result = analyze_pdfs(pdf_url, prompt)
print(f"Analysis result: {result}")