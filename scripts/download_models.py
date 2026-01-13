import os
from huggingface_hub import snapshot_download

BASE_DIR = "/workspace/models"
os.makedirs(BASE_DIR, exist_ok=True)
os.environ["HF_HOME"] = "/workspace/cache"

MODELS = {
    "llm": ["openlm-research/open_llama_3b_1"],  # smaller than Vicuna-7B
    "tts": ["coqui/XTTS-v2"],            # 1 GB, okay
    "sdxl": ["stabilityai/stable-diffusion-2-1-base"],  # smaller than SDXL
    "animatediff": [],                   # skip if size >1GB
    "upscalers": ["xinntao/Real-ESRGAN"] # small
}
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")

def download():
    for category, model_list in MODELS.items():
        for model in model_list:
            print(f"⬇ Downloading {model}")
            snapshot_download(
                repo_id=model,
                local_dir=os.path.join(
                    BASE_DIR,
                    category,
                    model.replace("/", "_")
                ),
                local_dir_use_symlinks=False
            )

if __name__ == "__main__":
    download()
    print("✅ All models downloaded.")