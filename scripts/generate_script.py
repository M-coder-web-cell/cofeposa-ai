import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompts.prompt import get_prompt

MODEL_NAME = "eleutherai/pythia-2.8b"
CACHE_DIR = "/workspace/cache"

# Load tokenizer & model from HF repo (automatic caching)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR,local_files_only=True,use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    cache_dir=CACHE_DIR,
    torch_dtype=torch.float16,
    device_map="auto"
)
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")
def generate_script():
    prompt_text = get_prompt()["title"]

    prompt = f"""
Write a dramatic 30 second YouTube narration about:
{prompt_text}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=200)

    return tokenizer.decode(output[0], skip_special_tokens=True)
