import os
import tempfile
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from prompts.prompt import get_prompt

def render_single_shot(image_local, audio_local, output_local, title=None, duration=None):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)
    fps = get_prompt().get("fps", 24)
    duration = duration or get_prompt().get("duration", 10)
    nframes = max(1, int(duration * fps))

    zoom_amount = float(os.environ.get("KB_ZOOM", "0.2"))
    out_w = int(os.environ.get("VIDEO_W", "1280"))
    out_h = int(os.environ.get("VIDEO_H", "720"))

    frames_dir = tempfile.mkdtemp(prefix="frames_")

    try:
        img = Image.open(image_local).convert("RGB")
        iw, ih = img.size

        for i in range(nframes):
            t = i / max(1, nframes-1)
            zoom = 1.0 + zoom_amount * t
            scaled_w, scaled_h = int(out_w*zoom), int(out_h*zoom)
            scale = max(scaled_w/iw, scaled_h/ih)
            rw, rh = int(iw*scale), int(ih*scale)
            resized = img.resize((rw,rh), Image.LANCZOS)
            angle = (t-0.5) * 1.0
            rotated = resized.rotate(angle, resample=Image.BICUBIC, expand=False)
            left, top = (rw - out_w)//2, (rh - out_h)//2
            frame = rotated.crop((left, top, left + out_w, top + out_h))

            frame = ImageEnhance.Brightness(frame).enhance(1.05)
            frame = ImageEnhance.Contrast(frame).enhance(1.1)
            frame = ImageEnhance.Color(frame).enhance(1.2)

            if title and i < 40:
                draw = ImageDraw.Draw(frame)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                except Exception:
                    font = ImageFont.load_default()
                draw.text((50,50), title, fill=(255,255,255), font=font)

            frame.save(os.path.join(frames_dir, f"frame_{i:06d}.png"))

        subprocess.run([
            "ffmpeg","-y","-r",str(fps),
            "-i", os.path.join(frames_dir,"frame_%06d.png"),
            "-i", audio_local,
            "-c:v","libx264",
            "-pix_fmt","yuv420p",
            "-c:a","aac",
            "-shortest",
            output_local
        ], check=True)
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)

    return output_local

def render_cinematic_video(state):
    """
    state must contain:
      - state['image_paths']: list of images for shots
      - state['voice_path']: narration audio
      - state['shots']: list of shot dicts with duration/prompt
    """
    tmp_dir = tempfile.mkdtemp(prefix="cinematic_")
    clips = []

    try:
        for idx, img_path in enumerate(state["image_paths"]):
            shot_out = os.path.join(tmp_dir, f"shot_{idx}.mp4")
            duration = state["shots"][idx]["duration"] if "shots" in state else None
            render_single_shot(img_path, state["voice_path"], shot_out,
                               title=state["shots"][idx]["prompt"] if "shots" in state else None,
                               duration=duration)
            clips.append(shot_out)

        concat_file = os.path.join(tmp_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        output_video = "/workspace/tmp/final_video.mp4"
        subprocess.run([
            "ffmpeg","-y","-f","concat","-safe","0",
            "-i", concat_file,
            "-i", state["voice_path"],
            "-c:v","libx264",
            "-c:a","aac",
            "-shortest",
            output_video
        ], check=True)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    state["video_path"] = output_video
    return state
