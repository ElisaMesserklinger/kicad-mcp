# MCP Server Footprint & Symbol Assistant Guide

This guide explains how to generate footprint and symbol Files and how they are added to Kicad Library automatically.

## Workflow:
1. Generating .kicad_mod footprint content from datasheet data
2. Creating .kicad_sym symbol files from component details
3. Saving generated files to custom libraries
4. Registering libraries in KiCad’s global tables

## Prerequisites:
- Write access to your KiCad custom footprint & symbol directories and %AppData%/Roaming/kicad/…/sym-lib-table / fp-lib-table

### Datasheet Scanning: list_pdfs
Listing all PDFs for the specified Path. Is similar to searching for Projects but just one Path is used: `DATASHEET_PATH`

### Prompt Extraction: analyzePdf_prompt:
- In Claude Desktop click on the `+` and select the Server, then choose one of the Prompts
- For this specific Prompt also add a PDF so Claude is able to analyze something
- Prompts the AI to extract relevant mechanical and electrical specifications from the datasheet, including pad dimensions, pin mapping, orientation indicators, mounting type, and IPC guidelines.
- The Prompt can be changed and tailored in: `C:\Git\kicad-mcp\kicad_mcp\prompts\footprint_prompts.py`

#### Projects and `make_pdf_smaller`
- If a datasheet has more then 100 pages claude can not parse it in chat
Claude cannot reliably parse datasheets or PDFs with more than 100 pages directly in chat.

- Workaround: Splitting Large PDFs
To handle large documents, use the `make_pdf_smaller` tool, which has access to your directory and can split a PDF into smaller, more manageable parts.

Workflow:
- Use make_pdf_smaller to break the PDF into smaller chunks (e.g., 100–500 pages per file, depending on content density).
- Upload the split PDFs into the Projects chat in the Claude desktop app.
- Once uploaded, Claude can access and work with the content when prompted.

⚠️ Note: While this method allows access to large documents, parsing quality may be lower than when working with smaller PDFs directly in chat.

### Footprint and Symbol Generation: get_footprint_mod, get_symbol_mod:
- After analyzing the datasheet let Claude create the Footprint and Symbol File with another Prompt 
- Outputs only the .kicad_mod file content and the .kicad_sym content, following the specified template (courtyard, silkscreen, pads, orientation marks, etc.). 
- The Prompts can be changed and tailored in: `C:\Git\kicad-mcp\kicad_mcp\prompts\footprint_prompts.py`

### Validate Structure of the generated Files
Before saving generated symbols and footprints into your KiCad libraries, the system can perform validation to catch structural issues that would cause errors in importing the file in KiCad

- `validate_kicad_symbol(symbolContent)` is performing following checks:
    - Ensures the presence of required global keys (version, generator, generator_version)
    - Searches for all (symbol ...) blocks, and processes them individually.
    - Confirms that each symbol contains all required properties (Reference, Value, Footprint)
    - Checks that each symbol includes at least one valid pin with (name, number, position, type )

- `validate_kicad_footprint(footprint_content)` is performing following checks:
    - Ensures the file starts with a (footprint ...) block, which is required in all .kicad_mod files.
    - Verifies that the footprint includes at least one (pad ...) block — necessary for electrical connectivity in layout.

### Saving Footprint and Symbol: save_footprint_mod & add_footprint_to_Lib, save_symbol & add_symbol_to_Lib:
- Save .kicad_mod into .../footprints/MyCustomFootprints.pretty/
- Update `fp-lib-table` automatically to register the new library
- Appends or creates symbol library file in .../symbols/MyCustomSymbols.kicad_sym
- Updates `sym-lib-table` so KiCad recognizes it
- A prompt can be used to provide instructions for generating the file, but saving the file and adding it to the library are handled by dedicated tools in `C:\Git\kicad-mcp\kicad_mcp\tools\create_foodprint_symbol_tools.py`

### Edit saved Files 
- Writes generated KiCad **symbol** or **footprint** content to the appropriate file location.
- Tool is useful for changing the generated Output after it was saved without creating new file again

## Quickstart
1. Open Claude Desktop, upload the PDF, and select `analyzePdf_prompt`.
2. After analysis, use `get_footprint_mod` and `get_symbol_mod` to generate content
3. Validate using built-in checks that (tell claude to also validate Projects before saving).
4. Save using `save_footprint_mod` and `save_symbol`.
5. Automatically register using `add_footprint_to_Lib` and `add_symbol_to_Lib` (generated Files will be safed to global Footprint and Symbol Table).


## Debugging
- Possible causes for not being able to open symbol editor or footprint editor in kicad:
    - there might be a syntax error in the .kicad_sym or .kicad_mod file
    - something went wrong when saving the footrint or symbol to Library 

    Fix:
    - claude is able to edit the config
    - Possible prompt: "there is something wrong with the symbol you created review it again"
    - edit global `fp-lib-table` or `sym-lib-table` Path: [text](../../../AppData/Roaming/kicad/9.0/sym-lib-table)
 


## TODO: Before using the code, search for all `#Edit` comments and update the paths below them to match your own environment.


