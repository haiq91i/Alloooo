"""
🤖 MAIN BOT FILE
Sab kuch yaha se connect hota hai - commands, buttons, messages
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

from config import BOT_TOKEN
import keyboards as kb
import state_manager as sm
from helpers import (
    get_download_path, get_output_path, download_telegram_file,
    cleanup_files, check_file_size, human_readable_size
)
from handlers import image_tools, pdf_tools, audio_tools, utility_tools

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ============================================================
# 🟢 START / MAIN MENU
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sm.clear_state(user.id)
    text = (
        f"👋 **Namaste {user.first_name}!**\n\n"
        f"🤖 Main tumhara **All-in-One Media Toolbox Bot** hu!\n\n"
        f"✨ Yaha tumhe milega:\n"
        f"🖼 Image Tools\n"
        f"🎵 Audio Tools\n"
        f"🎭 Sticker Tools\n"
        f"📄 PDF Tools\n"
        f"🔄 File Converters\n"
        f"🛠 Utility Tools (QR, ZIP)\n\n"
        f"👇 **Neeche menu se koi bhi feature choose karo:**"
    )
    await update.message.reply_text(text, reply_markup=kb.main_menu(), parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ **HELP - Bot Kaise Use Kare**\n\n"
        "1️⃣ **/start** likho ya **Main Menu** dabao\n"
        "2️⃣ Category choose karo (Image, PDF, Audio etc)\n"
        "3️⃣ Tool choose karo (e.g. Resize, Compress)\n"
        "4️⃣ Bot tumse file/image maangega - usse bhej do\n"
        "5️⃣ Agar extra info chahiye (size, text) to bot puchega\n"
        "6️⃣ Processing ke baad result mil jayega! ✅\n\n"
        "📌 **Important:**\n"
        "• Max file size: **20MB**\n"
        "• **/cancel** se koi bhi running task rok sakte ho\n"
        "• **/menu** se kabhi bhi main menu pe wapas aa sakte ho\n\n"
        "🛠 Koi problem ho to bot ko restart karne ke liye **/start** bhejo"
    )
    await update.message.reply_text(text, reply_markup=kb.back_button(), parse_mode="Markdown")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sm.clear_state(update.effective_user.id)
    await update.message.reply_text(
        "📋 **Main Menu** - Koi feature choose karo:",
        reply_markup=kb.main_menu(), parse_mode="Markdown"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cancelled = sm.cancel_task(user_id)
    sm.clear_state(user_id)
    if cancelled:
        await update.message.reply_text("❌ **Task cancel kar diya gaya!**", parse_mode="Markdown")
    else:
        await update.message.reply_text("ℹ️ Koi active task nahi tha. State clear kar diya.", parse_mode="Markdown")


# ============================================================
# 🔘 BUTTON CLICK HANDLER (callback queries)
# ============================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    # ---------- MAIN MENU NAVIGATION ----------
    if data == "main_menu":
        sm.clear_state(user_id)
        await query.edit_message_text(
            "📋 **Main Menu** - Koi feature choose karo:",
            reply_markup=kb.main_menu(), parse_mode="Markdown"
        )
        return

    if data == "menu_image":
        await query.edit_message_text("🖼 **IMAGE TOOLS**\n\nKoi tool choose karo:", reply_markup=kb.image_menu(), parse_mode="Markdown")
        return

    if data == "menu_audio":
        await query.edit_message_text("🎵 **AUDIO TOOLS**\n\nKoi tool choose karo:", reply_markup=kb.audio_menu(), parse_mode="Markdown")
        return

    if data == "menu_sticker":
        await query.edit_message_text("🎭 **STICKER TOOLS**\n\nKoi tool choose karo:", reply_markup=kb.sticker_menu(), parse_mode="Markdown")
        return

    if data == "menu_pdf":
        await query.edit_message_text("📄 **PDF TOOLS**\n\nKoi tool choose karo:", reply_markup=kb.pdf_menu(), parse_mode="Markdown")
        return

    if data == "menu_converter":
        await query.edit_message_text("🔄 **FILE CONVERTERS**\n\nKoi tool choose karo:", reply_markup=kb.converter_menu(), parse_mode="Markdown")
        return

    if data == "menu_utility":
        await query.edit_message_text("🛠 **UTILITY TOOLS**\n\nKoi tool choose karo:", reply_markup=kb.utility_menu(), parse_mode="Markdown")
        return

    if data == "menu_settings":
        settings = sm.get_settings(user_id)
        text = (
            f"⚙ **SETTINGS**\n\n"
            f"🖼 Default Image Format: **{settings['default_image_format']}**\n"
            f"📊 Default Quality: **{settings['default_quality']}%**\n"
            f"🔔 Notifications: **{'ON' if settings['notify_on_complete'] else 'OFF'}**"
        )
        await query.edit_message_text(text, reply_markup=kb.settings_menu(), parse_mode="Markdown")
        return

    if data == "menu_help":
        text = (
            "❓ **HELP**\n\n"
            "1️⃣ Category choose karo\n"
            "2️⃣ Tool choose karo\n"
            "3️⃣ File bhejo jab bot maange\n"
            "4️⃣ Result milega! ✅\n\n"
            "📌 Max file size: **20MB**\n"
            "📌 **/cancel** se task rok sakte ho"
        )
        await query.edit_message_text(text, reply_markup=kb.back_button(), parse_mode="Markdown")
        return

    if data == "cancel_task":
        sm.cancel_task(user_id)
        sm.clear_state(user_id)
        await query.edit_message_text("❌ **Cancel ho gaya!** /menu se wapas shuru karo.", parse_mode="Markdown")
        return

    # ---------- SETTINGS ACTIONS ----------
    if data == "set_img_format":
        await query.edit_message_text("🖼 Default format choose karo:", reply_markup=kb.format_choice_buttons())
        sm.set_state(user_id, "setting_format")
        return

    if data == "set_quality":
        await query.edit_message_text("📊 Default quality choose karo:", reply_markup=kb.quality_choice_buttons())
        return

    if data == "set_notify":
        settings = sm.get_settings(user_id)
        new_val = not settings["notify_on_complete"]
        sm.update_setting(user_id, "notify_on_complete", new_val)
        await query.edit_message_text(
            f"🔔 Notifications **{'ON' if new_val else 'OFF'}** kar diya!",
            reply_markup=kb.settings_menu(), parse_mode="Markdown"
        )
        return

    if data.startswith("q_"):
        quality = int(data.split("_")[1])
        sm.update_setting(user_id, "default_quality", quality)
        await query.edit_message_text(f"✅ Quality **{quality}%** set ho gaya!", reply_markup=kb.settings_menu(), parse_mode="Markdown")
        return

    if data.startswith("fmt_") and sm.get_state(user_id) == "setting_format":
        fmt = data.split("_")[1]
        sm.update_setting(user_id, "default_image_format", fmt)
        sm.clear_state(user_id)
        await query.edit_message_text(f"✅ Default format **{fmt}** set ho gaya!", reply_markup=kb.settings_menu(), parse_mode="Markdown")
        return

    # ---------- TOOL SELECTION -> SET STATE & ASK FOR FILE ----------
    tool_prompts = {
        "img_to_sticker": ("img_to_sticker", "🎭 **Image → Sticker**\n\n📤 Ek image bhejo (photo ya file dono chalega)"),
        "img_convert_format": ("img_convert_format", "🔁 **Format Convert**\n\n📤 Pehle image bhejo"),
        "img_resize": ("img_resize", "📐 **Resize Image**\n\n📤 Pehle image bhejo, fir size puchunga"),
        "img_crop": ("img_crop", "✂ **Crop Image**\n\n📤 Pehle image bhejo, fir crop area puchunga"),
        "img_rotate": ("img_rotate", "🔄 **Rotate Image**\n\n📤 Pehle image bhejo"),
        "img_compress": ("img_compress", "📉 **Compress Image**\n\n📤 Image bhejo - main compress kar dunga"),
        "img_collage": ("img_collage", "🖇 **Photo Collage**\n\n📤 2 ya zyada images bhejo ek ek karke.\nDone hone par '✅ Done' dabana."),
        "img_add_text": ("img_add_text", "✍ **Add Text on Image**\n\n📤 Pehle image bhejo, fir text puchunga"),
        "img_to_pdf": ("img_to_pdf", "📄 **Image → PDF**\n\n📤 Image bhejo"),
        "img_multi_to_pdf": ("img_multi_to_pdf", "📚 **Multiple Images → PDF**\n\n📤 Saari images bhejo ek ek karke.\nDone hone par '✅ Done' dabana."),
        "sticker_to_img": ("sticker_to_img", "🎭 **Sticker → Image**\n\n📤 Koi sticker bhejo"),
        "sticker_resize": ("sticker_resize", "📐 **Sticker Resize**\n\n📤 Sticker ya image bhejo"),
        "pdf_merge": ("pdf_merge", "🔗 **Merge PDF**\n\n📤 2 ya zyada PDF files bhejo ek ek karke.\nDone hone par '✅ Done' dabana."),
        "pdf_split": ("pdf_split", "✂ **Split PDF**\n\n📤 PDF file bhejo - main har page alag kar dunga"),
        "pdf_compress": ("pdf_compress", "📉 **Compress PDF**\n\n📤 PDF file bhejo"),
        "pdf_to_img": ("pdf_to_img", "📑 **PDF → Images**\n\n📤 PDF file bhejo"),
        "audio_trim": ("audio_trim", "✂ **Trim Audio**\n\n📤 Pehle audio file bhejo, fir start-end time puchunga"),
        "audio_merge": ("audio_merge", "🔗 **Merge Audio**\n\n📤 2 ya zyada audio files bhejo ek ek karke.\nDone hone par '✅ Done' dabana."),
        "audio_speed": ("audio_speed", "⏩ **Speed Changer**\n\n📤 Pehle audio bhejo, fir speed puchunga"),
        "audio_volume": ("audio_volume", "🔊 **Volume Changer**\n\n📤 Pehle audio bhejo, fir kitna badhana/ghatana hai puchunga"),
        "qr_generate": ("qr_generate", "📱 **QR Code Generator**\n\n✍ Wo text/link likho jiska QR banana hai:"),
        "qr_scan": ("qr_scan", "📷 **QR Code Scanner**\n\n📤 QR code wali image bhejo"),
        "zip_create": ("zip_create", "🗜 **ZIP Create**\n\n📤 Files bhejo ek ek karke jo ZIP me daalni hai.\nDone hone par '✅ Done' dabana."),
        "zip_extract": ("zip_extract", "📦 **ZIP Extract**\n\n📤 ZIP file bhejo"),
        "file_rename": ("file_rename", "✏ **File Renamer**\n\n📤 Pehle file bhejo, fir naya naam puchunga"),
    }

    if data in tool_prompts:
        state, prompt = tool_prompts[data]
        sm.clear_state(user_id)
        sm.set_state(user_id, state)
        await query.edit_message_text(prompt, reply_markup=kb.cancel_button(), parse_mode="Markdown")
        return

    # ---------- ROTATE ANGLE SELECTION ----------
    if data.startswith("rot_"):
        angle = int(data.split("_")[1])
        await process_rotate(query, context, user_id, angle)
        return

    # ---------- FORMAT SELECTION FOR CONVERT ----------
    if data.startswith("fmt_") and sm.get_state(user_id) == "img_convert_format_waiting":
        fmt = data.split("_")[1]
        await process_format_convert(query, context, user_id, fmt)
        return

    # ---------- DONE BUTTON (multi-file collection) ----------
    if data.startswith("done_"):
        action = data.replace("done_", "")
        await process_multi_file_action(query, context, user_id, action)
        return


# ============================================================
# 📥 FILE / PHOTO / DOCUMENT RECEIVE HANDLER
# ============================================================
async def file_receive_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = sm.get_state(user_id)

    if not state:
        await update.message.reply_text(
            "ℹ️ Pehle koi tool choose karo **/menu** se!", parse_mode="Markdown"
        )
        return

    # File object nikalo (photo, document, audio, sticker - jo bhi ho)
    file_obj = None
    file_ext = "jpg"

    if update.message.photo:
        file_obj = await update.message.photo[-1].get_file()
        file_ext = "jpg"
    elif update.message.document:
        doc = update.message.document
        if doc.file_size and not check_file_size(doc.file_size):
            await update.message.reply_text(f"❌ File bahut badi hai! Max **20MB** allowed.\nTumhari file: {human_readable_size(doc.file_size)}", parse_mode="Markdown")
            return
        file_obj = await doc.get_file()
        file_ext = doc.file_name.split(".")[-1] if "." in doc.file_name else "bin"
    elif update.message.audio:
        file_obj = await update.message.audio.get_file()
        file_ext = "mp3"
    elif update.message.voice:
        file_obj = await update.message.voice.get_file()
        file_ext = "ogg"
    elif update.message.sticker:
        file_obj = await update.message.sticker.get_file()
        file_ext = "webp"

    if not file_obj:
        await update.message.reply_text("⚠️ Ye file type support nahi hai. Image/PDF/Audio/Sticker bhejo.")
        return

    download_path = get_download_path(user_id, file_ext)
    await download_telegram_file(file_obj, download_path)

    # ---------- MULTI-FILE COLLECTION STATES ----------
    multi_file_states = {
        "img_collage": "collage_files",
        "img_multi_to_pdf": "multi_pdf_files",
        "pdf_merge": "merge_pdf_files",
        "audio_merge": "merge_audio_files",
        "zip_create": "zip_files",
    }

    if state in multi_file_states:
        key = multi_file_states[state]
        sm.append_data_list(user_id, key, download_path)
        count = len(sm.get_data(user_id, key, []))
        await update.message.reply_text(
            f"✅ File #{count} mil gayi!\n\n📤 Aur file bhejo, ya **✅ Done** dabao jab ho jaye.",
            reply_markup=kb.done_collecting_button(state)
        )
        return

    # ---------- SINGLE FILE -> IMMEDIATE PROCESSING TOOLS ----------
    if state == "img_to_sticker":
        await run_simple_image_task(update, context, user_id, download_path, "sticker", "🎭 Sticker bana raha hu...")
        return

    if state == "img_compress":
        await run_simple_image_task(update, context, user_id, download_path, "compress", "📉 Compress kar raha hu...")
        return

    if state == "img_to_pdf":
        await run_simple_image_task(update, context, user_id, download_path, "topdf", "📄 PDF bana raha hu...")
        return

    if state == "sticker_to_img":
        await run_simple_image_task(update, context, user_id, download_path, "stickertoimg", "🖼 Image bana raha hu...")
        return

    if state == "sticker_resize":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "sticker_resize_waiting_size")
        await update.message.reply_text("📐 Size batao (e.g. `300x300`):", parse_mode="Markdown")
        return

    # ---------- TOOLS NEEDING EXTRA INPUT ----------
    if state == "img_resize":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "img_resize_waiting_size")
        await update.message.reply_text("📐 Naya size batao is format me: `width x height`\nExample: `800x600`", parse_mode="Markdown")
        return

    if state == "img_crop":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "img_crop_waiting_coords")
        await update.message.reply_text("✂ Crop area batao: `left,top,right,bottom`\nExample: `0,0,500,500`", parse_mode="Markdown")
        return

    if state == "img_rotate":
        sm.set_data(user_id, "input_path", download_path)
        await update.message.reply_text("🔄 Kitna rotate karna hai?", reply_markup=kb.rotate_choice_buttons())
        return

    if state == "img_add_text":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "img_add_text_waiting_text")
        await update.message.reply_text("✍ Image pe kya text likhna hai?")
        return

    if state == "img_convert_format":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "img_convert_format_waiting")
        await update.message.reply_text("🔁 Kis format me convert karna hai?", reply_markup=kb.format_choice_buttons())
        return

    if state == "pdf_split":
        await run_pdf_split(update, context, user_id, download_path)
        return

    if state == "pdf_compress":
        await run_simple_pdf_task(update, context, user_id, download_path, "compress", "📉 PDF compress kar raha hu...")
        return

    if state == "pdf_to_img":
        await run_pdf_to_images(update, context, user_id, download_path)
        return

    if state == "audio_trim":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "audio_trim_waiting_time")
        await update.message.reply_text("✂ Start aur end time batao seconds me: `start,end`\nExample: `10,30` (10s se 30s tak)")
        return

    if state == "audio_speed":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "audio_speed_waiting_factor")
        await update.message.reply_text("⏩ Speed factor batao:\n`2` = 2x fast\n`0.5` = half speed")
        return

    if state == "audio_volume":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "audio_volume_waiting_db")
        await update.message.reply_text("🔊 Kitna change karna hai dB me?\n`+10` = badhao\n`-10` = ghatao")
        return

    if state == "qr_scan":
        await run_qr_scan(update, context, user_id, download_path)
        return

    if state == "zip_extract":
        await run_zip_extract(update, context, user_id, download_path)
        return

    if state == "file_rename":
        sm.set_data(user_id, "input_path", download_path)
        sm.set_state(user_id, "file_rename_waiting_name")
        await update.message.reply_text("✏ Naya naam batao (bina extension ke):")
        return


# ============================================================
# 💬 TEXT MESSAGE HANDLER (extra inputs jaise size, text, time)
# ============================================================
async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = sm.get_state(user_id)
    text = update.message.text.strip()

    if not state:
        return  # normal text, koi tool active nahi hai

    if state == "qr_generate":
        await run_qr_generate(update, context, user_id, text)
        return

    if state == "img_resize_waiting_size":
        try:
            width, height = map(int, text.lower().replace(" ", "").split("x"))
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "png")
            msg = await update.message.reply_text("📐 Resize kar raha hu...")
            image_tools.resize_image(input_path, output_path, width, height)
            await send_result_file(update, context, output_path, "✅ Resize done!")
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat format! `width x height` jaise: `800x600`")
        return

    if state == "img_crop_waiting_coords":
        try:
            left, top, right, bottom = map(int, text.replace(" ", "").split(","))
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "png")
            await update.message.reply_text("✂ Crop kar raha hu...")
            image_tools.crop_image(input_path, output_path, left, top, right, bottom)
            await send_result_file(update, context, output_path, "✅ Crop done!")
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat format! `left,top,right,bottom` jaise: `0,0,500,500`")
        return

    if state == "img_add_text_waiting_text":
        input_path = sm.get_data(user_id, "input_path")
        output_path = get_output_path(user_id, "png")
        await update.message.reply_text("✍ Text add kar raha hu...")
        image_tools.add_text_on_image(input_path, output_path, text)
        await send_result_file(update, context, output_path, "✅ Text add ho gaya!")
        cleanup_files(input_path, output_path)
        sm.clear_state(user_id)
        return

    if state == "sticker_resize_waiting_size":
        try:
            width, height = map(int, text.lower().replace(" ", "").split("x"))
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "png")
            await update.message.reply_text("📐 Resize kar raha hu...")
            image_tools.resize_image(input_path, output_path, width, height)
            await send_result_file(update, context, output_path, "✅ Sticker resize done!")
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat format! `width x height` jaise: `300x300`")
        return

    if state == "audio_trim_waiting_time":
        try:
            start, end = map(float, text.replace(" ", "").split(","))
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "mp3")
            await update.message.reply_text("✂ Trim kar raha hu...")
            audio_tools.trim_audio(input_path, output_path, start, end)
            await send_result_file(update, context, output_path, "✅ Trim done!", as_audio=True)
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat format! `start,end` jaise: `10,30`")
        return

    if state == "audio_speed_waiting_factor":
        try:
            factor = float(text)
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "mp3")
            await update.message.reply_text("⏩ Speed change kar raha hu...")
            audio_tools.change_speed(input_path, output_path, factor)
            await send_result_file(update, context, output_path, "✅ Speed change done!", as_audio=True)
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat number! Example: `1.5` ya `0.5`")
        return

    if state == "audio_volume_waiting_db":
        try:
            db = float(text)
            input_path = sm.get_data(user_id, "input_path")
            output_path = get_output_path(user_id, "mp3")
            await update.message.reply_text("🔊 Volume change kar raha hu...")
            audio_tools.change_volume(input_path, output_path, db)
            await send_result_file(update, context, output_path, "✅ Volume change done!", as_audio=True)
            cleanup_files(input_path, output_path)
            sm.clear_state(user_id)
        except Exception:
            await update.message.reply_text("⚠️ Galat number! Example: `+10` ya `-10`")
        return

    if state == "file_rename_waiting_name":
        from handlers.utility_tools import rename_file
        input_path = sm.get_data(user_id, "input_path")
        try:
            new_path = rename_file(input_path, text)
            await send_result_file(update, context, new_path, f"✅ Naam change ho gaya: **{os.path.basename(new_path)}**", as_document=True)
            cleanup_files(new_path)
            sm.clear_state(user_id)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")
        return


# ============================================================
# 🔧 PROCESSING FUNCTIONS
# ============================================================
async def run_simple_image_task(update, context, user_id, input_path, task_type, processing_msg):
    msg = await update.message.reply_text(processing_msg)
    try:
        if task_type == "sticker":
            output_path = get_output_path(user_id, "webp")
            image_tools.image_to_sticker(input_path, output_path)
            await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=open(output_path, "rb"))
            await update.message.reply_text("✅ **Sticker ready!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")

        elif task_type == "compress":
            settings = sm.get_settings(user_id)
            output_path = get_output_path(user_id, "jpg")
            image_tools.compress_image(input_path, output_path, settings["default_quality"])
            orig_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            await context.bot.send_document(
                chat_id=update.effective_chat.id, document=open(output_path, "rb"),
                caption=f"✅ **Compressed!**\n📊 {human_readable_size(orig_size)} → {human_readable_size(new_size)}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("Aur kuch?", reply_markup=kb.quick_menu_bar())

        elif task_type == "topdf":
            output_path = get_output_path(user_id, "pdf")
            pdf_tools.images_to_pdf([input_path], output_path)
            await context.bot.send_document(chat_id=update.effective_chat.id, document=open(output_path, "rb"))
            await update.message.reply_text("✅ **PDF ready!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")

        elif task_type == "stickertoimg":
            output_path = get_output_path(user_id, "png")
            image_tools.convert_format(input_path, output_path, "PNG")
            await context.bot.send_document(chat_id=update.effective_chat.id, document=open(output_path, "rb"))
            await update.message.reply_text("✅ **Image ready!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")

        cleanup_files(input_path, output_path)
    except Exception as e:
        logger.error(f"Error in {task_type}: {e}")
        await update.message.reply_text(f"❌ Error aaya: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def process_rotate(query, context, user_id, angle):
    input_path = sm.get_data(user_id, "input_path")
    if not input_path:
        await query.edit_message_text("⚠️ Pehle image bhejo!")
        return
    await query.edit_message_text(f"🔄 {angle}° rotate kar raha hu...")
    output_path = get_output_path(user_id, "png")
    image_tools.rotate_image(input_path, output_path, angle)
    await context.bot.send_document(chat_id=query.message.chat_id, document=open(output_path, "rb"))
    await context.bot.send_message(chat_id=query.message.chat_id, text="✅ **Rotate done!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
    cleanup_files(input_path, output_path)
    sm.clear_state(user_id)


async def process_format_convert(query, context, user_id, fmt):
    input_path = sm.get_data(user_id, "input_path")
    if not input_path:
        await query.edit_message_text("⚠️ Pehle image bhejo!")
        return
    await query.edit_message_text(f"🔁 {fmt} me convert kar raha hu...")
    ext = fmt.lower() if fmt != "JPEG" else "jpg"
    output_path = get_output_path(user_id, ext)
    image_tools.convert_format(input_path, output_path, fmt)
    await context.bot.send_document(chat_id=query.message.chat_id, document=open(output_path, "rb"))
    await context.bot.send_message(chat_id=query.message.chat_id, text="✅ **Convert done!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
    cleanup_files(input_path, output_path)
    sm.clear_state(user_id)


async def process_multi_file_action(query, context, user_id, action):
    multi_file_states = {
        "img_collage": "collage_files",
        "img_multi_to_pdf": "multi_pdf_files",
        "pdf_merge": "merge_pdf_files",
        "audio_merge": "merge_audio_files",
        "zip_create": "zip_files",
    }
    key = multi_file_states.get(action)
    files = sm.get_data(user_id, key, [])

    if len(files) < 2:
        await query.edit_message_text(f"⚠️ Kam se kam 2 files chahiye! Abhi sirf {len(files)} hai.")
        return

    await query.edit_message_text("⚙️ Processing ho rahi hai...")
    chat_id = query.message.chat_id

    try:
        if action == "img_collage":
            output_path = get_output_path(user_id, "jpg")
            image_tools.create_collage(files, output_path)
            await context.bot.send_document(chat_id=chat_id, document=open(output_path, "rb"))
            cleanup_files(output_path)

        elif action == "img_multi_to_pdf":
            output_path = get_output_path(user_id, "pdf")
            pdf_tools.images_to_pdf(files, output_path)
            await context.bot.send_document(chat_id=chat_id, document=open(output_path, "rb"))
            cleanup_files(output_path)

        elif action == "pdf_merge":
            output_path = get_output_path(user_id, "pdf")
            pdf_tools.merge_pdfs(files, output_path)
            await context.bot.send_document(chat_id=chat_id, document=open(output_path, "rb"))
            cleanup_files(output_path)

        elif action == "audio_merge":
            output_path = get_output_path(user_id, "mp3")
            audio_tools.merge_audios(files, output_path)
            await context.bot.send_audio(chat_id=chat_id, audio=open(output_path, "rb"))
            cleanup_files(output_path)

        elif action == "zip_create":
            output_path = get_output_path(user_id, "zip")
            utility_tools.create_zip(files, output_path)
            await context.bot.send_document(chat_id=chat_id, document=open(output_path, "rb"))
            cleanup_files(output_path)

        await context.bot.send_message(chat_id=chat_id, text="✅ **Done!**", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
        cleanup_files(*files)
    except Exception as e:
        logger.error(f"Error in {action}: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)


async def run_simple_pdf_task(update, context, user_id, input_path, task_type, processing_msg):
    msg = await update.message.reply_text(processing_msg)
    try:
        if task_type == "compress":
            output_path = get_output_path(user_id, "pdf")
            pdf_tools.compress_pdf(input_path, output_path)
            orig_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            await context.bot.send_document(
                chat_id=update.effective_chat.id, document=open(output_path, "rb"),
                caption=f"✅ **Compressed!**\n📊 {human_readable_size(orig_size)} → {human_readable_size(new_size)}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("Aur kuch?", reply_markup=kb.quick_menu_bar())
            cleanup_files(input_path, output_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def run_pdf_split(update, context, user_id, input_path):
    msg = await update.message.reply_text("✂ Split kar raha hu...")
    try:
        from config import OUTPUTS_DIR
        output_paths = pdf_tools.split_pdf(input_path, OUTPUTS_DIR, user_id)
        for path in output_paths[:20]:  # max 20 pages bhejega ek baar me (spam avoid)
            await context.bot.send_document(chat_id=update.effective_chat.id, document=open(path, "rb"))
        await update.message.reply_text(f"✅ **{len(output_paths)} pages** alag kar diye!", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
        cleanup_files(input_path, *output_paths)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def run_pdf_to_images(update, context, user_id, input_path):
    msg = await update.message.reply_text("📑 Images bana raha hu...")
    try:
        from config import OUTPUTS_DIR
        output_paths = pdf_tools.pdf_to_images(input_path, OUTPUTS_DIR, user_id)
        for path in output_paths[:20]:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path, "rb"))
        await update.message.reply_text(f"✅ **{len(output_paths)} images** bana di!", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
        cleanup_files(input_path, *output_paths)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def run_qr_generate(update, context, user_id, text):
    msg = await update.message.reply_text("📱 QR code bana raha hu...")
    try:
        output_path = get_output_path(user_id, "png")
        utility_tools.generate_qr(text, output_path)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(output_path, "rb"), caption="✅ **QR Code ready!**", parse_mode="Markdown")
        await update.message.reply_text("Aur kuch?", reply_markup=kb.quick_menu_bar())
        cleanup_files(output_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def run_qr_scan(update, context, user_id, input_path):
    msg = await update.message.reply_text("📷 QR scan kar raha hu...")
    try:
        results = utility_tools.scan_qr(input_path)
        if results:
            text = "✅ **QR Code mil gaya!**\n\n" + "\n\n".join([f"`{r}`" for r in results])
        else:
            text = "⚠️ Koi QR code nahi mila is image me."
        await update.message.reply_text(text, reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
        cleanup_files(input_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def run_zip_extract(update, context, user_id, input_path):
    msg = await update.message.reply_text("📦 Extract kar raha hu...")
    try:
        from config import OUTPUTS_DIR
        extracted = utility_tools.extract_zip(input_path, OUTPUTS_DIR)
        for path in extracted[:20]:
            try:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=open(path, "rb"))
            except Exception:
                pass
        await update.message.reply_text(f"✅ **{len(extracted)} files** extract ho gaye!", reply_markup=kb.quick_menu_bar(), parse_mode="Markdown")
        cleanup_files(input_path, *extracted)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        sm.clear_state(user_id)
        await msg.delete()


async def send_result_file(update, context, output_path, caption, as_audio=False, as_document=True):
    if as_audio:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(output_path, "rb"), caption=caption, parse_mode="Markdown")
    else:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(output_path, "rb"), caption=caption, parse_mode="Markdown")
    await update.message.reply_text("Aur kuch chahiye?", reply_markup=kb.quick_menu_bar())


# ============================================================
# 🚀 MAIN - BOT START
# ============================================================
def main():
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN nahi mila! .env file me ya Railway variables me BOT_TOKEN set karo.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Files (photo, document, audio, voice, sticker)
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.Document.ALL | filters.AUDIO | filters.VOICE | filters.Sticker.ALL,
        file_receive_handler
    ))

    # Text messages (extra inputs)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))

    print("🤖 Bot chalu ho gaya hai! Polling shuru...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
