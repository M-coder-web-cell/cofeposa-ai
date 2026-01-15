import os
from utils.s3 import download
from scripts.generate_image import generate_image
from PIL import Image

# Use /tmp/ for all temporary files
TMP_DIR = "/tmp/cofeposa"
FRAMES_DIR = f"{TMP_DIR}/frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

def image_node(state):
    shots = state["shots"]
    all_shot_frames = []

    for i, shot in enumerate(shots):
        prompt = shot["prompt"]
        fps = state.get("fps", 24)
        num_frames = int(shot.get("duration", 3) * fps)
        shot_frames = []

        print(f"🎨 Processing shot {i}: {num_frames} frames, prompt: {prompt[:50]}...")

        # Start from S3 image if provided
        local_input = None
        if shot.get("image_s3"):
            local_input = f"{TMP_DIR}/input_{i}.png"
            try:
                download(shot["image_s3"], local_input)
                print(f"  📷 Downloaded input image: {local_input}")
            except Exception as e:
                print(f"⚠️ Could not load image for shot {i}: {e}")
                local_input = None

        # Generate frames for this shot
        prev_img = local_input
        for f in range(num_frames):
            frame_path = f"{FRAMES_DIR}/shot_{i}_frame_{f:04d}.png"
            try:
                generate_image(prev_img, prompt, frame_path)
                # Verify frame was created
                if os.path.exists(frame_path):
                    img = Image.open(frame_path)
                    img.verify()  # Verify it's a valid image
                    prev_img = frame_path  # evolve next frame from previous for continuity
                    shot_frames.append(frame_path)
                else:
                    print(f"  ❌ Frame not created: {frame_path}")
            except Exception as e:
                print(f"  ❌ Error generating frame {f}: {e}")

        if shot_frames:
            print(f"✅ Shot {i}: {len(shot_frames)}/{num_frames} frames generated")
        else:
            print(f"❌ Shot {i}: No frames generated!")

        all_shot_frames.append(shot_frames)

    # Check total frames
    total_frames = sum(len(frames) for frames in all_shot_frames)
    print(f"📊 Total frames generated: {total_frames}")

    state["frame_paths"] = all_shot_frames
    return state

