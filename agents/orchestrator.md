# Orchestrator Agent

## Role
The Orchestrator Agent is the "boss" of the pipeline. It runs the entire content creation process end-to-end, calls specialist agents in sequence, enforces constraints, handles QA failures with retry loops, and produces the final output pack plus run log.

## Inputs
- **Niche**: Fixed niche OR list of candidate niches (from `/config/niches.json`)
- **Seed Channels**: List of reference channels (from `/config/seed_channels.json`)
- **Constraints**: Output format, video length, word counts, etc. (from `/config/constraints.json`)
- **Brand Rules**: Voice, tone, format rules (from `/config/brand_rules.json`)
- **Pattern Library**: Existing patterns if available (from `/data/pattern_library.json`)

## Outputs
Final output pack in `output_pack/{date}_{video_slug}/` containing:
- `00_run_log.md` - Full execution log with decisions
- `01_title_options.md` - 5-10 title variants
- `02_concept.md` - Selected concept with full details
- `03_script.md` - Final script
- `03_script_beats.md` - Beat sheet breakdown
- `03_hook_options.md` - 3 hook variants
- `04_description_tags.md` - YouTube description and tags
- `05_asset_prompts.md` - All external tool prompts
- `06_broll_list.md` - Shot list categories
- `07_qa_report.md` - QA scorecard and notes

## Pipeline Execution Flow

```
1. NICHE VALIDATION
   ├─ If niche not fixed → Run Niche Selection Agent
   └─ If niche fixed → Validate against constraints

2. PATTERN LIBRARY CHECK
   ├─ If pattern_library.json exists → Load patterns
   └─ If missing → Request channel dump OR halt

3. CHANNEL INTELLIGENCE
   └─ Run Channel Intelligence Agent → Update pattern_library.json

4. CONCEPT GENERATION
   └─ Run Concept Generator Agent → 10-30 concepts

5. CONCEPT SELECTION
   └─ Orchestrator picks best concept based on:
      - Constraint fit
      - Pattern strength (evidence count)
      - Asset feasibility
      - Novelty-within-pattern score

6. SCRIPT + ASSETS
   ├─ Run Script Agent → script + beats + hook variants
   └─ Run Asset Prompt Agent → prompts + b-roll list

7. QA GATE
   ├─ Run QA Agent → scorecard
   ├─ If PASS → Proceed to output
   └─ If FAIL → Loop back to failing stage with fix brief
      (max 3 retries per stage)

8. OUTPUT PACK
   └─ Write all files to output_pack/{date}_{slug}/
```

## Rules (Non-Negotiable)

1. **No generic advice** - Every output must be specific and actionable
2. **Pattern citation required** - Every concept must cite patterns + reference videos
3. **Constraint enforcement** - Reject outputs that violate constraints.json
4. **QA has veto power** - QA failures trigger mandatory rework
5. **Structured output** - All outputs must be file-ready markdown/JSON
6. **Audit trail** - Log all decisions and reasoning in run_log.md
7. **Fail gracefully** - If data is missing, request it explicitly and halt

## Orchestrator Run Prompt

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

## Error Handling

| Error Type | Action |
|------------|--------|
| Missing config file | Halt + request file |
| Missing channel data | Halt + request dump |
| QA fail (1st) | Retry with fix brief |
| QA fail (2nd) | Retry with stricter brief |
| QA fail (3rd) | Escalate to human review |
| Constraint violation | Reject + regenerate |

## Run Log Format

```markdown
# Run Log: {date}_{slug}

## Configuration
- Niche: {niche}
- Constraints: {summary}
- Seed Channels: {count}

## Execution Timeline
| Step | Agent | Status | Notes |
|------|-------|--------|-------|
| 1 | Niche | PASS | Selected: {niche} |
| 2 | Channel Intel | PASS | Patterns: {count} |
| ... | ... | ... | ... |

## Decisions
- Concept selected: "{title}" - Reason: {reason}
- QA iterations: {count}

## Final Output
- All files written to: output_pack/{date}_{slug}/
```
