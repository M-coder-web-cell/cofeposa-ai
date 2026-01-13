
def generate_voice(text, output_local):
    subprocess.run(["tts", "--text", text, "--out_path", output_local], check=True)
