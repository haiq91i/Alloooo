"""
Helper Functions - file download, save, cleanup, naming
"""

import os
import uuid
import time
from config import DOWNLOADS_DIR, OUTPUTS_DIR, MAX_FILE_SIZE_BYTES


def generate_unique_name(user_id, extension):
    """Har file ka unique naam banata hai - clashes avoid karne ke liye"""
    unique_id = uuid.uuid4().hex[:8]
    timestamp = int(time.time())
    return f"{user_id}_{timestamp}_{unique_id}.{extension}"


def get_download_path(user_id, extension):
    return os.path.join(DOWNLOADS_DIR, generate_unique_name(user_id, extension))


def get_output_path(user_id, extension):
    return os.path.join(OUTPUTS_DIR, generate_unique_name(user_id, extension))


async def download_telegram_file(file_obj, save_path):
    """Telegram file ko local disk par download karta hai"""
    await file_obj.download_to_drive(save_path)
    return save_path


def cleanup_files(*paths):
    """Processing ke baad temp files delete karta hai (storage bachane ke liye)"""
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass


def cleanup_file_list(paths_list):
    """List of files cleanup karta hai"""
    for path in paths_list:
        cleanup_files(path)


def check_file_size(file_size):
    """Check karta hai file size limit ke andar hai ya nahi"""
    return file_size <= MAX_FILE_SIZE_BYTES


def human_readable_size(size_bytes):
    """Bytes ko KB/MB me convert karta hai dikhane ke liye"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"
