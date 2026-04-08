"""
cache.py — JSON result caching for PhotoCull.

Keyed by "{abs_path}:{mtime}:{size}" so re-runs skip already-analysed images
and only re-analyse files that have changed on disk.
"""
import json
import os
from pathlib import Path

_CACHE_FILENAME = "photocull_cache.json"


def _cache_key(path: str) -> str:
    """Build a cache key from path + file metadata."""
    abs_path = os.path.abspath(path)
    stat = os.stat(abs_path)
    return f"{abs_path}:{stat.st_mtime}:{stat.st_size}"


def load_cache(output_dir: str) -> dict:
    """Load cache dict from output_dir.  Returns {} if missing or corrupt."""
    cache_path = Path(output_dir) / _CACHE_FILENAME
    if not cache_path.exists():
        return {}
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(output_dir: str, data: dict) -> None:
    """Atomically write cache dict to output_dir (write-then-replace)."""
    cache_path = Path(output_dir) / _CACHE_FILENAME
    tmp_path = cache_path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, cache_path)


def get_cached(cache: dict, path: str) -> dict | None:
    """Return cached result for path if the file hasn't changed, else None."""
    key = _cache_key(path)
    return cache.get(key)


def put_cached(cache: dict, path: str, result: dict) -> None:
    """Store result in the in-memory cache dict under the current file key."""
    key = _cache_key(path)
    cache[key] = result
