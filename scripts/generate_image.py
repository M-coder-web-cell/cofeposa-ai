import os
import random
from prompts.prompt import get_prompt

_USE_PLACEHOLDER = False
try:
    import torch
    from diffusers import StableDiffusionPipeline

    # ------------------------
    # Multi-creative models
    # ------------------------
    CREATIVE_MODELS = [
        "runwayml/stable-diffusion-v1-5",
        "dreamlike-art/dreamlike-diffusion-1.0",
        "kandinsky-2-2",
        "stabilityai/stable-diffusion-2",
        "hakurei/waifu-diffusion"
    ]

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    _PIPE_CACHE = {}

    def _load_pipeline(model_id):
        if model_id in _PIPE_CACHE:
            return _PIPE_CACHE[model_id]
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            local_files_only=True
        ).to(DEVICE)
        _PIPE_CACHE[model_id] = pipe
        return pipe

    def generate_image(output_path):
        prompt = get_prompt().get("image_prompt", "A surreal futuristic scene")
        prompt += " — highly detailed, cinematic lighting, ultra creative, vivid colors"

        model_id = random.choice(CREATIVE_MODELS)
        pipe = _load_pipeline(model_id)
        image = pipe(prompt, guidance_scale=7.5, num_inference_steps=30).images[0]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
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
