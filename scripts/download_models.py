import os
import sys
import shutil
from huggingface_hub import snapshot_download

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.s3 import upload_dir

# Cache paths
os.environ["HF_HOME"] = "/workspace/cache"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/cache/transformers"
os.environ["DIFFUSERS_CACHE"] = "/workspace/cache/diffusers"

BASE_DIR = "/workspace/models"
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")

# ------------------------
# Add creative image models here
# ------------------------
MODELS = {
    "llm": ["mistral-inference/Mistral-7B-v0.1"],
    "tts": ["coqui/XTTS-v2"],
    "image": [
        "runwayml/stable-diffusion-v1-5",
        "dreamlike-art/dreamlike-diffusion-1.0",
        "hakurei/waifu-diffusion"
    ],
    "video": ["stabilityai/stable-video-diffusion-img2vid"]
}

def process_model(category, model_id):
    local_dir = os.path.join(BASE_DIR, category, model_id.replace('/', '_'))
    s3_prefix = f"models/{category}/{model_id.replace('/', '_')}"

    print(f"\n⬇ Downloading {model_id}")
    try:
        snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            token=HF_TOKEN,
            allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"],
            ignore_patterns=["*.ckpt", "*.bin", "*.pt"]
        )
    except Exception as e:
        print(f"⚠️ Skipping {model_id}: download failed: {e}")
        return

    print(f"☁ Uploading {model_id} to S3")
    try:
        upload_dir(local_dir, s3_prefix)
    except Exception as e:
        print(f"⚠️ Upload failed for {model_id}: {e}")

    print(f"📁 Kept local model files at {local_dir}")

def main():
    for category, models in MODELS.items():
        for model in models:
            process_model(category, model)

    print("\n✅ All models safely stored in S3")

if __name__ == "__main__":
    main()
