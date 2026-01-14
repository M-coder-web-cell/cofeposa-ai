import os
from prompts.prompt import get_prompt
from utils.s3 import download
from scripts.generate_image import generate_image

TMP_DIR = "/workspace/tmp/images"

def image_node(state):
    prompt_data = get_prompt()
    shots = prompt_data.get("shots", [])

    os.makedirs(TMP_DIR, exist_ok=True)

    state["shots"] = []

    for idx, shot in enumerate(shots):
        prompt = shot["prompt"]
        duration = shot.get("duration", 3)
        image_s3 = shot.get("image_s3")

        local_image = os.path.join(TMP_DIR, f"shot_{idx}.png")

        if image_s3:
            print(f"🖼 Using S3 image for shot {idx}")
            download(image_s3, local_image)
        else:
            print(f"🎨 Generating image for shot {idx}")
            generate_image(local_image, prompt)

        state["shots"].append({
            "id": idx,
            "image": local_image,
            "duration": duration,
            "prompt": prompt
        })

    return state
