# Video 2 Slides 40-56 - Assets To Keep / Download

Conclusion: do not download everything from the old list.

The repo already has usable generated diffusion/noise frames in `assets/generated_40_56/`.
Those are enough for slides 40-51 and should be kept as-is unless we decide to redesign the whole visual language.

Please download or replace only the 5 image assets below. These are the ones that will make the video noticeably better.

## Keep / Download

1. `assets/external_40_56/cat_clean.jpg`
   - Status: missing / truly useful.
   - Used in slides 41 and 44 as the clean `x_0` image before noise is added.
   - Why it matters: the forward diffusion chain reads much better if the first image is a real clean cat, not a generated placeholder.
   - Recommended image: centered tabby cat portrait, clean background, clear lighting, square-ish crop.
   - Search terms: `tabby cat portrait indoor high resolution`, `cat sitting portrait clean background`, `cat on table high resolution`.

2. `assets/external_40_56/output_tabby_cat.jpg`
   - Status: existing placeholder should be replaced.
   - Used in slide 52 and guidance-scale examples.
   - Why it matters: this is one of the main "same noise, different guidance direction" outputs.
   - Recommended image: high-quality tabby cat portrait, dark/neutral background, same crop style as lion/leopard.

3. `assets/external_40_56/output_lion.jpg`
   - Status: existing placeholder should be replaced.
   - Used in slide 52.
   - Why it matters: makes the guidance branching visually obvious.
   - Recommended image: lion portrait, dark/neutral background, centered face, similar lighting/crop to `output_tabby_cat.jpg`.

4. `assets/external_40_56/output_leopard.jpg`
   - Status: existing placeholder should be replaced.
   - Used in slide 52.
   - Why it matters: completes the three-output guidance comparison.
   - Recommended image: leopard portrait, dark/neutral background, centered face, similar lighting/crop to the other two outputs.

5. `assets/external_40_56/cyberpunk_cat.jpg`
   - Status: existing placeholder should be replaced.
   - Used in slides 54 and 55 for CFG / CLIP guidance.
   - Why it matters: this is the most memorable visual for prompt-conditioned generation.
   - Recommended prompt/image: `A cyberpunk cat wearing neon glasses, cinematic portrait, dark background, studio lighting`.

## Do Not Need To Download

1. `assets/external_40_56/tv_static_background.mp4`
   - Not needed. The generated Gaussian noise already matches the diffusion explanation and keeps the style cleaner.

2. `assets/icons/steering_wheel.svg`
3. `assets/icons/compass.svg`
4. `assets/icons/classifier.svg`
5. `assets/icons/neural_network.svg`
6. `assets/icons/unet.svg`
7. `assets/icons/slider.svg`
8. `assets/icons/checkmark.svg`
9. `assets/icons/warning.svg`
   - Not needed for now. The current Manim-native icon/diagram style is more consistent with the 3b1b-like look and avoids asset mismatch.

## Notes For Consistency

- Prefer all output images as square or near-square crops.
- Keep the subject centered with enough margin around the face.
- Avoid watermarks, text, UI overlays, extreme blur, and busy backgrounds.
- For `output_tabby_cat.jpg`, `output_lion.jpg`, and `output_leopard.jpg`, try to keep the same lighting and composition so slide 52 feels like controlled guidance, not three unrelated images.
