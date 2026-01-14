import os
import subprocess
import tempfile
from utils.s3 import upload
from scripts.generate_voice import generate_voice
from datetime import datetime

TMP_AUDIO = "/workspace/tmp/voice.wav"

def video_node(state):
    # 1️⃣ Ensure script exists
    if not state.get("script"):
        state["script"] = " ".join([shot["prompt"] for shot in state.get("shots", [])])

    # 2️⃣ Generate voice
    generate_voice(state["script"], TMP_AUDIO)
    state["voice_path"] = TMP_AUDIO

    # 3️⃣ Assemble frames per shot
    tmp_dir = tempfile.mkdtemp(prefix="cinematic_")
    concat_txt = os.path.join(tmp_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for shot_frames in state["frame_paths"]:
            for frame in shot_frames:
                f.write(f"file '{frame}'\n")

    # 4️⃣ Render final video
    output_video = "/workspace/tmp/final_video.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-i", TMP_AUDIO,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output_video
    ], check=True)

    # 5️⃣ Upload to S3
    title = (state.get("title") or "video").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_uri = upload(output_video, f"videos/{title}_{timestamp}")

    state["video_path"] = s3_uri
    print(f"🚀 Final video uploaded to: {s3_uri}")

    return state
