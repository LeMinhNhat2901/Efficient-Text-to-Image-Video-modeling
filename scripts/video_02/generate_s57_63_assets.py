from __future__ import annotations

from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "assets" / "external_57_63"
GENERATED = ROOT / "assets" / "generated_57_63"
ICONS = ROOT / "assets" / "icons"

for folder in (EXTERNAL, GENERATED, ICONS):
    folder.mkdir(parents=True, exist_ok=True)

W = H = 640


def save_if_missing(path: Path, image: Image.Image) -> None:
    if not path.exists():
        image.convert("RGB").save(path, quality=92)
        print(f"saved {path.relative_to(ROOT)}")


def radial_bg(c1: tuple[int, int, int], c2: tuple[int, int, int], seed: int = 0) -> Image.Image:
    rng = np.random.default_rng(seed)
    xs = np.linspace(-1, 1, W)
    ys = np.linspace(-1, 1, H)
    xv, yv = np.meshgrid(xs, ys)
    r = np.sqrt((xv * 0.9) ** 2 + (yv * 1.1) ** 2)
    t = np.clip(1 - r, 0, 1)[..., None]
    noise = rng.normal(0, 5, (H, W, 1))
    arr = np.array(c2) * (1 - t) + np.array(c1) * t + noise
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def make_high_res() -> Image.Image:
    img = radial_bg((40, 150, 190), (12, 16, 22), 10)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(22):
        x0 = int((i * 37) % W)
        y0 = int((i * 83) % H)
        d.rectangle([x0, y0, x0 + 170, y0 + 110], outline=(0, 229, 255, 52), width=2)
    for r in range(0, H, 24):
        d.line([(0, r), (W, r)], fill=(255, 255, 255, 14))
    for c in range(0, W, 24):
        d.line([(c, 0), (c, H)], fill=(255, 255, 255, 14))
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=130))


def make_peonies() -> Image.Image:
    img = radial_bg((50, 42, 70), (18, 17, 24), 11)
    d = ImageDraw.Draw(img, "RGBA")
    centers = [(205, 250), (350, 230), (295, 380), (455, 365)]
    for cx, cy in centers:
        for k in range(18):
            a = 2 * math.pi * k / 18
            px = cx + int(math.cos(a) * 45)
            py = cy + int(math.sin(a) * 34)
            d.ellipse([px - 42, py - 28, px + 42, py + 28], fill=(255, 118, 190, 92))
        d.ellipse([cx - 48, cy - 42, cx + 48, cy + 42], fill=(255, 195, 224, 165))
        d.ellipse([cx - 14, cy - 12, cx + 14, cy + 12], fill=(245, 210, 87, 210))
    return img.filter(ImageFilter.GaussianBlur(0.3))


def make_porsche() -> Image.Image:
    img = radial_bg((28, 96, 150), (10, 15, 24), 12)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 410, W, H], fill=(18, 20, 26, 210))
    d.rounded_rectangle([115, 310, 530, 410], radius=46, fill=(34, 125, 220, 230))
    d.polygon([(210, 310), (270, 240), (410, 240), (485, 310)], fill=(42, 145, 245, 210))
    d.polygon([(285, 255), (410, 255), (460, 305), (245, 305)], fill=(18, 24, 32, 190))
    for x in (210, 455):
        d.ellipse([x - 45, 376, x + 45, 466], fill=(8, 10, 14, 255))
        d.ellipse([x - 23, 398, x + 23, 444], fill=(160, 190, 210, 235))
    d.ellipse([505, 330, 540, 355], fill=(0, 229, 255, 180))
    return img


def make_raccoon() -> Image.Image:
    img = radial_bg((85, 84, 100), (14, 15, 20), 13)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([180, 150, 460, 450], fill=(135, 140, 145, 230))
    d.ellipse([185, 205, 455, 335], fill=(34, 36, 45, 185))
    d.polygon([(230, 155), (280, 75), (320, 180)], fill=(110, 112, 118, 230))
    d.polygon([(410, 155), (360, 75), (320, 180)], fill=(110, 112, 118, 230))
    for x in (265, 375):
        d.ellipse([x - 20, 245, x + 20, 285], fill=(236, 244, 250, 245))
        d.ellipse([x - 8, 255, x + 8, 273], fill=(16, 18, 22, 255))
    d.polygon([(320, 290), (300, 318), (340, 318)], fill=(18, 18, 22, 255))
    d.rectangle([250, 85, 390, 142], fill=(18, 18, 24, 230))
    d.rectangle([280, 25, 360, 95], fill=(18, 18, 24, 230))
    d.polygon([(320, 365), (285, 485), (355, 485)], fill=(167, 139, 250, 190))
    return img


def make_cat() -> Image.Image:
    img = radial_bg((90, 45, 130), (12, 15, 24), 14)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(215, 190), (250, 80), (320, 200)], fill=(115, 78, 150, 230))
    d.polygon([(425, 190), (390, 80), (320, 200)], fill=(115, 78, 150, 230))
    d.ellipse([190, 150, 450, 440], fill=(112, 78, 150, 230))
    d.ellipse([240, 245, 290, 295], fill=(0, 230, 200, 230))
    d.ellipse([350, 245, 400, 295], fill=(0, 230, 200, 230))
    d.line([(255, 323), (160, 300)], fill=(238, 238, 238, 160), width=3)
    d.line([(385, 323), (480, 300)], fill=(238, 238, 238, 160), width=3)
    d.polygon([(320, 300), (300, 330), (340, 330)], fill=(245, 185, 210, 240))
    return img


def make_cyber_cat() -> Image.Image:
    fallback = ROOT / "assets" / "external_40_56" / "cyberpunk_cat.jpg"
    if fallback.exists():
        return Image.open(fallback).convert("RGB").resize((W, H))
    img = make_cat()
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 32):
        d.line([(x, 0), (x - 200, H)], fill=(255, 64, 129, 35), width=3)
    d.rounded_rectangle([215, 260, 425, 304], radius=18, outline=(0, 229, 255, 230), width=8)
    return img


def make_datacenter() -> Image.Image:
    img = radial_bg((30, 64, 82), (10, 12, 18), 15)
    d = ImageDraw.Draw(img, "RGBA")
    for i, x in enumerate(range(70, 560, 82)):
        d.rounded_rectangle([x, 150, x + 52, 520], radius=6, fill=(24, 34, 44, 230), outline=(0, 229, 255, 65), width=2)
        for y in range(180, 500, 42):
            col = (39, 224, 138, 170) if (i + y) % 3 else (242, 201, 76, 170)
            d.rectangle([x + 13, y, x + 39, y + 8], fill=col)
    return img


def make_parrot() -> Image.Image:
    img = radial_bg((30, 110, 130), (10, 16, 20), 20)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([185, 145, 455, 485], fill=(31, 170, 95, 245))
    d.ellipse([240, 90, 430, 275], fill=(36, 205, 116, 245))
    d.polygon([(390, 170), (545, 215), (393, 245)], fill=(245, 196, 70, 245))
    d.polygon([(405, 215), (535, 230), (410, 240)], fill=(255, 120, 70, 235))
    d.ellipse([348, 148, 388, 188], fill=(240, 250, 250, 250))
    d.ellipse([360, 160, 377, 177], fill=(12, 15, 20, 255))
    d.polygon([(260, 245), (100, 405), (320, 410)], fill=(25, 120, 200, 215))
    d.polygon([(300, 400), (250, 610), (395, 440)], fill=(245, 66, 129, 190))
    return img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=140))


def make_latent_grid(path: Path, seed: int, noise: float) -> None:
    rng = np.random.default_rng(seed)
    size = 384
    cells = 16
    cell = size // cells
    img = Image.new("RGB", (size, size), (15, 18, 24))
    d = ImageDraw.Draw(img, "RGBA")
    for r in range(cells):
        for c in range(cells):
            base = np.array([35, 224, 138]) * (1 - noise) + rng.integers(70, 185, 3) * noise
            alpha = int(105 + 105 * rng.random())
            x0, y0 = c * cell + 2, r * cell + 2
            d.rounded_rectangle([x0, y0, x0 + cell - 5, y0 + cell - 5], radius=3, fill=tuple(base.astype(int)) + (alpha,))
    img.save(path)
    print(f"saved {path.relative_to(ROOT)}")


def make_pixel_grid() -> None:
    img = make_high_res().resize((512, 512)).filter(ImageFilter.UnsharpMask(radius=2, percent=120))
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(0, 512, 16):
        d.line([(i, 0), (i, 512)], fill=(255, 255, 255, 30))
        d.line([(0, i), (512, i)], fill=(255, 255, 255, 30))
    img.save(GENERATED / "pixel_grid_large.png")
    print("saved assets/video_02/generated/57_63/pixel_grid_large.png")


def write_svg(path: Path, body: str) -> None:
    if path.exists():
        return
    path.write_text(body, encoding="utf-8")
    print(f"saved {path.relative_to(ROOT)}")


def generate_icons() -> None:
    write_svg(ICONS / "gpu_chip.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect x="54" y="54" width="148" height="148" rx="18" fill="#171b22" stroke="#00e5ff" stroke-width="10"/><rect x="92" y="92" width="72" height="72" rx="10" fill="#ff4081" opacity=".45"/><g stroke="#f2c94c" stroke-width="8">""" + "".join([f'<line x1="{x}" y1="28" x2="{x}" y2="54"/><line x1="{x}" y1="202" x2="{x}" y2="228"/>' for x in range(76, 181, 26)]) + "".join([f'<line y1="{y}" x1="28" y2="{y}" x2="54"/><line y1="{y}" x1="202" y2="{y}" x2="228"/>' for y in range(76, 181, 26)]) + """</g></svg>""")
    write_svg(ICONS / "funnel.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M32 48h192l-74 86v62l-44 24v-86z" fill="#10151c" stroke="#27e08a" stroke-width="12" stroke-linejoin="round"/><path d="M60 72h136" stroke="#00e5ff" stroke-width="8" opacity=".55"/></svg>""")
    write_svg(ICONS / "graph_network.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><g stroke="#a78bfa" stroke-width="7" opacity=".75"><line x1="70" y1="70" x2="150" y2="55"/><line x1="70" y1="70" x2="95" y2="168"/><line x1="150" y1="55" x2="190" y2="142"/><line x1="95" y1="168" x2="190" y2="142"/><line x1="150" y1="55" x2="95" y2="168"/></g><g fill="#111111" stroke="#27e08a" stroke-width="8"><circle cx="70" cy="70" r="22"/><circle cx="150" cy="55" r="22"/><circle cx="95" cy="168" r="22"/><circle cx="190" cy="142" r="22"/></g></svg>""")
    write_svg(ICONS / "shortcut_arrow.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M38 170C72 74 166 69 205 107" fill="none" stroke="#27e08a" stroke-width="16" stroke-linecap="round"/><path d="M190 68l32 54-62-6" fill="#27e08a"/></svg>""")
    write_svg(ICONS / "speedometer.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M44 170a84 84 0 0 1 168 0" fill="none" stroke="#00e5ff" stroke-width="14" stroke-linecap="round"/><path d="M128 170l58-58" stroke="#f2c94c" stroke-width="12" stroke-linecap="round"/><circle cx="128" cy="170" r="12" fill="#f2c94c"/></svg>""")
    write_svg(ICONS / "rocket_icon.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M88 162c-10-48 18-102 84-126 15 66-9 112-56 132z" fill="#111111" stroke="#27e08a" stroke-width="10"/><circle cx="151" cy="78" r="17" fill="#00e5ff"/><path d="M86 168l-28 30 36-10M113 190l-20 39 35-28" fill="#ff4081"/></svg>""")
    write_svg(ICONS / "fire_icon.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M130 224c58-24 64-86 34-122-5 25-21 39-38 48 14-48-3-83-35-118 3 45-40 73-40 122 0 43 35 70 79 70z" fill="#ff8a3d"/><path d="M128 220c26-17 31-47 14-70-6 18-22 25-37 34 0 21 9 31 23 36z" fill="#f2c94c"/></svg>""")
    write_svg(ICONS / "electric_meter.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect x="54" y="36" width="148" height="184" rx="18" fill="#111111" stroke="#9aa3aa" stroke-width="10"/><path d="M82 130a46 46 0 0 1 92 0" fill="none" stroke="#00e5ff" stroke-width="9"/><path d="M128 130l38-38" stroke="#ff4081" stroke-width="9" stroke-linecap="round"/><text x="128" y="184" font-size="28" fill="#f2c94c" text-anchor="middle" font-family="Arial">GPU</text></svg>""")
    write_svg(ICONS / "video_icon.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect x="42" y="70" width="128" height="102" rx="14" fill="#111111" stroke="#00e5ff" stroke-width="10"/><path d="M170 104l46-28v90l-46-28z" fill="#a78bfa"/></svg>""")
    write_svg(ICONS / "cube_3d.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path d="M128 28l82 46v104l-82 50-82-50V74z" fill="#111111" stroke="#27e08a" stroke-width="9"/><path d="M46 74l82 48 82-48M128 122v106" fill="none" stroke="#00e5ff" stroke-width="8"/></svg>""")


def main() -> None:
    save_if_missing(EXTERNAL / "high_res_image.jpg", make_high_res())
    save_if_missing(EXTERNAL / "flower_peonies.jpg", make_peonies())
    save_if_missing(EXTERNAL / "blue_porsche.jpg", make_porsche())
    save_if_missing(EXTERNAL / "raccoon_formal.jpg", make_raccoon())
    save_if_missing(EXTERNAL / "cat_portrait.jpg", make_cat())
    save_if_missing(EXTERNAL / "cyberpunk_cat.jpg", make_cyber_cat())
    save_if_missing(EXTERNAL / "parrot_full.jpg", make_parrot())
    save_if_missing(EXTERNAL / "data_center.jpg", make_datacenter())

    make_pixel_grid()
    for name, seed, noise in [
        ("latent_noise_00.png", 100, 1.0),
        ("latent_noise_25.png", 101, 0.72),
        ("latent_noise_50.png", 102, 0.45),
        ("latent_noise_75.png", 103, 0.18),
        ("latent_clean.png", 104, 0.03),
        ("latent_grid_small.png", 105, 0.12),
        ("latentcrf_before.png", 106, 0.55),
        ("latentcrf_after.png", 107, 0.12),
    ]:
        make_latent_grid(GENERATED / name, seed, noise)

    parrot = Image.open(EXTERNAL / "parrot_full.jpg").convert("RGB").resize((512, 512))
    for size in [16, 32, 64, 128, 256, 512]:
        low = parrot.resize((size, size), Image.Resampling.BILINEAR)
        up = low.resize((512, 512), Image.Resampling.NEAREST)
        up.save(GENERATED / f"parrot_{size}.png")
        print(f"saved assets/video_02/generated/57_63/parrot_{size}.png")

    generate_icons()


if __name__ == "__main__":
    main()
