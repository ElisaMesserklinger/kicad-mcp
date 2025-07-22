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
from kicad_mcp.utils.create_foodprint_symbol_utils import *

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




test = f"""
(module "SOT-23-5_LM7321" (layer F.Cu)
  (descr "SOT-23-5 package for LM7321 single op-amp")
  (tags "SOT-23-5 LM7321 opamp")
  (attr smd)

  (property "Reference" "U**"
    (at 0 -2.5 0)
    (layer "F.SilkS")
    (uuid "12345678-1234-1234-1234-123456789001")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.254)
      )
    )
  )
  (property "Value" "LM7321"
    (at 0 2.5 0)
    (layer "F.Fab")
    (uuid "12345678-1234-1234-1234-123456789002")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.254)
      )
    )
  )
  (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm7321.pdf"
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "12345678-1234-1234-1234-123456789003")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.15)
      )
    )
  )
  (property "Description" "Single Rail-to-Rail Op-Amp, SOT-23-5"
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "12345678-1234-1234-1234-123456789004")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.15)
      )
    )
  )

  ; Courtyard
  (fp_line (start -1.7 -1.75) (end 1.7 -1.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start 1.7 -1.75) (end 1.7 1.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start 1.7 1.75) (end -1.7 1.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start -1.7 1.75) (end -1.7 -1.75) (layer F.CrtYd) (width 0.05))

  ; Fabrication outline
  (fp_line (start -0.725 -1.45) (end 0.725 -1.45) (layer F.Fab) (width 0.1))
  (fp_line (start 0.725 -1.45) (end 0.725 1.45) (layer F.Fab) (width 0.1))
  (fp_line (start 0.725 1.45) (end -0.725 1.45) (layer F.Fab) (width 0.1))
  (fp_line (start -0.725 1.45) (end -0.725 -1.45) (layer F.Fab) (width 0.1))

  ; Silkscreen
  (fp_line (start -0.825 -1.55) (end 0.825 -1.55) (layer F.SilkS) (width 0.2))
  (fp_line (start 0.825 -1.55) (end 0.825 1.55) (layer F.SilkS) (width 0.2))
  (fp_line (start 0.825 1.55) (end -0.825 1.55) (layer F.SilkS) (width 0.2))
  (fp_line (start -0.825 1.55) (end -0.825 -1.55) (layer F.SilkS) (width 0.2))

  ; Pin 1 indicator
  (fp_circle (center -1.2 -0.95) (end -1.1 -0.95) (layer F.SilkS) (width 0.2))

  ; Pads
  (pad 1 smd rect (at -0.95 -0.95) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at -0.95 0.95) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
  (pad 3 smd rect (at 0.95 0.95) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
  (pad 4 smd rect (at 0.95 0) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
  (pad 5 smd rect (at 0.95 -0.95) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
)"""


def test_saving_foodprint():
    result = save_kicad_footprint(test, "SOT-23-5_LM7321", "c:/Users/messeel/KiCadProjects/KiCad/9.0/symbols/TI_OpAmps.pretty", "TI_OpAmps")
    return result


def test_saving_table():
    result = save_kicad_footprint_symbol_to_table("C:/Users/messeel/KiCadProjects/KiCad/9.0/footprints/TI_OpAmps.pretty", "TI_OpAmps", "test", "symbol")
    return result


test_symbol = """
(kicad_symbol_lib
(version 20231120)
(generator "kicad_symbol_editor")
(generator_version 9.0)

(symbol "LM7321_SOT-23-5"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)

    (property "Reference" "U"
    (at -2.54 5.08 0)
    (effects
        (font
        (size 1.27 1.27)
        )
    )
    )

    (property "Value" "LM7321"
    (at 0 -5.08 0)
    (effects
        (font
        (size 1.27 1.27)
        )
    )
    )

    (property "Footprint" "Texas_Instruments:SOT-23-5_2.9x1.6mm_P0.95mm"
    (at 0 -7.62 0)
    (effects
        (font
        (size 1.27 1.27)
        )
        (hide yes)
    )
    )

    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm7321.pdf"
    (at 0 -10.16 0)
    (effects
        (font
        (size 1.27 1.27)
        )
        (hide yes)
    )
    )

    (property "Description" "Single Rail-to-Rail Input and Output ±15V High-Output Current Op Amp, SOT-23-5"
    (at 0 -12.7 0)
    (effects
        (font
        (size 1.27 1.27)
        )
        (hide yes)
    )
    )

    (symbol "LM7321_SOT-23-5_0_1"
    (polyline
        (pts
        (xy -5.08 5.08)
        (xy 5.08 0)
        (xy -5.08 -5.08)
        (xy -5.08 5.08)
        )
        (stroke
        (width 0.254)
        (type default)
        )
        (fill
        (type background)
        )
    )
    )

    (symbol "LM7321_SOT-23-5_1_1"
    (pin power_in line
        (at -2.54 7.62 270)
        (length 3.81)
        (name "V+"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
        (number "5"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
    )
    (pin input line
        (at -7.62 -2.54 0)
        (length 2.54)
        (name "-"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
        (number "4"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
    )
    (pin input line
        (at -7.62 2.54 0)
        (length 2.54)
        (name "+"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
        (number "3"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
    )
    (pin power_in line
        (at -2.54 -7.62 90)
        (length 3.81)
        (name "V-"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
        (number "2"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
    )
    (pin output line
        (at 7.62 0 180)
        (length 2.54)
        (name "~"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
        (number "1"
        (effects
            (font
            (size 1.27 1.27)
            )
        )
        )
    )
    )
)
)
"""

print(validate_kicad_symbol(test_symbol))
#test_place_component_workflow()


#test_simplified_place_component()

#test_move_component()

#"path": "C:/Users/messeel/KiCadProjects/KiCad\\test1\\test1.kicad_pro",
#C:/Users/messeel/KiCadProjects/KiCad\\test\\test.kicad_pro

#test_load_board()

#"C:/Program Files/KiCad/9.0/bin/python.exe" kicad_script_subprocess.py load_board "{\"project_path\": "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro\"}"

#"C:/Users/messeel/AppData/Local/Programs/KiCad/9.0/bin/python.exe" "C:\Git\kicad-mcp\kicad_mcp\utils\kicad_script_subprocess.py load_board" "{"project_path": "C:/Users/messeel/KiCadProjects/KiCad/test/test.kicad_pro"}

#pdf_url = "https://www.ti.com/lit/ds/symlink/lm7321.pdf"  # Replace with actual URL
#prompt = "What are the key specifications and features of this component?"
    
#result = analyze_pdfs(pdf_url, prompt)
#print(f"Analysis result: {result}")

#print(test_saving_symbol())