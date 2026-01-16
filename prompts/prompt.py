def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "zeus.webp")  # reference image

    return {
        "title": "Prometheus and the Fire of Humanity",
        "fps": 7,
        "topic": "Greek mythology, rebellion, sacrifice, fire, Zeus, divine war",

        "shots": [
            {
                "prompt": (
                    "epic cinematic wide shot of Prometheus, a powerful ancient titan, "
                    "standing on a massive rocky cliff beneath a storm-filled sky, "
                    "holding a blazing golden fire stolen from Olympus, "
                    "firelight illuminating his face and muscular form, "
                    "Zeus visible faintly in the clouds above, watching in rage, "
                    "ancient Greek myth atmosphere, thunder, wind, "
                    "ultra realistic, dark cinematic lighting, film grain"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "cinematic medium shot of Prometheus descending toward humanity, "
                    "fire cradled carefully in his hands, "
                    "ancient humans reaching out in awe and fear, "
                    "warm firelight contrasting against a dark primitive world, "
                    "symbol of knowledge, progress, rebellion, "
                    "slow emotional mythic storytelling, realistic ancient world"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "violent cinematic war shot of Zeus, king of the gods, "
                    "standing in the sky surrounded by lightning and storm clouds, "
                    "throwing divine thunderbolts in fury, "
                    "Olympian war energy, cosmic power, rage and judgment, "
                    "epic god-scale battle atmosphere, ultra realistic, dramatic lighting"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "dark tragic cinematic shot of Prometheus chained to a massive mountain, "
                    "heavy iron chains binding his arms and torso, "
                    "storm raging overhead, Zeus watching from the heavens, "
                    "an eagle descending from the sky, "
                    "Prometheus unbroken, firelight still glowing faintly in his eyes, "
                    "eternal punishment for humanity’s gift, "
                    "powerful mythic ending, perfect reel loop frame"
                ),
                "duration": 5,
                "image_s3": f"file://{default_image}"
            }
        ],

        "duration": 20
    }
