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
    # creating a small padded copy with Pillow if necessary. This avoids
    # encoder errors like "width not divisible by 2" from libx264 when
    # input images have odd sizes.
    try:
        from PIL import Image
    except Exception:
        Image = None

    image_input = image_local
    padded_tmp = None
    if Image is not None and os.path.exists(image_local):
        try:
            img = Image.open(image_local)
            w, h = img.size
            pad_w = w + (w % 2)
            pad_h = h + (h % 2)
            if pad_w != w or pad_h != h:
                padded_tmp = f"{image_local}.padded.png"
                new_img = Image.new("RGB", (pad_w, pad_h), (0, 0, 0))
                new_img.paste(img, (0, 0))
                new_img.save(padded_tmp)
                image_input = padded_tmp
        except Exception:
            # If Pillow operations fail, fall back to using the original image
            image_input = image_local

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_input,
        "-i", audio_local,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-r", str(fps),
        output_local
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    finally:
        if padded_tmp and os.path.exists(padded_tmp):
            try:
                os.remove(padded_tmp)
            except Exception:
                pass

    # Upload to S3 if configured
    if s3 and BUCKET:
        s3_key = f"outputs/{os.path.basename(output_local)}"
        s3.upload_file(output_local, BUCKET, s3_key)
        return f"s3://{BUCKET}/{s3_key}"

    # Otherwise return local path
    return output_local
