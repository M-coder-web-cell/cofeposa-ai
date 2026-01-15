import os
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

# Get the directory of this script for config paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(SCRIPT_DIR, "..", "configs")

_PIPELINES = {}

# Use CPU if CUDA is not available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

def get_pipeline(model_id, mode="txt2img"):
    key = f"{model_id}:{mode}"

    if key not in _PIPELINES:
        if mode == "img2img":
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_id, torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
            )

        pipe = pipe.to(DEVICE)
        
        # Disable NSFW filter for unrestricted generation
        pipe.safety_checker = None
        
        # Optionally disable xformers if it causes issues
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            print("⚠️ xformers not available, continuing without memory-efficient attention")
        _PIPELINES[key] = pipe

    return _PIPELINES[key]

