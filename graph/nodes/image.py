from scripts.generate_image import generate_image
from prompts.prompt import get_prompt

def image_node(state):
    IMAGE_PATH = "/workspace/outputs/image.png"
    generate_image(IMAGE_PATH)
    state["image_path"] = IMAGE_PATH
    return state
