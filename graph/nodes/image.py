from scripts.generate_image import generate_image

IMAGE_PATH = "/workspace/outputs/image.png"

def image_node(state):
    generate_image(IMAGE_PATH)
    state["image_path"] = IMAGE_PATH
    return state
