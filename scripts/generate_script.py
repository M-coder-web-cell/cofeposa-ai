import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompts.prompt import get_prompt

MODEL_PATH = "/workspace/models/llm/pythia-2.8b"


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto"
)

def generate_script():
    topic = get_prompt()["topic"]
    prompt = f"Write a dramatic 30 second narration about {topic}"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)
