import torch
from diffusers import StableDiffusionPipeline
from prompts.prompt import get_prompt

MODEL_PATH = "/workspace/models/sd/sd-v1-5"


pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16
)

# Move pipeline to CUDA if available
if torch.cuda.is_available():
    pipe = pipe.to("cuda")


def generate_image(output_path):
    prompt = get_prompt()["image_prompt"]
    image = pipe(prompt, guidance_scale=7.5, num_inference_steps=30).images[0]
    image.save(output_path)
