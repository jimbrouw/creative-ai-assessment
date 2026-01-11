#!/usr/bin/env python3
"""
Batch Image Generator for Irish Folklore Shorts
Generates all 6 images for an episode using Stable Diffusion API (Automatic1111 or ComfyUI)

Usage:
    python generate_episode.py --episode 1 --api a1111
    python generate_episode.py --episode 1 --api comfy --workflow folklore_workflow.json
    python generate_episode.py --all --api a1111
"""

import argparse
import json
import os
import sys
import time
import requests
import base64
from pathlib import Path
from datetime import datetime

# Configuration
CONFIG = {
    "a1111_url": "http://127.0.0.1:7860",
    "comfy_url": "http://127.0.0.1:8188",
    "output_base": "./output",
    "pattern_library": "../data/pattern_library.json",
    "default_model": "sd_xl_base_1.0.safetensors",
    "lora_name": "folklore_papercut",
    "lora_weight": 0.8,
}

# Style configuration
STYLE_HEADER = """(paper-cut illustration:1.4), (flat watercolour background:1.3), (visible paper texture:1.2), (simple shapes:1.2), (1970s British children's TV animation:1.3), (Bagpuss style:1.2), (handmade tactile feel:1.2), warm muted colours, soft diffused lighting, (folk art:1.1), storybook illustration, nostalgic, gentle atmosphere, vertical composition"""

NEGATIVE_PROMPT = """photorealistic, photograph, 3d render, CGI, modern, harsh shadows, horror, creepy, dark, scary, gothic, spooky, text, watermark, logo, signature, face, detailed face, realistic human, anime, manga, cartoon network style, disney style, pixar, digital art, neon colours, high contrast, busy background, cluttered, multiple subjects, split frame"""

# Generation settings
GEN_SETTINGS = {
    "steps": 35,
    "cfg_scale": 7.5,
    "width": 768,
    "height": 1344,  # 9:16 aspect ratio
    "sampler_name": "DPM++ 2M Karras",
}


def load_pattern_library(path: str) -> dict:
    """Load the pattern library JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def get_episode(pattern_library: dict, episode_id: int) -> dict:
    """Get a specific episode from the pattern library."""
    for ep in pattern_library.get('starter_episodes', []):
        if ep.get('id') == episode_id:
            return ep
    raise ValueError(f"Episode {episode_id} not found in pattern library")


def build_prompt(scene_description: str, use_lora: bool = True) -> str:
    """Build the full prompt with style header and optional LoRA."""
    lora_tag = f"<lora:{CONFIG['lora_name']}:{CONFIG['lora_weight']}>, " if use_lora else ""
    return f"{lora_tag}{STYLE_HEADER}, {scene_description}"


def generate_a1111(prompt: str, negative: str, output_path: str, seed: int = -1) -> dict:
    """Generate image using Automatic1111 API."""
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "steps": GEN_SETTINGS["steps"],
        "cfg_scale": GEN_SETTINGS["cfg_scale"],
        "width": GEN_SETTINGS["width"],
        "height": GEN_SETTINGS["height"],
        "sampler_name": GEN_SETTINGS["sampler_name"],
        "seed": seed,
        "batch_size": 1,
        "n_iter": 1,
    }

    try:
        response = requests.post(
            f"{CONFIG['a1111_url']}/sdapi/v1/txt2img",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()

        # Save image
        if result.get('images'):
            image_data = base64.b64decode(result['images'][0])
            with open(output_path, 'wb') as f:
                f.write(image_data)

            # Get seed from info
            info = json.loads(result.get('info', '{}'))
            return {
                "success": True,
                "seed": info.get('seed', -1),
                "path": output_path
            }

        return {"success": False, "error": "No images returned"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def generate_comfy(prompt: str, negative: str, output_path: str, workflow_path: str) -> dict:
    """Generate image using ComfyUI API."""
    # Load workflow template
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)

    # Update workflow with our prompt (assumes standard node IDs)
    # This needs to be customized based on your workflow structure
    for node_id, node in workflow.items():
        if node.get('class_type') == 'CLIPTextEncode':
            if 'positive' in node.get('_meta', {}).get('title', '').lower():
                node['inputs']['text'] = prompt
            elif 'negative' in node.get('_meta', {}).get('title', '').lower():
                node['inputs']['text'] = negative

    try:
        # Queue the prompt
        response = requests.post(
            f"{CONFIG['comfy_url']}/prompt",
            json={"prompt": workflow},
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        prompt_id = result.get('prompt_id')

        # Poll for completion
        while True:
            history = requests.get(f"{CONFIG['comfy_url']}/history/{prompt_id}").json()
            if prompt_id in history:
                outputs = history[prompt_id].get('outputs', {})
                for node_id, output in outputs.items():
                    if 'images' in output:
                        # Get the image
                        image_info = output['images'][0]
                        image_url = f"{CONFIG['comfy_url']}/view?filename={image_info['filename']}&subfolder={image_info.get('subfolder', '')}&type={image_info['type']}"
                        image_response = requests.get(image_url)
                        with open(output_path, 'wb') as f:
                            f.write(image_response.content)
                        return {"success": True, "path": output_path}
                break
            time.sleep(1)

        return {"success": False, "error": "No images in output"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def generate_episode_images(episode: dict, output_dir: str, api: str = "a1111",
                           workflow_path: str = None, use_lora: bool = True):
    """Generate all 6 images for an episode."""

    os.makedirs(output_dir, exist_ok=True)

    # Extract image prompts from episode
    image_prompts = episode.get('image_prompts', {})

    results = []
    shot_names = [
        ("shot_1", "01_title_card"),
        ("shot_2", "02_hero_location"),
        ("shot_3", "03_beat_1"),
        ("shot_4", "04_beat_2"),
        ("shot_5", "05_beat_3"),
        ("shot_6", "06_meaning_card"),
    ]

    for prompt_key, filename in shot_names:
        scene_desc = image_prompts.get(prompt_key, "")
        if not scene_desc:
            print(f"  Warning: No prompt found for {prompt_key}")
            continue

        # Build full prompt
        full_prompt = build_prompt(scene_desc, use_lora)
        output_path = os.path.join(output_dir, f"{filename}.png")

        print(f"  Generating {filename}...")

        if api == "a1111":
            result = generate_a1111(full_prompt, NEGATIVE_PROMPT, output_path)
        elif api == "comfy":
            result = generate_comfy(full_prompt, NEGATIVE_PROMPT, output_path, workflow_path)
        else:
            result = {"success": False, "error": f"Unknown API: {api}"}

        results.append({
            "shot": prompt_key,
            "filename": filename,
            **result
        })

        if result.get("success"):
            print(f"    ✓ Saved to {output_path}")
            if result.get("seed"):
                print(f"    Seed: {result['seed']}")
        else:
            print(f"    ✗ Failed: {result.get('error')}")

        # Small delay between generations
        time.sleep(1)

    # Save generation log
    log_path = os.path.join(output_dir, "generation_log.json")
    with open(log_path, 'w') as f:
        json.dump({
            "episode_id": episode.get('id'),
            "episode_title": episode.get('title'),
            "generated_at": datetime.now().isoformat(),
            "api": api,
            "use_lora": use_lora,
            "settings": GEN_SETTINGS,
            "results": results
        }, f, indent=2)

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate images for folklore episodes")
    parser.add_argument("--episode", type=int, help="Episode ID to generate")
    parser.add_argument("--all", action="store_true", help="Generate all episodes")
    parser.add_argument("--api", choices=["a1111", "comfy"], default="a1111",
                       help="Which API to use (default: a1111)")
    parser.add_argument("--workflow", type=str, help="ComfyUI workflow JSON path")
    parser.add_argument("--no-lora", action="store_true", help="Don't use LoRA (prompt-only)")
    parser.add_argument("--output", type=str, default=CONFIG["output_base"],
                       help="Output directory base")
    parser.add_argument("--pattern-library", type=str, default=CONFIG["pattern_library"],
                       help="Path to pattern_library.json")

    args = parser.parse_args()

    if not args.episode and not args.all:
        parser.error("Must specify --episode ID or --all")

    if args.api == "comfy" and not args.workflow:
        parser.error("ComfyUI requires --workflow path")

    # Load pattern library
    try:
        pattern_library = load_pattern_library(args.pattern_library)
    except FileNotFoundError:
        print(f"Error: Pattern library not found at {args.pattern_library}")
        sys.exit(1)

    episodes = pattern_library.get('starter_episodes', [])

    if args.episode:
        episodes = [ep for ep in episodes if ep.get('id') == args.episode]
        if not episodes:
            print(f"Error: Episode {args.episode} not found")
            sys.exit(1)

    # Generate each episode
    for episode in episodes:
        ep_id = episode.get('id')
        title = episode.get('title', 'unknown')
        slug = title.lower().replace(' ', '_').replace('?', '').replace("'", '')[:30]

        output_dir = os.path.join(
            args.output,
            f"episode_{ep_id:02d}_{slug}"
        )

        print(f"\n{'='*60}")
        print(f"Episode {ep_id}: {title}")
        print(f"Output: {output_dir}")
        print(f"{'='*60}")

        results = generate_episode_images(
            episode=episode,
            output_dir=output_dir,
            api=args.api,
            workflow_path=args.workflow,
            use_lora=not args.no_lora
        )

        success = sum(1 for r in results if r.get('success'))
        print(f"\nCompleted: {success}/{len(results)} images generated")

    print("\nDone!")


if __name__ == "__main__":
    main()
