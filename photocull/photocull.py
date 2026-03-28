#!/usr/bin/env python3
"""
photocull.py — CLI entry point for the PhotoCull photo culling tool.

Usage:
    python photocull.py --input /path/to/photos \\
                        --mode balanced \\
                        --keep-duplicates 2 \\
                        --output-xmp \\
                        --output-html \\
                        --output-dir /path/to/output

    python photocull.py --input /path/to/photos --test
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from . import analyser, cache, duplicates, html_report, scorer, xmp_writer

_IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff",
    ".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng",
}


def _collect_images(input_dir: str) -> list[str]:
    """Recursively collect all supported image paths from input_dir."""
    paths = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if Path(f).suffix.lower() in _IMAGE_EXTENSIONS:
                paths.append(os.path.join(root, f))
    return sorted(paths)


def _print_test_table(results: list[dict]) -> None:
    """Print a formatted score breakdown table for --test mode."""
    header = (
        f"{'File':<35} {'Sharp':>7} {'Exp':>6} {'Faces':>5} "
        f"{'Score':>7} {'Stars':>5} {'Category':<10} {'Notes'}"
    )
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for r in results:
        filename = Path(r["path"]).name[:34]
        if "error" in r:
            print(f"{'ERROR: ' + filename:<35} {r['error']}")
            continue

        notes = []
        if r.get("is_blurry"):
            notes.append("BLURRY")
        if r.get("face_count", 0) > 0 and not r.get("eyes_open", True):
            notes.append("EYES-CLOSED")
        if r.get("is_duplicate"):
            notes.append(f"DUP#{r.get('duplicate_rank', '?')}")

        print(
            f"{filename:<35} "
            f"{r.get('sharpness_score', 0):>7.1f} "
            f"{r.get('exposure_score', 0):>6.1f} "
            f"{r.get('face_count', 0):>5} "
            f"{r.get('combined_score', 0):>7.1f} "
            f"{'★' * r.get('stars', 1):<5} "
            f"{r.get('category', '?'):<10} "
            f"{', '.join(notes)}"
        )
    print("=" * len(header) + "\n")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="PhotoCull — local photo culling tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--input", required=True, help="Folder of images to analyse")
    p.add_argument(
        "--mode",
        choices=["strict", "balanced", "generous"],
        default="balanced",
        help="Selection aggression: strict=top 20%%, balanced=top 40%%, generous=top 60%% (default: balanced)",
    )
    p.add_argument(
        "--keep-duplicates",
        type=int,
        default=1,
        metavar="N",
        help="Keep top N from each duplicate group (default: 1)",
    )
    p.add_argument("--output-xmp", action="store_true", help="Write XMP sidecar files")
    p.add_argument("--output-html", action="store_true", help="Write HTML review page")
    p.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for XMP/HTML (default: same as --input)",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=min(8, (os.cpu_count() or 4)),
        help="ThreadPoolExecutor workers (default: min(8, cpu_count))",
    )
    p.add_argument(
        "--test",
        action="store_true",
        help="Analyse first 10 images, print score table, write nothing",
    )
    p.add_argument(
        "--gemini-key",
        default=None,
        metavar="API_KEY",
        help="Gemini API key — enables tiebreaker for ambiguous duplicate pairs",
    )
    p.add_argument(
        "--suggest-thresholds",
        action="store_true",
        help="Use local Ollama (llama3) to suggest threshold adjustments from history",
    )
    return p


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    input_dir = os.path.abspath(args.input)
    if not os.path.isdir(input_dir):
        print(f"[photocull] ERROR: --input directory not found: {input_dir}")
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir) if args.output_dir else input_dir
    os.makedirs(output_dir, exist_ok=True)

    # --suggest-thresholds: run advisor and exit
    if args.suggest_thresholds:
        from . import style_advisor
        style_advisor.suggest_thresholds(output_dir)
        return

    # Collect images
    all_paths = _collect_images(input_dir)
    if not all_paths:
        print(f"[photocull] No supported images found in {input_dir}")
        sys.exit(0)

    if args.test:
        all_paths = all_paths[:10]
        print(f"[photocull] TEST MODE — analysing {len(all_paths)} images")

    # Load cache (skip in test mode to always get fresh results)
    result_cache = {} if args.test else cache.load_cache(output_dir)

    # Analyse (parallel)
    results = []
    to_analyse = []
    for p in all_paths:
        cached = cache.get_cached(result_cache, p)
        if cached is not None:
            results.append(cached)
        else:
            to_analyse.append(p)

    if to_analyse:
        print(f"[photocull] Analysing {len(to_analyse)} images "
              f"({len(results)} cached) with {args.workers} workers...")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(analyser.analyse, p): p for p in to_analyse}
            for future in tqdm(as_completed(futures), total=len(futures), unit="img"):
                result = future.result()
                results.append(result)
                if not args.test:
                    cache.put_cached(result_cache, result["path"], result)
    else:
        print(f"[photocull] All {len(results)} images loaded from cache.")

    if not args.test:
        cache.save_cache(output_dir, result_cache)

    # Score
    scorer.score_all(results, mode=args.mode)

    # Duplicate grouping
    duplicates.group_duplicates(results, keep=args.keep_duplicates)

    # Optional: Gemini tiebreaker
    if args.gemini_key:
        from . import tiebreaker
        tiebreaker.resolve_ties(results, args.gemini_key)

    # --test: print table and exit
    if args.test:
        _print_test_table(results)
        return

    # Write outputs
    if args.output_xmp:
        n = xmp_writer.write_xmp_batch(results, output_dir)
        print(f"[photocull] Wrote {n} XMP sidecar files → {output_dir}")

    if args.output_html:
        html_path = os.path.join(output_dir, "review.html")
        html_report.generate(results, html_path)

    # Summary
    selected = [r for r in results if r.get("category") == "selected"]
    maybe = [r for r in results if r.get("category") == "maybe"]
    rejected = [r for r in results if r.get("category") == "rejected"]
    total = len(results)
    cull_ratio = (total - len(selected)) / total * 100 if total else 0

    print(
        f"\n[photocull] Done.\n"
        f"  Total:    {total}\n"
        f"  Selected: {len(selected)}\n"
        f"  Maybe:    {len(maybe)}\n"
        f"  Rejected: {len(rejected)}\n"
        f"  Cull ratio: {cull_ratio:.0f}%"
    )


if __name__ == "__main__":
    main()
