import os

# 🔥 MUST BE FIRST (before huggingface imports)
os.environ["HF_HOME"] = "/workspace/cache"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/cache/transformers"
os.environ["DIFFUSERS_CACHE"] = "/workspace/cache/diffusers"
os.environ["TORCH_HOME"] = "/workspace/cache/torch"

from huggingface_hub import snapshot_download

BASE_DIR = "/workspace/models"
CACHE_DIR = "/workspace/cache"

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Optional HF token (for gated/private models)
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")
if HF_TOKEN:
    os.environ["HF_HUB_TOKEN"] = HF_TOKEN

MODELS = {
    "llm": ["eleutherai/pythia-2.8b"],
    "tts": ["coqui/XTTS-v2"],
    "sdxl": ["runwayml/stable-diffusion-v1-5"],
    "animatediff": [],
    "upscalers": ["xinntao/Real-ESRGAN"]
}

def download():
    for category, model_list in MODELS.items():
        for model in model_list:
            print(f"\n⬇ Downloading {model}")
            snapshot_download(
                repo_id=model,
                local_dir=os.path.join(
                    BASE_DIR,
                    category,
                    model.replace("/", "_")
                ),
                token=HF_TOKEN,
                local_dir_use_symlinks=False
            )

if __name__ == "__main__":
    download()
    print("\n✅ All models downloaded successfully.")
