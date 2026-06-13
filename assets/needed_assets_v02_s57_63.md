# Optional External Assets For Video 2 Slides 57-63

The final scenes can render with generated placeholder assets. Replace the files below with higher quality images when available; keep the same filenames so the Manim scenes pick them up automatically.

## Put These In `assets/external_57_63/`

- `high_res_image.jpg` - a sharp 1024x1024 or larger image for the "Pixel Space is expensive" hook.
- `flower_peonies.jpg` - peonies/flowers example for LatentCRF vs Full LDM.
- `blue_porsche.jpg` - blue Porsche or blue sports car example.
- `raccoon_formal.jpg` - formal/portrait raccoon example.
- `cat_portrait.jpg` - cat portrait example.
- `cyberpunk_cat.jpg` - cyberpunk cat with neon glasses for SANA.
- `parrot_full.jpg` - clean parrot photo, square crop preferred, for VAR next-scale prediction.
- `data_center.jpg` - data center or GPU server racks for discussion/cost.

## Optional Slide Crops

Put cropped reference images in `assets/slides_57_63/`:

- `s57_ldm_timeline.png`
- `s58_latent_diffusion_models.png`
- `s59_latentcrf_efficient_inference.png`
- `s60_latentcrf_results.png`
- `s61_sana_architecture.png`
- `s62_var_next_scale.png`
- `s63_discussion.png`

These are not shown for long in the animation. The main pipelines and graphs are rebuilt in Manim for clarity.

## Regenerate Derived Assets

After replacing `parrot_full.jpg`, run:

```powershell
E:\miniconda\envs\min_ds-env\python.exe scripts\generate_v02_s57_63_assets.py
```

This recreates:

- `assets/generated_57_63/parrot_16.png`
- `assets/generated_57_63/parrot_32.png`
- `assets/generated_57_63/parrot_64.png`
- `assets/generated_57_63/parrot_128.png`
- `assets/generated_57_63/parrot_256.png`
- `assets/generated_57_63/parrot_512.png`

GIFs are not necessary here. PNG sequences and Manim-native animations will stay cleaner and easier to sync.
