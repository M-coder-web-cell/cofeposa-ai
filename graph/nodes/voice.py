from scripts.generate_voice import generate_voice

def voice_node(state):
    VOICE_PATH = "/workspace/outputs/voice.wav"
    generate_voice(state["script"], VOICE_PATH)
    state["voice_path"] = VOICE_PATH
    return state
