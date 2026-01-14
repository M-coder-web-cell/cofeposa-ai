
import subprocess
import wave
import contextlib
import os
from prompts.prompt import get_prompt


def generate_voice(text, output_local):
    if text is None:
        raise ValueError("No text provided to generate_voice")

    try:
        # Attempt to use TTS CLI (like Coqui TTS)
        subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
        return
    except Exception as e:
        print("⚠️ TTS CLI failed, generating silent fallback —", e)

    # Fallback: generate silent audio with same duration as prompt
    os.makedirs(os.path.dirname(output_local), exist_ok=True)
    prompt = get_prompt()
    duration = int(prompt.get("duration", 30))  # default 30 seconds
    sample_rate = 16000
    n_channels = 1
    sampwidth = 2
    n_frames = sample_rate * max(1, duration)

    with wave.open(output_local, "w") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)