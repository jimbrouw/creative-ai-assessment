"""
duplicates.py — Perceptual hash duplicate grouping for PhotoCull.

Groups visually similar images using imagehash.phash (Hamming distance ≤ 8),
ranks within each group by combined_score, and marks lower-ranked duplicates
as rejected.
"""
from __future__ import annotations

from pathlib import Path

import imagehash
from PIL import Image

_RAW_EXTENSIONS = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}


def _open_for_hash(path: str) -> Image.Image:
    """Open an image for perceptual hashing.  Uses rawpy for RAW files."""
    ext = Path(path).suffix.lower()
    if ext in _RAW_EXTENSIONS:
        try:
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
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb)
        except Exception:
            pass
    return Image.open(path)


# ---------------------------------------------------------------------------
# Union-Find helpers
# ---------------------------------------------------------------------------

def _make_uf(n: int):
    parent = list(range(n))
    rank = [0] * n
    return parent, rank


def _find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _union(parent, rank, x, y):
    rx, ry = _find(parent, x), _find(parent, y)
    if rx == ry:
        return
    if rank[rx] < rank[ry]:
        rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]:
        rank[rx] += 1


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def group_duplicates(results: list[dict], keep: int = 1) -> list[dict]:
    """
    Compute perceptual hashes, cluster near-duplicates (Hamming ≤ 8),
    and annotate each result with:
        duplicate_group_id  — int (shared within group) or None for singletons
        duplicate_rank      — 1 = best in group by combined_score
        is_duplicate        — True if duplicate_rank > keep
    Images with is_duplicate=True have their category overridden to "rejected".
    """
    n = len(results)
    if n == 0:
        return results

    # Compute hashes — skip errored results (assign None)
    hashes = []
    for r in results:
        if "error" in r:
            hashes.append(None)
            continue
        try:
            img = _open_for_hash(r["path"])
            hashes.append(imagehash.phash(img))
        except Exception:
            hashes.append(None)

    # Build union-find clusters based on Hamming distance ≤ 8
    parent, rank_uf = _make_uf(n)
    threshold = 8

    for i in range(n):
        if hashes[i] is None:
            continue
        for j in range(i + 1, n):
            if hashes[j] is None:
                continue
            if hashes[i] - hashes[j] <= threshold:
                _union(parent, rank_uf, i, j)

    # Group indices by root
    from collections import defaultdict
    clusters: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        clusters[_find(parent, i)].append(i)

    # Assign group IDs and ranks
    group_id = 0
    for root, members in clusters.items():
        if len(members) == 1:
            # Singleton — no duplicate
            results[members[0]]["duplicate_group_id"] = None
            results[members[0]]["duplicate_rank"] = 1
            results[members[0]]["is_duplicate"] = False
            continue

        # Sort by combined_score descending (errored images score 0)
        members.sort(
            key=lambda idx: results[idx].get("combined_score", 0.0), reverse=True
        )
        for rank, idx in enumerate(members, start=1):
            r = results[idx]
            r["duplicate_group_id"] = group_id
            r["duplicate_rank"] = rank
            r["is_duplicate"] = rank > keep
            if r["is_duplicate"]:
                r["category"] = "rejected"
        group_id += 1

    return results
