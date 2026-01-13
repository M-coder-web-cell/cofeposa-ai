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
    "sd":  ["stabilityai/stable-diffusion-2-1-base"]
}

def process_model(category, model_id):
    local_dir = f"{BASE_DIR}/{model_id.replace('/', '_')}"
    s3_prefix = f"models/{category}/{model_id.replace('/', '_')}"

    print(f"\n⬇ Downloading {model_id}")
    snapshot_download(
        repo_id=model_id,
        local_dir=local_dir,
        token=HF_TOKEN,
        allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"],
        ignore_patterns=["*.ckpt", "*.bin", "*.pt"]
    )

    print(f"☁ Uploading {model_id} to S3")
    upload_dir(local_dir, s3_prefix)

    print(f"🧹 Cleaning local files for {model_id}")
    shutil.rmtree(local_dir)

def main():
    for category, models in MODELS.items():
        for model in models:
            process_model(category, model)

    print("\n✅ All models safely stored in S3")

if __name__ == "__main__":
    main()

