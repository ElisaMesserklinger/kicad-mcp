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
(footprint "DIP-28_W7.62mm_P2.54mm_ATmega328P" (version 20240108) (generator "pcbnew") (generator_version "9.0")
  (layer "F.Cu")
  (descr "28-lead through-hole mounted DIP package, row spacing 7.62 mm (300 mils), ATmega328P")
  (tags "THT DIP DIL PDIP 2.54mm 7.62mm 300mil ATmega328P")
  (property "Reference" "U" (at 0 -18.415 0) (layer "F.SilkS")
    (effects (font (size 1.27 1.27) (thickness 0.254)))
  )
  (property "Value" "ATmega328P" (at 0 18.415 0) (layer "F.Fab")
    (effects (font (size 1.27 1.27) (thickness 0.254)))
  )
  (property "Footprint" "DIP-28_W7.62mm_P2.54mm_ATmega328P" (at 0 0 0) (layer "F.Fab") hide
    (effects (font (size 1.27 1.27) (thickness 0.15)))
  )
  (property "Datasheet" "" (at 0 0 0) (layer "F.Fab") hide
    (effects (font (size 1.27 1.27) (thickness 0.15)))
  )
  (attr through_hole)

  (fp_line (start -4.6 -17.4) (end 4.6 -17.4) (stroke (width 0.05) (type solid)) (layer "F.CrtYd"))
  (fp_line (start 4.6 -17.4) (end 4.6 17.4) (stroke (width 0.05) (type solid)) (layer "F.CrtYd"))
  (fp_line (start 4.6 17.4) (end -4.6 17.4) (stroke (width 0.05) (type solid)) (layer "F.CrtYd"))
  (fp_line (start -4.6 17.4) (end -4.6 -17.4) (stroke (width 0.05) (type solid)) (layer "F.CrtYd"))

  (fp_line (start -3.81 -16.89) (end 3.81 -16.89) (stroke (width 0.1) (type solid)) (layer "F.Fab"))
  (fp_line (start 3.81 -16.89) (end 3.81 16.89) (stroke (width 0.1) (type solid)) (layer "F.Fab"))
  (fp_line (start 3.81 16.89) (end -3.81 16.89) (stroke (width 0.1) (type solid)) (layer "F.Fab"))
  (fp_line (start -3.81 16.89) (end -3.81 -15.62) (stroke (width 0.1) (type solid)) (layer "F.Fab"))
  (fp_line (start -3.81 -15.62) (end -2.54 -16.89) (stroke (width 0.1) (type solid)) (layer "F.Fab"))

  (fp_line (start -4.04 -16.89) (end 4.04 -16.89) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))
  (fp_line (start 4.04 -16.89) (end 4.04 16.89) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))
  (fp_line (start 4.04 16.89) (end -4.04 16.89) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))
  (fp_line (start -4.04 16.89) (end -4.04 -16.89) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))

  (fp_arc (start -2.54 -16.255) (mid -2.032 -16.767) (end -1.524 -16.255) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))

  (pad "1" thru_hole rect (at -3.81 -16.51) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "2" thru_hole oval (at -3.81 -13.97) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "3" thru_hole oval (at -3.81 -11.43) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "4" thru_hole oval (at -3.81 -8.89) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "5" thru_hole oval (at -3.81 -6.35) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "6" thru_hole oval (at -3.81 -3.81) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "7" thru_hole oval (at -3.81 -1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "8" thru_hole oval (at -3.81 1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "9" thru_hole oval (at -3.81 3.81) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "10" thru_hole oval (at -3.81 6.35) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "11" thru_hole oval (at -3.81 8.89) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "12" thru_hole oval (at -3.81 11.43) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "13" thru_hole oval (at -3.81 13.97) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "14" thru_hole oval (at -3.81 16.51) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "15" thru_hole oval (at 3.81 16.51) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "16" thru_hole oval (at 3.81 13.97) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "17" thru_hole oval (at 3.81 11.43) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "18" thru_hole oval (at 3.81 8.89) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "19" thru_hole oval (at 3.81 6.35) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "20" thru_hole oval (at 3.81 3.81) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "21" thru_hole oval (at 3.81 1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "22" thru_hole oval (at 3.81 -1.27) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "23" thru_hole oval (at 3.81 -3.81) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "24" thru_hole oval (at 3.81 -6.35) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "25" thru_hole oval (at 3.81 -8.89) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "26" thru_hole oval (at 3.81 -11.43) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "27" thru_hole oval (at 3.81 -13.97) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  (pad "28" thru_hole oval (at 3.81 -16.51) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask"))
  )
)"""


def test_saving_foodprint():
    result = save_kicad_footprint(test, "SOT-23-5_LM7321", "c:/Users/messeel/KiCadProjects/KiCad/9.0/symbols/TI_OpAmps.pretty", "TI_OpAmps")
    return result


def test_saving_table():
    result = save_kicad_footprint_symbol_to_table("C:/Users/messeel/KiCadProjects/KiCad/9.0/footprints/TI_OpAmps.pretty", "TI_OpAmps", "test", "symbol")
    return result

def test_getting_netlist():
    kicad = KiCadBridge()

    netlist = kicad.get_net_pcb("C:/Users/messeel/KiCadProjects/KiCad\hw_PB238_uiws_mainboard\PB238_uiws_mainboard.kicad_pcb")

    print(netlist)
    
def test_trace_routes():
    kicad = KiCadBridge()

    route_status = kicad.track_pcb_routes("C:/Users/messeel/KiCadProjects/KiCad/hw_PB238_uiws_mainboard/PB238_uiws_mainboard.kicad_pcb", {"x": 10.0, "y": 15.0}, {"x": 25.0, "y": 30.0}, "F.Cu", 0.25, "/power/LMR_VCC")
    print(route_status)


#print(validate_kicad_symbol(test_symbol_1))

#print(validate_kicad_footprint(test_symbol))
#test_place_component_workflow()
#print(readFileContent("TexasInstruments", "symbol"))

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




test_trace_routes()