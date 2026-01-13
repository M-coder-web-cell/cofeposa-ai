from typing import TypedDict, Optional

class VideoState(TypedDict):
    title: str
    script: Optional[str]
    image_path: Optional[str]
    voice_path: Optional[str]
    video_path: Optional[str]
    fps: int
