from scripts.render_video import render_video
from prompts.prompt import get_prompt

def video_node(state):
    VIDEO_PATH = "/workspace/outputs/final.mp4"
    render_video(state["image_path"], state["voice_path"], VIDEO_PATH)
    state["video_path"] = VIDEO_PATH
    return state
