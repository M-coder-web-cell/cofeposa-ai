import os
from huggingface_hub import snapshot_download

BASE_DIR = "/workspace/models"
os.makedirs(BASE_DIR, exist_ok=True)
os.environ["HF_HOME"] = "/workspace/cache"

MODELS = {
    "llm": ["TheBloke/vicuna-7B-1.1-HF"],
    "tts": ["coqui/XTTS-v2"],
    "sdxl": [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "stabilityai/stable-diffusion-xl-refiner-1.0"
    ],
    "animatediff": ["guoyww/animatediff-motion-adapter-v1-5"],
    "upscalers": ["xinntao/Real-ESRGAN"]
}

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
