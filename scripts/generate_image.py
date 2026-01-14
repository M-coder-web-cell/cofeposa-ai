import os
from PIL import Image

def generate_image(
    image_local: str | None,
    prompt: str,
    output_local: str
):
    """
    image_local → optional img2img source
    prompt → text prompt
    output_local → .png
    """

    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    if image_local:
        img = Image.open(image_local).convert("RGB")
    else:
        # placeholder until SD pipeline is plugged in
        img = Image.new("RGB", (1280, 720), color=(20, 20, 20))

    img.save(output_local)
    return output_local
