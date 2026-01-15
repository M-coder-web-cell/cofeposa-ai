from langgraph.graph import StateGraph
from graph.nodes.prompt import prompt_node
from graph.nodes.image import image_node
from graph.nodes.voice import voice_node
from graph.nodes.video import video_node

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("prompt", prompt_node)
    graph.add_node("image", image_node)
    graph.add_node("voice", voice_node)
    graph.add_node("video", video_node)

    graph.set_entry_point("prompt")
    graph.add_edge("prompt", "image")
    graph.add_edge("image", "voice")
    graph.add_edge("voice", "video")

    return graph.compile()
