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
    
    print(f"Place result: {place_result}")
    
    if not place_result.get("success"):
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
    
    project_path = "C:/Users/messeel/KiCadProjects/KiCad\\test1\\test1.kicad_pro"
    
    print("Testing simplified place_component (load -> place -> save)...")
    
    # Single method call does everything
    result = kicad.place_component(
        project_path=project_path,
        component_id="R_0805_2012Metric",
        position={"x": 25.0, "y": 15.0},
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


#test_place_component_workflow()
test_simplified_place_component()


#"path": "C:/Users/messeel/KiCadProjects/KiCad\\test1\\test1.kicad_pro",
  