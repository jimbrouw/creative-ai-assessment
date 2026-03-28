"""
html_report.py — Generate a self-contained HTML review page for PhotoCull.

No external dependencies.  Thumbnails are base64-encoded inline.
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image

_RAW_EXTENSIONS = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}

_STAR_GLYPHS = {5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆", 1: "★☆☆☆☆"}

_CATEGORY_COLOURS = {
    "selected": "#22c55e",   # green
    "maybe": "#eab308",      # yellow
    "rejected": "#ef4444",   # red
}

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #111; color: #e5e7eb; }
header { padding: 24px 32px; background: #1f2937; border-bottom: 1px solid #374151; }
header h1 { font-size: 1.5rem; font-weight: 700; }
header .stats { margin-top: 8px; font-size: 0.9rem; color: #9ca3af; }
.section { padding: 24px 32px; }
.section h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: 16px;
              text-transform: uppercase; letter-spacing: 0.05em; }
.section-selected h2 { color: #22c55e; }
.section-maybe     h2 { color: #eab308; }
.section-rejected  h2 { color: #ef4444; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 12px; }
.card { background: #1f2937; border-radius: 8px; overflow: hidden;
        border: 2px solid transparent; transition: transform 0.15s; }
.card:hover { transform: translateY(-2px); }
.card.selected { border-color: #22c55e; }
.card.maybe    { border-color: #eab308; }
.card.rejected { border-color: #ef4444; }
.card img { width: 100%; height: 160px; object-fit: cover; display: block; }
.card-body { padding: 8px 10px; }
.card-body .filename { font-size: 0.75rem; color: #9ca3af; white-space: nowrap;
                        overflow: hidden; text-overflow: ellipsis; }
.card-body .stars { font-size: 1rem; margin: 4px 0; }
.card-body .scores { font-size: 0.72rem; color: #6b7280; line-height: 1.6; }
.badges { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px; }
.badge { font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
.badge-dup  { background: #7c3aed; color: #fff; }
.badge-blur { background: #b45309; color: #fff; }
.badge-eyes { background: #991b1b; color: #fff; }
"""


def _b64_thumb(path: str, max_px: int = 300) -> str:
    """
    Load image, resize to thumbnail, return base64-encoded JPEG data URI.
    Falls back to a 1×1 grey pixel on any error.
    """
    try:
        ext = Path(path).suffix.lower()
        if ext in _RAW_EXTENSIONS:
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
        img.convert("RGB").save(buf, format="JPEG", quality=75, optimize=True)
        return base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        # 1×1 grey fallback
        fallback = Image.new("RGB", (1, 1), (128, 128, 128))
        buf = io.BytesIO()
        fallback.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode("ascii")


def _card_html(r: dict) -> str:
    category = r.get("category", "rejected")
    stars = r.get("stars", 1)
    b64 = _b64_thumb(r["path"])
    filename = Path(r["path"]).name

    badges = []
    if r.get("is_duplicate"):
        badges.append('<span class="badge badge-dup">DUP</span>')
    if r.get("is_blurry"):
        badges.append('<span class="badge badge-blur">BLUR</span>')
    if r.get("face_count", 0) > 0 and not r.get("eyes_open", True):
        badges.append('<span class="badge badge-eyes">EYES</span>')

    badges_html = (
        f'<div class="badges">{"".join(badges)}</div>' if badges else ""
    )

    scores_html = (
        f"Score: {r.get('combined_score', 0):.1f} &nbsp;|&nbsp; "
        f"Sharp: {r.get('sharpness_score', 0):.0f} &nbsp;|&nbsp; "
        f"Exp: {r.get('exposure_score', 0):.0f} &nbsp;|&nbsp; "
        f"Faces: {r.get('face_count', 0)}"
    )

    return f"""
    <div class="card {category}">
      <img src="data:image/jpeg;base64,{b64}" alt="{filename}" loading="lazy">
      <div class="card-body">
        <div class="filename" title="{filename}">{filename}</div>
        <div class="stars">{_STAR_GLYPHS.get(stars, "★☆☆☆☆")}</div>
        <div class="scores">{scores_html}</div>
        {badges_html}
      </div>
    </div>"""


def _section_html(title: str, css_class: str, items: list[dict]) -> str:
    if not items:
        return ""
    cards = "\n".join(_card_html(r) for r in items)
    return f"""
  <div class="section {css_class}">
    <h2>{title} ({len(items)})</h2>
    <div class="grid">{cards}</div>
  </div>"""


def generate(results: list[dict], output_path: str) -> None:
    """
    Generate a self-contained HTML review page at output_path.
    """
    selected = [r for r in results if r.get("category") == "selected"]
    maybe = [r for r in results if r.get("category") == "maybe"]
    rejected = [r for r in results if r.get("category") == "rejected"]

    total = len(results)
    sel_count = len(selected)
    cull_ratio = ((total - sel_count) / total * 100) if total else 0

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PhotoCull Review</title>
  <style>{_CSS}</style>
</head>
<body>
  <header>
    <h1>PhotoCull Review</h1>
    <div class="stats">
      Total: {total} &nbsp;|&nbsp;
      Selected: {sel_count} &nbsp;|&nbsp;
      Maybe: {len(maybe)} &nbsp;|&nbsp;
      Rejected: {len(rejected)} &nbsp;|&nbsp;
      Cull ratio: {cull_ratio:.0f}%
    </div>
  </header>
  {_section_html("Selected", "section-selected", selected)}
  {_section_html("Maybe", "section-maybe", maybe)}
  {_section_html("Rejected", "section-rejected", rejected)}
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(body, encoding="utf-8")
    print(f"[html_report] Written: {output_path}")
