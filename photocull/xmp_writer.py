"""
xmp_writer.py — Write XMP sidecar files for PhotoCull results.

Uses manual XML templating (no external XMP library required).
Compatible with Lightroom Classic and Adobe Bridge.
"""
from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

_LABEL_MAP = {5: "Green", 4: "Green", 3: "Yellow", 2: "Yellow", 1: "Red"}

_XMP_TEMPLATE = """\
<?xpacket begin='\ufeff' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='PhotoCull 0.1.0'>
  <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
    <rdf:Description rdf:about=''
      xmlns:xmp='http://ns.adobe.com/xap/1.0/'
      xmlns:dc='http://purl.org/dc/elements/1.1/'
      xmp:Rating='{rating}'
      xmp:Label='{label}'>
      <dc:description>
        <rdf:Alt>
          <rdf:li xml:lang='x-default'>{description}</rdf:li>
        </rdf:Alt>
      </dc:description>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>
"""


def _build_description(r: dict) -> str:
    """Build a human-readable score breakdown string for dc:description."""
    parts = [
        f"Category:{r.get('category', 'unknown')}",
        f"Score:{r.get('combined_score', 0.0):.1f}",
        f"Sharp:{r.get('sharpness_score', 0.0):.0f}",
        f"Exp:{r.get('exposure_score', 0.0):.0f}",
        f"Faces:{r.get('face_count', 0)}",
    ]
    if r.get("is_blurry"):
        parts.append("Blurry:yes")
    if r.get("face_count", 0) > 0 and not r.get("eyes_open", True):
        parts.append("EyesClosed:yes")
    if r.get("is_duplicate"):
        parts.append(f"DupRank:{r.get('duplicate_rank', '?')}")
    return " | ".join(parts)


def write_xmp(result: dict, output_dir: str | None = None) -> str | None:
    """
    Write a .xmp sidecar for a single result dict.
    If output_dir is given, writes there; otherwise writes alongside the source.
    Returns the path written, or None on failure.
    """
    if "error" in result:
        return None

    src_path = Path(result["path"])
    if output_dir:
        sidecar_path = Path(output_dir) / (src_path.stem + ".xmp")
    else:
        sidecar_path = src_path.with_suffix(".xmp")

    stars = result.get("stars", 1)
    label = _LABEL_MAP.get(stars, "Red")
    description = escape(_build_description(result))

    xmp_content = _XMP_TEMPLATE.format(
        rating=stars,
        label=label,
        description=description,
    )

    try:
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        sidecar_path.write_text(xmp_content, encoding="utf-8")
        return str(sidecar_path)
    except OSError as e:
        print(f"[xmp_writer] Failed to write {sidecar_path}: {e}")
        return None


def write_xmp_batch(results: list[dict], output_dir: str | None = None) -> int:
    """Write XMP sidecars for all valid results.  Returns count written."""
    count = 0
    for r in results:
        if write_xmp(r, output_dir):
            count += 1
    return count
