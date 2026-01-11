# LoRA Training Guide: Paper-Cut Folklore Style

## Overview

Train a custom LoRA to achieve consistent "1970s British children's TV paper-cut" aesthetic across all episodes. This eliminates prompt engineering variability and ensures visual brand consistency.

---

## Target Aesthetic

**Style Name**: `folklore_papercut` (suggested LoRA name)

**Visual Characteristics**:
- Paper-cut illustration with visible edges
- Flat painted watercolour backgrounds
- Simple shapes and silhouettes
- Warm, muted colour palette
- Handmade, tactile texture
- No realistic faces (silhouettes only)
- Soft, diffused lighting
- Folk art influence

**Reference Shows** (for visual research):
- Bagpuss (1974)
- Mr Benn (1971-1972)
- Ivor the Engine (1975-1977)
- The Clangers (paper-cut backgrounds)
- Noggin the Nog (1959-1965)

---

## Training Dataset Requirements

### Image Count
- **Minimum**: 30 images
- **Recommended**: 50-80 images
- **Optimal**: 100+ images for best consistency

### Image Specifications
- **Resolution**: 512x512 minimum (768x768 or 1024x1024 preferred)
- **Format**: PNG or high-quality JPG
- **Aspect**: Mix of square and vertical (9:16) for versatility

### Dataset Composition

| Category | Count | Description |
|----------|-------|-------------|
| Landscapes | 15-20 | Irish/British countryside, hills, fields |
| Trees | 10-15 | Lone trees, branches, forests |
| Figures | 10-15 | Silhouettes, back-facing, tiny people |
| Objects | 5-10 | Folk objects, icons, symbols |
| Title cards | 5-10 | Decorative frames, borders |
| Close-ups | 5-10 | Textures, details, ribbons |

---

## Reference Image Sources

### Where to Find Training Images

**1. Screenshot from reference shows** (fair use for style training)
- Search YouTube for clips
- Capture key frames showing the aesthetic
- Focus on backgrounds, not characters

**2. Stock illustration sites** (check licenses)
- Shutterstock: "paper cut illustration folk art"
- Adobe Stock: "watercolour paper craft illustration"
- iStock: "vintage children book illustration"

**3. Art communities**
- DeviantArt: "paper cut art"
- ArtStation: "folk illustration"
- Pinterest: "vintage children's illustration 1970s"

**4. Create your own**
- Generate initial images with SDXL using strong prompts
- Curate the best results
- Use these to train a more refined LoRA

**5. Public domain**
- Wikimedia Commons: vintage illustration
- Rawpixel: public domain folk art
- Internet Archive: old children's books

---

## Image Curation Checklist

For each training image, verify:

- [ ] Paper-cut or flat illustration style (not 3D)
- [ ] Muted, warm colour palette
- [ ] Simple shapes, not complex details
- [ ] No text or watermarks
- [ ] No realistic human faces
- [ ] Good quality (not blurry)
- [ ] Matches the target aesthetic

**Reject images that are**:
- Photorealistic
- Anime/manga style
- Modern digital art style
- Dark or horror themed
- Busy or cluttered
- Low resolution

---

## Caption Format

Each image needs a caption file (same name, .txt extension).

### Caption Template
```
[trigger_word], paper-cut illustration, flat watercolour background, visible paper texture, simple shapes, 1970s British children's TV style, warm muted colours, soft lighting, handmade feel, folk art, [specific_content]
```

### Example Captions

**landscape_001.png** → **landscape_001.txt**
```
folklore_papercut, paper-cut illustration, flat watercolour background, visible paper texture, simple shapes, 1970s British children's TV style, warm muted colours, soft lighting, handmade feel, folk art, rolling green hills, Irish countryside, misty morning, distant mountains
```

**tree_001.png** → **tree_001.txt**
```
folklore_papercut, paper-cut illustration, flat watercolour background, visible paper texture, simple shapes, 1970s British children's TV style, warm muted colours, soft lighting, handmade feel, folk art, lone hawthorn tree, hillside, peaceful atmosphere
```

**silhouette_001.png** → **silhouette_001.txt**
```
folklore_papercut, paper-cut illustration, flat watercolour background, visible paper texture, simple shapes, 1970s British children's TV style, warm muted colours, soft lighting, handmade feel, folk art, tiny silhouette figures, dancing in circle, magical glow
```

---

## Training Configuration

### For Kohya_ss (Recommended)

```yaml
# Training parameters
pretrained_model: stabilityai/stable-diffusion-xl-base-1.0
# Or for SD 1.5: runwayml/stable-diffusion-v1-5

network_module: networks.lora
network_dim: 32  # LoRA rank (16-64, higher = more detail)
network_alpha: 16  # Usually half of dim

resolution: 1024  # For SDXL, 512 for SD 1.5
batch_size: 1
max_train_epochs: 10
learning_rate: 1e-4
unet_lr: 1e-4
text_encoder_lr: 5e-5
lr_scheduler: cosine_with_restarts
lr_warmup_steps: 100

optimizer: AdamW8bit
mixed_precision: fp16
gradient_checkpointing: true
gradient_accumulation_steps: 1

# Regularization
noise_offset: 0.05
caption_dropout_rate: 0.05

# Output
output_name: folklore_papercut
save_every_n_epochs: 2
```

### Quick Start Command

```bash
# Using kohya_ss
accelerate launch train_network.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
  --train_data_dir="./training_images" \
  --output_dir="./output_lora" \
  --output_name="folklore_papercut" \
  --network_module="networks.lora" \
  --network_dim=32 \
  --network_alpha=16 \
  --resolution=1024 \
  --train_batch_size=1 \
  --max_train_epochs=10 \
  --learning_rate=1e-4 \
  --optimizer_type="AdamW8bit" \
  --mixed_precision="fp16" \
  --caption_extension=".txt" \
  --cache_latents
```

---

## Folder Structure for Training

```
lora_training/
├── training_images/
│   ├── landscape_001.png
│   ├── landscape_001.txt
│   ├── landscape_002.png
│   ├── landscape_002.txt
│   ├── tree_001.png
│   ├── tree_001.txt
│   └── ... (50-100 image/caption pairs)
├── output_lora/
│   └── folklore_papercut.safetensors (output)
├── config.toml
└── TRAINING_GUIDE.md (this file)
```

---

## Using the Trained LoRA

### In Automatic1111

1. Place `folklore_papercut.safetensors` in `models/Lora/`
2. Add to prompt: `<lora:folklore_papercut:0.8>`
3. Adjust weight (0.6-1.0) based on results

### In ComfyUI

1. Use "Load LoRA" node
2. Connect to model pipeline
3. Set strength to 0.7-0.9

### Simplified Prompt (with LoRA)

```
folklore_papercut, lone hawthorn tree on Irish hillside, misty morning, peaceful countryside

Negative: photorealistic, 3d render, anime, dark, scary, text, watermark
```

The LoRA handles the style, so prompts become much simpler.

---

## Validation Checklist

After training, test with these prompts:

1. **Landscape**: `folklore_papercut, rolling Irish hills, distant mountains, morning mist`
2. **Tree**: `folklore_papercut, single hawthorn tree, hillside, golden hour`
3. **Figures**: `folklore_papercut, tiny silhouette people dancing in circle, magical glow`
4. **Close-up**: `folklore_papercut, colourful ribbons on tree branches, folk tradition`
5. **Icon**: `folklore_papercut, simple tree icon with protective circle, symbolic`

**Success criteria**:
- Consistent paper-cut aesthetic across all
- Warm, muted colours
- No realistic faces appearing
- Handmade, tactile feel
- Matches reference show aesthetic

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Too realistic | Increase LoRA weight, add more paper-cut images to training |
| Faces appearing | Add more negative training, stronger negative prompt |
| Colours too saturated | Add more muted colour examples to training set |
| Inconsistent style | More training epochs, higher network_dim |
| Overfitting | Reduce epochs, lower learning rate, add regularization |

---

## Time Estimate

| Task | Time |
|------|------|
| Collect 50 images | 2-3 hours |
| Write captions | 1-2 hours |
| Training (GPU) | 2-4 hours |
| Testing & refinement | 1-2 hours |
| **Total** | 6-11 hours |

After initial setup, you'll have consistent style for hundreds of episodes.
