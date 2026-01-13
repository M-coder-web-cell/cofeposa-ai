import torch
from diffusers import StableDiffusionXLPipeline
from prompts.prompt import get_prompt

MODEL_PATH = "/workspace/models/sdxl/stabilityai_stable-diffusion-xl-base-1.0"

pipe = StableDiffusionXLPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16
).to("cuda")

def generate_image(output_path):
    prompt = get_prompt()["image_prompt"]
    image = pipe(prompt, guidance_scale=7.5, num_inference_steps=30).images[0]
    image.save(output_path)
