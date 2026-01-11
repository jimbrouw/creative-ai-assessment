# Stable Diffusion Pipeline for Irish Folklore Shorts

Automated image generation using Stable Diffusion for the Irish Folklore shorts channel.

## Quick Start

### Option 1: Automatic1111 (Recommended for beginners)

```bash
# 1. Start A1111 with API enabled
cd stable-diffusion-webui
python launch.py --api

# 2. Generate Episode 1
cd sd_pipeline/scripts
python generate_episode.py --episode 1 --api a1111
```

### Option 2: ComfyUI (Recommended for advanced users)

```bash
# 1. Start ComfyUI
cd ComfyUI
python main.py

# 2. Load the workflow
# Open workflows/folklore_workflow_lora.json in ComfyUI

# 3. Generate Episode 1
cd sd_pipeline/scripts
python generate_episode.py --episode 1 --api comfy --workflow ../workflows/folklore_workflow_lora.json
```

### Option 3: Batch All Episodes

```bash
cd sd_pipeline/scripts
./batch_generate.sh a1111
# or
./batch_generate.sh comfy
```

---

## Folder Structure

```
sd_pipeline/
├── README.md                    # This file
├── prompts/
│   └── episode_01_fairy_trees.md   # SD-optimized prompts
├── lora_training/
│   ├── TRAINING_GUIDE.md        # How to train the style LoRA
│   ├── reference_images.md      # What images to collect
│   └── training_images/         # Put training images here
├── scripts/
│   ├── generate_episode.py      # Main generation script
│   └── batch_generate.sh        # Batch all episodes
├── workflows/
│   ├── folklore_workflow.json       # Basic ComfyUI workflow
│   └── folklore_workflow_lora.json  # With LoRA support
├── reference_images/            # Style reference screenshots
└── output/                      # Generated images go here
```

---

## Setup Requirements

### Python Dependencies

```bash
pip install requests Pillow
```

### Stable Diffusion Setup

**Automatic1111:**
1. Install from https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Download SDXL base model to `models/Stable-diffusion/`
3. Start with `--api` flag

**ComfyUI:**
1. Install from https://github.com/comfyanonymous/ComfyUI
2. Download SDXL base model to `models/checkpoints/`
3. Start normally (API is enabled by default)

### Recommended Models

| Model | Download | Notes |
|-------|----------|-------|
| SDXL 1.0 Base | [HuggingFace](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | Best quality |
| SDXL Turbo | [HuggingFace](https://huggingface.co/stabilityai/sdxl-turbo) | Faster, less quality |
| SD 1.5 | [HuggingFace](https://huggingface.co/runwayml/stable-diffusion-v1-5) | If using old LoRAs |

---

## Two Approaches

### Approach 1: Prompt-Only (Quick Start)

Use the detailed prompts in `prompts/` without any LoRA.

**Pros:**
- No training needed
- Works immediately
- Full control per image

**Cons:**
- Less consistent style
- Longer prompts
- More variation between batches

**Example:**
```
(paper-cut illustration:1.4), (flat watercolour background:1.3),
(visible paper texture:1.2), (1970s British children's TV animation:1.3),
lone hawthorn tree on Irish hillside, misty morning...
```

### Approach 2: Train a LoRA (Recommended)

Train a custom LoRA on the paper-cut style for perfect consistency.

**Pros:**
- Consistent style across all episodes
- Simpler prompts
- Faster iteration
- Your unique visual brand

**Cons:**
- Requires training (6-11 hours setup)
- Needs 50+ reference images

**Example (with LoRA):**
```
folklore_papercut, lone hawthorn tree on Irish hillside, misty morning
```

See `lora_training/TRAINING_GUIDE.md` for full instructions.

---

## Image Settings

### Resolution
- **Shorts (9:16)**: 768 x 1344 (SDXL) or 576 x 1024 (SD 1.5)

### Generation Settings
```yaml
steps: 35
cfg_scale: 7.5
sampler: DPM++ 2M Karras
```

### Style Tokens (Weights)
```
(paper-cut illustration:1.4)     # Primary style
(flat watercolour background:1.3) # Background treatment
(Bagpuss style:1.2)              # Reference aesthetic
(handmade tactile feel:1.2)      # Texture
```

---

## Consistency Tips

1. **Record seeds** - Save working seeds for reference
2. **Batch together** - Generate all 6 episode shots in one session
3. **Same model** - Don't change models mid-episode
4. **Train LoRA** - Best long-term solution
5. **Color grading** - Post-process for final consistency

---

## Episode Workflow

For each episode:

1. **Get prompts** from `data/pattern_library.json`
2. **Run generation** with `generate_episode.py`
3. **Review outputs** in `output/episode_XX/`
4. **Regenerate failures** with specific seeds
5. **Post-process** (color grade, add captions)
6. **Assemble video** with audio

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API connection refused | Start A1111/ComfyUI first |
| Out of VRAM | Reduce resolution or batch size |
| Wrong aspect ratio | Check width/height settings |
| Style inconsistent | Use LoRA or same seed range |
| Faces appearing | Strengthen negative prompt |
| Too realistic | Increase style weights |

---

## Cost Comparison

| Method | Cost | Quality | Consistency |
|--------|------|---------|-------------|
| Midjourney | $10-30/mo | High | Medium |
| DALL-E API | ~$0.04/image | High | Medium |
| SD (local) | Free* | High | High (with LoRA) |
| SD (cloud) | ~$0.01/image | High | High (with LoRA) |

*Requires GPU hardware

---

## Next Steps

1. [ ] Set up Stable Diffusion (A1111 or ComfyUI)
2. [ ] Test Episode 1 prompts
3. [ ] Collect LoRA training images (optional but recommended)
4. [ ] Train LoRA (optional but recommended)
5. [ ] Batch generate all 10 episodes
6. [ ] Set up video assembly pipeline
