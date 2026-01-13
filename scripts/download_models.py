import os
from huggingface_hub import snapshot_download

BASE_DIR = "/workspace/models"
os.makedirs(BASE_DIR, exist_ok=True)

# Set HF token in environment if you have one
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")
if HF_TOKEN:
    os.environ["HF_HOME"] = "/workspace/cache"
    os.environ["HF_HUB_TOKEN"] = HF_TOKEN  # <-- required for private or gated models

MODELS = {
    "llm": ["eleutherai/pythia-2.8b"],  
    "tts": ["coqui/XTTS-v2"],            
    "sdxl": ["stabilityai/stable-diffusion-xl-base-1.0"],  
    "animatediff": [],                   
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
                local_dir_use_symlinks=False,
                token=HF_TOKEN  # <-- use token here
            )

if __name__ == "__main__":
    download()
    print("✅ All models downloaded.")
