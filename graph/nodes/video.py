from scripts.render_video import render_cinematic_video
from scripts.generate_voice import generate_voice

TMP_AUDIO = "/workspace/tmp/voice.wav"

def video_node(state):
    if "script" not in state or not state["script"]:
        state["script"] = " ".join([shot["prompt"] for shot in state.get("shots", [])])

    # 1️⃣ Generate narration
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = TMP_AUDIO

    # 2️⃣ Render cinematic video
    state = render_cinematic_video(state)
    return state

