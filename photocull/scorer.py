"""
scorer.py — Scoring, star ratings, and selection logic for PhotoCull.

Normalises sharpness relative to the set (percentile rank),
combines sub-scores, applies penalties, assigns 1-5 stars and
selected / maybe / rejected categories.
"""
from __future__ import annotations

import numpy as np

# Mode → fraction of images to mark as "selected"
_MODE_SELECTED_FRACTION = {
    "strict": 0.20,
    "balanced": 0.40,
    "generous": 0.60,
}
# Fraction to mark as "maybe" (on top of selected)
_MODE_MAYBE_FRACTION = 0.20


def _star_from_score(score: float) -> int:
    if score >= 80:
        return 5
    if score >= 60:
        return 4
    if score >= 40:
        return 3
    if score >= 20:
        return 2
    return 1


def normalise_sharpness(results: list[dict]) -> list[dict]:
    """
    Assign sharpness_score (0–100, percentile rank) and is_blurry flag.
    Operates on a copy — does not mutate the input list items.
    """
    valid = [r for r in results if "error" not in r]
    if not valid:
        return results

    raw_values = np.array([r["sharpness_raw"] for r in valid], dtype=np.float64)

    # Percentile rank: score = 100 * (rank / n)
    order = raw_values.argsort()
    ranks = np.empty_like(order)
    ranks[order] = np.arange(len(order))
    percentile_scores = 100.0 * ranks / max(len(order) - 1, 1)

    score_map = {id(r): float(s) for r, s in zip(valid, percentile_scores)}

    for r in results:
        if "error" in r:
            r["sharpness_score"] = 0.0
            r["is_blurry"] = True
        else:
            s = score_map[id(r)]
            r["sharpness_score"] = s
            r["is_blurry"] = s < 20.0

    return results


def score_all(results: list[dict], mode: str = "balanced") -> list[dict]:
    """
    Full scoring pass:
      1. Normalise sharpness
      2. Compute combined score
      3. Apply penalties
      4. Assign stars
      5. Assign category by mode

    Mutates result dicts in-place; returns the list for chaining.
    """
    if mode not in _MODE_SELECTED_FRACTION:
        raise ValueError(f"Unknown mode '{mode}'. Choose: {list(_MODE_SELECTED_FRACTION)}")

    results = normalise_sharpness(results)

    for r in results:
        if "error" in r:
            r.setdefault("sharpness_score", 0.0)
            r.setdefault("exposure_score", 0.0)
            r.setdefault("face_count", 0)
            r.setdefault("eyes_open", True)
            r.setdefault("is_blurry", True)
            r["combined_score"] = 0.0
            r["stars"] = 1
            r["category"] = "rejected"
            continue

        sharpness_score = r.get("sharpness_score", 0.0)
        exposure_score = r.get("exposure_score", 50.0)
        face_count = r.get("face_count", 0)
        eyes_open = r.get("eyes_open", True)
        is_blurry = r.get("is_blurry", False)

        # Weighted combination
        face_bonus = min(face_count, 1) * 20.0  # max 20pts for having ≥1 face
        combined = (sharpness_score * 0.5) + (exposure_score * 0.3) + face_bonus

        # Penalties
        if is_blurry:
            combined -= 40.0
        if face_count > 0 and not eyes_open:
            combined -= 20.0

        combined = float(np.clip(combined, 0.0, 100.0))
        r["combined_score"] = combined
        r["stars"] = _star_from_score(combined)

    # Assign categories based on rank within the whole set
    valid = [r for r in results if "error" not in r]
    valid.sort(key=lambda r: r["combined_score"], reverse=True)
    n = len(valid)

    sel_cutoff = max(1, int(round(n * _MODE_SELECTED_FRACTION[mode])))
    maybe_cutoff = sel_cutoff + max(1, int(round(n * _MODE_MAYBE_FRACTION)))

    for i, r in enumerate(valid):
        if i < sel_cutoff:
            r["category"] = "selected"
        elif i < maybe_cutoff:
            r["category"] = "maybe"
        else:
            r["category"] = "rejected"

    # Error entries are already set to rejected above
    return results
