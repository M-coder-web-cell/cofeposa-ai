import subprocess
from prompts.prompt import get_prompt

def render_video(image, audio, output):
    fps = get_prompt()["fps"]
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", image,
        "-i", audio,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-r", str(fps),
        output
    ])
