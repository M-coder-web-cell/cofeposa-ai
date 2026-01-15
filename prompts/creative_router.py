import os
import random
import yaml

# Get the directory of this script for config paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(SCRIPT_DIR, "..", "configs")

with open(os.path.join(CONFIGS_DIR, "models.yaml")) as f:
    MODELS = yaml.safe_load(f)["models"]

with open(os.path.join(CONFIGS_DIR, "creativity.yaml")) as f:
    CREATIVE = yaml.safe_load(f)

def choose_model(prompt: str):
    p = prompt.lower()
    if "anime" in p:
        return MODELS["waifu"]
    if "dream" in p or "surreal" in p:
        return MODELS["dreamlike"]
    return MODELS["runway"]

def enrich_prompt(base_prompt: str, frame_num=0, total_frames=1, motion_hint=None):
    camera = random.choice(CREATIVE["camera"])
    lighting = random.choice(CREATIVE["lighting"])
    mood = random.choice(CREATIVE["mood"])
    
    # Add temporal variation based on frame position
    if frame_num == 0:
        # First frame - establish the scene
        temporal = "wide establishing shot"
    elif frame_num == total_frames - 1:
        # Last frame - conclusion
        temporal = "final composition"
    elif frame_num % (total_frames // 3) == 0:
        # Every third of the way through
        temporal = "transitioning view"
    else:
        temporal = "continuous motion"
    
    # Add motion hint if provided
    if motion_hint:
        temporal = f"{temporal}, {motion_hint}"
    
    return f"{base_prompt}, {camera}, {lighting}, {mood}, {temporal}, ultra detailed, cinematic"

