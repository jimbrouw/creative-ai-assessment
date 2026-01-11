# Asset Prompts

> This is a template file showing the expected format.

---

## 1. ElevenLabs Voice Prompt

### Voice Selection
- **Recommended voice**: Adam (or similar deep, authoritative male voice)
- **Alternative**: Daniel, Antoni
- **Voice characteristics**:
  - Male, 35-50 years old
  - American accent (neutral/Midwest)
  - Authoritative but not dramatic
  - Documentary narrator style

### Tone Settings (ElevenLabs Parameters)
| Setting | Value | Notes |
|---------|-------|-------|
| Stability | 0.65 | Balanced consistency with some expression |
| Similarity | 0.75 | Stay close to base voice |
| Style | 0.30 | Subtle style, not exaggerated |
| Speaker Boost | On | Clearer pronunciation |

### Pacing Notes
- **Overall pace**: Medium (145-155 words per minute)
- **Hook**: Slightly slower, deliberate. Weight on "30 seconds" and "No one checked the math."
- **Context**: Steady, informative. Clear delivery.
- **Escalation**: Gradually build pace through beats. Beat 5 slightly faster.
- **Payoff**: Return to medium pace. Weight on "53%" and accountability details.
- **Wrap**: Slow down. Thoughtful, reflective. Pause before final line.

### Pronunciation Guide
| Word/Phrase | Pronunciation |
|-------------|---------------|
| Hyatt Regency | HY-at REE-jen-see |
| atrium | AY-tree-um |
| Kansas City | Standard American |
| NBS (if used) | Spell out: "National Bureau of Standards" |

### Emotion/Energy Map

| Section | Time | Energy | Emotion | Voice Notes |
|---------|------|--------|---------|-------------|
| Hook | 0:00-0:15 | 7/10 | Intrigue | Draw in. Weight on key phrases. |
| Context: Setting | 0:15-0:30 | 5/10 | Descriptive | Paint the picture. Steady. |
| Context: Walkways | 0:30-0:50 | 5/10 | Informative | Technical but accessible. |
| Context: The Night | 0:50-1:15 | 5/10 | Building | Slight tension building. |
| Context: Collapse | 1:15-1:30 | 6/10 | Somber | Respectful. Not dramatic. |
| Escalation 1 | 1:30-3:00 | 5/10 | Explanatory | Clear, educational. |
| Escalation 2 | 3:00-4:30 | 6/10 | Tension | "30 seconds" with weight. |
| Escalation 3 | 4:30-6:00 | 6/10 | Concern | The flaw revealed. |
| Escalation 4 | 6:00-7:00 | 6/10 | Dread | The trap is set. |
| Escalation 5 | 7:00-8:00 | 7/10 | Urgent | Building to failure. |
| Payoff | 8:00-9:30 | 6→5/10 | Resolution | Facts, then settle. |
| Wrap | 9:30-10:00 | 5/10 | Reflective | Thoughtful. Pause before end. |

### Do NOT
- Use "YouTube voice" (over-enthusiastic, exaggerated)
- Rush through technical explanations
- Dramatize the deaths (respectful, factual)
- Sound bored or monotone
- Add "um", "uh", or filler sounds

---

## 2. Thumbnail Prompt

### Concept
A dramatic but tasteful image conveying catastrophic structural failure—focus on the engineering aspect, not the human tragedy.

### Composition
- **Layout**: Rule of thirds, text in left third
- **Focal point**: A cracking/failing structural element (beam or connection)
- **Background**: Dark gradient, suggesting hotel atrium
- **Depth**: Foreground text, midground structure, dark background

### Text Overlay
- **Text**: "FATAL MISTAKE"
- **Word count**: 2 words
- **Position**: Left third, vertically centered
- **Font style**: Bold impact-style sans-serif, all caps
- **Text color**: White (#FFFFFF) with thin black outline
- **Drop shadow**: Yes, dark (#000000), 3px offset

### Color Palette
| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary (60%) | Dark Blue/Black | #1a1a2e | Background |
| Secondary (30%) | Red | #e63946 | Accent on break point |
| Accent (10%) | White | #FFFFFF | Text |

### Subject/Imagery
- **Main subject**: Structural beam or connection point with visible crack/failure
- **Style**: Photorealistic with subtle dramatic lighting
- **Emotion/mood**: Tension, impending failure, ominous
- **NO**: Blood, bodies, graphic imagery, actual crash photos

### Technical Requirements
- Aspect ratio: 16:9
- Resolution: 1920x1080
- File format: PNG
- Safe zones: Keep text 10% from edges

### AI Image Generator Prompt (Midjourney/DALL-E)

```
A dramatic close-up of a steel structural connection point showing stress fractures and deformation, with one bolt beginning to tear through the metal. Dark atmospheric lighting with a subtle red glow highlighting the point of failure. Industrial hotel architecture visible but blurred in the background. Photorealistic style, high contrast, cinematic lighting. Dark moody color palette with deep blues and blacks. No people visible. Engineering disaster aesthetic. --ar 16:9 --style raw --v 6
```

**Post-production notes:**
- Add "FATAL MISTAKE" text overlay manually
- Ensure text doesn't overlap with key visual elements
- Check contrast at 120x90px (search result size)

---

## 3. B-Roll Reference

See `06_broll_list.md` for complete shot list.

**Summary:**
- Total shots needed: ~25-30
- Stock footage: ~70%
- Archival footage: ~15%
- Custom graphics: ~15%

**Primary stock sources:**
- Storyblocks (construction, engineering)
- Pond5 (archival news footage)
- Archive.org (historical footage, public domain)

**Custom assets needed:**
- Walkway structural diagram (original vs. modified)
- Load distribution animation
- Timeline graphic
