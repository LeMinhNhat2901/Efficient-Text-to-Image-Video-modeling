from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "generated" / "spiral_frames"
OUT_PATH = OUT_DIR / "spiral_diffusion.npy"

FRAME_COUNT = 16
POINT_COUNT = 130


def make_spiral(seed: int = 8) -> np.ndarray:
    rng = np.random.default_rng(seed)
    points = []
    for i in range(POINT_COUNT):
        t = 0.25 + 3.9 * i / POINT_COUNT
        r = 0.18 + 0.22 * t
        x = r * np.cos(2.25 * t) + rng.normal(0, 0.035)
        y = r * np.sin(2.25 * t) + rng.normal(0, 0.035)
        points.append((x, y))
    return np.array(points, dtype=np.float32)


def main() -> None:
    rng = np.random.default_rng(2027)
    start = make_spiral()
    gaussian = rng.normal(0.0, 0.82, size=start.shape).astype(np.float32)
    frames = []

    for i in range(FRAME_COUNT):
        u = i / (FRAME_COUNT - 1)
        eased = u * u * (3.0 - 2.0 * u)
        jitter = rng.normal(0.0, 0.18 * u, size=start.shape).astype(np.float32)
        spread = (1.0 - eased) * start + eased * gaussian + jitter
        frames.append(spread.astype(np.float32))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(OUT_PATH, np.stack(frames, axis=0))
    print(f"frames: {OUT_PATH}")
    print(f"shape: {np.load(OUT_PATH).shape}")


if __name__ == "__main__":
    main()
