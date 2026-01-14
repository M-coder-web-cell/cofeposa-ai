from scripts.render_video import render_cinematic_video
from utils.s3 import download, upload

TMP_IMAGE = "/workspace/tmp/image.png"
TMP_AUDIO = "/workspace/tmp/voice.wav"
TMP_VIDEO = "/workspace/tmp/final.mp4"

def video_node(state):
    download(state["image_path"], TMP_IMAGE)
    download(state["voice_path"], TMP_AUDIO)

    render_cinematic_video(TMP_IMAGE, TMP_AUDIO, TMP_VIDEO)

    state["video_path"] = upload(TMP_VIDEO, "videos")
    return state
