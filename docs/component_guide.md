# MCP Placing Components

## What It Does

The `place_component`, `move_component`, and `load_pcb_board` tools provide a way to **automatically place components** onto a KiCad PCB layout by calling KiCad and using the pcbnew inteface in a subprocess.

Currently, this allows for:
- Loading `.kicad_pcb` boards from a `.kicad_pro` project.
- Placing a new component (footprint) at a given (x, y) coordinate.
- Moving an existing component to a new location.
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

