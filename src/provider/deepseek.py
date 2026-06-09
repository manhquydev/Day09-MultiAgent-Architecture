from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.config import Settings


def build_deepseek_model(settings: Settings) -> ChatOpenAI:
    import os
    api_key = settings.deepseek_api_key
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required for provider=deepseek")
    
    # Default to deepseek-chat if model is not deepseek
    model_name = settings.model
    if not model_name or "deepseek" not in model_name.lower():
        model_name = "deepseek-chat"
        
    kwargs = {
        "model": model_name,
        "api_key": api_key,
        "base_url": settings.deepseek_base_url,
        "temperature": settings.temperature,
    }
    
    max_tokens = os.getenv("DEEPSEEK_MAX_TOKENS")
    if max_tokens:
        kwargs["max_tokens"] = int(max_tokens)
        
    top_p = os.getenv("DEEPSEEK_TOP_P")
    if top_p:
        kwargs["top_p"] = float(top_p)
        
    return ChatOpenAI(**kwargs)
