
import subprocess


def generate_voice(text, output_local):
    if text is None:
        raise ValueError("No text provided to generate_voice")
    subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
