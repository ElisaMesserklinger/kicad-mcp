import os
from pypdf import PdfReader, PdfWriter

from kicad_mcp.utils.create_foodprint_symbol_utils import *
"""
def split_pdf(input_pdf_path, output_dir, pages_per_split):
    # Load the PDF
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Split into chunks
    for start_page in range(0, total_pages, pages_per_split):
        writer = PdfWriter()
        end_page = min(start_page + pages_per_split, total_pages)

        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])

        output_path = os.path.join(output_dir, f"split_{start_page + 1}_to_{end_page}.pdf")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"Saved: {output_path}")

# Example usage
input_pdf = "c:/Users/messeel/KiCadProjects/datasheets/SAM-E70-S70-V70-V71-Family-Data-Sheet-DS60001527.pdf"           # Replace with your input PDF path
output_folder = "c:/Users/messeel/KiCadProjects/datasheets/split_files"     # Folder to save split files
pages_per_file = 500                 # Split every 10 pages

split_pdf(input_pdf, output_folder, pages_per_file)
"""


# Example usage
input_pdf = "c:/Users/messeel/KiCadProjects/datasheets/SAM-E70-S70-V70-V71-Family-Data-Sheet-DS60001527.pdf"           # Replace with your input PDF path
output_folder = "split_files"     # Folder to save split files
pages_per_file = 500                 # Split every 10 pages
dir_name = "SAM-E70-S70-V70-V71"

split_pdf(input_pdf, output_folder, pages_per_file, dir_name)



