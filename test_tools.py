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


test_symbol = """
(module "ATmega328P_PDIP-28_300mil" (layer F.Cu)
  (descr "28-pin PDIP package, 0.300 inch wide, 2.54mm pitch")
  (tags "PDIP DIP 28 0.300 ATmega328P")
  (attr through_hole)

  (property "Reference" "U**"
    (at 0 -18.415 0)
    (layer "F.SilkS")
    (uuid "12345678-1234-1234-1234-123456789abc")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.254)
      )
    )
  )
  (property "Value" "ATmega328P"
    (at 0 18.415 0)
    (layer "F.Fab")
    (uuid "12345678-1234-1234-1234-123456789abd")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.254)
      )
    )
  )
  (property "Footprint" "Microchip:ATmega328P_PDIP-28_300mil"
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "12345678-1234-1234-1234-123456789abe")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.15)
      )
    )
  )
  (property "Datasheet" "http://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328_P_AVR_MCU_with_picoPower_Technology_Data_Sheet_40001984A.pdf"
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "12345678-1234-1234-1234-123456789abf")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.15)
      )
    )
  )
  (property "Description" "8-bit AVR RISC Microcontroller, 32KB Flash, 2KB SRAM, 1KB EEPROM, PDIP-28"
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "12345678-1234-1234-1234-123456789ac0")
    (effects
      (font
        (size 1.27 1.27)
        (thickness 0.15)
      )
    )
  )

  (fp_line (start -4.33 -17.78) (end 4.33 -17.78) (layer F.CrtYd) (width 0.05))
  (fp_line (start 4.33 -17.78) (end 4.33 17.78) (layer F.CrtYd) (width 0.05))
  (fp_line (start 4.33 17.78) (end -4.33 17.78) (layer F.CrtYd) (width 0.05))
  (fp_line (start -4.33 17.78) (end -4.33 -17.78) (layer F.CrtYd) (width 0.05))

  (fp_line (start -3.81 -17.27) (end 3.81 -17.27) (layer F.Fab) (width 0.1))
  (fp_line (start 3.81 -17.27) (end 3.81 17.27) (layer F.Fab) (width 0.1))
  (fp_line (start 3.81 17.27) (end -3.81 17.27) (layer F.Fab) (width 0.1))
  (fp_line (start -3.81 17.27) (end -3.81 -17.27) (layer F.Fab) (width 0.1))

  (fp_line (start -1.27 -17.27) (end -3.81 -14.99) (layer F.Fab) (width 0.1))

  (fp_line (start -3.93 -17.39) (end 3.93 -17.39) (layer F.SilkS) (width 0.12))
  (fp_line (start 3.93 -17.39) (end 3.93 17.39) (layer F.SilkS) (width 0.12))
  (fp_line (start 3.93 17.39) (end -3.93 17.39) (layer F.SilkS) (width 0.12))
  (fp_line (start -3.93 17.39) (end -3.93 -17.39) (layer F.SilkS) (width 0.12))

  (fp_arc (start -2.54 -16.51) (mid -2.04 -17.01) (end -2.54 -17.51) (layer F.SilkS) (width 0.12))

  (pad 1 thru_hole rect (at -3.81 -16.51) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 2 thru_hole oval (at -3.81 -13.97) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 3 thru_hole oval (at -3.81 -11.43) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 4 thru_hole oval (at -3.81 -8.89) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 5 thru_hole oval (at -3.81 -6.35) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 6 thru_hole oval (at -3.81 -3.81) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 7 thru_hole oval (at -3.81 -1.27) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 8 thru_hole oval (at -3.81 1.27) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 9 thru_hole oval (at -3.81 3.81) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 10 thru_hole oval (at -3.81 6.35) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 11 thru_hole oval (at -3.81 8.89) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 12 thru_hole oval (at -3.81 11.43) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 13 thru_hole oval (at -3.81 13.97) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 14 thru_hole oval (at -3.81 16.51) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 15 thru_hole oval (at 3.81 16.51) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 16 thru_hole oval (at 3.81 13.97) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 17 thru_hole oval (at 3.81 11.43) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 18 thru_hole oval (at 3.81 8.89) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 19 thru_hole oval (at 3.81 6.35) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 20 thru_hole oval (at 3.81 3.81) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 21 thru_hole oval (at 3.81 1.27) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 22 thru_hole oval (at 3.81 -1.27) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 23 thru_hole oval (at 3.81 -3.81) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 24 thru_hole oval (at 3.81 -6.35) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 25 thru_hole oval (at 3.81 -8.89) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 26 thru_hole oval (at 3.81 -11.43) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 27 thru_hole oval (at 3.81 -13.97) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))
  (pad 28 thru_hole oval (at 3.81 -16.51) (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask))

  (model "${KICAD8_3DMODEL_DIR}/Package_DIP.3dshapes/DIP-28_W7.62mm.wrl"
    (offset (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
"""

test_symbol_1 = f"""


(kicad_symbol_lib
  (version 20231120)
  (generator kicad_symbol_editor)
  (generator_version 9.0)

  (symbol "LM7321_SOIC-8"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)

    (property "Reference" "U"
      (at 0 8.89 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )

    (property "Value" "LM7321"
      (at 0 6.35 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )

    (property "Footprint" "TI_OpAmps:SOIC-8_3.9x4.9mm_P1.27mm"
      (at 0 -10.16 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm7321.pdf"
      (at 0 -12.7 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (property "Description" "Single Rail-to-Rail Input and Output ±15V High-Output Current Operational Amplifier, SOIC-8"
      (at 0 -15.24 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (symbol "LM7321_SOIC-8_0_1"
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
      (polyline
        (pts
          (xy -3.81 3.175)
          (xy -3.81 1.905)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 2.54)
          (xy -3.175 2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 -2.54)
          (xy -3.175 -2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
    )

    (symbol "LM7321_SOIC-8_1_1"
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
        (number "6"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
      )
      (pin power_in line
        (at -2.54 7.62 270)
        (length 3.048)
        (name "V+"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
        (number "7"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
      )
      (pin power_in line
        (at -2.54 -7.62 90)
        (length 3.048)
        (name "V-"
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
    )
  )

  (symbol "LM7322_SOIC-8"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (pin_names
      (offset 0.127)
    )
    (pin_numbers hide)

    (property "Reference" "U"
      (at 0 16.51 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )

    (property "Value" "LM7322"
      (at 0 13.97 0)
      (effects
        (font
          (size 1.27 1.27)
        )
      )
    )

    (property "Footprint" "TI_OpAmps:SOIC-8_3.9x4.9mm_P1.27mm"
      (at 0 -17.78 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm7322.pdf"
      (at 0 -20.32 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (property "Description" "Dual Rail-to-Rail Input and Output ±15V High-Output Current Operational Amplifier, SOIC-8"
      (at 0 -22.86 0)
      (effects
        (font
          (size 1.27 1.27)
        )
        (hide yes)
      )
    )

    (symbol "LM7322_SOIC-8_1_1"
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
      (polyline
        (pts
          (xy -3.81 3.175)
          (xy -3.81 1.905)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 2.54)
          (xy -3.175 2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 -2.54)
          (xy -3.175 -2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (text "A"
        (at 1.27 2.54 0)
        (effects
          (font
            (size 1.27 1.27)
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

    (symbol "LM7322_SOIC-8_2_1"
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
      (polyline
        (pts
          (xy -3.81 3.175)
          (xy -3.81 1.905)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 2.54)
          (xy -3.175 2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (polyline
        (pts
          (xy -4.445 -2.54)
          (xy -3.175 -2.54)
        )
        (stroke
          (width 0.1524)
          (type default)
        )
        (fill
          (type none)
        )
      )
      (text "B"
        (at 1.27 2.54 0)
        (effects
          (font
            (size 1.27 1.27)
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
        (number "6"
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
        (number "7"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
      )
    )

    (symbol "LM7322_SOIC-8_3_1"
      (rectangle
        (start -3.81 3.175)
        (end 3.81 -3.175)
        (stroke
          (width 0.254)
          (type default)
        )
        (fill
          (type background)
        )
      )

      (pin power_in line
        (at 0 5.08 270)
        (length 1.905)
        (name "V+"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
        (number "8"
          (effects
            (font
              (size 1.27 1.27)
            )
          )
        )
      )
      (pin power_in line
        (at 0 -5.08 90)
        (length 1.905)
        (name "V-"
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
    )
  )
)




"""
print(validate_kicad_symbol(test_symbol_1))

print(validate_kicad_footprint(test_symbol))
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