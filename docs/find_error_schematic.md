# Finding Faults in Schematic File

The client is attempting to identify errors in a schematic file itself without using an Electrical Rules Check (ERC) from Kicad.
To ensure high-quality output, it's important to provide Claude with sufficient information. 
This typically includes:
- The schematic file itself (.txt version)
- The exported netlist file (.txt version)
- A PDF version of the schematic (for visual reference) 
    - in Kicad Schematic Editor: Plot -> Plot All Pages or Plot Current Page
- Relevant datasheets (especially for critical components like Microcontroller)

For larger projects, keep in mind that Claude may hit rate limits, which can affect performance. Additionally, Claude will overlook critical errors, so manual review or supplemental verification is still neccesary.

- The prompt `analyze_schematic` located in `C:\Git\kicad-mcp\kicad_mcp\prompts\analyze_schematic_prompt.py` provides a solid template for identifying errors in schematic files.

## Example:

**Added errors for testing:**
- changed Capacity value C2 from 100n to 10n 
- delete connection from UCAP pin 27 to Capacity C3
- Disconnect the crystal (Y1) from C11
- Add a new pushbutton (SW3) to GND without a pull-up, directly connected to ~RESET
- Drive Two LEDs from One I/O Without Current-Limiting Resistors

**Error found by Claude:**
- delete connection from UCAP pin 27 to Capacity C3
- Disconnect the crystal (Y1) from C11
- changed Capacity value C2 from 100n to 10n 

When you ask more specific questions and provide more focused input, Claude is more likely to identify issues in the file accurately.