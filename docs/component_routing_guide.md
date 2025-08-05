# MCP Placing Components

## What It Does

The `place_component`, `move_component`, and `load_pcb_board` tools provide a way to **automatically place components** onto a KiCad PCB layout by calling KiCad and using the pcbnew inteface in a subprocess.

The same way the tool `track_routes` can be used to let the client place routes on the board automatically. 

Currently, this allows for:
- Loading `.kicad_pcb` boards from a `.kicad_pro` project.
- Placing a new component (footprint) at a given (x, y) coordinate.
- Moving an existing component to a new location.
- Placing routes on the board 
- Saving the board after the operation.

## Limitations

-   **No image or visual preview** of the component is available after placement in the .pcb File.
  - Only the **reference** (e.g., `R1`, `C5`, `U2`) is visible.

- This tool works by calling KiCad's backend logic (via `pcbnew`) in a **Python subprocess**, which has no GUI.


## How It Works

The MCP server uses a class called `KiCadBridge` that:
1. Locates the correct `python.exe` from your KiCad install to use Kicad Python Interface.
2. Builds a temporary script that runs in KiCad's environment.
3. Executes that script with a method and parameter set via JSON.
4. Uses KiCad APIs (`pcbnew`) to manipulate the board.

---

## Available Tools

### `load_pcb_board`
Loads the `.kicad_pcb` file and validates its availability.

### `place_component`
Places a new footprint on the PCB at a given location.
- Load PCB Board -> Place Component -> Save PCB Board 

### `move_component`
Moves an existing component (by reference) to a new position.

### `track_routes`
A `wire` two coordinates in the `.pcb` file of the project

## Workflow
All of these tools automatically load the PCB board file, as this is a prerequisite for performing any routing or placement operations.

**Example: Routing**
Before starting the wire placement process using the `track_routes` tool, it is important to first extract the netlist and other relevant design information from the PCB. This allows for proper analysis and validation before proceeding to route placement.

### Important Considerations:
Limitations of AI Routing Tools:
Tools like Claude currently do not enforce key PCB design constraints. For example:
- Routes are not restricted to 45° angles.
- Tracks may exceed board boundaries.
- Overlapping routes are not prevented or flagged.

A prompt template for routing is available to assist with automating the routing process. While this template can help guide the tool and streamline initial track placement, it does not ensure route correctness.

Recommended Alternative – FreeRouting Plugin for KiCad:
A more reliable approach is to use the FreeRouting plugin within KiCad. You can allow AI-assisted tools to control or optimize the output, but be aware

### Finalizing the Routing:
After completing the routing process:
- Save and close the PCB file.
- Reopen the file in your PCB design tool (e.g., KiCad) to view and verify the updated changes.


