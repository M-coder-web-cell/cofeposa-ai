import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

_PIPELINES = {}

def get_pipeline(model_id, mode="txt2img"):
    key = f"{model_id}:{mode}"

    if key not in _PIPELINES:
        if mode == "img2img":
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_id, torch_dtype=torch.float16
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, torch_dtype=torch.float16
            )

        pipe = pipe.to("cuda")
        pipe.enable_xformers_memory_efficient_attention()
        _PIPELINES[key] = pipe

    return _PIPELINES[key]
