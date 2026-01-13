import subprocess
import os
import boto3
from prompts.prompt import get_prompt

s3 = boto3.client("s3")
BUCKET = os.environ["S3_BUCKET"]

def render_video(image_local, audio_local, output_local):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    fps = get_prompt()["fps"]

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_local,
            "-i", audio_local,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-r", str(fps),
            output_local
        ],
        check=True
    )

    # Upload to S3
    s3_key = f"outputs/{os.path.basename(output_local)}"
    s3.upload_file(output_local, BUCKET, s3_key)

    return f"s3://{BUCKET}/{s3_key}"
