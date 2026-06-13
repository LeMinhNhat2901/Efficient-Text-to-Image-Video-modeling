from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "generated" / "ou_paths"
OUT_PATH = OUT_DIR / "ou_paths.npz"

PATH_COUNT = 5
STEP_COUNT = 90
T_MAX = 10.0


def main() -> None:
    rng = np.random.default_rng(31415)
    xs = np.linspace(0.0, T_MAX, STEP_COUNT, dtype=np.float32)
    dt = T_MAX / (STEP_COUNT - 1)
    theta = 0.85
    sigma = 0.62

    paths = np.zeros((PATH_COUNT, STEP_COUNT), dtype=np.float32)
    paths[:, 0] = rng.normal(0.0, 0.42, size=PATH_COUNT)

    for i in range(1, STEP_COUNT):
        noise = rng.normal(0.0, np.sqrt(dt), size=PATH_COUNT)
        paths[:, i] = paths[:, i - 1] + (-theta * paths[:, i - 1]) * dt + sigma * noise

    envelope = (sigma / np.sqrt(2.0 * theta)) * np.sqrt(1.0 - np.exp(-2.0 * theta * xs))
    particle = paths[0].copy()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.savez(
        OUT_PATH,
        xs=xs,
        paths=paths,
        envelope=envelope.astype(np.float32),
        particle=particle.astype(np.float32),
    )
    print(f"data: {OUT_PATH}")
    print(f"paths: {paths.shape}")


if __name__ == "__main__":
    main()
