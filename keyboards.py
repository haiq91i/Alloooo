"""
Saare Inline Keyboards (Buttons) yaha define hai
Telegram me "Menu Bar" jaisa har jagah quick-access button milega
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ============ MAIN MENU ============
def main_menu():
    buttons = [
        [InlineKeyboardButton("🖼 Image Tools", callback_data="menu_image"),
         InlineKeyboardButton("🎵 Audio Tools", callback_data="menu_audio")],
        [InlineKeyboardButton("🎭 Sticker Tools", callback_data="menu_sticker"),
         InlineKeyboardButton("📄 PDF Tools", callback_data="menu_pdf")],
        [InlineKeyboardButton("🔄 Converters", callback_data="menu_converter"),
         InlineKeyboardButton("🛠 Utilities", callback_data="menu_utility")],
        [InlineKeyboardButton("⚙ Settings", callback_data="menu_settings"),
         InlineKeyboardButton("❓ Help", callback_data="menu_help")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ QUICK MENU BAR (chhota - image ke sath bhejne ke liye) ============
def quick_menu_bar():
    """Ye wahi menu hai jo file/image bhejne ke baad uske sath dikhega"""
    buttons = [
        [InlineKeyboardButton("🖼 Image", callback_data="menu_image"),
         InlineKeyboardButton("🎵 Audio", callback_data="menu_audio"),
         InlineKeyboardButton("🎭 Sticker", callback_data="menu_sticker")],
        [InlineKeyboardButton("📄 PDF", callback_data="menu_pdf"),
         InlineKeyboardButton("🔄 Convert", callback_data="menu_converter"),
         InlineKeyboardButton("🛠 Utility", callback_data="menu_utility")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ BACK BUTTON (har sub-menu me hoga) ============
def back_button(target="main_menu"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", callback_data=target)]
    ])


# ============ IMAGE TOOLS MENU ============
def image_menu():
    buttons = [
        [InlineKeyboardButton("🎭 Image → Sticker", callback_data="img_to_sticker")],
        [InlineKeyboardButton("🔁 Image → PNG/JPG/WebP", callback_data="img_convert_format")],
        [InlineKeyboardButton("📐 Resize", callback_data="img_resize"),
         InlineKeyboardButton("✂ Crop", callback_data="img_crop")],
        [InlineKeyboardButton("🔄 Rotate", callback_data="img_rotate"),
         InlineKeyboardButton("📉 Compress", callback_data="img_compress")],
        [InlineKeyboardButton("🖇 Photo Collage", callback_data="img_collage")],
        [InlineKeyboardButton("✍ Add Text", callback_data="img_add_text")],
        [InlineKeyboardButton("📄 Image → PDF", callback_data="img_to_pdf")],
        [InlineKeyboardButton("📚 Multiple Images → PDF", callback_data="img_multi_to_pdf")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ AUDIO TOOLS MENU ============
def audio_menu():
    buttons = [
        [InlineKeyboardButton("✂ Trim Audio", callback_data="audio_trim")],
        [InlineKeyboardButton("🔗 Merge Audio Files", callback_data="audio_merge")],
        [InlineKeyboardButton("⏩ Speed Changer", callback_data="audio_speed")],
        [InlineKeyboardButton("🔊 Volume Up/Down", callback_data="audio_volume")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ STICKER TOOLS MENU ============
def sticker_menu():
    buttons = [
        [InlineKeyboardButton("🖼 Image → Sticker", callback_data="img_to_sticker")],
        [InlineKeyboardButton("🎭 Sticker → Image", callback_data="sticker_to_img")],
        [InlineKeyboardButton("📐 Sticker Resize", callback_data="sticker_resize")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ PDF TOOLS MENU ============
def pdf_menu():
    buttons = [
        [InlineKeyboardButton("🔗 Merge PDF", callback_data="pdf_merge")],
        [InlineKeyboardButton("✂ Split PDF", callback_data="pdf_split")],
        [InlineKeyboardButton("📉 Compress PDF", callback_data="pdf_compress")],
        [InlineKeyboardButton("🖼 Image → PDF", callback_data="img_to_pdf")],
        [InlineKeyboardButton("📑 PDF → Images", callback_data="pdf_to_img")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ CONVERTER MENU ============
def converter_menu():
    buttons = [
        [InlineKeyboardButton("🖼 JPG ↔ PNG ↔ WebP", callback_data="img_convert_format")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ UTILITY TOOLS MENU ============
def utility_menu():
    buttons = [
        [InlineKeyboardButton("📱 QR Code Generator", callback_data="qr_generate")],
        [InlineKeyboardButton("📷 QR Code Scanner", callback_data="qr_scan")],
        [InlineKeyboardButton("🗜 ZIP Create", callback_data="zip_create")],
        [InlineKeyboardButton("📦 ZIP Extract", callback_data="zip_extract")],
        [InlineKeyboardButton("✏ File Renamer", callback_data="file_rename")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ SETTINGS MENU ============
def settings_menu():
    buttons = [
        [InlineKeyboardButton("🖼 Default Image Format", callback_data="set_img_format")],
        [InlineKeyboardButton("📊 Default Quality", callback_data="set_quality")],
        [InlineKeyboardButton("🔔 Notifications Toggle", callback_data="set_notify")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(buttons)


# ============ CANCEL BUTTON (processing ke time) ============
def cancel_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel Task", callback_data="cancel_task")]
    ])


# ============ DONE BUTTON (multi-file collection - merge/collage ke liye) ============
def done_collecting_button(action_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Done - Process Now", callback_data=f"done_{action_key}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_task")]
    ])


# ============ IMAGE FORMAT CHOICE ============
def format_choice_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("PNG", callback_data="fmt_PNG"),
         InlineKeyboardButton("JPG", callback_data="fmt_JPEG"),
         InlineKeyboardButton("WebP", callback_data="fmt_WEBP")]
    ])


# ============ ROTATE ANGLE CHOICE ============
def rotate_choice_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("90°", callback_data="rot_90"),
         InlineKeyboardButton("180°", callback_data="rot_180"),
         InlineKeyboardButton("270°", callback_data="rot_270")]
    ])


# ============ QUALITY CHOICE (for settings) ============
def quality_choice_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Low (50%)", callback_data="q_50"),
         InlineKeyboardButton("Medium (75%)", callback_data="q_75")],
        [InlineKeyboardButton("High (90%)", callback_data="q_90"),
         InlineKeyboardButton("Max (100%)", callback_data="q_100")]
    ])
