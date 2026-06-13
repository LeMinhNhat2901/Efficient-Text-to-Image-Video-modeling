"""
generate_v02_noise_frames.py
============================
Generates a set of denoising-level PNG frames used by the diffusion
side of the two-backbone comparison (v02_s01_generative_backbones.py).

Each frame is a small square filled with Gaussian noise blended with
a clean coloured target at different signal-to-noise ratios.

Output: assets/generated/diffusion_frames/
  diffuse_00.png  (pure noise)
  diffuse_25.png  (heavy noise)
  diffuse_50.png  (medium noise)
  diffuse_75.png  (light noise)
  diffuse_100.png (clean, target colour)

Run:   python scripts/generate_v02_noise_frames.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "generated" / "diffusion_frames"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIZE = 256            # pixels per side
RNG  = np.random.default_rng(42)

# Target clean "image" — a soft gradient in the accent blue/purple palette.
def clean_target() -> np.ndarray:
    xs = np.linspace(0, 1, SIZE)
    ys = np.linspace(0, 1, SIZE)
    xv, yv = np.meshgrid(xs, ys)
    # Cyan (0, 229, 255) blending to violet (167, 139, 250)
    r = (yv * 167).astype(np.uint8)
    g = ((1 - xv) * 229 * 0.55).astype(np.uint8)
    b = (xv * 250 * 0.5 + yv * 255 * 0.5).astype(np.uint8)
    return np.stack([r, g, b], axis=-1)


def noise_frame(noise_frac: float, target: np.ndarray) -> np.ndarray:
    """Blend Gaussian noise with the target.  noise_frac=1.0 → pure noise."""
    noise = RNG.integers(0, 256, (SIZE, SIZE, 3), dtype=np.uint8)
    blended = (noise_frac * noise.astype(float) + (1.0 - noise_frac) * target.astype(float))
    return np.clip(blended, 0, 255).astype(np.uint8)


LEVELS = [
    ("diffuse_00.png",  1.00),   # pure noise
    ("diffuse_25.png",  0.75),   # heavy noise
    ("diffuse_50.png",  0.50),   # medium noise
    ("diffuse_75.png",  0.25),   # light noise
    ("diffuse_100.png", 0.00),   # clean
]


def main() -> None:
    target = clean_target()
    for filename, noise_frac in LEVELS:
        frame = noise_frame(noise_frac, target)
        path  = OUTPUT_DIR / filename
        Image.fromarray(frame, "RGB").save(path)
        print(f"  saved  {path.relative_to(Path.cwd()) if Path.cwd() in path.parents else path}")
    print(f"\nAll {len(LEVELS)} frames written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
