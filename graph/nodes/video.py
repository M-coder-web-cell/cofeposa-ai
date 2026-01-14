from scripts.render_video import render_cinematic_video
from scripts.generate_voice import generate_voice
from utils.s3 import upload
from datetime import datetime

TMP_AUDIO = "/workspace/tmp/voice.wav"


def video_node(state):
    # 🔹 Ensure script exists
    if not state.get("script"):
        state["script"] = " ".join(
            [shot["prompt"] for shot in state.get("shots", [])]
        )

    # 1️⃣ Generate narration
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = TMP_AUDIO

    # 2️⃣ Render cinematic video
    state = render_cinematic_video(state)

    # 🔹 Ensure video was created
    local_video = state.get("video_path")
    if not local_video:
        raise ValueError("render_cinematic_video did not set state['video_path']")

    # 3️⃣ Upload to S3
    title = (state.get("title") or "video").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    s3_uri = upload(
        local_video,
        f"videos/{title}_{timestamp}"
    )

    state["video_path"] = s3_uri
    print(f"🚀 Final video uploaded to: {s3_uri}")

    return state
