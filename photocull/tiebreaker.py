"""
tiebreaker.py — Gemini Flash vision tiebreaker for PhotoCull.

When two images in the same duplicate group score within 5 points of each
other, this module sends the thumbnail pair to Gemini 1.5 Flash and uses
the response to reorder their duplicate_rank.

Cost: ~$0.00002 per pair — fires on ~5–15% of a typical shoot.

Usage: pass --gemini-key YOUR_API_KEY to the CLI to enable.
"""
from __future__ import annotations

import base64
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)
_TIE_THRESHOLD = 5.0  # points — pairs closer than this trigger the API


def _thumb_b64(path: str, max_px: int = 512) -> str:
    """Return a base64-encoded JPEG thumbnail for the image."""
    try:
        ext = Path(path).suffix.lower()
        raw_exts = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}
        if ext in raw_exts:
            import rawpy  # noqa: PLC0415
            import numpy as np
            import cv2

            with rawpy.imread(path) as raw:
                preview = raw.extract_thumb()
            if preview.format == rawpy.ThumbFormat.JPEG:
                buf = np.frombuffer(preview.data, dtype=np.uint8)
                bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
            else:
                bgr = cv2.cvtColor(
                    np.array(preview.data, dtype=np.uint8), cv2.COLOR_RGB2BGR
                )
            img = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        else:
            img = Image.open(path)

        img.thumbnail((max_px, max_px), Image.LANCZOS)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return ""


def _ask_gemini(api_key: str, b64_a: str, b64_b: str) -> str:
    """Call Gemini Flash with two image thumbnails and return the response text."""
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Image A:"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_a}},
                    {"text": "Image B:"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_b}},
                    {
                        "text": (
                            "Which of these two photos is technically better and why? "
                            "Consider sharpness, exposure, composition, and subject quality. "
                            "Reply in one sentence starting with 'A' or 'B'."
                        )
                    },
                ]
            }
        ]
    }
    url = f"{_GEMINI_URL}?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read())
    return body["candidates"][0]["content"]["parts"][0]["text"].strip()


def resolve_ties(results: list[dict], api_key: str) -> list[dict]:
    """
    Find duplicate group pairs with scores within _TIE_THRESHOLD and resolve
    them with Gemini Flash.  Updates duplicate_rank in-place.
    Returns results for chaining.
    """
    from collections import defaultdict

    # Group by duplicate_group_id
    groups: dict[int, list[dict]] = defaultdict(list)
    for r in results:
        gid = r.get("duplicate_group_id")
        if gid is not None:
            groups[gid].append(r)

    tie_pairs_resolved = 0

    for gid, members in groups.items():
        # Only check adjacent pairs in rank order
        members.sort(key=lambda r: r.get("duplicate_rank", 999))
        for i in range(len(members) - 1):
            a, b = members[i], members[i + 1]
            score_a = a.get("combined_score", 0.0)
            score_b = b.get("combined_score", 0.0)

            if abs(score_a - score_b) > _TIE_THRESHOLD:
                continue  # not a tie

            try:
                b64_a = _thumb_b64(a["path"])
                b64_b = _thumb_b64(b["path"])
                if not b64_a or not b64_b:
                    continue

                response = _ask_gemini(api_key, b64_a, b64_b)

                # If Gemini prefers B, swap their ranks
                if response.upper().startswith("B"):
                    a["duplicate_rank"], b["duplicate_rank"] = (
                        b["duplicate_rank"],
                        a["duplicate_rank"],
                    )
                    tie_pairs_resolved += 1
                    # Re-sort members after swap for next iteration
                    members.sort(key=lambda r: r.get("duplicate_rank", 999))

            except Exception as e:
                print(f"[tiebreaker] Gemini call failed for group {gid}: {e}")
                continue

    if tie_pairs_resolved:
        print(f"[tiebreaker] Resolved {tie_pairs_resolved} tie pair(s) via Gemini Flash")

    return results
