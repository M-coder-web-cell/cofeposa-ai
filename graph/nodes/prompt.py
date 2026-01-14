from prompts.prompt import get_prompt

def prompt_node(state):
    prompt = get_prompt()

    return {
        **state,
        "shots": prompt["shots"],
        "fps": prompt.get("fps", 24),
        "title": prompt.get("title"),
        "duration": prompt.get("duration")
    }
