from scripts.render_video import render_cinematic_video
from scripts.generate_voice import generate_voice
from scripts.generate_image import render_single_shot

TMP_AUDIO = "/workspace/tmp/voice.wav"

def video_node(state):
    # 1️⃣ Generate narration
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = TMP_AUDIO

    # 2️⃣ Generate images per shot
    state = image_node(state)

    # 3️⃣ Render final cinematic video
    state = render_single_shot(state)

    return state
