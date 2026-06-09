from dataclasses import replace
from langchain_core.language_models.chat_models import BaseChatModel

from app.config import Settings
from provider.custom import build_custom_model
from provider.deepseek import build_deepseek_model
from provider.gemini import build_gemini_model
from provider.ollama import build_ollama_model
from provider.openai import build_openai_model
from provider.openrouter import build_openrouter_model


def get_chat_model(
    settings: Settings,
    provider: str | None = None,
    model: str | None = None,
) -> BaseChatModel:
    builders = {
        "gemini": build_gemini_model,
        "openai": build_openai_model,
        "openrouter": build_openrouter_model,
        "ollama": build_ollama_model,
        "custom": build_custom_model,
        "deepseek": build_deepseek_model,
    }
    
    temp_settings = settings
    if provider or model:
        changes = {}
        if provider:
            changes["provider"] = provider
        if model:
            changes["model"] = model
        temp_settings = replace(settings, **changes)
        
    try:
        builder = builders[temp_settings.provider]
    except KeyError as exc:
        raise ValueError(f"Unsupported provider: {temp_settings.provider}") from exc
    return builder(temp_settings)

