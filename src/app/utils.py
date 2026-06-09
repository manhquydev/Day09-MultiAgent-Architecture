from __future__ import annotations

import time
import random
from datetime import datetime, UTC
import json
from typing import Any, Callable, TypeVar

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage

T = TypeVar("T")


def retry_with_backoff(
    fn: Callable[[], T],
    max_retries: int = 6,
    base_delay: float = 10.0,
    max_delay: float = 90.0,
) -> T:
    """Retry fn on 429/ResourceExhausted with exponential backoff + jitter.

    Free-tier Gemini limit: 10 RPM per model. Each batch case calls the LLM
    2–4 times, so we retry automatically instead of crashing the whole batch.
    """
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            err_str = str(e)
            is_rate_limit = (
                "429" in err_str
                or "RESOURCE_EXHAUSTED" in err_str
                or "quota" in err_str.lower()
            )
            if not is_rate_limit or attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 2), max_delay)
            print(f"  [rate-limit] 429 hit, retry {attempt + 1}/{max_retries} in {delay:.1f}s...")
            time.sleep(delay)
    raise RuntimeError("retry_with_backoff: unreachable")


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def get_message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict) and "text" in p:
                parts.append(p["text"])
        return "".join(parts)
    return str(content) if content is not None else ""


def extract_json_payload(text: Any) -> dict[str, Any]:
    text_str = get_message_text(text)
    if not text_str:
        return {}
    candidate = text_str.strip()
    if candidate.startswith("```"):
        parts = [part for part in candidate.split("```") if part.strip()]
        candidate = parts[-1].replace("json", "", 1).strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(candidate[start : end + 1])
            except json.JSONDecodeError:
                return {}
    return {}


def timestamp_utc() -> str:
    return datetime.now(UTC).isoformat()


def serialize_message(message: BaseMessage) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": message.type,
        "content": message.content,
    }
    if isinstance(message, AIMessage):
        payload["tool_calls"] = message.tool_calls
    if isinstance(message, ToolMessage):
        payload["tool_name"] = message.name
        payload["tool_call_id"] = message.tool_call_id
    return payload


def list_worker_tools(messages: list[BaseMessage]) -> list[str]:
    tool_names: list[str] = []
    for message in messages:
        if isinstance(message, AIMessage):
            for tool_call in message.tool_calls:
                name = tool_call.get("name")
                if name and name not in tool_names:
                    tool_names.append(name)
    return tool_names


def get_last_ai_content(messages: list[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return str(message.content)
    return ""
