"""
🎵 AUDIO TOOLS - Lightweight audio processing (pydub use karke)
NOTE: Ye FFmpeg use karta hai jo Railway pe nixpacks.toml se install hota hai
"""

from pydub import AudioSegment


def trim_audio(input_path, output_path, start_sec, end_sec):
    audio = AudioSegment.from_file(input_path)
    trimmed = audio[start_sec * 1000:end_sec * 1000]
    trimmed.export(output_path, format="mp3")
    return output_path


def merge_audios(audio_paths, output_path):
    combined = AudioSegment.empty()
    for path in audio_paths:
        audio = AudioSegment.from_file(path)
        combined += audio
    combined.export(output_path, format="mp3")
    return output_path


def change_speed(input_path, output_path, speed_factor):
    """speed_factor: 1.5 = 1.5x fast, 0.5 = half speed"""
    audio = AudioSegment.from_file(input_path)
    new_frame_rate = int(audio.frame_rate * speed_factor)
    fast_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})
    fast_audio = fast_audio.set_frame_rate(audio.frame_rate)
    fast_audio.export(output_path, format="mp3")
    return output_path


def change_volume(input_path, output_path, db_change):
    """db_change: positive = increase, negative = decrease (e.g. +10, -10)"""
    audio = AudioSegment.from_file(input_path)
    new_audio = audio + db_change
    new_audio.export(output_path, format="mp3")
    return output_path


def get_audio_duration(input_path):
    audio = AudioSegment.from_file(input_path)
    return len(audio) / 1000  # seconds me
