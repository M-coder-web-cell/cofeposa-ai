import os
from utils.s3 import download
from scripts.render_image import render_single_shot

def image_node(state):
    shots = state["shots"]
    images = []

    os.makedirs("/tmp", exist_ok=True)

    for i, shot in enumerate(shots):
        prompt = shot["prompt"]
        duration = shot["duration"]

        output_image = f"/tmp/shot_{i}.png"

        # If S3 image exists for this shot
        image_s3 = shot.get("image_s3")
        if image_s3:
            print(f"🖼 Using S3 image for shot {i}")
            local_input = f"/tmp/input_{i}.png"
            try:
                download(image_s3, local_input)
                render_single_shot(local_input, prompt, output_image)
            except Exception as e:
                print(f"⚠️ S3 failed, generating instead: {e}")
                render_single_shot(None, prompt, output_image)
        else:
            print(f"🎨 Generating image for shot {i}")
            render_single_shot(None, prompt, output_image)

        images.append({
            "path": output_image,
            "duration": duration
        })

    return {
        **state,
        "images": images
    }
