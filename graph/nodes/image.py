import os
import random
from urllib.parse import urlparse
from utils.s3 import upload, S3_ENABLED, BUCKET, download

# Pillow fallback
from PIL import Image, ImageDraw, ImageFont

# Diffusers imports
try:
    import torch
    from diffusers import StableDiffusionPipeline
    _HAS_DIFFUSERS = True
except Exception:
    _HAS_DIFFUSERS = False

# ----------------------------
# Creative Open-Source Models
# ----------------------------
CREATIVE_MODELS = [
    "dreamlike-art/dreamlike-diffusion-1.0",  # painterly, surreal
    "runwayml/stable-diffusion-v1-5",        # classic SD
    "kandinsky-2-2",                          # abstract/artistic
    "stabilityai/stable-diffusion-2",         # realistic + creative
    "hakurei/waifu-diffusion"                 # anime/cartoon style
]

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_PIPE_CACHE = {}  # cache loaded pipelines

def _load_pipeline(model_id: str):
    """Load a diffusion pipeline and cache it."""
    global _PIPE_CACHE
    if model_id in _PIPE_CACHE:
        return _PIPE_CACHE[model_id]

    print(f"⬇ Loading creative model: {model_id}")
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        local_files_only=True
    ).to(DEVICE)
    _PIPE_CACHE[model_id] = pipe
    return pipe

# ----------------------------
# Image Generation Node
# ----------------------------
def image_node(state):
    """
    Picks or generates an image for the video pipeline.
    Supports:
      1. Explicit S3 key via IMAGE_S3_KEY
      2. First image under images/ prefix in S3
      3. Creative AI generation if no image found
    """
    # 1️⃣ Check for explicit S3 key
    image_key = os.environ.get("IMAGE_S3_KEY")
    if image_key:
        image_key = image_key.lstrip("/")
        state["image_path"] = f"s3://{BUCKET}/{image_key}"
        return state

    # 2️⃣ List S3 images if enabled
    if S3_ENABLED and "s3" in globals() and s3 is not None:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=BUCKET, Prefix="images/"):
            for obj in page.get("Contents", []):
                key = obj.get("Key")
                if not key or key.endswith("/"):
                    continue
                state["image_path"] = f"s3://{BUCKET}/{key}"
                return state

    # 3️⃣ Generate creative image
    print("⚡ No S3 image found — generating creative AI image...")

    prompt_data = state.get("title") or "A surreal futuristic scene"
    prompt_data += " — highly detailed, cinematic lighting, ultra creative, vivid colors"

    # Randomly pick a model for creativity
    model_id = random.choice(CREATIVE_MODELS) if _HAS_DIFFUSERS else None

    tmp_local = "/workspace/tmp/creative_image.png"

    if model_id and _HAS_DIFFUSERS:
        try:
            pipe = _load_pipeline(model_id)
            image = pipe(prompt_data, guidance_scale=7.5, num_inference_steps=30).images[0]
            os.makedirs(os.path.dirname(tmp_local), exist_ok=True)
            image.save(tmp_local)
        except Exception as e:
            print("⚠ Creative generation failed:", e)
            _generate_placeholder(tmp_local, prompt_data)
    else:
        _generate_placeholder(tmp_local, prompt_data)

    # Upload to S3 if enabled
    if S3_ENABLED:
        s3_uri = upload(tmp_local, "images")
        state["image_path"] = s3_uri
    else:
        state["image_path"] = tmp_local

    return state

# ----------------------------
# Placeholder Image Fallback
# ----------------------------
def _generate_placeholder(output_path, prompt_text):
    """Creates a simple placeholder image if diffusion fails."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (1024, 576), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    text = (prompt_text[:200] + "...") if len(prompt_text) > 200 else prompt_text
    draw.text((20, 20), text, fill=(220, 220, 220), font=font)
    img.save(output_path)
