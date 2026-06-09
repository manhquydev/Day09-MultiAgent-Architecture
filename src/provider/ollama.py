from __future__ import annotations

from langchain_ollama import ChatOllama

from app.config import Settings


def build_ollama_model(settings: Settings) -> ChatOllama:
    import os
    
    kwargs = {
        "model": settings.model,
        "base_url": settings.ollama_base_url,
        "temperature": settings.temperature,
    }
    
    num_predict = os.getenv("OLLAMA_NUM_PREDICT")
    if num_predict:
        kwargs["num_predict"] = int(num_predict)
        
    num_ctx = os.getenv("OLLAMA_NUM_CTX")
    if num_ctx:
        kwargs["num_ctx"] = int(num_ctx)
        
    format_type = os.getenv("OLLAMA_FORMAT")
    if format_type:
        kwargs["format"] = format_type
        
    return ChatOllama(**kwargs)
