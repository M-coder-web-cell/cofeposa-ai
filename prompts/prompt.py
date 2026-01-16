def get_prompt():
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "solo_travel.webp")

    return {
        "title": "Walking Into Freedom",
        "fps": 7,
        "topic": "Solo travel, inner peace, self discovery",

        "shots": [
            {
                "prompt": (
                    "cinematic wide shot of a lone traveler walking along a wooden path "
                    "through vast green grasslands, early golden hour light, "
                    "soft clouds in the sky, peaceful atmosphere, "
                    "slow camera push forward, gentle wind moving the grass, "
                    "natural colors, film grain, ultra realistic, "
                    "emotional and calming solo travel aesthetic"
                ),
                "duration": 3,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": (
                    "medium cinematic shot of the traveler from behind, "
                    "backpack visible, footsteps on the path, "
                    "sunlight breaking through clouds, "
                    "shallow depth of field, calm and reflective mood, "
                    "soft cinematic lighting, minimal motion, "
                    "Instagram reel style, peaceful journey"
                ),
                "duration": 3
            },
            {
                "prompt": (
                    "close cinematic shot of tall grass swaying in the wind, "
                    "wooden path leading into the distance, "
                    "warm sunset tones, dreamy atmosphere, "
                    "slow motion feel, natural film look, "
                    "quiet, emotional, introspective travel moment"
                ),
                "duration": 3
            },
            {
                "prompt": (
                    "wide ending shot of the traveler becoming smaller in the frame, "
                    "open landscape stretching endlessly, "
                    "soft fading sunlight, sense of freedom and solitude, "
                    "cinematic composition, peaceful ending, "
                    "perfect loop-friendly frame, aesthetic travel reel"
                ),
                "duration": 6
            }
        ],

        "duration": 15
    }
