"""
analyser.py — Per-image analysis pipeline for PhotoCull.

Returns a canonical result dict for every image:
{
    path, sharpness_raw, exposure_score, face_count,
    eyes_open, width, height, format
}
On failure returns: {path, error}
"""
import io
import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# RAW file extensions that need rawpy preview extraction
_RAW_EXTENSIONS = {".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2", ".dng"}

# Haar cascade path (bundled with opencv-python)
_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
_face_cascade = None  # lazy-loaded

# MediaPipe — optional, gracefully degraded if not installed
try:
    import mediapipe as mp

    _mp_face_detection = mp.solutions.face_detection
    _mp_face_mesh = mp.solutions.face_mesh
    _MEDIAPIPE_AVAILABLE = True
except ImportError:
    _MEDIAPIPE_AVAILABLE = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_face_cascade():
    global _face_cascade
    if _face_cascade is None:
        _face_cascade = cv2.CascadeClassifier(_CASCADE_PATH)
    return _face_cascade


def _load_image(path: str):
    """
    Load image as BGR numpy array.
    For RAW files, extract the embedded preview JPEG via rawpy.
    Returns (bgr_array, pil_image, format_str) or raises on failure.
    """
    ext = Path(path).suffix.lower()

    if ext in _RAW_EXTENSIONS:
        try:
            import rawpy  # noqa: PLC0415
            with rawpy.imread(path) as raw:
                preview = raw.extract_thumb()
            if preview.format == rawpy.ThumbFormat.JPEG:
                buf = np.frombuffer(preview.data, dtype=np.uint8)
                bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
            else:
                # Bitmap preview
                bgr = cv2.cvtColor(
                    np.array(preview.data, dtype=np.uint8), cv2.COLOR_RGB2BGR
                )
            pil = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            return bgr, pil, ext.lstrip(".")
        except Exception as e:
            raise RuntimeError(f"rawpy failed for {path}: {e}") from e

    bgr = cv2.imread(path)
    if bgr is None:
        raise RuntimeError(f"cv2.imread returned None for {path}")
    pil = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    return bgr, pil, ext.lstrip(".")


def _sharpness(gray: np.ndarray) -> float:
    """Laplacian variance — higher = sharper."""
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def _exposure(pil_img: Image.Image) -> float:
    """
    Score 0–100 based on histogram spread and midtone balance.
    Penalises heavily clipped highlights (>250) and crushed shadows (<5).
    """
    rgb = pil_img.convert("RGB")
    hist = rgb.histogram()  # 768 values: R[0:256] G[256:512] B[512:768]

    total_pixels = rgb.width * rgb.height
    if total_pixels == 0:
        return 50.0

    # Count clipped highlights (value > 250) across R+G+B
    highlight_count = sum(hist[250:256]) + sum(hist[506:512]) + sum(hist[762:768])
    # Count crushed shadows (value < 5) across R+G+B
    shadow_count = sum(hist[0:5]) + sum(hist[256:261]) + sum(hist[512:517])

    highlight_ratio = highlight_count / (total_pixels * 3)
    shadow_ratio = shadow_count / (total_pixels * 3)

    # Midtone spread: std-dev of combined channel histogram in range 5–250
    midtone_bins = []
    for channel_start in (0, 256, 512):
        midtone_bins.extend(hist[channel_start + 5: channel_start + 251])
    if sum(midtone_bins) > 0:
        values = np.array(midtone_bins, dtype=np.float64)
        spread = float(np.std(values) / (np.mean(values) + 1e-6))
        # Normalise spread to 0–20 contribution
        spread_score = min(spread / 5.0, 1.0) * 20.0
    else:
        spread_score = 0.0

    score = 100.0 - (highlight_ratio * 50.0) - (shadow_ratio * 30.0) + spread_score
    return float(np.clip(score, 0.0, 100.0))


def _face_analysis_mediapipe(bgr: np.ndarray) -> tuple[int, bool]:
    """
    Use MediaPipe FaceDetection + FaceMesh to detect faces and eye status.
    Eye aspect ratio (EAR) from landmarks 159/145 — threshold 0.2.
    Returns (face_count, eyes_open).
    """
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # Face count
    face_count = 0
    with _mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5
    ) as detector:
        results = detector.process(rgb)
        if results.detections:
            face_count = len(results.detections)

    if face_count == 0:
        return 0, True  # no faces → treat eyes as open (no penalty)

    # Eye status via FaceMesh — check first detected face
    eyes_open = True
    with _mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as mesh:
        result = mesh.process(rgb)
        if result.multi_face_landmarks:
            lm = result.multi_face_landmarks[0].landmark
            h, w = bgr.shape[:2]

            def pt(idx):
                return np.array([lm[idx].x * w, lm[idx].y * h])

            # Left eye EAR: landmarks 159 (top), 145 (bottom), 133 (inner), 33 (outer)
            # Right eye EAR: 386 (top), 374 (bottom), 362 (inner), 263 (outer)
            def ear(top, bottom, inner, outer):
                vert = np.linalg.norm(pt(top) - pt(bottom))
                horiz = np.linalg.norm(pt(inner) - pt(outer))
                return vert / (horiz + 1e-6)

            left_ear = ear(159, 145, 133, 33)
            right_ear = ear(386, 374, 362, 263)
            avg_ear = (left_ear + right_ear) / 2.0
            eyes_open = avg_ear >= 0.2

    return face_count, eyes_open


def _face_analysis_haar(bgr: np.ndarray) -> tuple[int, bool]:
    """Fallback face detection using OpenCV Haar cascade."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    cascade = _get_face_cascade()
    faces = cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    return len(faces), True  # can't detect eye status with basic Haar


def _face_analysis(bgr: np.ndarray) -> tuple[int, bool]:
    if _MEDIAPIPE_AVAILABLE:
        try:
            return _face_analysis_mediapipe(bgr)
        except Exception:
            pass
    return _face_analysis_haar(bgr)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyse(path: str) -> dict:
    """
    Analyse a single image file.
    Returns a result dict with keys:
        path, sharpness_raw, exposure_score, face_count, eyes_open,
        width, height, format
    On failure: {path, error}
    """
    try:
        bgr, pil, fmt = _load_image(path)
        h, w = bgr.shape[:2]
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        sharpness_raw = _sharpness(gray)
        exposure_score = _exposure(pil)
        face_count, eyes_open = _face_analysis(bgr)

        return {
            "path": os.path.abspath(path),
            "sharpness_raw": sharpness_raw,
            "exposure_score": exposure_score,
            "face_count": face_count,
            "eyes_open": eyes_open,
            "width": w,
            "height": h,
            "format": fmt,
        }
    except Exception as exc:
        return {"path": os.path.abspath(path), "error": str(exc)}
