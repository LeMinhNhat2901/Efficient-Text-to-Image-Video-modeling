# Keep / Download Assets For Video 2 Slides 57-63

Use this list instead of downloading everything from the optional slide-crop section.
The Manim scenes rebuild most diagrams directly, so real image assets are only needed where a visual example makes the scene feel richer.

## Keep And Improve These Files

Put these in `assets/external_57_63/` with the exact filenames below.

| Filename | Priority | Why keep it | Suggested image style |
|---|---:|---|---|
| `high_res_image.jpg` | Must keep | Used in the pixel-space / latent-compression hook and reused in SANA compression. | Sharp 1024x1024+ image with visible detail; avoid abstract placeholder graphics. |
| `flower_peonies.jpg` | Must keep | Used in the LatentCRF vs Full LDM results grid. | Clean peonies/flower image, square or near-square crop. |
| `blue_porsche.jpg` | Must keep | Used in the decoder pipeline and the LatentCRF results grid. | Blue Porsche or blue sports car, clear side/front view, not too dark. |
| `raccoon_formal.jpg` | Must keep | Used in the LatentCRF results grid to make examples varied. | Formal portrait style, centered subject, clean background. |
| `cat_portrait.jpg` | Must keep | Used in the LatentCRF results grid. | Cat portrait, centered, good contrast. |
| `cyberpunk_cat.jpg` | Must keep | Used as the SANA illustrative output. | Cyberpunk cat with neon glasses; high contrast, readable at small size. |
| `parrot_full.jpg` | Must keep | Source image for VAR next-scale sequence. | Clean parrot image, square crop preferred, colorful and recognizable at low resolution. |
| `data_center.jpg` | Must keep | Used in the cost/discussion scene. | Data center / GPU server racks, clear perspective, not overly dark. |

## Do Not Need To Download

These slide screenshots/crops are optional and currently not necessary:

- `assets/slides_57_63/s57_ldm_timeline.png`
- `assets/slides_57_63/s58_latent_diffusion_models.png`
- `assets/slides_57_63/s59_latentcrf_efficient_inference.png`
- `assets/slides_57_63/s60_latentcrf_results.png`
- `assets/slides_57_63/s61_sana_architecture.png`
- `assets/slides_57_63/s62_var_next_scale.png`
- `assets/slides_57_63/s63_discussion.png`

Reason: the important timelines, pipelines, graphs, and comparisons are rebuilt as Manim-native diagrams for clearer animation and better timing.

## After Replacing `parrot_full.jpg`

Run this so the VAR sequence updates from the new parrot image:

```powershell
E:\miniconda\envs\min_ds-env\python.exe scripts\generate_v02_s57_63_assets.py
```

This regenerates:

- `assets/generated_57_63/parrot_16.png`
- `assets/generated_57_63/parrot_32.png`
- `assets/generated_57_63/parrot_64.png`
- `assets/generated_57_63/parrot_128.png`
- `assets/generated_57_63/parrot_256.png`
- `assets/generated_57_63/parrot_512.png`

