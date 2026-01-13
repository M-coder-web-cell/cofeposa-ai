from scripts.generate_image import generate_image
from utils.s3 import upload

TMP_IMAGE = "/workspace/tmp/image.png"

def image_node(state):
    generate_image(TMP_IMAGE)
    state["image_path"] = upload(TMP_IMAGE, "images")
    return state