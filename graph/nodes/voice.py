from scripts.generate_voice import generate_voice
from utils.s3 import upload

TMP_AUDIO = "/workspace/tmp/voice.wav"

def voice_node(state):
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = upload(TMP_AUDIO, "audio")
    return state
