
import subprocess
import wave
import contextlib
import os


def generate_voice(text, output_local):
    if text is None:
        raise ValueError("No text provided to generate_voice")

    # Try to run a TTS CLI; on failure, write a short silent WAV as a fallback
    try:
        subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
    except Exception as e:
        print("Warning: TTS CLI failed, creating silent WAV fallback —", e)
        os.makedirs(os.path.dirname(output_local), exist_ok=True)
        # create 1 second of silence at 16kHz
        sample_rate = 16000
        n_channels = 1
        sampwidth = 2
        n_frames = sample_rate * 1
        with wave.open(output_local, "w") as wf:
            wf.setnchannels(n_channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(sample_rate)
            wf.writeframes(b"\x00\x00" * n_frames)
