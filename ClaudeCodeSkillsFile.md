# ClaudeCodeSkillsFile.md

**Version:** 1.0
**Purpose:** Build a Claude Code "agent system" to automate a faceless YouTube content pipeline (niche → channel intel → concepts → scripts → asset prompts → QA → output pack).

---

## 0) What You're Building (Plain English)

You're not "using AI to make videos". You're building a **repeatable pipeline** that:

1. Picks a niche that suits faceless automation
2. Studies what already works in that niche
3. Extracts reusable patterns (titles, hooks, thumbnails)
4. Generates new ideas strictly derived from those patterns
5. Writes scripts to a fixed structure
6. Produces clean prompts for voiceover + thumbnails + b-roll
7. Runs QA that rejects weak output and forces regeneration
8. Outputs a publish-ready "content pack" per video

This is a production system. The win is **consistency + QA + volume**, not "clever prompts".

---

## 1) Architecture (Orchestrator + Specialist Agents)

### A) Orchestrator Agent (The Boss)

**Job:** Run the entire pipeline end-to-end, call specialist agents, enforce constraints, and produce a final output pack + run log.

**Input:**
- Niche OR list of candidate niches
- Seed channels
- Output target (e.g., 3/week)
- Brand voice rules

**Output:** `output_pack/{date}_{video_slug}/` folder with:
- title
- script
- thumbnail prompt
- voice prompt
- description
- tags
- QA report
- log

**Spec:** See `agents/orchestrator.md`

---

### B) Niche Selection Agent

**Job:** Score candidate niches for faceless viability and monetisation pathways.

**Output:** Top 1–2 niches with reasons + red flags.

**Spec:** See `agents/niche.md`

---

### C) Channel Intelligence Agent (Most Important)

**Job:** Analyse seed channels and derive **observable patterns** from top-performing videos.

**Output:** Pattern library in JSON:
- title_templates
- hook_patterns
- thumbnail_text_rules
- topic_clusters

**Spec:** See `agents/channel_intel.md`

---

### D) Concept Generator Agent

**Job:** Generate video ideas that are *provably derived* from the pattern library.

**Output:** 10–30 concepts, each citing:
- Which pattern(s) it uses
- Which reference video(s) it maps to

**Spec:** See `agents/concepts.md`

---

### E) Script Agent

**Job:** Write scripts to a fixed structure and length, audio-first, no fluff.

**Output:**
- Final script
- Beat sheet
- Cold open options (3 variants)

**Spec:** See `agents/script.md`

---

### F) Asset Prompt Agent

**Job:** Generate clean prompts for external tools (voiceover, thumbnails, b-roll lists).

**Output:** Prompt pack with strict constraints:
- Composition rules
- Word limits
- Tone requirements

**Spec:** See `agents/assets.md`

---

### G) QA + Feedback Agent (Non-Optional)

**Job:** Adversarial review. Reject weak output. Send back to upstream agent with specific fix instructions.

**Output:**
- QA scorecard
- Pass/fail decision
- Required changes (if fail)

**Spec:** See `agents/qa.md`

---

## 2) Folder Structure

```
youtube-agent/
├── README.md
├── ClaudeCodeSkillsFile.md
│
├── agents/
│   ├── orchestrator.md
│   ├── niche.md
│   ├── channel_intel.md
│   ├── concepts.md
│   ├── script.md
│   ├── assets.md
│   └── qa.md
│
├── config/
│   ├── brand_rules.json
│   ├── niches.json
│   ├── seed_channels.json
│   └── constraints.json
│
├── data/
│   ├── channel_dumps/        # Raw scraped / API results
│   └── pattern_library.json  # Derived patterns
│
└── output_pack/
    └── {date}_{slug}/
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

---

## 3) Input Configuration Files

### config/niches.json

```json
{
  "candidate_niches": [
    "History mysteries",
    "Personal finance explainers",
    "Engineering disasters",
    "Courtroom stories"
  ],
  "selected_niche": null
}
```

### config/seed_channels.json

```json
{
  "seed_channels": [
    {
      "url": "https://www.youtube.com/@examplechannel1",
      "name": "Example Channel 1"
    },
    {
      "url": "https://www.youtube.com/@examplechannel2",
      "name": "Example Channel 2"
    }
  ]
}
```

### config/constraints.json

```json
{
  "output_format": "longform",
  "video_length_minutes": [8, 14],
  "script_word_count": [1100, 1800],
  "thumbnail": {
    "text_words_max": 5,
    "color_limit": 3
  },
  "tone": "direct, factual, no cringe",
  "cadence": "3_per_week"
}
```

### config/brand_rules.json

```json
{
  "voice": {
    "do": ["short sentences", "active voice", "clear claims"],
    "dont": ["hype", "cliches", "rambling intros"]
  },
  "format_rules": {
    "hook_seconds": 5,
    "sections": ["HOOK", "CONTEXT", "ESCALATION", "PAYOFF", "WRAP"]
  }
}
```

---

## 4) Agent Specifications Summary

### 4.1 Niche Agent

**Skill:** Niche scoring and filtering.

**Hard rules:**
- Do not brainstorm endlessly
- Return top 1–2 niches only
- Use a scoring table
- Kill weak niches decisively

**Scoring dimensions (1–5):**
- Faceless suitability
- Asset availability
- Evergreen potential
- Competition density
- Monetisation options

---

### 4.2 Channel Intelligence Agent

**Skill:** Extract patterns from channel performance data.

**Hard rules:**
- Only claim patterns that are observable from data
- No "generic advice"
- Normalise performance by size (views/subs; velocity)
- Ignore creator personality

**Output:** `pattern_library.json` with:
- title_templates
- hook_templates
- topic_clusters
- thumbnail_rules

---

### 4.3 Concept Generator Agent

**Skill:** Generate concepts strictly derived from patterns.

**Hard rules:**
- Every concept must cite pattern template used
- Every concept must cite reference video(s)
- No random creativity
- Keep concepts feasible with available assets

---

### 4.4 Script Agent

**Skill:** Scriptwriting with structure + constraints.

**Hard rules:**
- Must follow structure: HOOK → CONTEXT → ESCALATION → PAYOFF → WRAP
- Audio-first: short sentences, easy to read aloud
- No fluff phrases, no self-references
- Must hit word count range

---

### 4.5 Asset Prompt Agent

**Skill:** Generate prompts for external tools.

**Hard rules:**
- Do not generate images
- Produce prompts with strict composition rules
- Thumbnail text ≤ 5 words
- Limit palette to ≤ 3 colours
- Single focal point, high contrast, no clutter

---

### 4.6 QA Agent

**Skill:** Adversarial QA.

**Hard rules:**
- Be strict. Reject weak work.
- Score and explain clearly.
- If fail: specify exactly what to fix and which agent must redo it.

**Scorecard (1–5):**
- Clickability
- Hook strength
- Clarity
- Novelty-within-pattern
- Feasibility
- Script pacing

**Pass criteria:** Average ≥ 4.0 and no category < 3.

---

## 5) Orchestrator Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. NICHE SELECTION                                          │
│    If niche not fixed → Run Niche Agent                     │
│    If fixed → Validate against constraints                  │
├─────────────────────────────────────────────────────────────┤
│ 2. PATTERN LIBRARY CHECK                                    │
│    If pattern_library.json exists → Load                    │
│    If missing → Request channel dump OR halt                │
├─────────────────────────────────────────────────────────────┤
│ 3. CHANNEL INTELLIGENCE                                     │
│    Run Channel Intel Agent → Update pattern_library.json    │
├─────────────────────────────────────────────────────────────┤
│ 4. CONCEPT GENERATION                                       │
│    Run Concept Agent → 10-30 concepts                       │
├─────────────────────────────────────────────────────────────┤
│ 5. CONCEPT SELECTION                                        │
│    Orchestrator picks best concept based on:                │
│    - Constraint fit                                         │
│    - Pattern strength                                       │
│    - Asset feasibility                                      │
├─────────────────────────────────────────────────────────────┤
│ 6. SCRIPT + ASSETS                                          │
│    Run Script Agent → script + beats + hooks                │
│    Run Asset Agent → prompts + b-roll list                  │
├─────────────────────────────────────────────────────────────┤
│ 7. QA GATE                                                  │
│    Run QA Agent → scorecard                                 │
│    If PASS → Proceed to output                              │
│    If FAIL → Loop back with fix brief (max 3 retries)       │
├─────────────────────────────────────────────────────────────┤
│ 8. OUTPUT PACK                                              │
│    Write all files to output_pack/{date}_{slug}/            │
└─────────────────────────────────────────────────────────────┘
```

---

## 6) Copy-Paste Prompt Blocks

### 6.1 Orchestrator "Run" Prompt

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

### 6.2 Channel Intel Agent Prompt

```
Act as the Channel Intelligence Agent.

Input: channel video dataset (titles, views, publish dates, durations; optionally thumbnails).
Task: identify repeatable patterns that correlate with high performance relative to channel size and time since publish.

Output: JSON pattern library with evidence per pattern.
Do not invent data. If dataset is missing, ask for it and stop.
```

### 6.3 Concept Generator Prompt

```
Act as the Concept Generator Agent.

Input: pattern_library.json.
Generate 20 concepts. Each must include:
- Working title
- Hook line
- Promise
- Asset requirements
- Pattern template used
- Reference video(s) that inspired it

No random creativity. Only pattern-derived ideas.
```

### 6.4 Script Agent Prompt

```
Act as the Script Agent.

Input: selected concept + constraints.
Write a script that follows:
HOOK (<=5s) / CONTEXT / ESCALATION (3-5 beats) / PAYOFF / WRAP
Audio-first. Short sentences. No fluff.
Hit the specified word count range.

Deliver:
- Final script
- Beat sheet
- 3 hook variants
```

### 6.5 Asset Prompts Agent Prompt

```
Act as the Asset Prompt Agent.

Input: concept + title + script + constraints.
Deliver:
- ElevenLabs voice prompt (tone, pace, pronunciation)
- Thumbnail prompt (composition, text <=5 words, <=3 colours, single focal point)
- B-roll shot list (categories)

Do not generate images. Produce prompts only.
```

### 6.6 QA Agent Prompt

```
Act as the QA Agent.

Score:
- Clickability
- Hook strength
- Clarity
- Novelty-within-pattern
- Feasibility
- Pacing

Pass if avg >= 4.0 and no category < 3.
If fail: specify exact fixes and which stage must redo work.
Be strict.
```

---

## 7) Non-Negotiables

1. **Pattern evidence or it doesn't ship** - Every concept needs data backing
2. **QA must be allowed to reject output** - No bypassing quality gates
3. **Keep niche count low (1–2) until proven** - Focus beats sprawl
4. **Publish cadence matters more than perfect prompts** - Consistency wins

---

## 8) Configuration Checklist

Before running the pipeline, answer these and update `config/constraints.json`:

| Question | Options | Your Choice |
|----------|---------|-------------|
| Output format | longform / shorts / both | |
| Preferred niches | 3 candidates OR "cold selection" | |
| Volume | 1/day / 3/week / batch weekly | |
| Risk level | evergreen / trend surfing | |
| Monetisation target | ads / affiliate / lead gen / sell channel / funnel | |

---

## 9) Getting Started

1. **Configure niches** → Edit `config/niches.json`
2. **Add seed channels** → Edit `config/seed_channels.json`
3. **Provide channel data** → Add JSON files to `data/channel_dumps/`
4. **Set constraints** → Edit `config/constraints.json`
5. **Run orchestrator** → Use the prompt from section 6.1

The pipeline will produce a complete content pack in `output_pack/`.

---

## 10) Example Output

See `output_pack/_example_video/` for a complete example showing all generated files with the expected format and structure.
