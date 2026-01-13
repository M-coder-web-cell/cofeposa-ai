from scripts.generate_script import generate_script

def script_node(state):
    state["script"] = generate_script()
    return state
