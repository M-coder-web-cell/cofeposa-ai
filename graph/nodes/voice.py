from scripts.generate_voice import generate_voice

VOICE_PATH = "/workspace/outputs/voice.wav"

def voice_node(state):
    generate_voice(state["script"], VOICE_PATH)
    state["voice_path"] = VOICE_PATH
    return state
