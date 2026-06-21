"""
User State Manager
- Har user ka current mode track karta hai (jaise "waiting_for_image_resize")
- Queue system handle karta hai
- User settings store karta hai
"""

import asyncio
import time

# user_id -> current action/mode (e.g. "img_resize", "pdf_merge" etc)
user_state = {}

# user_id -> extra data needed for multi-step actions (e.g. list of files for merge)
user_data = {}

# user_id -> user settings (default format, quality etc)
user_settings = {}

# Global semaphore - ek time pe MAX_CONCURRENT_TASKS hi process honge
from config import MAX_CONCURRENT_TASKS
task_semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

# Active tasks tracker - cancel karne ke liye
active_tasks = {}  # user_id -> asyncio.Task object


def set_state(user_id, state):
    user_state[user_id] = state


def get_state(user_id):
    return user_state.get(user_id, None)


def clear_state(user_id):
    user_state.pop(user_id, None)
    user_data.pop(user_id, None)


def set_data(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value


def get_data(user_id, key, default=None):
    return user_data.get(user_id, {}).get(key, default)


def append_data_list(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}
    if key not in user_data[user_id]:
        user_data[user_id][key] = []
    user_data[user_id][key].append(value)


def get_settings(user_id):
    if user_id not in user_settings:
        user_settings[user_id] = {
            "default_image_format": "PNG",
            "default_quality": 85,
            "notify_on_complete": True,
        }
    return user_settings[user_id]


def update_setting(user_id, key, value):
    settings = get_settings(user_id)
    settings[key] = value
    user_settings[user_id] = settings


def register_task(user_id, task):
    active_tasks[user_id] = {"task": task, "started_at": time.time()}


def unregister_task(user_id):
    active_tasks.pop(user_id, None)


def is_task_running(user_id):
    return user_id in active_tasks


def cancel_task(user_id):
    info = active_tasks.get(user_id)
    if info:
        info["task"].cancel()
        unregister_task(user_id)
        return True
    return False
