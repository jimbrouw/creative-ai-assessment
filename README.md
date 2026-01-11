# Irish Folklore Shorts - Faceless YouTube Pipeline

A Claude Code agent system for automated faceless YouTube Shorts production. Currently configured for **Irish Folklore** content with a 70s British children's TV paper-cut visual style.

## Current Configuration

| Setting | Value |
|---------|-------|
| **Niche** | Irish Folklore |
| **Format** | Shorts (45-60 seconds) |
| **Visual Style** | Paper-cut illustration (Bagpuss/Mr Benn aesthetic) |
| **Voice** | Labhaoise (ElevenLabs, Irish accent) |
| **Cadence** | 1 per day |
| **Episodes Ready** | 10 starter episodes |

## Quick Start

### 1. Generate Images (Stable Diffusion)

```bash
# Start Automatic1111 with API
cd stable-diffusion-webui && python launch.py --api

# Generate Episode 1
cd sd_pipeline/scripts
python generate_episode.py --episode 1 --api a1111
```

See `sd_pipeline/README.md` for full setup.

### 2. Generate Voice (ElevenLabs)

1. Go to ElevenLabs
2. Select voice: **Labhaoise**
3. Copy script from `output_pack/2026-01-11_fairy-trees/03_script.md`
4. Settings: Stability 0.55, Similarity 0.75, Style 0.35

### 3. Assemble Video

1. Import 6 images to editor
2. Add voiceover track
3. Add captions (see script for text)
4. Add subtle music bed
5. Export 1080x1920 (9:16)

---

## Folder Structure

```
├── agents/                    # Agent specifications
│   ├── orchestrator.md       # Pipeline controller
│   ├── script.md             # Shorts scriptwriting
│   ├── assets.md             # Image prompt generation
│   └── qa.md                 # Quality assurance
│
├── config/                    # Configuration
│   ├── niches.json           # Irish Folklore (locked in)
│   ├── constraints.json      # Shorts format specs
│   └── brand_rules.json      # Paper-cut style, voice rules
│
├── data/
│   └── pattern_library.json  # 10 episodes with full prompts
│
├── sd_pipeline/               # Stable Diffusion automation
│   ├── README.md             # SD setup guide
│   ├── prompts/              # SD-optimized prompts
│   ├── lora_training/        # Train custom style LoRA
│   ├── scripts/              # Batch generation scripts
│   └── workflows/            # ComfyUI workflows
│
└── output_pack/               # Production-ready assets
    └── 2026-01-11_fairy-trees/
        ├── 03_script.md
        └── 05_asset_prompts.md
```

---

## 10 Starter Episodes

| # | Title | Pillar | Status |
|---|-------|--------|--------|
| 1 | Why do Irish people never cut this tree? | Places | Ready |
| 2 | The real meaning of Samhain | Festivals | Ready |
| 3 | What happens if you take a selkie's coat? | Creatures | Ready |
| 4 | Why do Irish people leave ribbons at wells? | Places | Ready |
| 5 | What is a púca and why is it so tricky? | Creatures | Ready |
| 6 | The real meaning of Bealtaine | Festivals | Ready |
| 7 | The legend of Fionn and the Salmon of Knowledge | Creatures | Ready |
| 8 | Why do Irish people make Brigid's crosses? | Festivals | Ready |
| 9 | How the Giant's Causeway was really made | Places | Ready |
| 10 | What is Wren Day and why do people dress up? | Festivals | Ready |

All episodes have full scripts, image prompts, and captions in `data/pattern_library.json`.

---

## Visual Style

**Aesthetic**: Late 1970s British children's TV animation

**References**: Bagpuss, Mr Benn, Willow the Wisp, Ivor the Engine

**Characteristics**:
- Paper-cut illustration style
- Flat painted watercolour backgrounds
- Visible paper-edge texture
- Simple shapes and silhouettes
- Warm, muted colour palette
- No realistic faces (silhouettes only)

**6-Shot Template**:
1. Title card (0-2s)
2. Hero location (2-8s)
3. Beat 1 visual (8-17s)
4. Beat 2 visual (17-26s)
5. Beat 3 visual (26-35s)
6. Meaning card (35-60s)

---

## Script Structure

Each 45-60 second script follows:

```
HOOK (0-2s)     → Question to spark curiosity
CONTEXT (2-8s)  → Ground the tradition/creature
BEAT 1 (8-17s)  → The belief or tradition
BEAT 2 (17-26s) → Famous example or story
BEAT 3 (26-35s) → Modern practice
MEANING (35-50s)→ Educational payoff
PROMPT (50-60s) → Invite comments
```

---

## Stable Diffusion Setup

### Option 1: Prompt-Only (Quick)
Use the detailed prompts in `sd_pipeline/prompts/`. Works immediately, less consistent.

### Option 2: Train LoRA (Recommended)
Train a custom LoRA on the paper-cut style. See `sd_pipeline/lora_training/TRAINING_GUIDE.md`.

### Batch Generation

```bash
# Generate all 10 episodes
cd sd_pipeline/scripts
./batch_generate.sh a1111
```

---

## Content Guidelines

**Tone**: Warm, curious, educational (NOT scary)

**Kid-Safe Rules**:
- No gore or explicit violence
- No horror framing
- Implied consequences only ("vanished", "never returned")
- Respect living traditions

**Forbidden**:
- "Hey guys", "Like and subscribe"
- Horror language ("terrifying", "creepy")
- Realistic faces
- Modern objects in visuals

---

## Production Pipeline

### Daily (30-45 min once running)
1. Generate 6 images (same style)
2. Generate voiceover from script
3. Assemble in editor with captions
4. Export and upload

### Weekly (2-3 hours)
1. Research 10 new topics
2. Write scripts using template
3. Batch generate 60 images
4. Batch generate 10 voiceovers

---

## Expansion Path

Once Irish Folklore is established:
- Scottish folklore (same visual style)
- Welsh folklore
- Breton/Cornish folklore
- Norse mythology

Same template, new subjects.

---

## Resources

- `ClaudeCodeSkillsFile.md` - Full system specification
- `sd_pipeline/README.md` - Stable Diffusion setup
- `sd_pipeline/lora_training/TRAINING_GUIDE.md` - LoRA training
- `agents/` - Agent specifications
