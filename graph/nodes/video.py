from scripts.render_video import render_video
from utils.s3 import download, upload

def video_node(state):
    image = "/tmp/image.png"
    audio = "/tmp/voice.wav"
    video = "/tmp/final.mp4"

    download(state["image_path"], image)
    download(state["voice_path"], audio)

    render_video(image, audio, video)

    state["video_path"] = upload(video, "videos")
    return state
