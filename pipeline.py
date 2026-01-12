import os
from scripts.generate_script import generate_script
from scripts.generate_image import generate_image
from scripts.generate_voice import generate_voice
from scripts.render_video import render_video

OUTPUT_DIR = "/workspace/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

image_path = f"{OUTPUT_DIR}/image.png"
audio_path = f"{OUTPUT_DIR}/voice.wav"
video_path = f"{OUTPUT_DIR}/final.mp4"

print("🧠 Generating script...")
script = generate_script()

print("🖼️ Generating image...")
generate_image(image_path)

print("🔊 Generating voice...")
generate_voice(script, audio_path)

print("🎬 Rendering video...")
render_video(image_path, audio_path, video_path)

print("🎉 PIPELINE COMPLETE:", video_path)
