#!/bin/bash
# Batch generate all episode images
# Usage: ./batch_generate.sh [a1111|comfy]

API=${1:-a1111}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/../output"
PATTERN_LIB="${SCRIPT_DIR}/../../data/pattern_library.json"

echo "=========================================="
echo "Folklore Shorts Batch Image Generator"
echo "=========================================="
echo "API: $API"
echo "Output: $OUTPUT_DIR"
echo ""

# Check if API is running
if [ "$API" == "a1111" ]; then
    if ! curl -s http://127.0.0.1:7860/sdapi/v1/sd-models > /dev/null 2>&1; then
        echo "Error: Automatic1111 API not running on port 7860"
        echo "Start it with: python launch.py --api"
        exit 1
    fi
    echo "✓ Automatic1111 API detected"
elif [ "$API" == "comfy" ]; then
    if ! curl -s http://127.0.0.1:8188/system_stats > /dev/null 2>&1; then
        echo "Error: ComfyUI API not running on port 8188"
        exit 1
    fi
    echo "✓ ComfyUI API detected"
fi

echo ""
echo "Starting batch generation..."
echo ""

# Generate all episodes
python3 "${SCRIPT_DIR}/generate_episode.py" \
    --all \
    --api "$API" \
    --output "$OUTPUT_DIR" \
    --pattern-library "$PATTERN_LIB"

echo ""
echo "=========================================="
echo "Batch generation complete!"
echo "Images saved to: $OUTPUT_DIR"
echo "=========================================="
