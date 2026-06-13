"""
generate_v02_s16_39_placeholders.py
===================================
Generates placeholder and synthetic images for Scenes 3, 4, and 5
so that the dry-runs and renders do not crash due to missing files.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_solid_image(path: Path, color: tuple[int, int, int], text: str, size: tuple[int, int] = (512, 512)) -> None:
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    # Simple cross lines
    draw.rectangle([10, 10, size[0] - 10, size[1] - 10], outline=(255, 255, 255), width=2)
    # Text
    draw.text((size[0] // 2, size[1] // 2), text, fill=(255, 255, 255), anchor="mm")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def create_gradient_grid(path: Path, color: tuple[int, int, int], text: str, size: tuple[int, int] = (256, 256)) -> None:
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    # Draw a 4x4 grid
    w, h = size[0] // 4, size[1] // 4
    for i in range(4):
        for j in range(4):
            # Alternate colors slightly
            val = (i + j) * 20
            r = min(255, color[0] + val)
            g = min(255, color[1] + val)
            b = min(255, color[2] + val)
            draw.rectangle([i * w, j * h, (i + 1) * w, (j + 1) * h], fill=(r, g, b), outline=(255, 255, 255), width=1)
            draw.text((i * w + w // 2, j * h + h // 2), str(10 + i * 4 + j), fill=(255, 255, 255), anchor="mm")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    assets_dir = root / "assets"
    
    # Define directories
    slides_dir = assets_dir / "slides_16_39"
    external_dir = assets_dir / "external_16_39"
    patches_dir = assets_dir / "patches"
    gen_dir = assets_dir / "generated"
    
    # 1. Slide Crops
    slides = [
        "s17_visual_words_dog_car.png", "s18_visual_words_clustering.png",
        "s20_image_tokenization.png", "s22_vqgan_overview.png",
        "s23_codebook_token_image.png", "s25_vq_loss.png",
        "s26_gan_loss.png", "s30_model_hierarchy.png",
        "s31_vit.png", "s33_ordering_problem.png",
        "s34_conditioned_synthesis.png", "s35_muse.png",
        "s36_markovgen.png", "s37_mrf_formulation.png",
        "s38_speedup.png"
    ]
    for s in slides:
        create_solid_image(slides_dir / s, (30, 40, 50), f"Slide Crop:\n{s}", (600, 400))
        
    # 2. External Images
    externals = {
        "dog_main.jpg": (130, 90, 40),       # brown/golden puppy
        "red_car_main.jpg": (180, 20, 20),   # red car
        "mona_lisa.jpg": (70, 75, 60),       # green/brown painting
        "bicycle.jpg": (50, 80, 110),        # blueish bike
        "violin.jpg": (120, 70, 30),         # wood/brown violin
        "city_building.jpg": (40, 70, 90),   # metallic/glass facade
        "sydney_opera_house.jpg": (210, 200, 180), # cream/white sails
    }
    for filename, color in externals.items():
        create_solid_image(external_dir / filename, color, f"External:\n{filename}", (800, 600))
        
    # 3. Patches
    patches = {
        "dog_eye_patch.png": (100, 70, 30),
        "dog_nose_patch.png": (40, 30, 20),
        "dog_ear_patch.png": (120, 80, 40),
        "car_wheel_patch.png": (30, 30, 30),
        "car_edge_patch.png": (160, 20, 20),
        "fur_texture_patch.png": (140, 100, 50),
        "road_texture_patch.png": (80, 80, 80),
    }
    for filename, color in patches.items():
        create_solid_image(patches_dir / filename, color, f"Patch:\n{filename}", (128, 128))
        
    # 4. Generated images
    create_gradient_grid(gen_dir / "dog_token_grid.png", (130, 90, 40), "dog_token_grid")
    create_solid_image(gen_dir / "dog_token_numbers.png", (20, 20, 20), "Grid:\n[12, 45, 96...]", (256, 256))
    create_gradient_grid(gen_dir / "sydney_imperfect_tokens.png", (210, 200, 180), "sydney_imperfect_tokens")
    create_gradient_grid(gen_dir / "sydney_fixed_tokens.png", (210, 200, 180), "sydney_fixed_tokens")
    
    # 5. Conditioned Maps
    create_solid_image(gen_dir / "edge_map_city.png", (10, 10, 10), "City Edges\n(Canny filter)", (256, 256))
    create_solid_image(gen_dir / "lowres_city.png", (40, 70, 90), "City Low-Res\n(64x64 pixelated)", (256, 256))
    create_solid_image(gen_dir / "highres_city.png", (40, 70, 90), "City High-Res", (256, 256))
    create_solid_image(gen_dir / "semantic_map_city.png", (0, 0, 255), "City Semantic Map\n(Blue=sky, Green=tree)", (256, 256))
    create_solid_image(gen_dir / "fake_depth_map_city.png", (128, 128, 128), "City Depth Map\n(Grayscale)", (256, 256))
    
    print("All mock assets successfully generated.")


if __name__ == "__main__":
    main()
