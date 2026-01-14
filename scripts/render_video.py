from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def render_cinematic_video(image_local, audio_local, output_local, title=None):
    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    fps = get_prompt()["fps"]

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

            # Subtle rotation (-0.5 to +0.5 degrees)
            angle = (t - 0.5) * 1.0
            rotated = resized.rotate(angle, resample=Image.BICUBIC, expand=False)

            left = (rw - out_w) // 2
            top = (rh - out_h) // 2
            frame = rotated.crop((left, top, left + out_w, top + out_h))

            # Color grading: brightness + contrast + saturation
            frame = ImageEnhance.Brightness(frame).enhance(1.05)
            frame = ImageEnhance.Contrast(frame).enhance(1.1)
            frame = ImageEnhance.Color(frame).enhance(1.2)

            # Title overlay in first 40 frames
            if title and i < 40:
                draw = ImageDraw.Draw(frame)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                except Exception:
                    font = ImageFont.load_default()
                draw.text((50, 50), title, fill=(255, 255, 255), font=font)

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
