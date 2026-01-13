import subprocess

def generate_voice(text, output):
    subprocess.run([
        "tts",
        "--text", text,
        "--out_path", output
    ])
