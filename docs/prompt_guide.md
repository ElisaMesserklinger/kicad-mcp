# KiCad Prompt Templates Guide

This guide explains how to use the prompt templates feature in the KiCad MCP Server to improve your interaction with Claude and other LLMs when working with KiCad projects.

## Overview

Prompt templates are pre-built conversation starters designed to help you get the most out of LLMs when working with KiCad. They provide structured formats for common KiCad tasks, ensuring you get high-quality assistance from the AI.

## Available Prompt Templates

The KiCad MCP Server includes several specialized prompt templates for common KiCad workflows:

### General KiCad Prompts

| Prompt Template | Description | Use When |
|----------------|-------------|----------|
| `create_new_component` | Guidance for creating new KiCad components | You need to create a schematic symbol, PCB footprint, or 3D model |
| `debug_pcb_issues` | Help with troubleshooting PCB problems | You encounter issues with your PCB design |
| `pcb_manufacturing_checklist` | Preparation guidance for manufacturing | You're getting ready to send your PCB for fabrication |

### DRC-Specific Prompts

| Prompt Template | Description | Use When |
|----------------|-------------|----------|
| `fix_drc_violations` | Help with resolving DRC violations | You have design rule violations to fix |
| `custom_design_rules` | Guidance for creating custom design rules | You need specialized design rules for your project |

### BOM-Related Prompts

| Prompt Template | Description | Use When |
|----------------|-------------|----------|
| `analyze_components` | Analysis of component usage in your design | You want insights about your component selections |
| `cost_estimation` | Help with estimating project costs | You need to budget for your PCB project |
| `bom_export_help` | Assistance with exporting BOMs | You need help creating or customizing BOMs |
| `component_sourcing` | Guidance for finding and sourcing components | You need to purchase components for your project |
| `bom_comparison` | Compare BOMs between different design revisions | You want to understand changes between versions |

### Prompts to Create Footprints and Sybols

| Prompt Template | Description | Use When |
|----------------|-------------|----------|
| `analyzePdf_prompt` | Extracts Information from Datasheet | You want to get summary of datasheet |
| `get_footprint_mod` | Claude generates .mod file and .pretty Folder as Library | You want to create Footprint for Footprint Editor |
| `get_symbol_mod` | Claude generates .kicad_sym File | You want to create Symbol for Symbol Editor |
| `save_prompt` | Claude saves the generated Files and adds to Library | You want to use the generated Files in kicad |
