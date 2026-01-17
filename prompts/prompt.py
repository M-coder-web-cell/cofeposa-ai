def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "memories.webp")  # reference image

    return {
        "title": "A Memory From a Future Life",
        "fps": 18,
        "topic": "future memories, urban sci-fi, destiny, latent power, realism",

        "shots": [
            {
                "prompt": (
                    "cinematic ultra-close opening shot of the same person from the reference image, "
                    "standing in a narrow urban alley at night, "
                    "intense glowing light source forming in their hands, "
                    "bright energy flare visible immediately in the first frame, "
                    "high contrast lighting with deep shadows, "
                    "wet concrete reflecting the light, "
                    "subtle rain mist in the air catching the glow, "
                    "futuristic yet realistic atmosphere, "
                    "the person’s face partially lit, eyes focused and calm, "
                    "a feeling of recognition, like remembering something that hasn’t happened yet, "
                    "modern cinematic realism, anamorphic depth of field, "
                    "film grain, sharp focus, dramatic color contrast, "
                    "scroll-stopping first frame, strong focal point"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "same person, same pose and clothing, "
                    "environment subtly changed, street looks slightly emptier, "
                    "light in hands brighter and more focused, "
                    "cinematic contrast, gentle wind movement, "
                    "future memory atmosphere, "
                    "everything feels familiar but slightly off, "
                    "realistic urban sci-fi, film grain"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "same person, same framing, "
                    "nightfall version of the same alley, "
                    "street lights glowing, reflections on wet ground, "
                    "the glowing light now pulsing softly, "
                    "sense of destiny, time folding in on itself, "
                    "subtle sci-fi realism, cinematic lighting, ultra realistic"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "final cinematic shot, same person unchanged, "
                    "the alley now quiet and empty, "
                    "light in hands slowly dimming, "
                    "expression calm, as if remembering something that hasn’t happened yet, "
                    "melancholic but hopeful tone, "
                    "perfect loop ending frame, "
                    "realistic cinematic urban future memory"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            }
        ],

        "duration": 12
    }
