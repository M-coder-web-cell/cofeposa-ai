import os
from prompts.prompt import get_prompt

# Try to load a diffusion pipeline; if unavailable or out-of-disk,
# create a simple placeholder image using Pillow. The SD model path can be
# overridden with `SD_MODEL_PATH` env var. Default matches the downloader
# location for the `runwayml/stable-diffusion-v1-5` model.
_USE_PLACEHOLDER = False
try:
    import torch
    from diffusers import StableDiffusionPipeline

    MODEL_PATH = os.environ.get("SD_MODEL_PATH", "/workspace/models/image/runwayml_stable-diffusion-v1-5")

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )

    if torch.cuda.is_available():
        pipe = pipe.to("cuda")

    def generate_image(output_path):
        prompt = get_prompt()["image_prompt"]
        image = pipe(prompt, guidance_scale=7.5, num_inference_steps=30).images[0]
        image.save(output_path)

except Exception as e:
    _USE_PLACEHOLDER = True
    print("Warning: StableDiffusion unavailable, using placeholder image —", e)

    from PIL import Image, ImageDraw, ImageFont

    def generate_image(output_path):
        prompt = get_prompt().get("image_prompt", "placeholder image")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img = Image.new("RGB", (1024, 576), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        text = (prompt[:200] + "...") if len(prompt) > 200 else prompt
        draw.text((20, 20), text, fill=(220, 220, 220), font=font)
        img.save(output_path)
