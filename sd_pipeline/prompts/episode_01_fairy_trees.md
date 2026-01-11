# Stable Diffusion Prompts: Episode 1 - Fairy Trees

## Model Recommendations

| Model | Best For | Notes |
|-------|----------|-------|
| **SDXL 1.0** | Quality, detail | Recommended for final production |
| **SD 1.5** | LoRA compatibility | Better if using custom style LoRA |
| **Juggernaut XL** | Photorealistic + artistic | Good middle ground |

## Global Settings

```yaml
# Recommended settings for paper-cut style
steps: 30-40
cfg_scale: 7-8
sampler: DPM++ 2M Karras
scheduler: Karras
width: 576
height: 1024
# Or for SDXL:
width: 768
height: 1344
```

---

## Style Header (Apply to ALL prompts)

### Positive Style Tokens
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition
```

### Negative Prompt (Use for ALL)
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame
```

---

## Shot 1: Title Card

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

(decorative storybook frame border:1.3), (silhouette of Ireland map:1.2) in sage green, (single lone tree icon:1.3) in center, cream background, simple folk art design, centered symmetrical composition, title card style, warm golden light, (Celtic-inspired simple border:1.1)
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, complex patterns, realistic map
```

### Settings
- Seed: [record for consistency]
- CFG: 7.5
- Steps: 35

---

## Shot 2: Lone Hawthorn Tree

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

(single lone hawthorn tree:1.4) standing on (rolling Irish hillside:1.2), (soft misty morning:1.2), sage green and brown muted palette, (distant blue mountains:1.1), patchwork fields in background, peaceful countryside, the tree stands alone and special, (gentle fog:1.1) at base of hills, wide establishing shot, tranquil mood
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, forest, many trees, dense woodland
```

### Settings
- Seed: [record for consistency]
- CFG: 7.5
- Steps: 35

---

## Shot 3: Fairies Dancing

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

hawthorn tree at (gentle golden dusk:1.2), (tiny simple silhouette figures:1.3) dancing in a ring underneath branches, (soft golden magical glow:1.3) around the small figures, warm orange and purple sunset colours, (whimsical fairy ring:1.2), friendly not scary, paper-cut dancing figures are very small and simple, (enchanted warm atmosphere:1.2), magical but gentle
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, menacing, threatening, evil fairies, dark magic, night time, black colours
```

### Settings
- Seed: [record for consistency]
- CFG: 7
- Steps: 40

---

## Shot 4: Road Curves Around Tree

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

(aerial birds eye view:1.3), (country road curving around a single lone tree:1.4), (simple map illustration style:1.3), the road clearly bends to avoid the tree, green patchwork fields on either side, grey road with white center line, hawthorn tree preserved in the middle, (simplified landscape:1.2), warm afternoon colours, top-down perspective
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, cars, vehicles, buildings, urban, city, highway, motorway
```

### Settings
- Seed: [record for consistency]
- CFG: 7.5
- Steps: 35

---

## Shot 5: Ribbons on Branches

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

(close view of tree branches:1.2) with (many colourful fabric ribbons:1.4) tied to them, red blue yellow green white ribbons flutter gently, small cloth strips and tokens, (warm afternoon golden light:1.2) filtering through branches, feeling of care and tradition, (ribbons as simple paper-cut shapes:1.3), peaceful respectful atmosphere, (folk tradition:1.2), wishing tree
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, dead tree, bare branches, winter, dark colours, tattered ribbons
```

### Settings
- Seed: [record for consistency]
- CFG: 7
- Steps: 35

---

## Shot 6: Meaning Icon

### Prompt
```
(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition,

(simple centered icon:1.4), (single tree silhouette:1.3) with (soft glowing protective circle:1.3) around it, (folk art symbol style:1.3), very simple and symbolic, cream background, sage green tree, (golden warm glow:1.2) suggesting protection and respect, (minimal design:1.3), meaning card, peaceful, (simple geometric shapes:1.2), centered composition
```

### Negative
```
photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame, complex, detailed, realistic tree, multiple icons, off-center
```

### Settings
- Seed: [record for consistency]
- CFG: 8
- Steps: 30

---

## Batch Generation Command (A1111)

If using Automatic1111 with API enabled:

```bash
# Generate all 6 shots with consistent style
python generate_episode.py --episode 1 --model sd_xl_base_1.0.safetensors --output ./output/episode_01/
```

---

## Consistency Tips

1. **Record seeds** - Once you get a good result, save the seed
2. **Use same model** - Don't switch models mid-episode
3. **Batch in one session** - Generate all 6 together
4. **Keep CFG consistent** - Stick to 7-8 range
5. **Train a LoRA** - Best long-term solution for style lock-in
