"""generate_v02_s40_56_assets.py

Generate programmatic assets for Video 2 Slides 40–56 (Diffusion Models & Guidance).

Creates:
  assets/video_02/generated/40_56/
    cat_noise_00.png   — clean placeholder (128×128 cyan gradient)
    cat_noise_10.png   — 10% noised
    cat_noise_25.png   — 25% noised
    cat_noise_50.png   — 50% noised
    cat_noise_75.png   — 75% noised
    cat_noise_100.png  — 100% noised (pure Gaussian noise)
    pure_noise.png     — pure Gaussian noise (white noise texture)
    reverse_00_noise.png   — pure noise (start of reverse)
    reverse_01_less_noise.png
    reverse_02_shape.png
    reverse_03_clearer.png
    reverse_04_final.png   — cleanest (same as cat_noise_00)
    true_noise.png         — fixed noise pattern (ground truth ε)
    predicted_noise_bad.png — initially wrong predicted noise
    predicted_noise_good.png — after training, close to true noise
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "generated_40_56"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 256, 256          # output resolution
rng = np.random.default_rng(42)


# ──────────────────────────────────────────────────────────────────────────────
# Base "clean" image — a soft cyan/blue gradient (mimics a clean cat silhouette)
# ──────────────────────────────────────────────────────────────────────────────

def make_clean_image() -> np.ndarray:
    """Generate a synthetic 'clean cat' — a smooth radial gradient."""
    cx, cy = W // 2, H // 2
    xs = np.linspace(-1, 1, W)
    ys = np.linspace(-1, 1, H)
    xv, yv = np.meshgrid(xs, ys)
    r = np.sqrt(xv**2 + yv**2)
    # Main body: blue-cyan radial gradient
    body = np.clip(1 - r * 1.2, 0, 1)
    # Ears: two smaller circles
    ear_l = np.clip(1 - np.sqrt((xv + 0.42)**2 + (yv + 0.55)**2) * 5.5, 0, 1)
    ear_r = np.clip(1 - np.sqrt((xv - 0.42)**2 + (yv + 0.55)**2) * 5.5, 0, 1)
    mask = np.clip(body + ear_l * 0.7 + ear_r * 0.7, 0, 1)

    r_ch = (0.12 + 0.28 * mask) * 255
    g_ch = (0.28 + 0.42 * mask) * 255
    b_ch = (0.55 + 0.42 * mask) * 255
    img = np.stack([r_ch, g_ch, b_ch], axis=-1).astype(np.uint8)
    return img


def add_noise(base: np.ndarray, alpha: float) -> np.ndarray:
    """Blend base image with Gaussian noise at level alpha (0=clean, 1=pure noise)."""
    noise = rng.normal(128, 55, base.shape)
    blended = (1 - alpha) * base.astype(float) + alpha * noise
    return np.clip(blended, 0, 255).astype(np.uint8)


# ──────────────────────────────────────────────────────────────────────────────
# Forward diffusion sequence
# ──────────────────────────────────────────────────────────────────────────────

def generate_noise_sequence() -> None:
    clean = make_clean_image()
    levels = {
        "cat_noise_00.png": 0.00,
        "cat_noise_10.png": 0.10,
        "cat_noise_25.png": 0.25,
        "cat_noise_50.png": 0.50,
        "cat_noise_75.png": 0.75,
        "cat_noise_100.png": 1.00,
    }
    for fname, alpha in levels.items():
        img = add_noise(clean, alpha)
        Image.fromarray(img).save(OUT_DIR / fname)
        print(f"  saved {fname}")

    # Pure noise (uniform)
    pure = rng.integers(0, 255, (H, W, 3), dtype=np.uint8)
    Image.fromarray(pure).save(OUT_DIR / "pure_noise.png")
    print("  saved pure_noise.png")


# ──────────────────────────────────────────────────────────────────────────────
# Reverse denoising sequence
# ──────────────────────────────────────────────────────────────────────────────

def generate_reverse_sequence() -> None:
    clean = make_clean_image()
    alphas = [1.0, 0.75, 0.45, 0.18, 0.04]
    names = [
        "reverse_00_noise.png",
        "reverse_01_less_noise.png",
        "reverse_02_shape.png",
        "reverse_03_clearer.png",
        "reverse_04_final.png",
    ]
    for fname, alpha in zip(names, alphas):
        img = add_noise(clean, alpha)
        Image.fromarray(img).save(OUT_DIR / fname)
        print(f"  saved {fname}")


# ──────────────────────────────────────────────────────────────────────────────
# True noise / predicted noise maps (for MSE loss animation)
# ──────────────────────────────────────────────────────────────────────────────

def make_noise_pattern(seed: int, sharpness: float = 1.0) -> np.ndarray:
    """Generate a colored noise pattern in orange/purple to distinguish from cat."""
    rng2 = np.random.default_rng(seed)
    base = rng2.normal(128, 40 * sharpness, (H, W, 3))
    # Tint: true noise → orange, predicted → purple
    return np.clip(base, 0, 255).astype(np.uint8)


def generate_noise_maps() -> None:
    # True noise: orange tint
    true_n = make_noise_pattern(10, 1.0)
    true_n[:, :, 0] = np.clip(true_n[:, :, 0] + 60, 0, 255)   # more red
    true_n[:, :, 2] = np.clip(true_n[:, :, 2] - 40, 0, 255)   # less blue
    Image.fromarray(true_n).save(OUT_DIR / "true_noise.png")
    print("  saved true_noise.png")

    # Predicted noise bad (very different from true)
    pred_bad = make_noise_pattern(99, 1.2)
    pred_bad[:, :, 2] = np.clip(pred_bad[:, :, 2] + 60, 0, 255)  # purple tint
    Image.fromarray(pred_bad).save(OUT_DIR / "predicted_noise_bad.png")
    print("  saved predicted_noise_bad.png")

    # Predicted noise good (close to true noise but slightly different)
    pred_good = (0.82 * true_n.astype(float) + 0.18 * make_noise_pattern(7, 0.5).astype(float))
    Image.fromarray(np.clip(pred_good, 0, 255).astype(np.uint8)).save(OUT_DIR / "predicted_noise_good.png")
    print("  saved predicted_noise_good.png")


# ──────────────────────────────────────────────────────────────────────────────
# Guidance output placeholders (tabby, lion, leopard)
# ──────────────────────────────────────────────────────────────────────────────

def make_feline_portrait(seed: int, primary: tuple, secondary: tuple) -> np.ndarray:
    """Generate a simple feline portrait placeholder with given color palette."""
    rng3 = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), dtype=np.uint8)
    # Dark background
    img[:] = [18, 18, 24]
    # Body ellipse
    cx, cy = W // 2, int(H * 0.55)
    for y in range(H):
        for x in range(W):
            dx = (x - cx) / (W * 0.32)
            dy = (y - cy) / (H * 0.38)
            if dx**2 + dy**2 < 1:
                t = 1 - (dx**2 + dy**2)
                img[y, x] = [
                    int(primary[0] * t + 18 * (1 - t)),
                    int(primary[1] * t + 18 * (1 - t)),
                    int(primary[2] * t + 24 * (1 - t)),
                ]
    # Head
    hy = int(H * 0.3)
    for y in range(H):
        for x in range(W):
            dx = (x - cx) / (W * 0.22)
            dy = (y - hy) / (H * 0.2)
            if dx**2 + dy**2 < 1:
                t = 1 - (dx**2 + dy**2)
                img[y, x] = [
                    int(primary[0] * t * 1.1 + img[y, x, 0] * (1 - t)),
                    int(primary[1] * t * 1.1 + img[y, x, 1] * (1 - t)),
                    int(primary[2] * t * 1.1 + img[y, x, 2] * (1 - t)),
                ]
    # Stripe texture
    stripe_noise = rng3.normal(0, 12, (H, W))
    for c in range(3):
        img[:, :, c] = np.clip(img[:, :, c].astype(float) + stripe_noise * 0.4, 0, 255).astype(np.uint8)
    # Eyes
    for ex in [int(cx - 28), int(cx + 28)]:
        ey = int(H * 0.27)
        for y in range(H):
            for x in range(W):
                if (x - ex)**2 + (y - ey)**2 < 64:
                    img[y, x] = [int(secondary[0]), int(secondary[1]), int(secondary[2])]
    return img


def generate_guidance_outputs() -> None:
    out_ext = ROOT / "assets" / "external_40_56"
    out_ext.mkdir(parents=True, exist_ok=True)

    felines = [
        ("output_tabby_cat.jpg", 11, (180, 130, 60), (220, 180, 20)),    # orange tabby
        ("output_lion.jpg",      22, (200, 155, 70), (255, 180, 50)),     # golden lion
        ("output_leopard.jpg",   33, (160, 130, 70), (40, 200, 200)),     # leopard
    ]
    for fname, seed, primary, secondary in felines:
        img = make_feline_portrait(seed, primary, secondary)
        Image.fromarray(img).save(out_ext / fname)
        print(f"  saved external_40_56/{fname}")

    # Cyberpunk cat
    cyber = make_feline_portrait(77, (60, 40, 120), (0, 230, 200))
    # Add neon green overlay (glasses)
    for y in range(int(H * 0.22), int(H * 0.32)):
        for x in range(int(W * 0.28), int(W * 0.72)):
            if abs(y - int(H * 0.27)) < 10:
                cyber[y, x] = np.clip(
                    cyber[y, x].astype(int) + np.array([0, 60, 80]), 0, 255
                ).astype(np.uint8)
    Image.fromarray(cyber).save(out_ext / "cyberpunk_cat.jpg")
    print("  saved external_40_56/cyberpunk_cat.jpg")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    try:
        from PIL import Image as _PIL_check
    except ImportError:
        raise SystemExit("Pillow not found. Install with: pip install Pillow")

    print("Generating assets for Video 2 Slides 40–56 …")
    print("\n[1] Forward noise sequence:")
    generate_noise_sequence()
    print("\n[2] Reverse denoising sequence:")
    generate_reverse_sequence()
    print("\n[3] Noise maps (true / predicted):")
    generate_noise_maps()
    print("\n[4] Guidance output portraits (tabby / lion / leopard / cyberpunk):")
    generate_guidance_outputs()

    print(f"\nAll assets written to:\n  {OUT_DIR}\n  {ROOT / 'assets' / 'external_40_56'}")
    print("\nDone!")


if __name__ == "__main__":
    main()
