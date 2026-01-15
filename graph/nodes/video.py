import os
import subprocess
import tempfile
from utils.s3 import upload
from scripts.generate_voice import generate_voice
from datetime import datetime

# Use /tmp/ for temporary files (works on macOS and Linux)
TMP_DIR = "/tmp/cofeposa"
TMP_AUDIO = f"{TMP_DIR}/voice.wav"

def video_node(state):
    # 1️⃣ Ensure script exists
    if not state.get("script"):
        state["script"] = " ".join([shot["prompt"] for shot in state.get("shots", [])])

    # 2️⃣ Calculate total video duration from frames
    fps = state.get("fps", 24)
    total_frames = sum(len(shot_frames) for shot_frames in state.get("frame_paths", []))
    video_duration = total_frames / fps
    
    print(f"📊 Video will be {video_duration:.2f} seconds ({total_frames} frames at {fps} fps)")
    
    # 3️⃣ Generate voice with duration matching video
    os.makedirs(TMP_DIR, exist_ok=True)
    generate_voice(state["script"], TMP_AUDIO, duration=int(video_duration) + 2)  # Add 2 sec buffer
    state["voice_path"] = TMP_AUDIO

    # 4️⃣ Assemble frames per shot (flatten nested frame_paths list)
    tmp_dir = tempfile.mkdtemp(prefix="cinematic_")
    concat_txt = os.path.join(tmp_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        # Flatten nested list: [[shot1_frames], [shot2_frames]] -> [frame1, frame2, ...]
        all_frames = [frame for shot_frames in state.get("frame_paths", []) for frame in shot_frames]
        for frame in all_frames:
            f.write(f"file '{frame}'\n")

    # 5️⃣ Render final video - set framerate explicitly
    output_video = f"{TMP_DIR}/final_video.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-r", str(fps),  # Force output framerate
        "-i", TMP_AUDIO,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac",
        "-shortest",  # Stop when video ends
        output_video
    ], check=True)

    # 6️⃣ Upload to S3
    title = (state.get("title") or "video").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_uri = upload(output_video, f"videos/{title}_{timestamp}")

    state["video_path"] = s3_uri
    print(f"🚀 Final video uploaded to: {s3_uri}")

    return state

