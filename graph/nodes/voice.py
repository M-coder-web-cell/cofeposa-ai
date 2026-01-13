from scripts.generate_voice import generate_voice
from utils.s3 import upload

def voice_node(state):
    local_path = "/tmp/voice.wav"
    generate_voice(state["script"], local_path)
    state["voice_path"] = upload(local_path, "audio")
    return state
