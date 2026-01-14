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

    # Generate frames with Pillow (robust) and encode with ffmpeg.
    try:
        from PIL import Image
    except Exception:
        Image = None

    frames_dir = None
    try:
        if Image is not None and os.path.exists(image_input):
            frames_dir = tempfile.mkdtemp(prefix="kb_frames_")
            img = Image.open(image_input).convert("RGB")
            iw, ih = img.size

            for i in range(nframes):
                t = i / max(1, nframes - 1)
                zoom = 1.0 + zoom_amount * t

                scaled_w = int(out_w * zoom)
                scaled_h = int(out_h * zoom)

                scale_factor = max(scaled_w / iw, scaled_h / ih)
                res_w = max(1, int(iw * scale_factor))
                res_h = max(1, int(ih * scale_factor))
                resized = img.resize((res_w, res_h), Image.LANCZOS)

                left = max(0, (res_w - out_w) // 2)
                top = max(0, (res_h - out_h) // 2)
                frame = resized.crop((left, top, left + out_w, top + out_h))

                frame_path = os.path.join(frames_dir, f"frame_{i:06d}.png")
                frame.save(frame_path)

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-r", str(fps),
                "-i", os.path.join(frames_dir, "frame_%06d.png"),
                "-i", audio_local,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                "-r", str(fps),
                output_local
            ]

            subprocess.run(ffmpeg_cmd, check=True)
        else:
            # Fallback: simple ffmpeg without ken-burns
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
            subprocess.run(ffmpeg_cmd, check=True)
    finally:
        if frames_dir:
            shutil.rmtree(frames_dir, ignore_errors=True)
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
