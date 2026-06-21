"""
🛠 UTILITY TOOLS - QR Code, ZIP, File operations
"""

import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import zipfile
import os


def generate_qr(text, output_path):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path


def scan_qr(input_path):
    """QR code se text/data nikalta hai. List of decoded strings return karta hai"""
    img = Image.open(input_path)
    decoded_objects = decode(img)
    results = [obj.data.decode("utf-8") for obj in decoded_objects]
    return results


def create_zip(file_paths, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in file_paths:
            zf.write(path, arcname=os.path.basename(path))
    return output_path


def extract_zip(input_path, output_dir):
    extracted_files = []
    with zipfile.ZipFile(input_path, "r") as zf:
        zf.extractall(output_dir)
        for name in zf.namelist():
            full_path = os.path.join(output_dir, name)
            if os.path.isfile(full_path):
                extracted_files.append(full_path)
    return extracted_files


def rename_file(input_path, new_name):
    directory = os.path.dirname(input_path)
    extension = os.path.splitext(input_path)[1]
    if not new_name.endswith(extension):
        new_name = new_name + extension
    new_path = os.path.join(directory, new_name)
    os.rename(input_path, new_path)
    return new_path
