from graph.graph import build_graph

if __name__ == "__main__":
    graph = build_graph()

    result = graph.invoke({
        "title": "",
        "script": None,
        "image_path": None,
        "voice_path": None,
        "video_path": None,
        "fps": 24
    })

    print("🎉 Final video:", result["video_path"])
