# PhotoCull

**Free, offline, open-source photo culling tool.**
No subscription. No cloud. Nothing leaves your machine.

---

## Why PhotoCull?

| | Aftershoot / FilterPixel | PhotoCull |
|---|---|---|
| Cost | $15–19/month | Free forever |
| Cloud upload | Required | Never |
| Score explanation | None | Full breakdown |
| Style learning | Proprietary | Local Llama 3 (free) |
| Tiebreaker AI | Black box | Gemini Flash (~$0.00002/pair) |
| Source code | Closed | Open |

---

## Features

- **Sharpness detection** — Laplacian variance, normalised relative to the set
- **Exposure scoring** — histogram analysis, penalises clipped highlights and crushed shadows
- **Face & eye detection** — MediaPipe face mesh (eyes-open/closed via EAR landmarks), fallback to Haar cascade
- **Duplicate grouping** — perceptual hash (phash) with Hamming distance ≤ 8, keeps best N per group
- **XMP sidecars** — Lightroom/Bridge compatible ratings and labels
- **HTML review page** — self-contained, no server needed, shareable
- **JSON cache** — re-runs skip already-analysed images
- **Ollama style advisor** — local Llama 3 suggests threshold adjustments from your history
- **Gemini Flash tiebreaker** — resolves genuinely ambiguous duplicate pairs via vision API

---

## Requirements

- Python 3.10+
- Supported formats: JPEG, PNG, TIFF, CR2, CR3, NEF, ARW, ORF, RW2, DNG

---

## Installation

```bash
git clone https://github.com/jimbrouw/photocull
cd photocull
pip install -r photocull/requirements.txt
```

---

## Usage

### Basic cull
```bash
python -m photocull.photocull \
  --input /path/to/photos \
  --mode balanced \
  --output-xmp \
  --output-html \
  --output-dir /path/to/output
```

### Keep 2 best from each burst group
```bash
python -m photocull.photocull \
  --input /path/to/photos \
  --keep-duplicates 2 \
  --output-xmp
```

### Test mode — calibrate thresholds before committing
```bash
python -m photocull.photocull --input /path/to/photos --test
```

Prints a table like:
```
File                                Sharp    Exp  Faces   Score Stars Category
====================================...
IMG_0042.jpg                         78.2   82.4      2    80.0 ★★★★★ selected
IMG_0043.jpg                         21.4   79.1      2    40.7 ★★★☆☆ maybe    BLURRY
IMG_0044.jpg                         55.1   61.3      2    60.8 ★★★★☆ selected DUP#2
```

### Mode options
| Mode | Selected | Maybe | Rejected |
|---|---|---|---|
| `strict` | Top 20% | Next 20% | Rest |
| `balanced` | Top 40% | Next 20% | Rest |
| `generous` | Top 60% | Next 20% | Rest |

### With Gemini Flash tiebreaker (optional)
```bash
python -m photocull.photocull \
  --input /path/to/photos \
  --gemini-key YOUR_GEMINI_API_KEY \
  --output-xmp
```
Fires only when two images in the same duplicate group score within 5 points.
Get a key at [ai.google.dev](https://ai.google.dev).

### Ollama style advisor (optional, fully free)
After 3+ shoots, run this to get personalised threshold suggestions:
```bash
# One-time setup
ollama pull llama3
ollama serve

# Then:
python -m photocull.photocull \
  --input /path/to/photos \
  --output-dir /path/to/output \
  --suggest-thresholds
```

---

## Module Overview

| Module | Purpose |
|---|---|
| `photocull.py` | CLI entry point, ThreadPoolExecutor, tqdm progress |
| `analyser.py` | Per-image pipeline: sharpness, exposure, face/eye detection |
| `scorer.py` | Normalisation, combined score, stars, category assignment |
| `duplicates.py` | Perceptual hash clustering, rank-within-group |
| `xmp_writer.py` | XMP sidecar XML output |
| `html_report.py` | Self-contained HTML review page with base64 thumbnails |
| `cache.py` | JSON result caching keyed by file path + mtime + size |
| `style_advisor.py` | Ollama/Llama 3 threshold suggestions from cull history |
| `tiebreaker.py` | Gemini Flash vision API for ambiguous duplicate pairs |

---

## Non-Destructive

PhotoCull **never** moves, renames, or modifies original image files.
It only creates `.xmp` sidecar files and the `review.html` report in `--output-dir`.

---

## Licence

MIT — do whatever you want with it.
