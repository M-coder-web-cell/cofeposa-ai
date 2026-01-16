def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "echoes.webp")  # replace later if needed

    return {
        "title": "Echoes of the Forgotten Age",
        "fps": 7,
        "topic": "Ancient history, myth, lost civilizations, timeless legacy",

        "shots": [
            {
                "prompt": (
                    "cinematic wide shot of an ancient forgotten city emerging from morning mist, "
                    "massive stone temples and ruins covered in moss, "
                    "golden sunrise light breaking through clouds, "
                    "mythical atmosphere, sense of lost civilization, "
                    "slow camera push forward, subtle fog movement, "
                    "epic yet calm, historical fantasy, ultra realistic, "
                    "film grain, timeless ancient world aesthetic"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "medium cinematic shot of a lone ancient traveler or warrior seen from behind, "
                    "wearing flowing robes or armor, standing before towering ruins, "
                    "tattered banners moving gently in the wind, "
                    "soft dramatic lighting, mysterious mood, "
                    "mythical history, quiet power, slow motion feel, "
                    "ancient legend atmosphere"
                ),
                "duration": 2
            },
            {
                "prompt": (
                    "close cinematic shot of ancient stone carvings and symbols glowing faintly, "
                    "weathered inscriptions telling forgotten stories, "
                    "dust particles floating in the air, "
                    "warm torchlight, mystical energy, "
                    "deep history, secrets of the past, "
                    "slow, hypnotic, cinematic detail"
                ),
                "duration": 2
            },
            {
                "prompt": (
                    "wide final cinematic shot of the ancient city fading into mist, "
                    "sun setting behind massive stone structures, "
                    "sense of eternity and legend, "
                    "mythical silence, peaceful yet powerful ending, "
                    "perfect loop-friendly frame, "
                    "ancient history reel aesthetic"
                ),
                "duration": 3
            }
        ],

        "duration": 10
    }
