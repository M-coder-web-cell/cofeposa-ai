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
                    "cinematic urban street shot, same person as reference image, "
                    "standing in a narrow city alley, "
                    "holding a glowing light between their hands, "
                    "realistic modern environment, brick wall, parked cars, "
                    "soft cinematic lighting, shallow depth of field, "
                    "grounded sci-fi realism, "
                    "this moment feels remembered rather than happening, "
                    "ultra realistic, film grain, natural skin texture"
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
