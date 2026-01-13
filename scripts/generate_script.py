import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompts.prompt import get_prompt

MODEL_NAME = "TheBloke/vicuna-7B-1.1-HF"
CACHE_DIR = "/workspace/cache"

# Load tokenizer & model from HF repo (automatic caching)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    cache_dir=CACHE_DIR,
    torch_dtype=torch.float16,
    device_map="auto"
)

def generate_script():
    prompt_text = get_prompt()["title"]

    prompt = f"""
Write a dramatic 30 second YouTube narration about:
{prompt_text}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=200)

    return tokenizer.decode(output[0], skip_special_tokens=True)
