# Video 2 — Asset Needs
## Cornerstones of the Text-to-Pixels Journey

Download / crop / generate these assets before rendering Video 2.
Once downloaded, place each file at the path shown under "Save to".
The Manim scenes fall back gracefully to built-in placeholder icons
when the file is absent, so missing assets won't break the render.

---

## A. Slide crops (HIGH PRIORITY)

Crop these directly from the lecture PDF at high resolution (≥ 1920 px wide).
Export as PNG with a **white or transparent** background, then the scene
wraps each in a dark rounded card automatically.

| Save to | Slide | What to crop |
|---|---|---|
| `assets/slides/s04_robot_cooking.png` | Slide 4 | Robot cooking in kitchen image |
| `assets/slides/s04_robot_graffiti.png` | Slide 4 | Robot graffiti on brick wall image |
| `assets/slides/s04_raccoon.png` | Slide 4 | Raccoon in formal clothes + tophat image |
| `assets/slides/s04_alien_pyramid.png` | Slide 4 | Alien pyramid landscape image |
| `assets/slides/s05_text_to_video_grid.png` | Slide 5 | Lumiere video grid (all frames) |
| `assets/slides/s06_text_to_3d.png` | Slide 6 | DreamFusion / text-to-3D diagram |
| `assets/slides/s07_backbone.png` | Slide 7 | Autoregressive + diffusion backbone diagram |
| `assets/slides/s08_centerpiece.png` | Slide 8 | Text-to-image centerpiece spider diagram |
| `assets/slides/s09_puzzle.png` | Slides 9-10 | Timeline/puzzle pieces (full view) |
| `assets/slides/s11_feature_clusters.png` | Slide 11 | Image feature cluster scatter plot |
| `assets/slides/s12_co_embedding.png` | Slide 12 | Image-text co-embedding diagram |
| `assets/slides/s13_two_tower.png` | Slide 13 | Single-tower vs two-tower diagram |
| `assets/slides/s14_clip_align.png` | Slide 14 | CLIP/ALIGN similarity matrix + InfoNCE formula |

**Crop tip**: open the PDF at 300 dpi in Adobe Acrobat / Preview,
use the Crop/Selection tool to export just the figure, not the full slide.

---

## B. AI-generated images (use your preferred image AI)

These are the "raccoon" and other hook images that are cleaner than
stock photography. Use the exact prompt from the slide.

| Save to | Prompt to use |
|---|---|
| `assets/generated/raccoon_prompt_image.png` | `A raccoon wearing formal clothes, wearing a tophat, cinematic portrait, dark background, fur detail, photorealistic` |
| `assets/generated/robot_cooking.png` | `A friendly robot cooking in a modern kitchen, cinematic lighting, photorealistic` |
| `assets/generated/robot_graffiti.png` | `A robot painted as colorful graffiti mural on a brick wall, street art style` |
| `assets/generated/alien_pyramid.png` | `Hyper-realistic alien pyramid landscape, dramatic sky, science fiction, cinematic` |

**Size**: export at 1024×1024 or 1024×768. The scene auto-crops to card size.

---

## C. Stock media (Pexels / Pixabay / Unsplash — free license)

Download at highest available resolution, rename to the paths below.

### C1. Particle / background video loop
| Save to | Search keywords | Source |
|---|---|---|
| `assets/external/particles_bg.mp4` | `blue technology particles background dark loop` | Pexels / Pixabay |

Usage: **very faint background** in opening scene (opacity ≈ 10–15%).
Not required — the Manim dot-burst animation is used instead if absent.

### C2. Text-to-video examples (for 2×3 Lumiere-style grid)
Pick 4–6 short clips (2–4 s each) from the same category if possible.

| Save to | Search keywords |
|---|---|
| `assets/external/vid_dog_run.mp4` | `dog running slow motion grass` |
| `assets/external/vid_astronaut.mp4` | `astronaut walking desert cinematic` |
| `assets/external/vid_northern_lights.mp4` | `northern lights timelapse` |
| `assets/external/vid_puppy.mp4` | `puppy playing grass` |

Source priority: **Pexels** (free for commercial use, no attribution required
on the video itself; add to credits slide). Pixabay also acceptable.

### C3. Feature-clustering representative images
Small thumbnails (200–400 px wide) placed inside the feature-space dots.

| Save to | Subject | Search keywords |
|---|---|---|
| `assets/slides/img_dog.jpg` | Dog (spaniel) | `dog portrait natural light` |
| `assets/slides/img_wolf.jpg` | Wolf | `gray wolf portrait` |
| `assets/slides/img_sunglasses.jpg` | Sunglasses | `sunglasses product photo white background` |
| `assets/slides/img_car.jpg` | Self-driving car | `autonomous car road photo` |

Source: **Unsplash** (free, attribution appreciated but not mandatory for
educational/non-commercial use; add to credits slide).

### C4. Co-embedding graph node images
| Save to | Subject | Notes |
|---|---|---|
| `assets/slides/img_autonomous_car.jpg` | Self-driving car | Can reuse `img_car.jpg` above |
| `assets/slides/img_brain.png` | Brain / AI concept | PNG with transparent or dark bg preferred |
| `assets/slides/img_code.png` | Code / software screenshot | Dark-theme code editor screenshot |

---

## D. SVG icons (SVG Repo / Tabler Icons — free)

Download SVG, save to `assets/icons/`. The scenes use these as node
decorations; they are optional (built-in Manim shapes are used if absent).

| Save to | Icon name | Tabler / SVG Repo search |
|---|---|---|
| `assets/icons/text_icon.svg` | Text / document | `file-text` |
| `assets/icons/image_icon.svg` | Image / picture | `photo` |
| `assets/icons/video_icon.svg` | Video / film | `video` |
| `assets/icons/cube_3d.svg` | 3D cube | `box` or `cube` |
| `assets/icons/encoder.svg` | Neural network block | `cpu` or `brain` |
| `assets/icons/neural_net.svg` | Neural network | `network` |

Tabler Icons: https://tabler.io/icons  (MIT license, free)
SVG Repo:     https://www.svgrepo.com/ (check individual file license)

---

## E. Noise frames (auto-generated, no download needed)

Run the helper script once to create diffusion-level frames:

```powershell
python scripts/generate_v02_noise_frames.py
```

Output: `assets/generated/diffusion_frames/diffuse_00.png` … `diffuse_100.png`

---

## F. Folder structure summary

After downloading everything the tree should look like:

```
assets/
  slides/
    s04_robot_cooking.png
    s04_robot_graffiti.png
    s04_raccoon.png
    s04_alien_pyramid.png
    s05_text_to_video_grid.png
    s06_text_to_3d.png
    s07_backbone.png
    s08_centerpiece.png
    s09_puzzle.png
    s11_feature_clusters.png
    s12_co_embedding.png
    s13_two_tower.png
    s14_clip_align.png
    img_dog.jpg
    img_wolf.jpg
    img_sunglasses.jpg
    img_car.jpg
    img_autonomous_car.jpg
    img_brain.png
    img_code.png

  generated/
    raccoon_prompt_image.png
    robot_cooking.png
    robot_graffiti.png
    alien_pyramid.png
    diffusion_frames/
      diffuse_00.png
      diffuse_25.png
      diffuse_50.png
      diffuse_75.png
      diffuse_100.png

  external/
    particles_bg.mp4
    vid_dog_run.mp4
    vid_astronaut.mp4
    vid_northern_lights.mp4
    vid_puppy.mp4

  icons/
    text_icon.svg
    image_icon.svg
    video_icon.svg
    cube_3d.svg
    encoder.svg
    neural_net.svg
    Warning.svg          ← already present
    neural_network.png   ← already present
```

---

## G. Attribution / license tracking

Add every downloaded asset to `assets/attribution.md` with columns:

```
filename | source_url | author | license | usage | date
```

### Quick license reference

| Source | License | Commercial? | Attribution needed? |
|---|---|---|---|
| Pexels | Pexels License | ✅ Yes | Optional (nice to have) |
| Pixabay | Pixabay Content License | ✅ Yes | Not required |
| Unsplash | Unsplash License | ✅ Yes | Not required (appreciated) |
| Tabler Icons | MIT | ✅ Yes | Not required in video |
| SVG Repo | Per-file (check!) | Varies | Check each file |

> **Important**: if the video will be monetised or distributed commercially,
> double-check each asset license before publishing.

---

## H. Priority order

1. **Must-have for any scene to look good**: slide crops (Section A).
2. **Nice visual upgrade**: AI-generated images (Section B).
3. **Cinematic extras**: stock clips for text-to-video grid (Section C2).
4. **Feature cluster detail**: small representative photos (Section C3).
5. **Low priority**: SVG icons (the scenes use built-in Manim shapes instead).
