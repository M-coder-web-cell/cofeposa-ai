from PIL import Image
from prompts.prompt import get_prompt
import torch
from diffusers import StableDiffusionXLImg2ImgPipeline

MODEL_PATH = "/workspace/models/sdxl/stabilityai_stable-diffusion-xl-base-1.0"

pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")
pipe.enable_xformers_memory_efficient_attention()

def generate_image(output_path: str):
    data = get_prompt()
    
    if "reference_image" in data and data["reference_image"]:
        init_image = Image.open(data["reference_image"]).convert("RGB")
        result = pipe(
            prompt=data["image_prompt"],
            image=init_image,
            strength=data.get("strength", 0.6),
            guidance_scale=7.5,
            num_inference_steps=30
        ).images[0]
    else:
        # Pure text-to-image
        result = pipe(
            prompt=data["image_prompt"],
            strength=1.0,
            guidance_scale=7.5,
            num_inference_steps=30
        ).images[0]

    result.save(output_path)
    print(f"🖼️ Image saved → {output_path}")
