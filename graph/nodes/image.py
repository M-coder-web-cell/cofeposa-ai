import os
from utils.s3 import download
from scripts.generate_image import generate_image
from PIL import Image

# Use /tmp/ for all temporary files
TMP_DIR = "/tmp/cofeposa"
FRAMES_DIR = f"{TMP_DIR}/frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

# IMAGE_FPS: How many diffusion images to generate per second
# Lower = slower, more cinematic pacing. Higher = faster changes.
# For Instagram Reels/Shorts, 1 image per second is recommended.
IMAGE_FPS = 1

def image_node(state):
    shots = state["shots"]
    all_shot_frames = []
    frame_counter = 0  # Sequential counter for all frames

    for i, shot in enumerate(shots):
        base_prompt = shot["prompt"]
        fps = state.get("fps", 24)
        duration = shot.get("duration", 3)
        
        # Decouple image generation from fps
        # Generate images at IMAGE_FPS rate, not fps rate
        num_images = max(1, round(duration * IMAGE_FPS))
        repeat_factor = fps // IMAGE_FPS  # Each generated image is repeated this many times
        total_frames = duration * fps  # But we still need this many frames for correct duration
        
        shot_frames = []

        print(f"🎨 Processing shot {i}: {duration}s @ {fps}fps = {int(total_frames)} frames")
        print(f"  📊 Generating {num_images} diffusion images (IMAGE_FPS={IMAGE_FPS})")
        print(f"  🔄 Each image repeated {repeat_factor} times for smooth playback")

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

        # Generate diffusion images at IMAGE_FPS rate (not per frame)
        prev_img = local_input
        
        for img_i in range(num_images):
            # Use sequential naming for ffmpeg image2 demuxer
            image_path = f"{FRAMES_DIR}/frame_{frame_counter:06d}.png"
            
            # Generate one diffusion image
            try:
                # Generate one diffusion image
                generate_image(prev_img, base_prompt, image_path, frame_num=img_i, total_frames=num_images)
                
                # Verify image was created
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img.verify()  # Verify it's a valid image
                    prev_img = image_path  # Use as input for next img2img pass
                else:
                    print(f"  ❌ Image not created: {image_path}")
                    prev_img = None
            except Exception as e:
                print(f"  ❌ Error generating image {img_i}: {e}")
                prev_img = None
            
            # Copy this image to ALL frame slots for this repetition
            for r in range(repeat_factor):
                dest_path = f"{FRAMES_DIR}/frame_{frame_counter:06d}.png"
                if image_path != dest_path:
                    import shutil
                    shutil.copy2(image_path, dest_path)
                shot_frames.append(dest_path)
                frame_counter += 1

        if shot_frames:
            print(f"✅ Shot {i}: {len(shot_frames)} frames from {num_images} images (repeat={repeat_factor}x)")
        else:
            print(f"❌ Shot {i}: No frames generated!")

        all_shot_frames.append(shot_frames)

    # Check total frames
    total_frames = sum(len(frames) for frames in all_shot_frames)
    print(f"📊 Total frames generated: {total_frames}")

    state["frame_paths"] = all_shot_frames
    return state

