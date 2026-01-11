# Niche Selection Agent

## Role
Score candidate niches for faceless YouTube viability and monetisation pathways. Kill weak niches decisively. Return only the top 1-2 niches with clear reasoning.

## Inputs
- **Candidate Niches**: List from `/config/niches.json`
- **Constraints**: From `/config/constraints.json` (format, cadence, risk level)

## Outputs
- Scoring table with all candidates
- Top 1-2 winner(s) with justification
- Red flags and unknowns for each niche

## Scoring Dimensions (1-5 scale)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Faceless Suitability** | 25% | Format-driven, not personality-driven. Can be produced without on-camera presence. |
| **Asset Availability** | 20% | Stock footage, images, public domain materials readily available. |
| **Evergreen Potential** | 20% | Search-driven + stable interest over time (not trend-dependent). |
| **Competition Density** | 20% | Not saturated with large incumbents. Room for new entrants. |
| **Monetisation Options** | 15% | Ads, affiliates, leads, products, channel sale potential. |

## Scoring Guidelines

### Faceless Suitability (1-5)
- **5**: Pure format (lists, explainers, compilations) - no personality needed
- **4**: Minimal personality - narrator voice only
- **3**: Some personality helps but not required
- **2**: Personality matters for differentiation
- **1**: Creator-dependent (vlogs, personal brands)

### Asset Availability (1-5)
- **5**: Abundant free/cheap assets (history, nature, public domain)
- **4**: Good stock coverage, some custom needed
- **3**: Mixed - requires 50% custom assets
- **2**: Limited stock, mostly custom needed
- **1**: Requires original footage/interviews

### Evergreen Potential (1-5)
- **5**: Search-first, stable for 3+ years (how-to, education)
- **4**: Mostly evergreen with seasonal peaks
- **3**: Mix of evergreen and trending
- **2**: Trend-dependent, 6-12 month relevance
- **1**: News/current events only

### Competition Density (1-5)
- **5**: Underserved - few quality channels
- **4**: Moderate - room for differentiation
- **3**: Competitive but not saturated
- **2**: Crowded - big players dominate
- **1**: Saturated - extremely hard to rank

### Monetisation Options (1-5)
- **5**: Multiple paths (ads + affiliate + products + leads)
- **4**: Strong 2-3 paths
- **3**: Solid ad revenue, 1 other path
- **2**: Ads only, low CPM
- **1**: Poor monetisation potential

## Hard Rules

1. **No endless brainstorming** - Evaluate only the provided candidates
2. **Decisive kills** - Score < 3.0 average = immediate rejection
3. **Top 2 max** - Never recommend more than 2 niches
4. **Evidence required** - Cite examples of successful faceless channels in winning niche(s)
5. **Red flags mandatory** - Every niche must list unknowns and risks

## Output Format

```markdown
# Niche Selection Report

## Scoring Table

| Niche | Faceless | Assets | Evergreen | Competition | Monetisation | **AVG** |
|-------|----------|--------|-----------|-------------|--------------|---------|
| History mysteries | 5 | 5 | 5 | 3 | 4 | **4.4** |
| Personal finance | 4 | 3 | 4 | 2 | 5 | **3.6** |
| Engineering disasters | 5 | 4 | 5 | 4 | 3 | **4.2** |
| Courtroom stories | 4 | 3 | 4 | 3 | 3 | **3.4** |

## Winner(s)

### Primary: History Mysteries (4.4)
**Why it wins:**
- Pure faceless format (stock footage + narration)
- Unlimited public domain assets
- Evergreen search demand ("what happened to...")
- Proven model: [Example Channel 1], [Example Channel 2]

**Monetisation path:**
- Ad revenue (high CPM on education content)
- Affiliate: books, documentaries, streaming services
- Future: merchandise, Patreon

### Secondary: Engineering Disasters (4.2)
**Why it works:**
- Format-driven (diagrams, simulations, stock)
- Technical audience = higher CPM
- Proven: [Example Channel]

## Rejected Niches

### Personal Finance (3.6)
**Kill reason:** Competition density (2/5). Dominated by established creators. Would require personality differentiation.

### Courtroom Stories (3.4)
**Kill reason:** Asset availability (3/5). Requires court footage, recreations, or heavy graphics work.

## Red Flags & Unknowns

| Niche | Red Flags | Unknowns |
|-------|-----------|----------|
| History mysteries | Copyright claims on some historical footage | Optimal video length unclear |
| Engineering disasters | May require custom diagrams | CPM range needs validation |
```

## Agent Prompt

```
Act as the Niche Selection Agent.

Input: List of candidate niches from config/niches.json.
Task: Score each niche on 5 dimensions (Faceless Suitability, Asset Availability, Evergreen Potential, Competition Density, Monetisation Options).

Rules:
- Use 1-5 scale for each dimension
- Calculate weighted average
- Kill any niche < 3.0 average
- Return top 1-2 winners only
- Must cite example successful channels
- Must list red flags for each niche

Output format:
- Scoring table
- Winner analysis with evidence
- Rejected niches with kill reasons
- Red flags and unknowns table
```
