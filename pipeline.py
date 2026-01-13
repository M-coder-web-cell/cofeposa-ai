from graph.graph import build_graph

if __name__ == "__main__":
    graph = build_graph()

    initial_state = {
        "title": "",
        "script": None,
        "image_path": None,
        "voice_path": None,
        "video_path": None,
        "fps": 24
    }

    result = graph.invoke(initial_state)
    print("🎉 Video generated at:", result["video_path"])
