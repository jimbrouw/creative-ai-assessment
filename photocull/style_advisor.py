"""
style_advisor.py — Ollama-based style learning for PhotoCull.

Reads the JSON cache history from previous shoots and asks a local
Llama 3 model (via Ollama) to suggest personalised threshold adjustments.

Usage:
    photocull --suggest-thresholds --output-dir /path/to/output

Requires Ollama running locally: https://ollama.ai
    ollama pull llama3
    ollama serve
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

_OLLAMA_URL = "http://localhost:11434/api/generate"
_MODEL = "llama3"
_CACHE_FILENAME = "photocull_cache.json"


def _load_history(output_dir: str) -> list[dict]:
    """Load all cached results from a shoot directory."""
    cache_path = Path(output_dir) / _CACHE_FILENAME
    if not cache_path.exists():
        return []
    try:
        with open(cache_path) as f:
            data = json.load(f)
        return list(data.values())
    except (json.JSONDecodeError, OSError):
        return []


def _build_summary(records: list[dict]) -> str:
    """Summarise accept/reject patterns from cached results."""
    selected = [r for r in records if r.get("category") == "selected"]
    rejected = [r for r in records if r.get("category") == "rejected"]

    def avg(items, key):
        vals = [v for r in items if (v := r.get(key)) is not None]
        return statistics.mean(vals) if vals else 0.0

    lines = [
        f"Total images analysed: {len(records)}",
        f"Selected: {len(selected)}  Rejected: {len(rejected)}",
        "",
        "Average scores for SELECTED images:",
        f"  sharpness_score: {avg(selected, 'sharpness_score'):.1f}",
        f"  exposure_score:  {avg(selected, 'exposure_score'):.1f}",
        f"  combined_score:  {avg(selected, 'combined_score'):.1f}",
        f"  face_count:      {avg(selected, 'face_count'):.2f}",
        "",
        "Average scores for REJECTED images:",
        f"  sharpness_score: {avg(rejected, 'sharpness_score'):.1f}",
        f"  exposure_score:  {avg(rejected, 'exposure_score'):.1f}",
        f"  combined_score:  {avg(rejected, 'combined_score'):.1f}",
        f"  face_count:      {avg(rejected, 'face_count'):.2f}",
        "",
        f"Blurry rate in selected: {sum(1 for r in selected if r.get('is_blurry'))}/{len(selected)}",
        f"Closed-eye rate in selected: {sum(1 for r in selected if not r.get('eyes_open', True))}/{len(selected)}",
    ]
    return "\n".join(lines)


def _ask_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama API and return the response text."""
    import urllib.request

    payload = json.dumps({"model": _MODEL, "prompt": prompt, "stream": False})
    req = urllib.request.Request(
        _OLLAMA_URL,
        data=payload.encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read())
    return body.get("response", "").strip()


def suggest_thresholds(output_dir: str) -> None:
    """
    Print Llama 3's threshold adjustment suggestions to stdout.
    Fails gracefully if Ollama is not running.
    """
    records = _load_history(output_dir)
    if not records:
        print("[style_advisor] No cache history found in", output_dir)
        return

    summary = _build_summary(records)
    prompt = f"""You are helping a photographer calibrate their photo culling software.

Here is statistical data from their recent shoots showing the scores of images they accepted vs rejected:

{summary}

Based on this data, suggest specific threshold adjustments for this photographer's style.
Focus on:
1. Should the blur penalty threshold (currently images below 20th percentile flagged as blurry) be adjusted?
2. Should the minimum exposure score be higher or lower?
3. Should the face bonus be higher or lower for their genre of photography?
4. What combined_score cutoff would better match their select/reject pattern?

Be specific with numbers. Keep your response under 200 words."""

    print("[style_advisor] Querying local Ollama (llama3)...")
    try:
        response = _ask_ollama(prompt)
        print("\n--- PhotoCull Style Advisor ---")
        print(response)
        print("--------------------------------\n")
    except OSError as e:
        print(
            f"[style_advisor] Could not reach Ollama at {_OLLAMA_URL}: {e}\n"
            "  Make sure Ollama is running: ollama serve\n"
            "  And llama3 is pulled:        ollama pull llama3"
        )
