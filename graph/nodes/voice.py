import os
from scripts.generate_voice import generate_voice
from utils.s3 import upload

# Use /tmp/ for temporary files (works on macOS and Linux)
TMP_DIR = "/tmp/cofeposa"
TMP_AUDIO = f"{TMP_DIR}/voice.wav"

def voice_node(state):
    os.makedirs(TMP_DIR, exist_ok=True)
    
    # Calculate expected video duration from frames
    fps = state.get("fps", 24)
    total_frames = sum(len(shot_frames) for shot_frames in state.get("frame_paths", []))
    video_duration = total_frames / fps
    
    # Generate voice matching video duration
    duration = int(video_duration) + 1
    generate_voice(state["script"], TMP_AUDIO, duration=duration)
    
    # Store BOTH local path and S3 path
    local_path = TMP_AUDIO
    s3_uri = upload(local_path, "audio")
    
    state["voice_path"] = local_path  # Use local path for ffmpeg
    state["voice_s3_uri"] = s3_uri    # Store S3 URI for reference
    
    return state
