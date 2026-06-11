from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_NAMES = ("puppy.jpg", "puppy.png", "puppy.jpeg")
OUT_DIR = ROOT / "assets" / "generated" / "noise_frames"
FRAME_PREFIX = "puppy_noise"
NOISE_LEVELS = tuple(np.linspace(0.0, 1.0, 13))
FRAME_SIZE = (720, 508)


def find_source_image() -> Path:
    assets_dir = ROOT / "assets"
    for name in ASSET_NAMES:
        candidate = assets_dir / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "No puppy source image found. Put puppy.jpg, puppy.png, or puppy.jpeg in assets/."
    )


def fit_source(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageOps.fit(image, FRAME_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def make_noise_frame(base: Image.Image, level: float, seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    clean = np.asarray(base).astype(np.float32)
    gaussian = rng.normal(loc=128.0, scale=74.0, size=clean.shape)
    gaussian = np.clip(gaussian, 0, 255)

    mixed = (1.0 - level) * clean + level * gaussian
    contrast_loss = 1.0 - 0.22 * level
    mixed = 128.0 + (mixed - 128.0) * contrast_loss
    return Image.fromarray(np.clip(mixed, 0, 255).astype(np.uint8))


def main() -> None:
    source = find_source_image()
    base = fit_source(source)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for index, level in enumerate(NOISE_LEVELS):
        frame = make_noise_frame(base, level, seed=2026 + index)
        frame.save(OUT_DIR / f"{FRAME_PREFIX}_{index:02d}.png", optimize=True)

    print(f"source: {source}")
    print(f"frames: {OUT_DIR}")
    print(f"count: {len(NOISE_LEVELS)}")


if __name__ == "__main__":
    main()
