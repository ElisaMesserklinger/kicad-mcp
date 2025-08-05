# KiCad Netlist Extraction Guide

This guide explains how to use the schematic netlist extraction features in the KiCad MCP Server.

## Overview

The netlist extraction functionality allows you to:

1. Extract comprehensive netlist information from KiCad schematics
2. Analyze component connections and relationships
3. Identify power and signal nets
4. Find specific component connections
5. Visualize the connectivity of your design

## Quick Reference

| Task | Example Prompt |
|------|---------------|
| Extract netlist | `Extract the netlist from my schematic at /path/to/project.kicad_sch (if there are subsheet every sheet netlist is being extracted)` |
| Analyze project netlist | `Analyze the netlist in my KiCad project at /path/to/project.kicad_pro` |
| Check component connections | `Show me the connections for R5 in my schematic at /path/to/project.kicad_sch` |
| View formatted netlist | `Show me the netlist report for /path/to/project.kicad_sch` |

## Using Netlist Features

### Extracting a Netlist

To extract a netlist from a schematic:

``` 
Extract the netlist from my schematic at /path/to/project.kicad_sch
```

This will:
- Parse the schematic file
- Extract all components and their properties
- Identify connections between components
- Analyze power and signal nets
- Return comprehensive netlist information

### Project-Based Netlist Extraction

To extract a netlist from a KiCad project:

```
Extract the netlist for my KiCad project at /path/to/project.kicad_pro
```

This will find the schematic associated with your project and extract its netlist.

### Analyzing Component Connections

To find all connections for a specific component:

```
Show me the connections for U1 in my schematic at /path/to/project.kicad_sch
```

This will provide:
- Detailed component information
- All pins and their connections
- Components connected to each pin
- Net names for each connection

### Viewing Netlist Reports

For a formatted netlist report:

```
Show me the netlist report for /path/to/project.kicad_sch
```

This will load the `kicad://netlist/project_path` resource, showing:
- Component summary
- Net summary
- Connection details
- Power nets
- Potential issues

## Understanding Netlist Data

### Components

Components in a netlist include:

| Field | Description | Example |
|-------|-------------|---------|
| Reference | Component reference designator | R1, C2, U3 |
| Type (lib_id) | Component type from library | Device:R, Device:C |
| Value | Component value | 10k, 100n, ATmega328P |
| Footprint | PCB footprint | Resistor_SMD:R_0805 |
| Pins | List of pin numbers and names | 1 (VCC), 2 (GND) |

### Nets

Nets in a netlist include:

| Field | Description | Example |
|-------|-------------|---------|
| Name | Net name | VCC, GND, NET1 |
| Pins | List of connected pins | R1.1, C1.1, U1.5 |
| Type | Power or signal | Power, Signal |

## Advanced Usage

### Integration with BOM Analysis

You can combine netlist extraction with BOM analysis:

```
Compare the netlist and BOM for my project at /path/to/project.kicad_pro
```

This helps identify:
- Components in the schematic but missing from the BOM
- Components in the BOM but missing from the schematic
- Value or footprint inconsistencies

### Design Validation

Use netlist extraction for design validation:

```
Check for floating inputs in my schematic at /path/to/project.kicad_sch
```

```
Verify power connections for all ICs in my project at /path/to/project.kicad_pro
```

### Power Analysis

Analyze your design's power distribution:

```
Show me all power nets in my schematic at /path/to/project.kicad_sch
```

```
List all components connected to the VCC net in my project at /path/to/project.kicad_pro
```

## Tips for Better Netlist Analysis

### Schematic Organization

For more meaningful netlist analysis:

1. **Use descriptive net names** instead of auto-generated ones
2. **Add power flags** to explicitly mark power inputs
3. **Organize hierarchical sheets** by function
4. **Use global labels** consistently for important signals
5. **Add metadata as properties** to components for better analysis

### Working with Complex Designs

For large schematics:

1. Focus on **specific sections** using hierarchical labels
2. Analyze **one component type at a time**
3. Examine **critical nets** individually
4. Use **reference designators systematically** (e.g., U1-U10 for microcontrollers)

## Troubleshooting

### Netlist Extraction Fails

If netlist extraction fails:

1. **Check file paths**: Ensure the schematic file exists and has the correct extension
2. **Verify file format**: Make sure the schematic is a valid KiCad 6+ .kicad_sch file
3. **Check file permissions**: Ensure you have read access to the file
4. **Look for syntax errors**: Recent edits might have corrupted the schematic file
5. **Try a simpler schematic**: Start with a small test case to verify functionality

### Missing Connections

If connections are missing from the netlist:

1. **Check for disconnected wires**: Wires that appear connected in KiCad might not actually be connected
2. **Verify junction points**: Make sure junction dots are present where needed
3. **Check hierarchical connections**: Ensure labels match across hierarchical sheets
4. **Verify net labels**: Net labels must be correctly placed to establish connections
