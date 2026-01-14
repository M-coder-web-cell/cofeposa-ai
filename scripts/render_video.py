import subprocess
import os
from prompts.prompt import get_prompt

try:
    import boto3
    _HAS_BOTO3 = True
except Exception:
    boto3 = None
    _HAS_BOTO3 = False

BUCKET = os.environ.get("S3_BUCKET")

if _HAS_BOTO3 and BUCKET:
    s3 = boto3.client("s3")
else:
    s3 = None


def render_video(image_local, audio_local, output_local):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    fps = get_prompt()["fps"]
    # Ensure image dimensions are even (width/height divisible by 2) by
    # padding if necessary. This avoids encoder errors like "width not
    # divisible by 2" from libx264 when input images have odd sizes.
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_local,
        "-i", audio_local,
        # pad width/height to even values if odd
        "-vf", "pad=iw+mod(iw,2):ih+mod(ih,2)",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-r", str(fps),
        output_local
    ]

    subprocess.run(ffmpeg_cmd, check=True)

    # Upload to S3 if configured
    if s3 and BUCKET:
        s3_key = f"outputs/{os.path.basename(output_local)}"
        s3.upload_file(output_local, BUCKET, s3_key)
        return f"s3://{BUCKET}/{s3_key}"

    # Otherwise return local path
    return output_local
