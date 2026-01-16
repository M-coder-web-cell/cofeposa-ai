def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "zeus.webp")  # reference image

    return {
        "title": "Prometheus and the Wrath of Zeus",
        "fps": 14,
        "topic": "Greek mythology, divine war, rebellion, fire, thunder, punishment",

        "shots": [
            {
                "prompt": (
                    "epic cinematic wide shot of Prometheus standing on a towering mountain cliff, "
                    "night sky tearing open above him, "
                    "holding a blazing golden fire stolen from Olympus, "
                    "violent storm clouds swirling as Zeus’s colossal silhouette forms in the sky, "
                    "lightning flashing around divine armor, "
                    "mythic scale, rebellion before a god of war, "
                    "ultra realistic, dramatic contrast, film grain"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "cinematic war shot of Zeus in full fury, "
                    "ancient god of thunder descending from the sky, "
                    "muscular divine form surrounded by crackling lightning, "
                    "throwing massive thunderbolts toward the earth, "
                    "explosions of light and energy tearing through clouds, "
                    "Olympian war atmosphere, chaos, power, destruction, "
                    "ultra realistic god-scale combat, dark cinematic lighting"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "dramatic cinematic shot of Prometheus being struck by Zeus’s thunder, "
                    "divine lightning wrapping around his body, "
                    "rocks exploding, fire falling from his hands toward humanity below, "
                    "sacrifice frozen in time, "
                    "slow-motion mythic tragedy, "
                    "epic ancient war storytelling, ultra realistic detail"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "dark final cinematic shot of Prometheus chained to a desolate mountain, "
                    "heavy iron chains glowing from divine lightning burns, "
                    "Zeus hovering in the storm above, still throwing thunder into the sky, "
                    "an eagle descending through rain and lightning, "
                    "Prometheus unbroken, eyes glowing faintly with fire, "
                    "eternal punishment, tragic beauty, "
                    "powerful ending frame, perfect reel loop"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            }
        ],

        "duration": 12
    }
