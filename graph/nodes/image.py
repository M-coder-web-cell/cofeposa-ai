import os
from utils.s3 import download
from scripts.generate_image import generate_image
from PIL import Image

# Use /tmp/ for all temporary files
TMP_DIR = "/tmp/cofeposa"
FRAMES_DIR = f"{TMP_DIR}/frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

# Keyframe interval - refresh from base prompt every N frames to prevent degradation
KEYFRAME_INTERVAL = 8

def image_node(state):
    shots = state["shots"]
    all_shot_frames = []

    for i, shot in enumerate(shots):
        base_prompt = shot["prompt"]
        fps = state.get("fps", 24)
        num_frames = round(shot.get("duration", 3) * fps)  # Use round() to avoid truncation
        shot_frames = []

        print(f"🎨 Processing shot {i}: {num_frames} frames, prompt: {base_prompt[:50]}...")

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

        # Generate frames with keyframe refresh
        prev_img = local_input
        keyframe_count = 0
        
        for f in range(num_frames):
            frame_path = f"{FRAMES_DIR}/shot_{i}_frame_{f:04d}.png"
            
            # Keyframe logic: every KEYFRAME_INTERVAL frames, use txt2img for fresh output
            is_keyframe = (f % KEYFRAME_INTERVAL == 0) or (prev_img is None)
            
            if is_keyframe and f > 0:
                # Generate fresh frame from base prompt (txt2img)
                prev_img = None
                keyframe_count += 1
            
            try:
                generate_image(prev_img, base_prompt, frame_path, frame_num=f, total_frames=num_frames)
                
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
                # On error, try txt2img for next frame
                prev_img = None

        if shot_frames:
            print(f"✅ Shot {i}: {len(shot_frames)}/{num_frames} frames generated (keyframes: {keyframe_count})")
        else:
            print(f"❌ Shot {i}: No frames generated!")

        all_shot_frames.append(shot_frames)

    # Check total frames
    total_frames = sum(len(frames) for frames in all_shot_frames)
    print(f"📊 Total frames generated: {total_frames}")

    state["frame_paths"] = all_shot_frames
    return state

