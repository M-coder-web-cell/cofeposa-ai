import os
from PIL import Image

def generate_image(image_local: str | None, prompt: str, output_local: str):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    if image_local:
        try:
            img = Image.open(image_local).convert("RGB")
        except Exception:
            img = Image.new("RGB", (1280, 720), color=(20,20,20))
    else:
        img = Image.new("RGB", (1280, 720), color=(20,20,20))

    img.save(output_local)
    return output_local
