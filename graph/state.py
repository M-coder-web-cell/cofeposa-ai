from typing import TypedDict, Optional

class VideoState(TypedDict):
    title: str
    script: Optional[str]
    image_path: Optional[str]   # S3
    voice_path: Optional[str]   # S3
    video_path: Optional[str]   # S3
    fps: int
