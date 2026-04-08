#!/usr/bin/env python3
"""
PhotoCull engine — spawned as a subprocess by the Tauri Mac app.
Emits newline-delimited JSON events to stdout as analysis progresses.

Events:
  {"event": "start",    "total": N}
  {"event": "progress", "done": N, "total": N, "file": "name.jpg"}
  {"event": "results",  "batch": [...]}
  {"event": "complete", "summary": {total, selected, maybe, rejected, cull_ratio}}
  {"event": "xmp_done", "count": N}
  {"event": "html_done","path": "/path/to/review.html"}
  {"event": "error",    "message": "..."}
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Make the photocull package importable from wherever this script is called
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from photocull import analyser, cache, duplicates, html_report, scorer, xmp_writer

_IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff",
    ".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng",
}


def emit(obj: dict) -> None:
    print(json.dumps(obj), flush=True)


def collect_images(input_dir: str) -> list[str]:
    paths = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if Path(f).suffix.lower() in _IMAGE_EXTENSIONS:
                paths.append(os.path.join(root, f))
    return sorted(paths)


def main() -> None:
    parser = argparse.ArgumentParser(description="PhotoCull engine")
    parser.add_argument("--input", required=True)
    parser.add_argument("--mode", default="balanced")
    parser.add_argument("--keep-duplicates", type=int, default=1)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--write-xmp", action="store_true")
    parser.add_argument("--write-html", action="store_true")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else input_dir
    os.makedirs(output_dir, exist_ok=True)

    paths = collect_images(input_dir)
    total = len(paths)
    emit({"event": "start", "total": total})

    if total == 0:
        emit({"event": "error", "message": f"No supported images found in {input_dir}"})
        return

    # Load cache — skip already-analysed images
    result_cache = cache.load_cache(output_dir)
    results = []
    to_analyse = []

    for p in paths:
        cached = cache.get_cached(result_cache, p)
        if cached is not None:
            results.append(cached)
        else:
            to_analyse.append(p)

    done = len(results)

    # Analyse new images in parallel
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(analyser.analyse, p): p for p in to_analyse}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            cache.put_cached(result_cache, result["path"], result)
            done += 1
            emit({
                "event": "progress",
                "done": done,
                "total": total,
                "file": Path(result["path"]).name,
            })

    cache.save_cache(output_dir, result_cache)

    # Score and group duplicates
    scorer.score_all(results, mode=args.mode)
    duplicates.group_duplicates(results, keep=args.keep_duplicates)

    # Emit results in batches of 20
    for i in range(0, len(results), 20):
        emit({"event": "results", "batch": results[i : i + 20]})

    selected = [r for r in results if r.get("category") == "selected"]
    maybe    = [r for r in results if r.get("category") == "maybe"]
    rejected = [r for r in results if r.get("category") == "rejected"]

    emit({
        "event": "complete",
        "summary": {
            "total": total,
            "selected": len(selected),
            "maybe": len(maybe),
            "rejected": len(rejected),
            "cull_ratio": round((total - len(selected)) / total * 100) if total else 0,
        },
    })

    if args.write_xmp:
        n = xmp_writer.write_xmp_batch(results, output_dir)
        emit({"event": "xmp_done", "count": n, "output_dir": output_dir})

    if args.write_html:
        html_path = os.path.join(output_dir, "review.html")
        html_report.generate(results, html_path)
        emit({"event": "html_done", "path": html_path})


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit({"event": "error", "message": str(exc)})
        sys.exit(1)
