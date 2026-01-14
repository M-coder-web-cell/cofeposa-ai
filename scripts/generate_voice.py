import os
import subprocess
import wave

from prompts.prompt import get_prompt

def generate_voice(text, output_local):
    if not text:
        text = " "  # fallback empty text

    os.makedirs(os.path.dirname(output_local), exist_ok=True)

    try:
        subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
        return output_local
    except Exception:
        print("⚠️ TTS failed, generating silent audio")
        duration = int(get_prompt().get("duration", 30))
        sample_rate = 16000
        n_frames = sample_rate * max(1, duration)
        with wave.open(output_local, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b"\x00\x00" * n_frames)
        return output_local
