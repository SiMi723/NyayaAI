from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data" / "legal_sources.json"


def load_sources(path: str | Path = DEFAULT_REGISTRY) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sources", [])


def retrieve_sources(query: str, jurisdiction: str | None = None, *, path: str | Path = DEFAULT_REGISTRY, limit: int = 5) -> list[dict[str, Any]]:
    """Small transparent lexical retrieval over locally curated source passages.

    Portal-only records with no source_text are intentionally not treated as legal evidence.
    """
    words = {w for w in re.findall(r"[a-zA-Z]{3,}", query.lower())}
    candidates = []
    for source in load_sources(path):
        source_text = str(source.get("source_text", "")).strip()
        if not source.get("active", False) or not source_text:
            continue
        source_jurisdiction = str(source.get("jurisdiction", "")).lower()
        if jurisdiction and source_jurisdiction not in {jurisdiction.lower(), "india", "central"}:
            continue
        corpus = " ".join([
            str(source.get("title", "")), str(source.get("provision", "")), source_text
        ]).lower()
        score = sum(1 for word in words if word in corpus)
        if score:
            candidates.append((score, source))
    candidates.sort(key=lambda item: item[0], reverse=True)
    return [dict(item[1], retrieval_score=item[0]) for item in candidates[:limit]]
