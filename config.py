import os
from dotenv import load_dotenv

load_dotenv()

# ===== BOT TOKEN =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ===== FILE SIZE LIMITS (Railway Free Tier ke liye safe limits) =====
MAX_FILE_SIZE_MB = 20  # Telegram bot API ka bhi 20MB download limit hai
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# ===== FOLDERS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
DOWNLOADS_DIR = os.path.join(TEMP_DIR, "downloads")
OUTPUTS_DIR = os.path.join(TEMP_DIR, "outputs")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# ===== QUEUE SETTINGS =====
MAX_CONCURRENT_TASKS = 2  # ek time pe sirf 2 task process honge (RAM bachane ke liye)

# ===== SUPPORTED FORMATS =====
IMAGE_FORMATS = ["PNG", "JPEG", "WEBP"]
AUDIO_FORMATS = ["mp3", "wav", "ogg", "m4a"]
