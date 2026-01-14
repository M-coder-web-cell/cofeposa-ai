import os
from utils.s3 import download
from scripts.generate_image import generate_image
from PIL import Image
import random

def image_node(state):
    shots = state["shots"]
    all_shot_frames = []

    os.makedirs("/tmp/frames", exist_ok=True)

    for i, shot in enumerate(shots):
        prompt = shot["prompt"]
        num_frames = int(shot.get("duration", 3) * state.get("fps", 24))
        shot_frames = []

        # Start from S3 image if provided
        if shot.get("image_s3"):
            local_input = f"/tmp/input_{i}.png"
            download(shot["image_s3"], local_input)
        else:
            local_input = None

        # Generate frames for this shot
        prev_img = local_input
        for f in range(num_frames):
            frame_path = f"/tmp/frames/shot_{i}_frame_{f:04d}.png"
            generate_image(prev_img, prompt, frame_path)
            prev_img = frame_path  # evolve next frame from previous for continuity
            shot_frames.append(frame_path)

        all_shot_frames.append(shot_frames)

    state["frame_paths"] = all_shot_frames
    return state
