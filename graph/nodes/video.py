import os
import subprocess
from utils.s3 import upload
from datetime import datetime

# Use /tmp/ for temporary files
TMP_DIR = "/tmp/cofeposa"
OUTPUT_VIDEO = f"{TMP_DIR}/final_video.mp4"
AUDIO_PAD = f"{TMP_DIR}/voice_padded.wav"

def video_node(state):
    fps = state.get("fps", 24)
    
    # Get frames and voice from previous nodes
    all_frames = [frame for shot_frames in state.get("frame_paths", []) for frame in shot_frames]
    voice_path = state.get("voice_path", f"{TMP_DIR}/voice.wav")
    
    total_frames = len(all_frames)
    video_duration = total_frames / fps
    
    print(f"📊 Video: {total_frames} frames at {fps} fps = {video_duration:.2f} seconds")
    print(f"🎵 Audio: {voice_path}")

    if not all_frames:
        raise ValueError("No frames to process - image generation may have failed")

    # Create concat file for image sequence
    concat_txt = f"{TMP_DIR}/concat.txt"
    with open(concat_txt, "w") as f:
        for frame in all_frames:
            f.write(f"file '{frame}'\n")

    # Pad audio to match video duration (loop if shorter)
    if os.path.exists(voice_path):
        subprocess.run([
            "ffmpeg", "-y",
            "-i", voice_path,
            "-filter_complex", f"aloop=loop=-1:size={int(video_duration * 48000)},asetpts=PTS-STARTPTS",
            "-i", concat_txt,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-r", str(fps),
            "-c:a", "aac",
            "-shortest",  # Now safe because audio is pre-padded to video length
            OUTPUT_VIDEO
        ], check=True)
    else:
        # No audio - just video
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-r", str(fps),
            OUTPUT_VIDEO
        ], check=True)

    # Upload to S3
    title = (state.get("title") or "video").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_uri = upload(OUTPUT_VIDEO, f"videos/{title}_{timestamp}")

    state["video_path"] = s3_uri
    print(f"🚀 Final video: {s3_uri}")

    return state

