from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import Settings


def build_gemini_model(settings: Settings) -> ChatGoogleGenerativeAI:
    import os
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is required for provider=gemini")
    
    kwargs = {
        "model": settings.model,
        "google_api_key": settings.google_api_key,
        "temperature": settings.temperature,
    }
    
    max_tokens = os.getenv("GEMINI_MAX_TOKENS")
    if max_tokens:
        kwargs["max_output_tokens"] = int(max_tokens)
        
    top_p = os.getenv("GEMINI_TOP_P")
    if top_p:
        kwargs["top_p"] = float(top_p)
        
    return ChatGoogleGenerativeAI(**kwargs)
