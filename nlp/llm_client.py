"""
Local Ollama Client Module for Judi Legal Support Chatbot.

Interfaces with the local Ollama server running Qwen to generate grounded,
empathetic legal summary responses based strictly on the structured report data.
"""

import os
import logging
from typing import Any
import requests

from nlp.prompt_builder import build_prompts

logger = logging.getLogger("judi.llm_client")

# Configuration defaults
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:1.5b"
DEFAULT_TIMEOUT_SECONDS = 30


def get_ollama_base_url() -> str:
    """Get the Ollama base URL from environment or fallback default."""
    return os.environ.get("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL).rstrip("/")


def get_ollama_model() -> str:
    """Get the Ollama model name from environment or fallback default."""
    return os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)


def get_request_timeout() -> int:
    """Get the request timeout in seconds."""
    try:
        return int(os.environ.get("OLLAMA_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS)))
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS


def generate_legal_summary(report_data: dict[str, Any]) -> str | None:
    """
    Generate a natural language legal preliminary summary using the local Ollama Qwen model.
    
    Args:
        report_data: Structured report dictionary containing classified categories,
                     laws, steps, context, resources, and warnings.
                     
    Returns:
        Generated markdown summary string if successful, or None if Ollama is unavailable/fails.
    """
    if not report_data or not isinstance(report_data, dict):
        return None

    # Only process valid complaints
    if report_data.get("is_complaint") is False or report_data.get("category") == "not_complaint":
        return None

    base_url = get_ollama_base_url()
    model = get_ollama_model()
    timeout = get_request_timeout()

    system_prompt, user_prompt = build_prompts(report_data)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
        }
    }

    endpoint = f"{base_url}/api/chat"

    try:
        response = requests.post(endpoint, json=payload, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            message_obj = result.get("message", {})
            content = message_obj.get("content", "")
            if content and content.strip():
                return content.strip()
            logger.warning("Ollama returned empty response content")
            return None
        else:
            logger.warning(
                f"Ollama API returned HTTP {response.status_code}: {response.text[:200]}"
            )
            return None
    except requests.exceptions.Timeout:
        logger.warning(f"Ollama request timed out after {timeout}s at {endpoint}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"Could not connect to local Ollama server at {endpoint}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error when querying Ollama: {e}")
        return None
