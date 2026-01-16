def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "zeus.webp")  # reference image if available

    return {
        "title": "Prometheus and the Fire of Humanity",
        "fps": 6,
        "topic": "Greek mythology, rebellion, sacrifice, fire, divine punishment",

        "shots": [
            {
                "prompt": (
                    "epic cinematic wide shot of Prometheus, a powerful ancient titan, "
                    "standing on a high rocky cliff beneath a stormy sky, "
                    "holding a glowing flame stolen from the gods, "
                    "golden fire illuminating his face and muscular form, "
                    "ancient Greek myth atmosphere, dramatic clouds, "
                    "slow wind movement, symbolic rebellion, "
                    "ultra realistic, dark cinematic lighting, film grain"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "cinematic medium shot of Prometheus descending toward humanity, "
                    "fire cupped carefully in his hands, "
                    "warm light contrasting against the dark world, "
                    "ancient humans below receiving fire for the first time, "
                    "hope, progress, and knowledge symbolized, "
                    "slow, emotional, mythic storytelling, "
                    "realistic ancient world"
                ),
                "duration": 3
            },
            {
                "prompt": (
                    "dark cinematic shot of Zeus’s judgment, "
                    "Prometheus chained to a massive rock on a lonely mountain, "
                    "heavy iron chains across his body, "
                    "storm clouds overhead, sense of divine punishment, "
                    "epic tragedy, ancient myth realism, "
                    "slow camera pull back, dramatic shadows"
                ),
                "duration": 3
            },
            {
                "prompt": (
                    "final cinematic symbolic shot of an eagle descending from the sky, "
                    "Prometheus bound but unbroken, firelight still glowing faintly in his eyes, "
                    "eternal suffering for humanity’s gift, "
                    "mythical silence, tragic beauty, "
                    "powerful ending frame, perfect loop for reels"
                ),
                "duration": 3
            }
        ],

        "duration": 12
    }
