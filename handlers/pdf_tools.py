"""
📄 PDF TOOLS - Saare PDF processing functions
"""

from PyPDF2 import PdfReader, PdfWriter
import img2pdf
from pdf2image import convert_from_path
import os


def merge_pdfs(pdf_paths, output_path):
    writer = PdfWriter()
    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


def split_pdf(input_path, output_dir, user_id):
    """Har page ko alag PDF file banata hai, list of paths return karta hai"""
    reader = PdfReader(input_path)
    output_paths = []
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = os.path.join(output_dir, f"{user_id}_page_{i+1}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        output_paths.append(out_path)
    return output_paths


def compress_pdf(input_path, output_path):
    """PyPDF2 se basic compression - images recompress nahi karta, sirf structure optimize karta hai"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


def images_to_pdf(image_paths, output_path):
    """Single ya multiple images ko ek PDF me convert karta hai"""
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    return output_path


def pdf_to_images(input_path, output_dir, user_id):
    """PDF ke har page ko image me convert karta hai"""
    pages = convert_from_path(input_path, dpi=150)
    output_paths = []
    for i, page in enumerate(pages):
        out_path = os.path.join(output_dir, f"{user_id}_page_{i+1}.png")
        page.save(out_path, "PNG")
        output_paths.append(out_path)
    return output_paths


def get_pdf_page_count(input_path):
    reader = PdfReader(input_path)
    return len(reader.pages)
