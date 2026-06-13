# Video 2 Pipeline - Slides 1-15

Video 2 follows the provided script line by line and is split into three Manim scenes:

| Order | File | Class | Script Coverage |
| ---: | --- | --- | --- |
| 00 | `scenes/v02_s00_text_pixels_opening.py` | `V02TextPixelsOpening` | Scene 0, slides 1-3 |
| 01 | `scenes/v02_s01_generative_backbones.py` | `V02GenerativeBackbones` | Scene 1, slides 4-8 |
| 02 | `scenes/v02_s02_clip_coembedding.py` | `V02ClipCoEmbedding` | Scene 2, slides 9-15 |

## Shot Mapping

- 0.1 Opening title: particle burst, title, speaker, cyan scanline.
- 0.2 Tutorial map: curved route with four speakers, Srikumar highlighted with "YOU ARE HERE".
- 0.3 Route to pixel grid: route morphs to four pixels, expands to a 16x9-like pixel grid, then becomes a prompt bar.
- 1.1 Prompt to image: search bar, typed robot prompt, text particles, pixel reveal.
- 1.2 Text-to-image montage: four prompt cards for robot cooking, robot graffiti, raccoon, and alien pyramid.
- 1.3 Text-to-video: keyframes collapse into a film strip, with Text Prompt -> Keyframes -> Super-resolution -> Video.
- 1.4 Text-to-3D: DreamFusion-style card, cube icon, Text-to-Image + NeRF label.
- 1.5 Backbones: split screen for autoregressive token filling and diffusion denoising.
- 1.6 Centerpiece: Text-to-Image hub branches to video, 3D, image editing, and super-resolution, then highlights CLIP.
- 2.1 Puzzle timeline: U-Net, Diffusion, Transformers, CLIP, VQGAN, DALL-E, LDM.
- 2.2 Image feature space: dots cluster from chaos into semantic groups.
- 2.3 Text outside image space: two-universe layout with vision and language separated.
- 2.4 Co-embedding: CLIP/ALIGN bridge, image/text nodes pulled into a shared graph.
- 2.5 Single vs two tower: fixed label classifier versus open-vocabulary alignment.
- 2.6 InfoNCE matrix: green diagonal positives, orange negatives, compact contrastive formulas.
- 2.7 Visual address: raccoon prompt and image pass through encoders, vectors meet, address pin appears.
- 2.8 Tokenization transition: address dissolves into image card, pixel grid, and token matrix.

## Render

Render one scene:

```powershell
python render.py -ql --scene V02TextPixelsOpening
```

Render all current Video 2 slide 1-15 scenes:

```powershell
python render.py -ql --video 2
```

Concatenate the low-quality preview:

```powershell
python scripts/concat_video2_preview.py
```
