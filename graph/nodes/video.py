import os
import subprocess
from utils.s3 import upload
from datetime import datetime

# Use /tmp/ for temporary files
TMP_DIR = "/tmp/cofeposa"
OUTPUT_VIDEO = f"{TMP_DIR}/final_video.mp4"

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

    # Check if audio exists and get its duration
    audio_exists = os.path.exists(voice_path)
    
    if audio_exists:
        # Get audio duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", voice_path],
            capture_output=True, text=True
        )
        audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 0
        print(f"🎵 Audio duration: {audio_duration:.2f}s")
        
        # If audio is shorter, pad it using ffmpeg
        if audio_duration < video_duration - 0.5:
            padded_audio = f"{TMP_DIR}/voice_padded.wav"
            subprocess.run([
                "ffmpeg", "-y", "-i", voice_path,
                "-af", f"apad=whole_dur={video_duration:.3f}",
                padded_audio
            ], check=True)
            voice_path = padded_audio
            print(f"🔊 Audio padded to {video_duration:.2f}s")

    # Build video from images - use image2 demuxer for frame sequences
    # Apply light cinematic post-processing: unsharp, slight contrast & saturation boost
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", f"{TMP_DIR}/frames/frame_%06d.png",
        "-i", voice_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "slow",
        "-crf", "18",
        "-vf", "unsharp=5:5:1.0:5:5:0.0,eq=saturation=1.1,eq=contrast=1.05",
        "-r", str(fps),
        "-c:a", "aac",
        "-shortest",
        OUTPUT_VIDEO
    ], check=True)

    # Upload to S3
    title = (state.get("title") or "video").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_uri = upload(OUTPUT_VIDEO, f"videos/{title}_{timestamp}")

    state["video_path"] = s3_uri
    print(f"🚀 Final video: {s3_uri}")

    return state