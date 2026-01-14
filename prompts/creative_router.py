import random
import yaml

with open("configs/models.yaml") as f:
    MODELS = yaml.safe_load(f)["models"]

with open("configs/creativity.yaml") as f:
    CREATIVE = yaml.safe_load(f)

def choose_model(prompt: str):
    p = prompt.lower()
    if "anime" in p:
        return MODELS["waifu"]
    if "dream" in p or "surreal" in p:
        return MODELS["dreamlike"]
    return MODELS["runway"]

def enrich_prompt(base_prompt: str):
    camera = random.choice(CREATIVE["camera"])
    lighting = random.choice(CREATIVE["lighting"])
    mood = random.choice(CREATIVE["mood"])

    return f"{base_prompt}, {camera}, {lighting}, {mood}, ultra detailed"
