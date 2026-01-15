import os
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

# Get the directory of this script for config paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(SCRIPT_DIR, "..", "configs")

_PIPELINES = {}

# Use CPU if CUDA is not available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
print(f"Using device: {DEVICE}, dtype: {DTYPE}")

def get_pipeline(model_id, mode="txt2img"):
    key = f"{model_id}:{mode}"

    if key not in _PIPELINES:
        print(f"Loading pipeline: {model_id} ({mode})")
        
        if mode == "img2img":
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_id, torch_dtype=DTYPE
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, torch_dtype=DTYPE
            )

        pipe = pipe.to(DEVICE)
        
        # Disable NSFW filter for unrestricted generation
        pipe.safety_checker = None
        
        # Pipeline stability features
        try:
            pipe.enable_attention_slicing()
            print("  ✅ Attention slicing enabled")
        except Exception as e:
            print(f"  ⚠️ Attention slicing failed: {e}")
        
        try:
            pipe.enable_vae_tiling()
            print("  ✅ VAE tiling enabled")
        except Exception as e:
            print(f"  ⚠️ VAE tiling failed: {e}")
        
        # Memory-efficient attention with safe fallback
        try:
            pipe.enable_xformers_memory_efficient_attention()
            print("  ✅ xformers enabled")
        except Exception:
            print("  ⚠️ xformers not available, using fallback attention")
        
        _PIPELINES[key] = pipe

    return _PIPELINES[key]

