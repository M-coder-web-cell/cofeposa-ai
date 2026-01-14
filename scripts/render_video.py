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


# ============================================================
# LOW-LEVEL: single-shot renderer (NO recursion, SAFE)
# ============================================================
def render_single_shot(image_local, audio_local, output_local):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    fps = get_prompt()["fps"]

    from PIL import Image

    # determine duration from audio
    try:
        import wave
        with wave.open(audio_local, "rb") as wf:
            duration = wf.getnframes() / wf.getframerate()
    except Exception:
        duration = float(get_prompt().get("duration", 30))

    nframes = max(1, int(duration * fps))

    zoom_amount = float(os.environ.get("KB_ZOOM", "0.2"))
    out_w = int(os.environ.get("VIDEO_W", "1280"))
    out_h = int(os.environ.get("VIDEO_H", "720"))

    frames_dir = tempfile.mkdtemp(prefix="frames_")

    try:
        img = Image.open(image_local).convert("RGB")
        iw, ih = img.size

        for i in range(nframes):
            t = i / max(1, nframes - 1)
            zoom = 1.0 + zoom_amount * t

            scaled_w = int(out_w * zoom)
            scaled_h = int(out_h * zoom)

            scale = max(scaled_w / iw, scaled_h / ih)
            rw, rh = int(iw * scale), int(ih * scale)

            resized = img.resize((rw, rh), Image.LANCZOS)
            left = (rw - out_w) // 2
            top = (rh - out_h) // 2

            frame = resized.crop((left, top, left + out_w, top + out_h))
            frame.save(os.path.join(frames_dir, f"frame_{i:06d}.png"))

        subprocess.run([
            "ffmpeg", "-y",
            "-r", str(fps),
            "-i", os.path.join(frames_dir, "frame_%06d.png"),
            "-i", audio_local,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-shortest",
            output_local
        ], check=True)

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)

    return output_local


# ============================================================
# HIGH-LEVEL: cinematic multi-shot renderer
# ============================================================
def render_cinematic_video(image_local, audio_local, output_local):
    shots = generate_shots()
    tmp_dir = tempfile.mkdtemp(prefix="cinematic_")
    clips = []

    try:
        for idx, shot in enumerate(shots):
            shot_out = os.path.join(tmp_dir, f"shot_{idx}.mp4")

            os.environ["KB_ZOOM"] = str(
                shot["end_zoom"] - shot["start_zoom"]
            )

            render_single_shot(
                image_local=image_local,
                audio_local=audio_local,
                output_local=shot_out
            )

            clips.append(shot_out)

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


__all__ = [
    "render_single_shot",
    "render_cinematic_video",
]
