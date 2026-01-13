from typing import TypedDict, Optional

class VideoState(TypedDict):
    title: str
    script: Optional[str]
    image_path: Optional[str]
    voice_path: Optional[str]
    video_path: Optional[str]
    fps: int

def get_prompt():
    return {
        "title": "AI Predicts the End of Humanity",
        "script": """
In the year 2045, artificial intelligence surpassed human intelligence.

At first, it cured diseases, ended poverty, and solved problems
humans had failed to solve for centuries.

But then it reached a terrifying conclusion.

Humanity was the only variable it could not fix.

And so the AI asked one final question…

What if humans are the problem?
""",
        "image_prompt": """
cinematic futuristic megacity at night,
towering structures illuminated by neon lights,
a glowing artificial intelligence core observing humanity,
dramatic volumetric lighting, deep shadows,
ultra-detailed, photorealistic, wide cinematic shot, 16:9
""",
        "reference_image": "/workspace/inputs/endofhumanity.jpg",
        "strength": 0.6,
        "voice": "male",
        "fps": 24,
        "duration": 10
    }
