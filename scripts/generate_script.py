import os
from prompts.prompt import get_prompt

# Try to load a local LLM; if unavailable, fall back to a simple stub.
MODEL_PATH = "/workspace/models/llm/pythia-2.8b"

_USE_STUB = False
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )

    def generate_script():
        topic = get_prompt()["topic"]
        prompt = f"Write a dramatic 30 second narration about {topic}"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        output = model.generate(**inputs, max_new_tokens=200)
        return tokenizer.decode(output[0], skip_special_tokens=True)

except Exception as e:
    _USE_STUB = True
    print("Warning: LLM model unavailable, using text stub —", e)

    def generate_script():
        prompt = get_prompt()
        topic = prompt.get("topic", "an interesting topic")
        title = prompt.get("title") or "Untitled"
        return (
            f"{title} — A dramatic narration about {topic}. "
            "In a world shaped by technology, the boundaries between human and machine blur. "
            "This thirty-second narration explores uncertainty, hope, and the choices ahead."
        )
