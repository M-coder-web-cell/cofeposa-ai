"""
Generate cinematic shot plan from a single image.
This does NOT generate video yet.
It only defines HOW the video should move.
"""

from typing import List, Dict
from prompts.prompt import get_prompt


def generate_shots() -> List[Dict]:
    """
    Returns a list of shot definitions.
    Each shot becomes a short cinematic clip.
    """

    prompt = get_prompt()
    duration = int(prompt.get("duration", 30))

    # 3-shot cinematic structure (industry standard)
    shots = [
        {
            "id": 1,
            "type": "push_in",
            "start_zoom": 1.0,
            "end_zoom": 1.2,
            "pan": (0.0, 0.0),
            "duration": duration * 0.4,
            "mood": "calm"
        },
        {
            "id": 2,
            "type": "pan_left",
            "start_zoom": 1.2,
            "end_zoom": 1.25,
            "pan": (-0.1, 0.0),
            "duration": duration * 0.3,
            "mood": "curious"
        },
        {
            "id": 3,
            "type": "dramatic_close",
            "start_zoom": 1.25,
            "end_zoom": 1.4,
            "pan": (0.05, -0.05),
            "duration": duration * 0.3,
            "mood": "intense"
        }
    ]

    return shots
