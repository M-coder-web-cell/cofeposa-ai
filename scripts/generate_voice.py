
import subprocess
import wave
import contextlib
import os
from prompts.prompt import get_prompt


def generate_voice(text, output_local):
    if text is None:
        raise ValueError("No text provided to generate_voice")

    # Try to run a TTS CLI; on failure, write a silent WAV fallback whose
    # duration matches the prompt duration (so the final video isn't only 1s).
    try:
        subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
        return
    except Exception as e:
        print("Warning: TTS CLI failed, creating silent WAV fallback —", e)

    os.makedirs(os.path.dirname(output_local), exist_ok=True)
    # create silence with duration derived from the prompt (default 30s)
    prompt = get_prompt()
    duration = int(prompt.get("duration", 30))
    sample_rate = 16000
    n_channels = 1
    sampwidth = 2
    n_frames = sample_rate * max(1, duration)
    with wave.open(output_local, "w") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)
