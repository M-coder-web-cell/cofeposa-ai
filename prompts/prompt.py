def get_prompt():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..")
    default_image = os.path.join(project_root, "endofhumanity.jpg")

    return {
        "title": "Futuristic Smart City of Tomorrow",
        "fps": 24,
        "topic": "Advanced AI technology improving human life",
        "shots": [
            {
                "prompt": "Breathtaking aerial view of a futuristic smart city at golden hour, sleek towers with green gardens, flying vehicles, beautiful sunset sky",
                "duration": 8,
                "image_s3": f"file://{default_image}"
            },
            {
                "prompt": "Modern AI control center with holographic displays showing data visualizations, clean white room, soft ambient lighting, friendly robots assisting humans",
                "duration": 7
            },
            {
                "prompt": "Peaceful city street at twilight, glowing lanterns, robots carrying packages for delivery, misty atmosphere, beautiful architecture",
                "duration": 7
            },
            {
                "prompt": "Indoor futuristic workspace, humans working with AI assistants on holographic screens, warm cozy lighting, floor to ceiling windows with city view",
                "duration": 7
            }
        ],
        "duration": 29
    }

