def get_prompt():
    return {
        "title": "AI Predicts the End of Humanity",
        "fps": 24,
        "topic": "AI taking over humanity",
        "shots": [
            {
                "prompt": "Cinematic futuristic megacity, neon lights, AI core",
                "duration": 4,
                "image_s3": "s3://cofeposa-ai/images/endofhumanity.jpeg"
            },
            {
                "prompt": "AI control room with holographic screens",
                "duration": 3
            },
            {
                "prompt": "Robots walking through dark city streets, fog",
                "duration": 3
            }
        ],
        "duration": 10
    }
