"""
🖼 IMAGE TOOLS - Saare image processing functions
"""

from PIL import Image, ImageDraw, ImageFont
import os


def resize_image(input_path, output_path, width, height):
    img = Image.open(input_path)
    img = img.resize((width, height), Image.LANCZOS)
    img.save(output_path)
    return output_path


def crop_image(input_path, output_path, left, top, right, bottom):
    img = Image.open(input_path)
    img = img.crop((left, top, right, bottom))
    img.save(output_path)
    return output_path


def rotate_image(input_path, output_path, angle):
    img = Image.open(input_path)
    img = img.rotate(-angle, expand=True)
    img.save(output_path)
    return output_path


def compress_image(input_path, output_path, quality=50):
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=quality, optimize=True)
    return output_path


def convert_format(input_path, output_path, target_format):
    img = Image.open(input_path)
    if target_format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, target_format.upper())
    return output_path


def add_text_on_image(input_path, output_path, text, position="bottom"):
    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Font size image size ke hisaab se adjust
    font_size = max(20, width // 15)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if position == "bottom":
        x, y = (width - text_w) / 2, height - text_h - 30
    elif position == "top":
        x, y = (width - text_w) / 2, 20
    else:
        x, y = (width - text_w) / 2, (height - text_h) / 2

    # Outline effect (kala border safed text - readability ke liye)
    outline_range = 2
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            draw.text((x + dx, y + dy), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill="white")

    img.save(output_path)
    return output_path


def create_collage(image_paths, output_path, columns=2):
    images = [Image.open(p).convert("RGB") for p in image_paths]

    # Sab images ko same size karo (smallest ke hisaab se)
    thumb_size = (400, 400)
    images = [img.resize(thumb_size) for img in images]

    rows = (len(images) + columns - 1) // columns
    collage_w = columns * thumb_size[0]
    collage_h = rows * thumb_size[1]

    collage = Image.new("RGB", (collage_w, collage_h), "white")
    for idx, img in enumerate(images):
        x = (idx % columns) * thumb_size[0]
        y = (idx // columns) * thumb_size[1]
        collage.paste(img, (x, y))

    collage.save(output_path)
    return output_path


def image_to_sticker(input_path, output_path):
    """Telegram sticker requirement: 512x512, ek side fix, WebP format"""
    img = Image.open(input_path).convert("RGBA")
    img.thumbnail((512, 512), Image.LANCZOS)

    # Canvas 512x512 banao aur center me paste karo (transparent background)
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    offset = ((512 - img.width) // 2, (512 - img.height) // 2)
    canvas.paste(img, offset, img)

    canvas.save(output_path, "WEBP")
    return output_path
