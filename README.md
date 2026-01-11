# Faceless YouTube Pipeline - Agent System

A Claude Code agent system for automating faceless YouTube content production. This system uses multiple specialized agents to handle niche selection, channel analysis, concept generation, scriptwriting, asset prompts, and quality assurance.

## What This Does

This is a **repeatable production pipeline** that:

1. Picks a niche suited for faceless automation
2. Studies what works in that niche (seed channels)
3. Extracts reusable patterns (titles, hooks, thumbnails)
4. Generates ideas derived from proven patterns
5. Writes scripts to a fixed structure
6. Produces prompts for voiceover, thumbnails, and b-roll
7. Runs QA that rejects weak output
8. Outputs a publish-ready "content pack" per video

The win is **consistency + QA + volume**, not clever prompts.

## Quick Start

### 1. Configure Your Niche

Edit `config/niches.json`:

```json
{
  "candidate_niches": [
    "Your niche 1",
    "Your niche 2"
  ],
  "selected_niche": null
}
```

Set `selected_niche` to lock in a specific niche, or leave `null` for the Niche Agent to evaluate candidates.

### 2. Add Seed Channels

Edit `config/seed_channels.json`:

```json
{
  "seed_channels": [
    {
      "url": "https://www.youtube.com/@YourSeedChannel",
      "name": "Channel Name"
    }
  ]
}
```

Add 3-5 successful channels in your chosen niche.

### 3. Provide Channel Data

The system needs performance data for seed channels. Place JSON files in `data/channel_dumps/`:

```json
{
  "channel": "@ChannelHandle",
  "subscriber_count": 500000,
  "videos": [
    {
      "video_id": "xxx",
      "title": "Video Title",
      "views": 1000000,
      "publish_date": "2025-06-15",
      "duration_seconds": 720
    }
  ]
}
```

**Data sources:**
- YouTube Data API v3 (recommended)
- vidIQ / TubeBuddy exports
- Manual collection

### 4. Set Constraints

Edit `config/constraints.json`:

```json
{
  "output_format": "longform",
  "video_length_minutes": [8, 14],
  "script_word_count": [1100, 1800],
  "cadence": "3_per_week"
}
```

### 5. Run the Orchestrator

In Claude Code, use this prompt:

```
You are the Orchestrator Agent for a faceless YouTube pipeline.

Goal: produce a publish-ready output pack for one video, using the specialist agent specs in /agents.

Read:
- /config/constraints.json
- /config/seed_channels.json
- /config/brand_rules.json (if exists)
- /data/pattern_library.json (if exists)

Pipeline:
1) If niche not fixed, run Niche Selection Agent.
2) Ensure pattern_library.json exists; if missing, request channel dump input OR produce a plan to fetch it.
3) Run Channel Intelligence Agent to update pattern_library.json.
4) Run Concept Generator Agent (10–30 concepts).
5) Select best concept (fit constraints + pattern strength).
6) Run Script Agent and Asset Prompt Agent.
7) Run QA Agent. If fail, loop to the correct stage with a fix brief.
8) If pass, write output_pack/{date}_{slug}/ with all required files.

Rules:
- No generic advice.
- Every concept must cite patterns + references.
- Enforce constraints strictly.
- Output must be structured, file-ready.
```

## Folder Structure

```
youtube-agent/
├── README.md
├── ClaudeCodeSkillsFile.md      # Full system specification
│
├── agents/                       # Agent specifications
│   ├── orchestrator.md          # Pipeline controller
│   ├── niche.md                 # Niche selection & scoring
│   ├── channel_intel.md         # Pattern extraction
│   ├── concepts.md              # Idea generation
│   ├── script.md                # Scriptwriting
│   ├── assets.md                # Prompt generation
│   └── qa.md                    # Quality assurance
│
├── config/                       # Configuration files
│   ├── niches.json              # Candidate niches
│   ├── seed_channels.json       # Reference channels
│   ├── constraints.json         # Production constraints
│   └── brand_rules.json         # Voice & style rules
│
├── data/                         # Working data
│   ├── channel_dumps/           # Raw channel exports
│   └── pattern_library.json     # Extracted patterns
│
└── output_pack/                  # Generated content
    └── {date}_{slug}/           # Per-video folder
        ├── 00_run_log.md
        ├── 01_title_options.md
        ├── 02_concept.md
        ├── 03_script.md
        ├── 03_script_beats.md
        ├── 03_hook_options.md
        ├── 04_description_tags.md
        ├── 05_asset_prompts.md
        ├── 06_broll_list.md
        └── 07_qa_report.md
```

## Agents Overview

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| **Orchestrator** | Run pipeline end-to-end | All configs | Output pack + log |
| **Niche Selection** | Score niches for viability | Candidates list | Top 1-2 niches |
| **Channel Intel** | Extract patterns from data | Channel video data | pattern_library.json |
| **Concept Generator** | Generate pattern-derived ideas | Pattern library | 10-30 concepts |
| **Script** | Write structured scripts | Concept + constraints | Script + beats + hooks |
| **Asset Prompts** | Create external tool prompts | Script + concept | Voice/thumb/b-roll prompts |
| **QA** | Adversarial review | All outputs | Scorecard + pass/fail |

## Non-Negotiables

1. **Pattern evidence required** - Every concept must cite patterns with data
2. **QA has veto power** - Weak output gets rejected and redone
3. **Constraints enforced** - Word count, thumbnail rules, structure
4. **No generic advice** - Every output must be specific and actionable
5. **Publish cadence > perfect prompts** - Consistency is the goal

## Example Output

See `output_pack/_example_video/` for a complete example of all generated files.

## Configuration Reference

### constraints.json

| Field | Description | Example |
|-------|-------------|---------|
| `output_format` | longform / shorts / both | `"longform"` |
| `video_length_minutes` | Duration range | `[8, 14]` |
| `script_word_count` | Word count range | `[1100, 1800]` |
| `thumbnail.text_words_max` | Max thumbnail text | `5` |
| `thumbnail.color_limit` | Max colors | `3` |
| `cadence` | Production rate | `"3_per_week"` |
| `risk_level` | evergreen / trend_surfing | `"evergreen"` |
| `monetisation_target` | ads / affiliate / lead_gen | `"ads"` |

### brand_rules.json

Defines voice, tone, and style rules:
- `voice.do` - Writing rules to follow
- `voice.dont` - Things to avoid
- `format_rules` - Script structure requirements
- `thumbnail_rules` - Visual guidelines
- `title_rules` - Title constraints

## Getting Channel Data

### Option 1: YouTube Data API v3 (Recommended)

1. Create Google Cloud project
2. Enable YouTube Data API v3
3. Create API credentials
4. Use `channels.list` and `search.list` endpoints

### Option 2: Third-Party Tools

- **vidIQ**: Export channel analytics
- **TubeBuddy**: Export competitor data
- **Social Blade**: Historical data

### Option 3: Manual Collection

For small datasets, manually record:
- Video titles
- View counts
- Publish dates
- Durations

## License

This system is designed for legitimate content creation. Use responsibly.
