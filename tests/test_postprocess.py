#!/usr/bin/env python3
"""Unit tests for the postprocessing module (context extraction and legal framework)."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from nlp.postprocess import (
    extract_age_indicator,
    extract_authority,
    extract_medium,
    extract_discrimination_type,
    get_legal_framework,
)


def test_age_extraction():
    assert extract_age_indicator("I am 16 years old") == "minor"
    assert extract_age_indicator("I am 22 years old") == "adult"
    assert extract_age_indicator("age: 15") == "minor"
    assert extract_age_indicator("I go to school") == "minor"
    assert extract_age_indicator("I study at university") == "adult"
    assert extract_age_indicator("Something happened to me") is None
    print("[PASS] test_age_extraction")


def test_authority_extraction():
    assert extract_authority("My teacher yelled at me") == "faculty"
    assert extract_authority("The principal suspended me") == "administration"
    assert extract_authority("My senior ragged me") == "senior_student"
    assert extract_authority("Someone bothered me") is None
    print("[PASS] test_authority_extraction")


def test_medium_extraction():
    assert extract_medium("Someone sent me threats on WhatsApp") == "online"
    assert extract_medium("I was beaten in the hostel") == "offline"
    assert extract_medium("They hit me and then posted a video") == "mixed"
    assert extract_medium("Something bad happened") is None
    print("[PASS] test_medium_extraction")


def test_discrimination_type():
    assert "caste" in extract_discrimination_type("They called me Dalit slurs")
    assert "religion" in extract_discrimination_type("They mocked my religion at the mosque")
    assert "race" in extract_discrimination_type("They discriminated because I'm from Northeast")
    assert "gender" in extract_discrimination_type("They said girls can't do engineering")
    assert extract_discrimination_type("I was hurt") == []
    print("[PASS] test_discrimination_type")


def test_legal_framework_pocso():
    context = {"age_indicator": "minor", "discrimination_types": []}
    frameworks = get_legal_framework("sexual_assault", context)
    assert any("POCSO" in fw for fw in frameworks), f"Expected POCSO in {frameworks}"
    print("[PASS] test_legal_framework_pocso")


def test_legal_framework_ipc():
    context = {"age_indicator": "adult", "discrimination_types": []}
    frameworks = get_legal_framework("physical_assault", context)
    assert any("IPC" in fw for fw in frameworks), f"Expected IPC in {frameworks}"
    print("[PASS] test_legal_framework_ipc")


def test_legal_framework_caste():
    context = {"age_indicator": None, "discrimination_types": ["caste"]}
    frameworks = get_legal_framework("caste_discrimination", context)
    assert any("Atrocities" in fw for fw in frameworks), f"Expected SC/ST Act in {frameworks}"
    print("[PASS] test_legal_framework_caste")


if __name__ == "__main__":
    test_age_extraction()
    test_authority_extraction()
    test_medium_extraction()
    test_discrimination_type()
    test_legal_framework_pocso()
    test_legal_framework_ipc()
    test_legal_framework_caste()
    print("\n[ALL PASS] All postprocess unit tests passed!")
