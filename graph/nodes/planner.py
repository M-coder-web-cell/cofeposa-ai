from prompts.prompt import get_prompt

def planner_node(state):
    prompt = get_prompt()
    state["title"] = prompt["title"]
    state["fps"] = prompt["fps"]
    return state
