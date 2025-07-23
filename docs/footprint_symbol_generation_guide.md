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
- Prompts AI to analyze datasheet and extract dimensions, pin layout, pad sizes, orientation marks, mount type, assembly suggestions, IPC standards, etc.
- The Prompt can be changed and tailored in: `C:\Git\kicad-mcp\kicad_mcp\prompts\footprint_prompts.py`

### Footprint and Symbol Generation: get_footprint_mod, get_symbol_mod:
- After analyzing the datasheet let Claude create the Footprint and Symbol File with another Prompt
- Outputs only the .kicad_mod file content and the .kicad_sym content, following the specified template (courtyard, silkscreen, pads, orientation marks, etc.). 
- The Prompts can be changed and tailored in: `C:\Git\kicad-mcp\kicad_mcp\prompts\footprint_prompts.py`

###  Saving Footprint and Symbol: save_footprint_mod & add_footprint_to_Lib, save_symbol & add_symbol_to_Lib:
- Save .kicad_mod into .../footprints/MyCustomFootprints.pretty/
- Update `fp-lib-table` automatically to register the new library
- Appends or creates symbol library file in .../symbols/MyCustomSymbols.kicad_sym
- Updates `sym-lib-table` so KiCad recognizes it
- A prompt can be used to provide instructions for generating the file, but saving the file and adding it to the library are handled by dedicated tools in `C:\Git\kicad-mcp\kicad_mcp\tools\create_foodprint_symbol_tools.py`


## TODO: Before using the code, search for all `#Edit` comments and update the paths below them to match your own environment.


