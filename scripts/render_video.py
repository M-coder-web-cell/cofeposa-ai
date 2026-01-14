import subprocess
import os
import tempfile
import shutil
from prompts.prompt import get_prompt
from scripts.generate_shots import generate_shots


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
    """
    Cinematic multi-shot renderer built ON TOP of render_video logic.
    """
    from PIL import Image
    import math

    shots = generate_shots()
    fps = get_prompt()["fps"]

    tmp_dir = tempfile.mkdtemp(prefix="cinematic_")
    clips = []

    try:
        base_img = Image.open(image_local).convert("RGB")

        for idx, shot in enumerate(shots):
            shot_out = os.path.join(tmp_dir, f"shot_{idx}.mp4")

            # Temporarily override env vars per shot
            os.environ["KB_ZOOM"] = str(
                shot["end_zoom"] - shot["start_zoom"]
            )

            os.environ["VIDEO_W"] = os.environ.get("VIDEO_W", "1280")
            os.environ["VIDEO_H"] = os.environ.get("VIDEO_H", "720")

            # Slice audio duration logically
            render_video(
                image_local=image_local,
                audio_local=audio_local,
                output_local=shot_out
            )

            clips.append(shot_out)

        # Stitch shots together
        concat_file = os.path.join(tmp_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-i", audio_local,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_local
        ], check=True)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return output_local

