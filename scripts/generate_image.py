import os
import random
from PIL import Image
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from scripts.model_registry import get_pipeline
from prompts.creative_router import choose_model, enrich_prompt

# Global negative prompt for quality improvement
NEGATIVE_PROMPT = "blurry, low quality, distorted, deformed, bad anatomy, watermark, text, logo, jpeg artifacts"

# Camera motion hints for temporal variation
CAMERA_MOTIONS = [
    "slow pan left",
    "slow pan right",
    "gentle push in",
    "gentle pull back",
    "slow tilt up",
    "slow tilt down",
    "static shot",
    "slight tracking shot",
]

def generate_image(input_image, prompt, output_path, frame_num=0, total_frames=1):
    try:
        model = choose_model(prompt)
        
        # Add temporal variation based on frame position
        motion_hint = CAMERA_MOTIONS[frame_num % len(CAMERA_MOTIONS)]
        final_prompt = enrich_prompt(prompt, frame_num, total_frames, motion_hint)
        
        print(f"    🎨 Model: {model['id']}, Frame: {frame_num}/{total_frames}")
        print(f"    📝 Prompt: {final_prompt[:60]}...")

        # Check if input_image exists, otherwise fall back to txt2img
        img_exists = input_image and os.path.exists(input_image)

        if img_exists:
            # 🔁 IMG2IMG (photo → creative) - use lower strength for subtle evolution
            pipe = get_pipeline(model["id"], mode="img2img")

            init_image = Image.open(input_image).convert("RGB").resize((512, 512))

            # Lower strength for gradual evolution, higher for keyframes
            strength = 0.20 if frame_num > 0 else 0.45
            
            image = pipe(
                prompt=final_prompt,
                negative_prompt=NEGATIVE_PROMPT,
                image=init_image,
                strength=strength,
                guidance_scale=8.5,
                num_inference_steps=40
            ).images[0]

        else:
            # 🎨 TXT2IMG (no photo or file not found)
            pipe = get_pipeline(model["id"], mode="txt2img")

            image = pipe(
                prompt=final_prompt,
                negative_prompt=NEGATIVE_PROMPT,
                guidance_scale=8.5,
                num_inference_steps=40
            ).images[0]

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        image.save(output_path)
        print(f"    ✅ Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"    ❌ Error in generate_image: {e}")
        import traceback
        traceback.print_exc()
        raise

