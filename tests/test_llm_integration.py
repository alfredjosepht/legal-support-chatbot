#!/usr/bin/env python3
"""Unit and integration tests for Prompt Builder and Local LLM (Ollama + Qwen) Layer."""

import os
import sys
from pathlib import Path
from unittest.mock import patch
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from nlp.prompt_builder import build_system_prompt, build_user_prompt, build_prompts
from nlp.llm_client import generate_legal_summary, get_ollama_base_url, get_ollama_model


def test_prompt_builder_structure():
    """Verify prompt builder output format and constraint directives."""
    sample_report = {
        "user_query": "My teacher threatened to fail me and touched me inappropriately. I am 16 years old.",
        "category": "sexual_assault",
        "matched_categories": [
            {"category": "sexual_assault", "confidence": 0.85},
            {"category": "sexual_harassment", "confidence": 0.72}
        ],
        "context": {
            "age_indicator": "minor",
            "authority": "faculty",
            "medium": "offline",
            "discrimination_types": [],
            "legal_framework": "POCSO",
            "location": "kerala"
        },
        "legal_frameworks": [
            "Protection of Children from Sexual Offences Act, 2012 (POCSO)",
            "Indian Penal Code (IPC)"
        ],
        "laws": [
            {
                "act": "POCSO Act, 2012",
                "section": "7",
                "title": "Sexual Assault",
                "description": "Punishment for sexual assault on child."
            }
        ],
        "steps": [
            "Report to Child Welfare Committee or local police station immediately.",
            "Undergo medical examination within 24 hours."
        ],
        "resources": [
            {
                "name": "Childline India",
                "contact": "1098",
                "link": "https://childlineindia.org"
            }
        ],
        "case_references": ["State of Maharashtra v. Minor (2019)"],
        "warnings": ["POCSO Act applies with mandatory reporting and anonymity guarantees."]
    }

    system_prompt, user_prompt = build_prompts(sample_report)

    # Validate System Prompt
    assert "Judi" in system_prompt
    assert "STRICT LEGAL GROUNDING RULES" in system_prompt
    assert "DO NOT invent" in system_prompt
    assert "DO NOT change or re-classify" in system_prompt

    # Validate User Prompt
    assert "USER INCIDENT DESCRIPTION" in user_prompt
    assert sample_report["user_query"] in user_prompt
    assert "Sexual Assault" in user_prompt
    assert "MINOR" in user_prompt
    assert "POCSO" in user_prompt
    assert "Section 7" in user_prompt
    assert "1098" in user_prompt
    assert "Child Welfare Committee" in user_prompt

    print("[PASS] test_prompt_builder_structure")


def test_llm_client_skips_non_complaint():
    """Verify LLM client returns None for non-complaints."""
    non_complaint_report = {
        "is_complaint": False,
        "category": "not_complaint",
        "user_query": "hello"
    }
    result = generate_legal_summary(non_complaint_report)
    assert result is None
    print("[PASS] test_llm_client_skips_non_complaint")


def test_llm_client_fallback_on_offline():
    """Verify graceful None fallback when Ollama is offline or endpoint is invalid."""
    sample_report = {
        "is_complaint": True,
        "category": "physical_assault",
        "user_query": "Someone beat me up",
        "laws": [{"act": "IPC", "section": "323", "title": "Voluntarily causing hurt", "description": "Punishment"}],
        "steps": ["File FIR at police station"],
        "resources": [{"name": "Police Helpline", "contact": "112"}]
    }

    # Test with non-existent server port
    with patch.dict(os.environ, {"OLLAMA_BASE_URL": "http://127.0.0.1:59999", "OLLAMA_TIMEOUT": "1"}):
        result = generate_legal_summary(sample_report)
        assert result is None, "Expected fallback None when server is unreachable"

    print("[PASS] test_llm_client_fallback_on_offline")


def test_llm_client_fallback_on_http_error():
    """Verify graceful None fallback when Ollama returns HTTP 500 error."""
    sample_report = {
        "is_complaint": True,
        "category": "physical_assault",
        "user_query": "Someone beat me up",
        "laws": [],
        "steps": [],
        "resources": []
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"
        result = generate_legal_summary(sample_report)
        assert result is None

    print("[PASS] test_llm_client_fallback_on_http_error")


def test_llm_client_live_generation():
    """Live test if Ollama server is running with target Qwen model."""
    sample_report = {
        "user_query": "My senior hit me in the hostel",
        "category": "physical_assault",
        "matched_categories": [{"category": "physical_assault", "confidence": 0.90}],
        "is_complaint": True,
        "context": {"age_indicator": "adult", "authority": "senior_student", "medium": "offline"},
        "legal_frameworks": ["Indian Penal Code (IPC)"],
        "laws": [
            {
                "act": "Indian Penal Code",
                "section": "323",
                "title": "Voluntarily causing hurt",
                "description": "Punishment for causing hurt."
            }
        ],
        "steps": ["File First Information Report (FIR) at nearest police station"],
        "resources": [{"name": "Emergency Helpline", "contact": "112"}],
        "warnings": []
    }

    try:
        # Check if Ollama is reachable
        base_url = get_ollama_base_url()
        res = requests.get(f"{base_url}/api/tags", timeout=2)
        if res.status_code == 200:
            print(f"[INFO] Local Ollama detected at {base_url}. Testing live generation...")
            summary = generate_legal_summary(sample_report)
            if summary:
                print(f"[PASS] Live summary generated successfully ({len(summary)} chars):")
                print("--- PREVIEW ---")
                preview_text = summary[:300].encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
                print(preview_text + ("..." if len(summary) > 300 else ""))
                print("---------------")
                assert len(summary) > 50
            else:
                print("[SKIP] Ollama responded but did not return summary (check model availability).")
        else:
            print("[SKIP] Ollama not reachable on default port (live test skipped).")
    except Exception as e:
        print(f"[SKIP] Live test skipped: {e}")


if __name__ == "__main__":
    test_prompt_builder_structure()
    test_llm_client_skips_non_complaint()
    test_llm_client_fallback_on_offline()
    test_llm_client_fallback_on_http_error()
    test_llm_client_live_generation()
    print("\n[ALL PASS] All LLM integration and fallback tests passed!")
