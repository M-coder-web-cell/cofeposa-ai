from typing import TypedDict, Optional

class VideoState(TypedDict):
    title: str
    script: Optional[str]
    shots: Optional[list]
    frame_paths: Optional[list]
    voice_path: Optional[str]
    voice_s3_uri: Optional[str]
    video_path: Optional[str]
    fps: int

