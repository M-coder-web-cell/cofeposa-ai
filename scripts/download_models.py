import os
import sys
import requests
from huggingface_hub import HfApi

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.s3 import upload_fileobj  # NEW helper

# ------------------------
# Config
# ------------------------
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")
S3_PREFIX = "models"
CHUNK_SIZE = 8 * 1024 * 1024  # 8MB

# ------------------------
# Models
# ------------------------
MODELS = {
    "llm": ["EleutherAI/pythia-2.8b"],
    "tts": ["coqui/XTTS-v2"],
    "image": [
        "runwayml/stable-diffusion-v1-5",
        "dreamlike-art/dreamlike-diffusion-1.0",
        "hakurei/waifu-diffusion"
    ],
    "video": ["stabilityai/stable-video-diffusion-img2vid"]
}

# ------------------------
# File filters
# ------------------------
ALLOW_EXT = (".json", ".safetensors", ".txt", ".model")
IGNORE_EXT = (".ckpt", ".bin", ".pt", ".non_ema")

api = HfApi(token=HF_TOKEN)

def should_upload(file):
    if file.endswith(IGNORE_EXT):
        return False
    return file.endswith(ALLOW_EXT)

def stream_to_s3(model_id, category, file_path):
    url = f"https://huggingface.co/{model_id}/resolve/main/{file_path}"
    s3_key = f"{S3_PREFIX}/{category}/{model_id.replace('/', '_')}/{file_path}"

    print(f"⬇ Streaming {file_path}")

    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        upload_fileobj(
            fileobj=r.raw,
            s3_key=s3_key
        )

def process_model(category, model_id):
    print(f"\n🚀 Processing {model_id}")

    try:
        files = api.list_repo_files(model_id)
    except Exception as e:
        print(f"❌ Failed to list files: {e}")
        return

    for file in files:
        if not should_upload(file):
            continue

        try:
            stream_to_s3(model_id, category, file)
        except Exception as e:
            print(f"⚠️ Failed {file}: {e}")

def main():
    for category, models in MODELS.items():
        for model in models:
            process_model(category, model)

    print("\n✅ All models streamed directly to S3 (no disk used)")

if __name__ == "__main__":
    main()
