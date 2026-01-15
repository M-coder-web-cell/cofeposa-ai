import os
import subprocess
import wave

from prompts.prompt import get_prompt

def generate_voice(text, output_local, duration=None):
    if not text:
        text = " "  # fallback empty text

    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    try:
        # Try TTS with duration if supported
        if duration:
            result = subprocess.run(
                ["tts", "--text", text, "--out_path", output_local, "--duration", str(duration)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"⚠️ TTS --duration not supported: {result.stderr}")
                # Fall through to generate silent audio of exact duration
                raise Exception("Duration arg not supported")
        else:
            subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
        return output_local
    except Exception as e:
        print(f"⚠️ TTS failed ({e}), generating silent audio of exact duration: {duration}s")
        # Generate silent audio with EXACT duration
        if duration is None:
            duration = int(get_prompt().get("duration", 30))
        sample_rate = 16000
        n_frames = sample_rate * max(1, duration)
        with wave.open(output_local, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b"\x00\x00" * n_frames)
        return output_local

