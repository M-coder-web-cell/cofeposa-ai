def get_prompt():
    """
    Returns the main prompt configuration for cinematic video generation.
    Supports multiple shots with individual prompts and durations.
    """
    return {
        "title": "AI Predicts the End of Humanity",
        "fps": 24,  # frames per second for video
        "topic": "AI taking over humanity",
        "shots": [
            {
                "prompt": "Cinematic futuristic megacity, neon lights, AI core",
                "duration": 4  # duration in seconds for this shot
            },
            {
                "prompt": "AI control room with holographic screens, glowing data streams",
                "duration": 3
            },
            {
                "prompt": "Robots walking through dark city streets, foggy atmosphere",
                "duration": 3
            }
        ],
        # Total duration in seconds (sum of all shots)
        "duration": 10
    }
