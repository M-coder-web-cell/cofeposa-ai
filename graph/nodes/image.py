import os
import random
from prompts.prompt import get_prompt
from utils.s3 import upload, S3_ENABLED
from PIL import Image, ImageDraw, ImageFont

try:
    import torch
    from diffusers import StableDiffusionPipeline
    _HAS_DIFFUSERS = True
except Exception:
    _HAS_DIFFUSERS = False

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
_PIPE_CACHE = {}

CREATIVE_MODELS = [
    "runwayml/stable-diffusion-v1-5",
    "dreamlike-art/dreamlike-diffusion-1.0",
    "hakurei/waifu-diffusion"
]

def _load_pipeline(model_id):
    if model_id in _PIPE_CACHE:
        return _PIPE_CACHE[model_id]
    print(f"⬇ Loading creative model: {model_id}")
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if DEVICE=="cuda" else torch.float32,
        local_files_only=True
    ).to(DEVICE)
    _PIPE_CACHE[model_id] = pipe
    return pipe

def _generate_placeholder(output_path, prompt_text):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (1024, 576), color=(30,30,30))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    text = (prompt_text[:200] + "...") if len(prompt_text) > 200 else prompt_text
    draw.text((20, 20), text, fill=(220,220,220), font=font)
    img.save(output_path)

def image_node(state):
    """
    Generates images for each scene/shot based on the prompt.
    Returns state with a list of image paths in state['image_paths'].
    """
    shots = state.get("shots")
    if not shots:
        # Default: one shot using the main image_prompt
        shots = [{"prompt": get_prompt()["image_prompt"], "duration": get_prompt().get("duration", 10)}]
    
    image_paths = []

    for idx, shot in enumerate(shots):
        prompt_text = shot["prompt"] + " — highly detailed, cinematic lighting, ultra creative, vivid colors"
        model_id = random.choice(CREATIVE_MODELS) if _HAS_DIFFUSERS else None
        tmp_local = f"/workspace/tmp/shot_{idx}.png"

        if model_id and _HAS_DIFFUSERS:
            try:
                pipe = _load_pipeline(model_id)
                image = pipe(prompt_text, guidance_scale=7.5, num_inference_steps=30).images[0]
                os.makedirs(os.path.dirname(tmp_local), exist_ok=True)
                image.save(tmp_local)
            except Exception as e:
                print("⚠ Creative generation failed:", e)
                _generate_placeholder(tmp_local, prompt_text)
        else:
            _generate_placeholder(tmp_local, prompt_text)

        if S3_ENABLED:
            tmp_local = upload(tmp_local, "images")

        image_paths.append(tmp_local)

    state["image_paths"] = image_paths
    return state
