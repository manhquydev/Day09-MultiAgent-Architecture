from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.config import Settings


def build_openai_model(settings: Settings) -> ChatOpenAI:
    import os
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required for provider=openai")
    
    kwargs = {
        "model": settings.model,
        "api_key": settings.openai_api_key,
        "temperature": settings.temperature,
    }
    
    max_tokens = os.getenv("OPENAI_MAX_TOKENS")
    if max_tokens:
        kwargs["max_tokens"] = int(max_tokens)
        
    openai_api_base = os.getenv("OPENAI_API_BASE")
    if openai_api_base:
        kwargs["base_url"] = openai_api_base
        
    top_p = os.getenv("OPENAI_TOP_P")
    if top_p:
        kwargs["top_p"] = float(top_p)
        
    return ChatOpenAI(**kwargs)
