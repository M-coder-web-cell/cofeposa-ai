from typing import TypedDict, Optional

class VideoState(TypedDict):
    title: str
    script: Optional[str]
    shots: Optional[list]
    frame_paths: Optional[list]
    image_path: Optional[str]   # S3
    voice_path: Optional[str]   # S3
    voice_s3_uri: Optional[str]  # S3 URI for voice
    video_path: Optional[str]   # S3
    fps: int
