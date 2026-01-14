from scripts.render_video import render_cinematic_video
from scripts.generate_voice import generate_voice

TMP_AUDIO = "/workspace/tmp/voice.wav"

def video_node(state):
    # 🔹 SAFETY CHECK
    if "script" not in state or not state["script"]:
        raise ValueError("state['script'] is required before video_node")

    # 1️⃣ Generate narration
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = TMP_AUDIO

    # 2️⃣ Render cinematic video
    state = render_cinematic_video(state)

    return state

