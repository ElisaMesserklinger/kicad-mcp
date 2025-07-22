import os
import logging # Import logging
import subprocess
import sys # Add sys import
from typing import Dict, List, Any, Optional
import pathlib
import anthropic
from dotenv import load_dotenv
from pathlib import Path
import sexpdata



from kicad_mcp.config import KICAD_USER_DIR, KICAD_APP_PATH, KICAD_EXTENSIONS, ADDITIONAL_SEARCH_PATHS, DATASHEET_PATH

#for symbol validation 
REQUIRED_PROPERTIES = {"Reference", "Value", "Footprint"}
REQUIRED_TOP_LEVEL_KEYS = {"version", "generator", "generator_version"}



# Remove all existing handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Now configure your logging cleanly
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_sunprocess.log', mode='w'),
        logging.StreamHandler()  # Also logs to console
    ]
)

logging.debug("Logger initialized correctly")


def find_pdfs() -> List[Dict[str, Any]]:
    """Find PDF files in the given directories.
    
    Args:
        search_dirs: List of base directories to search in.

    Returns:
        List of dictionaries with PDF file information.
    """
    pdfs = []
    logging.info("Attempting to find PDF files...")

    search_dirs = [DATASHEET_PATH]
    logging.info(f"Raw KICAD_USER_DIR: '{KICAD_USER_DIR}'")
    logging.info(f"Raw search list before expansion: {search_dirs}")

    expanded_search_dirs = []
    for raw_dir in search_dirs:
        expanded_dir = os.path.expanduser(raw_dir)
        if expanded_dir not in expanded_search_dirs:
            expanded_search_dirs.append(expanded_dir)
        else:
            logging.info(f"Skipping duplicate expanded path: {expanded_dir}")

    logging.info(f"Expanded search directories: {expanded_search_dirs}")

    for search_dir in expanded_search_dirs:
        if not os.path.exists(search_dir):
            logging.warning(f"Expanded search directory does not exist: {search_dir}")
            continue
        
        logging.info(f"Scanning expanded directory: {search_dir}")
        for root, _, files in os.walk(search_dir, followlinks=True):
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    if not os.path.isfile(file_path):
                        logging.info(f"Skipping non-file/broken symlink: {file_path}")
                        continue
                    
                    try:
                        mod_time = os.path.getmtime(file_path)
                        rel_path = os.path.relpath(file_path, search_dir)
                        url = pathlib.Path(file_path).absolute().as_uri() 


                        logging.info(f"Found accessible PDF: {file_path}")
                        pdfs.append({
                            "name": os.path.splitext(file)[0],
                            "path": file_path,
                            "relative_path": rel_path,
                            "modified": mod_time,
                             "url": url
                        })
                    except OSError as e:
                        logging.error(f"Error accessing PDF file {file_path}: {e}")
                        continue

    logging.info(f"Found {len(pdfs)} PDF files after scanning.")
    return pdfs

# not helpful because of Claude Rate Limits
'''
def analyze_pdfs(pdf_url: str, prompt: str) -> List[Dict[str, Any]]:
    """
    Analyze a list of PDFs using Claude (Anthropic) via URL-based document references.

    Args:
        pdf_urls: publicly accessible PDF URL.
        prompt: Custom prompt/question to ask Claude about each PDF.

    Returns:
        List of analysis results per PDF (as Claude's structured response).
    """
    #does not really work because of limited tokens per minute 
    client = anthropic.Anthropic()
    results = []

    try:
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",  #change to other models
                max_tokens=2000,
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
'''

def save_kicad_footprint(footprint_content: str, footprint_name: str, lib_name: str):
    """
    Save a KiCad footprint (.kicad_mod) file to a library
    
    Args:
        footprint_content: The complete .kicad_mod file content
        footprint_name: Name of the footprint (without .kicad_mod extension)
        library_path: Path to the .pretty library folder
    """

    #Edit if needed 
    footprint_path = "c:/Users/messeel/KiCadProjects/KiCad/9.0/footprints"

    try:
        # Validate inputs
        if not footprint_content or not footprint_content.strip():
            raise ValueError("Footprint content cannot be empty")
        
        if not footprint_name or not footprint_name.strip():
            raise ValueError("Footprint name cannot be empty")
        
        if not footprint_path or not footprint_path.strip():
            raise ValueError("Library path cannot be empty")
        
        
        # Create library directory if it doesn't exist
        library_dir = Path(footprint_path)
        # if .pretty already exists
        #if lib_name.endswith(".pretty"):
         #   lib_name = lib_name[:-7]  # ".pretty" has 7 signs

        path_to_lib = library_dir / f"{lib_name}.pretty"
        path_to_lib.mkdir(parents=True, exist_ok=True)
        
        # Create the footprint file path
        footprint_file = path_to_lib / f"{footprint_name}.kicad_mod"
        
        # Check if file already exists and warn
        if footprint_file.exists():
            print(f"Warning: Footprint {footprint_file} already exists and will be overwritten")
        
        
        # Write the footprint content to file
        with open(footprint_file, 'w', encoding='utf-8') as f:
            f.write(footprint_content)
        
        #print(f"Successfully saved footprint: {footprint_file}")
        return True
        
    except ValueError as e:
        print(f"Validation error: {e}")
        logging.debug("Validation error")

        logging.debug(e)
        return False
    
    except OSError as e:
        print(f"File system error: {e}")
        logging.debug("File System error")

        logging.debug(e)

        return False
    
    except PermissionError as e:
        print(f"Permission error: {e}")
        logging.debug("Permission error")
        logging.debug(e)

        return False
    
    except Exception as e:
        print(f"Unexpected error saving footprint: {e}")
        logging.debug("Unexpected error")
        logging.debug(e)

        return False
    
    
    
def save_kicad_footprint_symbol_to_table(lib_name: str, description: str, type: str):
    """
    Adds a custom .pretty footprint library to the global KiCad footprint library table (fp-lib-table).
    
    Args:
        lib_path (str): Full path to the .pretty folder containing the custom footprint library.
    """

    #change version
    kicad_version = "9.0" 

    logging.debug("Library Path")
    
    if(type == "symbol"):
        table = "sym-lib-table"
        #Edit 
        lib_path = f"c:/Users/messeel/KiCadProjects/KiCad/9.0/symbols/{lib_name}.kicad_sym"
    else:
        table = "fp-lib-table"
        #Edit
    
        lib_path = f"c:/Users/messeel/KiCadProjects/KiCad/9.0/footprints/{lib_name}.pretty"

    logging.debug(lib_path)
    

    #Path to global lib table: c:\Users\<User>\%AppData%\kicad\9.0\fp-lib-table
    #Edit
    lib_table_path = Path(f"C:/Users/messeel/AppData/Roaming/kicad/{kicad_version}/{table}")

    if lib_table_path.exists():
        with open(lib_table_path, "r") as f:
            lines = f.readlines()
    else:
        # No global Path exists
        return False
    
    lib_entry = f'''(lib (name "{lib_name}") (type KiCad) (uri "{lib_path}") (options "") (descr "{description}"))\n'''

    if any(f'(name "{lib_name}")' in line for line in lines):
        logging.debug("Library already exists")
        print(f"Library '{lib_name}' already exists in fp-lib-table.")
        return False
    else:
    # Insert in the end 
        if lines[-1].strip() == ")":
            lines.insert(-1, lib_entry)
        else:
            lines.append(lib_entry + ")\n")

    # Write back
    with open(lib_table_path, "w") as f:
        f.writelines(lines)

    print(f"Library '{lib_name}' added.")
    return True

def save_kicad_symbol(symbol_content: str, symbol_name: str, lib_name: str):
    """
    Save a KiCad symbol (.kicad_sym) to a symbol library.
    
    Args:
        symbol_content: The symbol definition
        symbol_name: Name of the symbol
        lib_name: Name of the symbol library (without .kicad_sym)
        lib_path: Path where the library file is or should be located
    """
    #Edit
    symbol_path = "c:/Users/messeel/KiCadProjects/KiCad/9.0/symbols"

    
    try:
            # Validate inputs
            if not symbol_content or not symbol_content.strip():
                raise ValueError("Symbol content cannot be empty")
            
            if not symbol_name or not symbol_name.strip():
                raise ValueError("Symbol name cannot be empty")
            
            if not symbol_path or not symbol_path.strip():
                raise ValueError("Library path cannot be empty")

            # Construct full library file path
            library_file = Path(symbol_path) / f"{lib_name}.kicad_sym"
            is_new_library = not library_file.exists()
            

            if is_new_library:
                # Create directory if needed
                library_file.parent.mkdir(parents=True, exist_ok=True)

                #Claude already generates Header 
                with open(library_file, 'w', encoding='utf-8') as f:
                    #f.write('(kicad_symbol_lib (version 20211014) (generator "claude_generator") (generator_version "9.0") (symbol')
                    f.write(symbol_content.strip() + '\n')
        

            else:
                # Read existing content
                with open(library_file, 'r+', encoding='utf-8') as f:
                    content = f.read().strip()

                    # Check if the symbol already exists
                    if f"(symbol {symbol_name} " in content:
                        print(f"Warning: Symbol '{symbol_name}' already exists in {library_file} and will be duplicated")

                    # Insert symbol before final closing `))`
                    insert_pos = find_insert_position(content)
                    if insert_pos == -1:
                        raise ValueError("Invalid .kicad_sym file format")


                    new_content = content[:insert_pos].rstrip() + '\n' + symbol_content.strip() + '\n' + content[insert_pos:]

                    # Go back to start and overwrite
                    f.seek(0)
                    f.write(new_content)
                    f.truncate()

            #print(f"Successfully saved symbol '{symbol_name}' to {library_file}")
            return True

    except ValueError as e:
            print(f"Validation error: {e}")
            return False

    except OSError as e:
            print(f"File system error: {e}")
            return False

    except PermissionError as e:
            print(f"Permission error: {e}")
            return False

    except Exception as e:
            print(f"Unexpected error saving symbol: {e}")
            return False

def find_insert_position(content: str) -> int:
    """
    Finds the position just before the final closing `))` of the top-level kicad_symbol_lib block.
    Assumes that the content starts with (kicad_symbol_lib ... (symbols
    """
    depth = 0
    for i in range(len(content)):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1 

def find_blocks_symbol(symbol_data, block_name):
    """Recursively find blocks like (property ...) or (symbol ...) for validation of symbol file"""
    matches = []

    def walk(node):
        if isinstance(node, list) and node:
            if isinstance(node[0], sexpdata.Symbol) and node[0].value() == block_name:
                matches.append(node)
            for child in node:
                walk(child)

    walk(symbol_data)
    return matches


def validate_properties_symbol(symbol_data):
    props = find_blocks_symbol(symbol_data, "property")
    found = {
        p[1]  # p[1] is the property name (e.g., 'Reference')
        for p in props
        if len(p) > 1 and isinstance(p[1], str)
    }
    missing = REQUIRED_PROPERTIES - found
    return missing

def validate_top_level_keys(parsed_data):
    found_keys = {
        item[0].value()  # get the symbol name
        for item in parsed_data
        if isinstance(item, list) and item and isinstance(item[0], sexpdata.Symbol)
    }

    missing_keys = REQUIRED_TOP_LEVEL_KEYS - found_keys
    return missing_keys

def validate_pins_symbol(symbol_data):
    pin_blocks = find_blocks_symbol(symbol_data, "pin")
    valid_pins = []
    for pin in pin_blocks:
        try:
            pin_type = pin[1].value()
            pos = next(x for x in pin if isinstance(x, list) and x[0].value() == 'at')
            name = next(x for x in pin if isinstance(x, list) and x[0].value() == 'name')
            number = next(x for x in pin if isinstance(x, list) and x[0].value() == 'number')
            valid_pins.append((pin_type, pos, name, number))
        except Exception:
            continue
    return valid_pins


def validate_kicad_symbol(symbolContent):
    try:
        if not symbolContent.strip().startswith("("):
            symbolContent = f"({symbolContent})"
        parsed = sexpdata.loads(symbolContent)

        # validate top-level keys
        missing_top = validate_top_level_keys(parsed)
        if missing_top:
            return {"success": False, "error": f"Missing top-level keys: {missing_top}"}

        #Find all (symbol ...) blocks in the top-level list
        symbol_blocks = [
            item for item in parsed 
            if isinstance(item, list) and item and isinstance(item[0], sexpdata.Symbol) and item[0].value() == "symbol"
        ]

        if not symbol_blocks:
            return {"success": False, "error": "No symbol blocks found."}

        results = []
        for symbol in symbol_blocks:
            # Extract symbol name from second element (e.g., (symbol "LM7321")
            symbol_name = symbol[1].value() if isinstance(symbol[1], sexpdata.Quoted) else str(symbol[1])

            missing_props = validate_properties_symbol(symbol)
            pins = validate_pins_symbol(symbol)

            if missing_props:
                results.append({
                    "symbol": symbol_name,
                    "success": False,
                    "error": "Missing properties: " + ", ".join(missing_props)
                })
            elif not pins:
                results.append({
                    "symbol": symbol_name,
                    "success": False,
                    "error": "No valid pins found"
                })
            else:
                results.append({
                    "symbol": symbol_name,
                    "success": True
                })

        return {"results": results}

    except Exception as e:
        return {"success": False, "error": f"Error parsing file: {str(e)}"}