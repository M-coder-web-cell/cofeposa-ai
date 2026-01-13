from scripts.render_video import render_video

VIDEO_PATH = "/workspace/outputs/final.mp4"

def video_node(state):
    render_video(
        state["image_path"],
        state["voice_path"],
        VIDEO_PATH
    )
    state["video_path"] = VIDEO_PATH
    return state
