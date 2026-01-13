from scripts.generate_image import generate_image
from utils.s3 import upload

def image_node(state):
    local_path = "/tmp/image.png"
    generate_image(local_path)
    state["image_path"] = upload(local_path, "images")
    return state
