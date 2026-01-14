from prompts.prompt import get_prompt

def prompt_node(state):
    prompt = get_prompt()
    shots = prompt["shots"]
    script = prompt.get("script") or " ".join([shot["prompt"] for shot in shots])

    return {
        **state,
        "shots": shots,
        "fps": prompt.get("fps", 24),
        "title": prompt.get("title"),
        "duration": prompt.get("duration"),
        "script": script
    }
