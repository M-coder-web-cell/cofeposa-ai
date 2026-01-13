from langgraph.graph import StateGraph
from graph.state import VideoState

from graph.nodes.planner import planner_node
from graph.nodes.script import script_node
from graph.nodes.image import image_node
from graph.nodes.voice import voice_node
from graph.nodes.video import video_node

def build_graph():
    graph = StateGraph(VideoState)

    graph.add_node("planner", planner_node)
    graph.add_node("script", script_node)
    graph.add_node("image", image_node)
    graph.add_node("voice", voice_node)
    graph.add_node("video", video_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "script")
    graph.add_edge("script", "image")
    graph.add_edge("image", "voice")
    graph.add_edge("voice", "video")
    graph.set_finish_point("video")

    return graph.compile()
