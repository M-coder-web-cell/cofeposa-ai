import os
from utils.s3 import download
from scripts.generate_image import generate_image

def image_node(state):
    shots = state["shots"]
    image_paths = []
    os.makedirs("/tmp", exist_ok=True)

    for i, shot in enumerate(shots):
        prompt = shot["prompt"]
        output_image = f"/tmp/shot_{i}.png"
        image_s3 = shot.get("image_s3")

        if image_s3:
            print(f"🖼 Using S3 image for shot {i}")
            local_input = f"/tmp/input_{i}.png"
            try:
                download(image_s3, local_input)
                generate_image(local_input, prompt, output_image)
            except Exception as e:
                print(f"⚠️ S3 failed, generating placeholder: {e}")
                generate_image(None, prompt, output_image)
        else:
            print(f"🎨 Generating image for shot {i}")
            generate_image(None, prompt, output_image)

        image_paths.append(output_image)

    state["image_paths"] = image_paths
    return state
