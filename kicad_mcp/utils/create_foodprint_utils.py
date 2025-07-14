import os
import logging # Import logging
import subprocess
import sys # Add sys import
from typing import Dict, List, Any
import pathlib
import anthropic
from dotenv import load_dotenv



from kicad_mcp.config import KICAD_USER_DIR, KICAD_APP_PATH, KICAD_EXTENSIONS, ADDITIONAL_SEARCH_PATHS, DATASHEET_PATH



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


def analyze_pdfs(pdf_url: str, prompt: str) -> List[Dict[str, Any]]:
    """
    Analyze a list of PDFs using Claude (Anthropic) via URL-based document references.

    Args:
        pdf_urls: publicly accessible PDF URL.
        prompt: Custom prompt/question to ask Claude about each PDF.

    Returns:
        List of analysis results per PDF (as Claude's structured response).
    """
    client = anthropic.Anthropic()
    results = []

    try:
            message = client.messages.create(
                model="claude-sonnet-4-20250514",  #change to other models
                max_tokens=10000,
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

