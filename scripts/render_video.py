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

    # Determine audio duration to drive the Ken-Burns effect length. Fall
    # back to prompt duration if audio duration can't be read.
    duration = None
    try:
        import wave as _wave
        with _wave.open(audio_local, "rb") as wf:
            duration = wf.getnframes() / float(wf.getframerate())
    except Exception:
        try:
            prompt = get_prompt()
            duration = float(prompt.get("duration", 30))
        except Exception:
            duration = 30.0

    nframes = max(1, int(duration * fps))

    # Ken-Burns parameters (can be tuned via env vars)
    zoom_amount = float(os.environ.get("KB_ZOOM", "0.2"))  # total additional zoom (e.g., 0.2 -> 20%)
    out_w = int(os.environ.get("VIDEO_W", "1280"))
    out_h = int(os.environ.get("VIDEO_H", "720"))

    # Build ffmpeg filter_complex for zoompan. We use `n` (frame index)
    # to compute an increasing zoom from 1 -> 1+zoom_amount over nframes.
    z_expr = f"1+{zoom_amount}*n/{nframes}"
    filter_complex = (
        f"[0:v]scale={out_w}:{out_h},"
        f"zoompan=z={z_expr}:x=(iw-iw/zoom)/2:y=(ih-ih/zoom)/2:d=1:s={out_w}x{out_h},"
        f"fps={fps},format=yuv420p[v]"
    )

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_input,
        "-i", audio_local,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
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
