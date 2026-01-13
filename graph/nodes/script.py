from scripts.generate_script import generate_script

def script_node(state):
    script = generate_script()
    state["script"] = script
    return state
