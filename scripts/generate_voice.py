from TTS.api import TTS
from prompts.prompt import get_prompt

MODEL_NAME = "coqui/XTTS-v2"
CACHE_DIR = "/workspace/cache"

tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=True, cache_path=CACHE_DIR)

def generate_voice(text, output_path):
    tts.tts_to_file(text=text, file_path=output_path)
    print(f"🔊 Voice saved → {output_path}")
