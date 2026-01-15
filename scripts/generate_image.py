import os
import random
from PIL import Image
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from scripts.model_registry import get_pipeline
from prompts.creative_router import choose_model, enrich_prompt

def generate_image(input_image, prompt, output_path):
    model = choose_model(prompt)
    final_prompt = enrich_prompt(prompt)

    # Check if input_image exists, otherwise fall back to txt2img
    img_exists = input_image and os.path.exists(input_image)

    if img_exists:
        # 🔁 IMG2IMG (photo → creative)
        pipe = get_pipeline(model["id"], mode="img2img")

        init_image = Image.open(input_image).convert("RGB").resize((512, 512))

        image = pipe(
            prompt=final_prompt,
            image=init_image,
            strength=random.uniform(*model["strength"]),
            guidance_scale=random.uniform(*model["guidance"]),
            num_inference_steps=20  # Reduced from 30 for faster execution
        ).images[0]

    else:
        # 🎨 TXT2IMG (no photo or file not found)
        pipe = get_pipeline(model["id"], mode="txt2img")

        image = pipe(
            prompt=final_prompt,
            guidance_scale=random.uniform(*model["guidance"]),
            num_inference_steps=25  # Reduced from 30 for faster execution
        ).images[0]

    image.save(output_path)
    return output_path
