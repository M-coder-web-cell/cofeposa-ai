from scripts.generate_voice import generate_voice
from utils.s3 import upload

# Use /tmp/ for temporary files (works on macOS and Linux)
TMP_DIR = "/tmp/cofeposa"
TMP_AUDIO = f"{TMP_DIR}/voice.wav"

def voice_node(state):
    os.makedirs(TMP_DIR, exist_ok=True)
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = upload(TMP_AUDIO, "audio")
    return state

