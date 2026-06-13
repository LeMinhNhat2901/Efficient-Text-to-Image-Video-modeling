# Video 2 Asset Needs - Slides 16-39

Use this file if you want to replace the current placeholder assets with real crops/photos.
The scenes already have fallback drawings/placeholders, so missing assets should not break rendering.

## Slide Crops

Crop these from the lecture slides and save as PNG:

| Save to | Source | Use |
|---|---|---|
| `assets/slides_16_39/s17_visual_words_dog_car.png` | Slide 17 | Dog/car visual parts reference |
| `assets/slides_16_39/s18_visual_words_clustering.png` | Slide 18 | Visual-word clustering reference |
| `assets/slides_16_39/s20_image_tokenization.png` | Slide 20 | 256x256 image to 16x16 token grid |
| `assets/slides_16_39/s22_vqgan_overview.png` | Slide 22 | VQGAN overview |
| `assets/slides_16_39/s23_codebook_token_image.png` | Slide 23 | Codebook and token image |
| `assets/slides_16_39/s25_vq_loss.png` | Slide 25 | VQ reconstruction/codebook losses |
| `assets/slides_16_39/s26_gan_loss.png` | Slide 26 | Perceptual/GAN loss |
| `assets/slides_16_39/s30_model_hierarchy.png` | Slide 30 | MRF -> CNN -> Transformer hierarchy |
| `assets/slides_16_39/s31_vit.png` | Slide 31 | Vision Transformer diagram |
| `assets/slides_16_39/s33_ordering_problem.png` | Slide 33 | Ordering paths/loss plots |
| `assets/slides_16_39/s34_conditioned_synthesis.png` | Slide 34 | Depth/low-res/semantic/edge conditioning examples |
| `assets/slides_16_39/s35_muse.png` | Slide 35 | Muse masked decoding |
| `assets/slides_16_39/s36_markovgen.png` | Slide 36 | MarkovGen overview |
| `assets/slides_16_39/s37_mrf_formulation.png` | Slide 37 | Unary/pairwise MRF formulation |
| `assets/slides_16_39/s38_speedup.png` | Slide 38 | Muse vs MarkovGen timing/results |

## External Photos

Minimum useful set:

| Save to | Search suggestion |
|---|---|
| `assets/external_16_39/dog_main.jpg` | golden retriever puppy grass / dog portrait high resolution |
| `assets/external_16_39/red_car_main.jpg` | red sports car road side view |
| `assets/external_16_39/mona_lisa.jpg` | Mona Lisa Wikimedia Commons public domain |
| `assets/external_16_39/bicycle.jpg` | bicycle photo Unsplash / Pixabay / Pexels |
| `assets/external_16_39/violin.jpg` | violin photo Unsplash / Pixabay / Pexels |
| `assets/external_16_39/city_building.jpg` | building facade / urban street high resolution |
| `assets/external_16_39/sydney_opera_house.jpg` | Sydney Opera House waterfront |

## Generated/Cropped Assets

These are more important than stock-photo polish because they make the process feel simulated:

| Save to | How to create |
|---|---|
| `assets/patches/dog_eye_patch.png` | Crop from `dog_main.jpg` |
| `assets/patches/dog_nose_patch.png` | Crop from `dog_main.jpg` |
| `assets/patches/dog_ear_patch.png` | Crop from `dog_main.jpg` |
| `assets/patches/car_wheel_patch.png` | Crop from `red_car_main.jpg` |
| `assets/patches/car_edge_patch.png` | Crop from `red_car_main.jpg` |
| `assets/patches/fur_texture_patch.png` | Crop from `dog_main.jpg` |
| `assets/patches/road_texture_patch.png` | Crop from `red_car_main.jpg` or road photo |
| `assets/generated/dog_token_grid.png` | Pixelated/tokenized dog image |
| `assets/generated/dog_token_numbers.png` | 16x16 or 4x4 numeric token grid |
| `assets/generated/sydney_imperfect_tokens.png` | Sydney image with swapped/blurred blocks |
| `assets/generated/sydney_fixed_tokens.png` | Refined/fixed Sydney token image |
| `assets/generated/edge_map_city.png` | Canny edge map from `city_building.jpg` |
| `assets/generated/lowres_city.png` | Downscale then upscale city image |
| `assets/generated/highres_city.png` | Original/high-res city image |
| `assets/generated/semantic_map_city.png` | Simple colored semantic map |
| `assets/generated/fake_depth_map_city.png` | Grayscale depth-like map |

## Optional Icons

Save in `assets/icons/` if you want to replace drawn Manim blocks:

| Save to | Suggested icon |
|---|---|
| `assets/icons/encoder.svg` | CPU / neural module |
| `assets/icons/decoder.svg` | output / reconstruction module |
| `assets/icons/dictionary.svg` | book / dictionary |
| `assets/icons/discriminator.svg` | shield / judge |
| `assets/icons/stopwatch.svg` | stopwatch / timer |
| `assets/icons/checkmark.svg` | check / success |
| `assets/icons/warning.svg` | warning / inconsistency |
| `assets/icons/gpu_chip.svg` | GPU/TPU chip |

## Current State

The repo currently contains placeholder versions for the main external images, patches, slide crops, and generated maps. You can replace any placeholder with a real file using the same path and filename.
