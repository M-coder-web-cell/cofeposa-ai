import os
import sys
import shutil
from huggingface_hub import snapshot_download

# When running this script directly (python scripts/download_models.py),
# Python's import path will set the working directory to the `scripts` folder,
# which makes top-level imports like `utils` fail. Ensure project root is on
# sys.path so `from utils.s3 import upload_dir` works.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.s3 import upload_dir

# Cache paths
os.environ["HF_HOME"] = "/workspace/cache"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/cache/transformers"
os.environ["DIFFUSERS_CACHE"] = "/workspace/cache/diffusers"

BASE_DIR = "/workspace/tmp_model"
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")

MODELS = {
    "llm": ["eleutherai/pythia-2.8b"],
    "tts": ["coqui/XTTS-v2"],
    # Use a small public image model by default to avoid large downloads
    # on limited disk environments. Replace with a larger SD model if you
    # have the space and access.
    "sd":  ["google/ddpm-celebahq-256"]
}

def process_model(category, model_id):
    local_dir = f"{BASE_DIR}/{model_id.replace('/', '_')}"
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

    print(f"🧹 Cleaning local files for {model_id}")
    try:
        shutil.rmtree(local_dir)
    except Exception:
        pass

def main():
    for category, models in MODELS.items():
        for model in models:
            process_model(category, model)

    print("\n✅ All models safely stored in S3")

if __name__ == "__main__":
    main()

