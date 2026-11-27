"""Vendored analytics base-9.1 pin is present on the client load path."""

from __future__ import annotations

import json
from pathlib import Path

from travel_planner.paths import PROJECT_ROOT

CHAT_DIR = PROJECT_ROOT / "data" / "chat_requests"
PIN = CHAT_DIR / "chat_request_analytics_base-9.1.json"
LOAD_PATH = CHAT_DIR / "travel-sample__default" / "chat_request_analytics_v2.json"
ROOT_ALIAS = CHAT_DIR / "chat_request_analytics_v2.json"


def _load(path: Path) -> dict:
    assert path.is_file(), f"missing vendored catalog {path}"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict)
    return doc


def test_analytics_base_9_1_pin_is_vendored():
    doc = _load(PIN)
    lineage = doc.get("_lineage") or {}
    assert lineage.get("base_id") == "base-9.1"
    assert lineage.get("file_stem") == "chat_request_analytics_base-9.1.json"


def test_default_scope_load_path_matches_pin():
    pin = PIN.read_bytes()
    assert LOAD_PATH.read_bytes() == pin
    assert ROOT_ALIAS.read_bytes() == pin
