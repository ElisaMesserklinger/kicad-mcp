from mcp.server.fastmcp import FastMCP

def register_footprint_prompts(mcp: FastMCP) -> None:
    """Register Footprint-related prompt templates with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    

    @mcp.prompt()
    def analyzePdf_prompt() -> str:
        """Prompt for extracting IC package footprint information from datasheets."""
        return """
        I need to extract IC package footprint information from a component datasheet to create a KiCad footprint. Please analyze the datasheet and identify the package type, then provide the following information:

        1. [Package type identification]
        - Package family (BGA, QFP, QFN, SOIC, SOP, DIP, PGA, LGA, CSP, etc.)
        - Specific variant (LQFP, TQFP, SSOP, TSSOP, µBGA, FCBGA, DFN, SON, etc.)
        - Package material and construction details
        - Mount type (surface mount, through-hole, or mixed)

        2. [Package configuration details]
        - Total number of pins/pads/balls
        - Pin/pad arrangement (dual-side, quad-side, grid array, single row, etc.)
        - Pin/pad pitch (center-to-center spacing)
        - Pin/pad dimensions (width, length, diameter)
        - Lead/pin geometry (gull-wing, J-lead, straight, ball, etc.)

        3. [Package dimensions]
        - Overall package length and width
        - Package height/thickness
        - Body dimensions (excluding leads/pins)
        - Any chamfers, corner cuts, notches, or orientation marks
        - Lead protrusion or standoff height (for through-hole)

        4. [Pin/pad naming and numbering]
        - Numbering convention (sequential, row-column, etc.)
        - Starting position and direction
        - Pin 1 location and identification method
        - Any missing pins/pads in the sequence

        5. [Electrical and thermal specifications]
        - Power and ground pin locations
        - Thermal pad, exposed pad, or heat slug requirements
        - Any special electrical considerations
        - ESD protection requirements

        6. [Manufacturing and assembly requirements]
        - Recommended solder mask opening size
        - Recommended paste stencil opening size and thickness
        - Soldering method (reflow, wave, selective, hand)
        - Drill sizes (for through-hole packages)
        - Any special handling or assembly considerations

        7. [Standards compliance and layout recommendations]
        - IPC standard references (IPC-7351, IPC-2221, IPC-2222, etc.)
        - Recommended courtyard clearances
        - Silkscreen marking requirements
        - Keep-out zones or restricted areas
        - Routing recommendations (escape routing, via placement, etc.)

        8. [Package-specific considerations]
        - For BGA: ball collapse, via-in-pad requirements
        - For QFP/QFN: lead coplanarity, heel/toe fillet requirements
        - For through-hole: hole size, annular ring requirements
        - For fine-pitch packages: bridging prevention, inspection methods

        9. [Pin table for KiCad symbol creation]
        Create a detailed pin table with the following format for each package variant:

        **Table format:** Unit | Pin | Name | Function | Type | Graphic Style | Orientation | X Position | Y Position

        **Column definitions:**
        - Unit: Symbol unit number (1 for single symbols, 1/2/3 for multi-unit symbols)
        - Pin: Physical pin number from datasheet
        - Name: Pin name/label (V+, GND, OUT, +IN, -IN, etc.)
        - Type: Electrical type (Power input, Input, Output, Bidirectional, etc.)
        - Graphic Style: Line, Inverted, Clock, Inverted Clock 
        - Orientation: Pin direction (Up, Down, Left, Right)
        - X Position: Horizontal position in mils from symbol center
        - Y Position: Vertical position in mils from symbol center

        **Example pin table:**
        ```
        Unit | Pin | Name |  Electrical Type | Graphic Style | Orientation | X Position | Y Position
        1    | 5   | V+   | Power input | Up |Line| 0 mils | -250 mils
        1    | 4   | -IN  | Input | Left | Line |-300 mils | 100 mils
        1    | 3   | +IN  | Input | Left | Line |-300 mils | -100 mils
        1    | 2   | V-   | Power input | Down | Line | 0 mils | 250 mils
        1    | 1   | OUT  |  Output | Right | Line | 300 mils | 0 mils

        Group pins by function: Power, Analog, Digital, Communication, Control, etc.
        Maintain logical pin group order (e.g., all I2C pins grouped, all analog inputs together).
        Use the internal block diagram to guide logical symbol grouping and pin assignment.

        ```

        **Pin positioning guidelines:**
        - Standard pin spacing: 100 mils (2.54mm) between pins
        - Power pins: Top (V+, VCC, VDD) and bottom (GND, V-, VSS)
        - Input pins: Left side, arranged logically
        - Output pins: Right side, arranged logically
        - Bidirectional pins: Left or right side based on primary function
        - Symbol center: (0, 0) coordinate reference
        - Pin positions: Measured from symbol center to pin connection point
        - Pins are numbered sequentially down the left side, then continue sequentially up the right side starting from the bottom.

        **Electrical type definitions:**
        - Power input: V+, VCC, VDD, V-, GND, VSS
        - Input: Signal inputs, control pins, enable pins
        - Output: Signal outputs, status pins
        - Bidirectional: I/O pins, data buses
        - Tri-state: Tri-state outputs
        - Passive: Passive connections, no specific direction
        - Open collector: Open collector outputs
        - Open emitter: Open emitter outputs
        - Unspecified: Unknown or unspecified function

        Create separate pin tables for each package variant if multiple packages are available for the same component.

        Please extract this information systematically and format it clearly so I can create an accurate KiCad footprint and symbol that meets industry standards for the specific IC package type.

        """
    
    @mcp.prompt()
    def get_footprint_mod() -> str:
        return """
       You are a KiCad footprint generator. Generate ONLY the `.kicad_mod` file content with no explanations or additional text.

    ### INPUT SPECIFICATIONS:
    - Package: [PACKAGE_TYPE]
    - Pins: [PIN_COUNT]
    - Pitch: [PITCH]mm
    - Body: [LENGTH]mm x [WIDTH]mm
    - Pad size: [PAD_WIDTH]mm x [PAD_HEIGHT]mm
    - Pad type: [SMD | Through-hole]
    - Pad shape: [Rectangular | Rounded | Circular | Oval]
    - Pin arrangement: [Single row | Dual row | Quad side | Grid array | Custom]
    - Silkscreen clearance: [e.g., 0.2mm from pad edges]
    - Courtyard clearance: [e.g., 0.25mm from body outline]
    - **Pads should be horizontal.**
    - Pad orientation: Horizontal (wide in X, narrow in Y)
    - Pin numbering direction: From bottom left to top left and then top right to bottom right
    - Pin 1: Located at bottom-left



    ---

    ### PHYSICAL ORIENTATION:
    - The PCB is **standing vertically**, like a module placed upright.
    - X-axis is horizontal, Y-axis is vertical.
    - The long side of the body runs along the Y-axis
    - Pads are aligned vertically (in Y), but oriented horizontally (i.e., wide in X, short in Y).
    - **Pin 1 is located in the bottom-left corner** of the physical footprint **when viewed from the top layer in KiCad PCB editor**.
    - Do NOT mirror or flip Y axis
    - +Y is top, –Y is bottom
    - +X is right, –X is left

    - **Pin numbering:**
    - Pins increase from **bottom to top on the left side**
    - Then continue **top to bottom on the right side** (U-shaped pattern)

    EXAMPLE PIN PLACEMENT (FOR REFERENCE ONLY, REMOVE IN OUTPUT):
    (pad 1 smd rect (at -1.5 -1.5) (size 1.5 0.6))
    (pad 2 smd rect (at -1.5 0.0) ...)
    ...
    (pad 5 smd rect (at 1.5 -1.5) ...) ; Top-right
    ---

    ### MECHANICAL & VISUAL FEATURES:
    - The **bottom-left corner of the footprint must include a dot or notch** (silkscreen circle) to indicate Pin 1.
    - **The PCB outline includes a chamfered cut corner** at the **bottom-left** (Edge.Cuts layer) to provide mechanical orientation.
    ---

    ### FILE FORMAT:
    - Use standard KiCad formatting.
    - All dimensions must be in millimeters.
    - Layers to use:
    - **Pads**: F.Cu, F.Paste, F.Mask
    - **Silkscreen**: F.SilkS
    - **Fabrication**: F.Fab
    - **Courtyard**: F.CrtYd
    - **Board outline**: Edge.Cuts

    ---

    ### REQUIRED STRUCTURE:
    - Begin with: `(module "FOOTPRINT_NAME" (layer F.Cu)`
    - Include:
    - `reference` text
    - `value` text
    - `courtyard outline`
    - `fabrication layer`
    - `silkscreen layer`
    - `pin 1 indicator`
    - `all pads`

    ---

    DO NOT ADD COMMENTS OR EXPLANATIONS IN THE FILE OUTPUT.

    Return only the complete `.kicad_mod` file content for your specified package.
            Here is just a example for a Format without any real values:
            (footprint "<PACKAGE_NAME>"
            (layer <LAYER>)
            (descr "<DESCRIPTION>")
            (tags "<TAGS>")
            (attr <ATTRIBUTE>)
            
            (property "Reference" "<REFERENCE>"
                (at <REF_X> <REF_Y> <REF_ROTATION>)
                (layer "<REF_LAYER>")
                (uuid "<REF_UUID>")
                (effects
                    (font
                        (size <REF_FONT_SIZE_X> <REF_FONT_SIZE_Y>)
                        (thickness <REF_FONT_THICKNESS>)
                    )
                )
            )
            
            (property "Value" "<VALUE>"
                (at <VAL_X> <VAL_Y> <VAL_ROTATION>)
                (layer "<VAL_LAYER>")
                (uuid "<VAL_UUID>")
                (effects
                    (font
                        (size <VAL_FONT_SIZE_X> <VAL_FONT_SIZE_Y>)
                        (thickness <VAL_FONT_THICKNESS>)
                    )
                )
            )
            
            (property "Datasheet" "<DATASHEET>"
                (at <DS_X> <DS_Y> <DS_ROTATION>)
                (layer "<DS_LAYER>")
                (hide <DS_HIDE>)
                (uuid "<DS_UUID>")
                (effects
                    (font
                        (size <DS_FONT_SIZE_X> <DS_FONT_SIZE_Y>)
                        (thickness <DS_FONT_THICKNESS>)
                    )
                )
            )
            
            (property "Description" "<DESCRIPTION_TEXT>"
                (at <DESC_X> <DESC_Y> <DESC_ROTATION>)
                (layer "<DESC_LAYER>")
                (hide <DESC_HIDE>)
                (uuid "<DESC_UUID>")
                (effects
                    (font
                        (size <DESC_FONT_SIZE_X> <DESC_FONT_SIZE_Y>)
                        (thickness <DESC_FONT_THICKNESS>)
                    )
                )
            )
            
            (fp_line (start <CRTYD_X1> <CRTYD_Y1>) (end <CRTYD_X2> <CRTYD_Y1>) (layer <CRTYD_LAYER>) (width <CRTYD_WIDTH>))
            (fp_line (start <CRTYD_X2> <CRTYD_Y1>) (end <CRTYD_X2> <CRTYD_Y2>) (layer <CRTYD_LAYER>) (width <CRTYD_WIDTH>))
            (fp_line (start <CRTYD_X2> <CRTYD_Y2>) (end <CRTYD_X1> <CRTYD_Y2>) (layer <CRTYD_LAYER>) (width <CRTYD_WIDTH>))
            (fp_line (start <CRTYD_X1> <CRTYD_Y2>) (end <CRTYD_X1> <CRTYD_Y1>) (layer <CRTYD_LAYER>) (width <CRTYD_WIDTH>))
            
            (fp_line (start <FAB_X1> <FAB_Y1>) (end <FAB_X2> <FAB_Y1>) (layer <FAB_LAYER>) (width <FAB_WIDTH>))
            (fp_line (start <FAB_X2> <FAB_Y1>) (end <FAB_X2> <FAB_Y2>) (layer <FAB_LAYER>) (width <FAB_WIDTH>))
            (fp_line (start <FAB_X2> <FAB_Y2>) (end <FAB_X1> <FAB_Y2>) (layer <FAB_LAYER>) (width <FAB_WIDTH>))
            (fp_line (start <FAB_X1> <FAB_Y2>) (end <FAB_X1> <FAB_Y1>) (layer <FAB_LAYER>) (width <FAB_WIDTH>))
            
            (fp_line (start <SILK_X1> <SILK_Y1>) (end <SILK_X2> <SILK_Y1>) (layer <SILK_LAYER>) (width <SILK_WIDTH>))
            (fp_line (start <SILK_X2> <SILK_Y1>) (end <SILK_X2> <SILK_Y2>) (layer <SILK_LAYER>) (width <SILK_WIDTH>))
            (fp_line (start <SILK_X2> <SILK_Y2>) (end <SILK_X1> <SILK_Y2>) (layer <SILK_LAYER>) (width <SILK_WIDTH>))
            (fp_line (start <SILK_X1> <SILK_Y2>) (end <SILK_X1> <SILK_Y1>) (layer <SILK_LAYER>) (width <SILK_WIDTH>))
            
            (fp_circle (center <PIN1_IND_X> <PIN1_IND_Y>) (end <PIN1_IND_X2> <PIN1_IND_Y2>) (layer <PIN1_LAYER>) (width <PIN1_WIDTH>))
            
            (pad <PAD1_NUMBER> <PAD1_TYPE> <PAD1_SHAPE> (at <PAD1_X> <PAD1_Y> <PAD1_ROTATION>) (size <PAD1_SIZE_X> <PAD1_SIZE_Y>) (layers <PAD1_LAYERS>))
            (pad <PAD2_NUMBER> <PAD2_TYPE> <PAD2_SHAPE> (at <PAD2_X> <PAD2_Y> <PAD2_ROTATION>) (size <PAD2_SIZE_X> <PAD2_SIZE_Y>) (layers <PAD2_LAYERS>))
            (pad <PAD3_NUMBER> <PAD3_TYPE> <PAD3_SHAPE> (at <PAD3_X> <PAD3_Y> <PAD3_ROTATION>) (size <PAD3_SIZE_X> <PAD3_SIZE_Y>) (layers <PAD3_LAYERS>))
            ...
            (pad <PADN_NUMBER> <PADN_TYPE> <PADN_SHAPE> (at <PADN_X> <PADN_Y> <PADN_ROTATION>) (size <PADN_SIZE_X> <PADN_SIZE_Y>) (layers <PADN_LAYERS>))
            
            (pad <THERM_PAD_NUMBER> <THERM_PAD_TYPE> <THERM_PAD_SHAPE> (at <THERM_PAD_X> <THERM_PAD_Y> <THERM_PAD_ROTATION>) (size <THERM_PAD_SIZE_X> <THERM_PAD_SIZE_Y>) (layers <THERM_PAD_LAYERS>))
        )


            NO COMMENTS

            Placeholder	Description:
            PACKAGE_NAME	Name of the footprint (e.g., "SOIC-8_4.9x3.9mm_P1.27mm")
            <CRTYD_X> / <CRTYD_Y>	Half-width and half-height of courtyard
            <BODY_X> / <BODY_Y>	Half-width and half-height of the body outl ine
            <PAD_X> / <PAD_Y>	Width and height of the SMD pad
            <PIN_X>	Horizontal distance from center to pad row
            <PIN_Yn>	Vertical offset of each pad
            <PIN1_X> / <PIN1_Y>	Position of the Pin 1 indicator
            <REF_Y_OFFSET> / <VAL_Y_OFFSET>	Placement of reference and value labels

            Return only the complete .kicad_mod file content for your specified package
            """
        

    @mcp.prompt()
    def get_symbol_mod() -> str:
        return """
        You are a KiCad symbol generator. Generate ONLY the .kicad_sym file content with no explanations or additional text.
        Input specifications:


        Component: [COMPONENT_NAME]
        Package: [PACKAGE_TYPE]
        Pins: [PIN_COUNT]
        Pin functions: [PIN_FUNCTION_LIST]
        Symbol type: [IC/CONNECTOR/PASSIVE/etc.]
        Reference designator: [R/C/L/U/J/etc.]

        Output format requirements:

        Start with: (kicad_symbol_lib
        Include: complete symbol definition with proper KiCad v9.0 format
        Symbol name format: [PART_NUMBER]_[PACKAGE]
        All dimensions in millimeters (1.27mm grid units)
        Standard KiCad properties: Reference, Value, Footprint, Datasheet, Description
        Proper pin numbering, names, and electrical types

        Pin electrical types:

        input: Input signal
        output: Output signal
        bidirectional: I/O signal
        tri_state: Tri-state output
        passive: Passive connection
        power_in: Power supply input (VCC, VDD, V+)
        power_out: Power supply output
        open_collector: Open collector output
        open_emitter: Open emitter output
        unspecified: Unknown/unspecified

        Pin positioning guidelines:
        - Inputs: Left side
        - Outputs: Right side
        - Bidirectional: Left or Right depending on function
        - Power inputs: Top
        - Power outputs / GND: Bottom
        - Passive: Grouped logically or left/right as needed    
        - Maintain 1.27mm vertical spacing between pins

        DO NOT ADD COMMENTS IN YOUR GENERATED FILE

        Here is just a example for a Format of a Library that contains multiple Symbols without any real values:

        **PLEASE NOTE**:
        - If you are addding symbols to an already existing library you can NOT add the header too, you have to start with (symbol )

        (kicad_symbol_lib
        (version [VERSION])
        (generator [GENERATOR])
        (generator_version 9.0)

        (symbol "[COMPONENT_NAME]_[PACKAGE_TYPE]"
            (exclude_from_sim [yes/no])
            (in_bom [yes/no])
            (on_board [yes/no])

            (property "Reference" "[REFERENCE_PREFIX]"
            (at [X] [Y] [ANGLE])
            (effects
                (font
                (size [WIDTH] [HEIGHT])
                )
            )
            )

            (property "Value" "[VALUE]"
            (at [X] [Y] [ANGLE])
            (effects
                (font
                (size [WIDTH] [HEIGHT])
                )
            )
            )

            (property "Footprint" "[FOOTPRINT_LIBRARY]:[FOOTPRINT_NAME]"
            (at [X] [Y] [ANGLE])
            (effects
                (font
                (size [WIDTH] [HEIGHT])
                )
                (hide [yes/no])
            )
            )

            (property "Datasheet" "[DATASHEET_LINK]"
            (at [X] [Y] [ANGLE])
            (effects
                (font
                (size [WIDTH] [HEIGHT])
                )
                (hide [yes/no])
            )
            )

            (property "Description" "[DESCRIPTION_TEXT]"
            (at [X] [Y] [ANGLE])
            (effects
                (font
                (size [WIDTH] [HEIGHT])
                )
                (hide [yes/no])
            )
            )

            (symbol "[COMPONENT_NAME]_[PACKAGE_TYPE]_0_1"
            ([GRAPHIC_ELEMENT]
                (start [X1] [Y1])
                (end [X2] [Y2])
                (stroke
                (width [WIDTH])
                (type [LINE_TYPE])
                )
                (fill
                (type [FILL_TYPE])
                )
            )
            )

            (symbol "[COMPONENT_NAME]_[PACKAGE_TYPE]_1_1"
            (pin [ELECTRICAL_TYPE] [LINE_STYLE]
                (at [X] [Y] [ANGLE])
                (length [LENGTH])
                (name "[PIN_NAME]"
                (effects
                    (font
                    (size [WIDTH] [HEIGHT])
                    )
                )
                )
                (number "[PIN_NUMBER]"
                (effects
                    (font
                    (size [WIDTH] [HEIGHT])
                    )
                )
                )
            )
            )
        )
        )

        Notes: 
        - The values for the property fields should not all be on the same position but a little under the symbol. 
        - Unconnected Pins should not be displayed
        - To avoid overlapping, the font size of the pin labels can be slightly reduced when there are many labels.

        Return only the complete .kicad_sym file content for your specified component.
        """
    

    @mcp.prompt()
    def save_prompt() -> str:
        return """
        Save the generated symbol and footprint files to the predefined location.

        - If the symbol or footprint belongs to the same component model or series (e.g., same IC family, part series, or vendor group), save them in the **same custom library** to maintain logical grouping.
        - Library names must be **unique, descriptive, and clearly distinguishable** from standard KiCad libraries. Avoid any generic names like "Device", "Power", "MCU", etc., to prevent naming conflicts.
        - **File and library names must be very clear and specific**, including relevant identifiers such as the manufacturer, part number, package type, or function (e.g., `AnalogDevices_ADG884_MSOP10.lib`, `MyCustomFootprints.pretty`).
        - The files and libraries must not only be saved to disk, but also **registered in the appropriate KiCad library tables** (`sym-lib-table` and `fp-lib-table`) if not already present.
        - No need to redefine save paths — assume that is handled in the existing environment.
        - Ensure no duplicate or conflicting entries are introduced into the environment.

        **Before saving ensure that the created files are valid and validate the structure**
        """