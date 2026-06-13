# Video 2 Needed Assets

This is the download/crop list for Video 2, slides 1-15. The current Manim scenes include procedural fallback visuals, so renders work without these files, but the final video will look better once these assets are added.

## Slide Crops

Put these under `assets/slides/`:

- `s04_robot_cooking.png` - crop from slide 4, robot cooking example.
- `s04_robot_graffiti.png` - crop from slide 4, robot graffiti example.
- `s04_raccoon.png` - crop from slide 4, raccoon in formal clothes and tophat.
- `s04_alien_pyramid.png` - crop from slide 4, alien pyramid landscape.
- `s05_text_to_video_grid.png` - crop from slide 5, Lumiere text-to-video grid.
- `s06_text_to_3d.png` - crop from slide 6, DreamFusion/text-to-3D visual.
- `s07_backbone.png` - crop from slide 7, text-to-image backbone reference.
- `s08_centerpiece.png` - crop from slide 8, text-to-image as centerpiece.
- `s09_puzzle.png` - crop from slide 9 or 10, timeline puzzle.
- `s11_feature_clusters.png` - crop from slide 11, image feature clusters.
- `s12_co_embedding.png` - crop from slide 12, image-text co-embedding.
- `s13_two_tower.png` - crop from slide 13, single-tower vs two-tower.
- `s14_clip_align.png` - crop from slide 14, CLIP/ALIGN matrix and formula.

## Optional Generated Or Licensed Assets

Put generated images under `assets/generated/` and external media under `assets/external/`:

- `generated/raccoon_prompt_image.png` - AI-generated or slide-faithful image for "A raccoon wearing formal clothes, wearing a tophat."
- `generated/robot_cooking_prompt_image.png` - optional hook image if the slide crop is too low-res.
- `generated/robot_graffiti_prompt_image.png` - optional hook image if the slide crop is too low-res.
- `generated/alien_pyramid_prompt_image.png` - optional hook image if the slide crop is too low-res.
- `external/particle_grid_background.mp4` - abstract digital particles or dark pixel grid, used only as a subtle background.
- `external/text_to_video_loop_01.mp4` through `external/text_to_video_loop_04.mp4` - short public-domain or permissively licensed loops for text-to-video montage.
- `external/rotating_3d_object.mp4` or a PNG sequence - optional rotating 3D object for the text-to-3D beat.
- `external/dog_photo.jpg`, `external/wolf_photo.jpg`, `external/sunglasses_photo.jpg`, `external/autonomous_car_photo.jpg` - optional visual anchors for feature clusters.
- `icons/text_icon.svg`, `icons/image_icon.svg`, `icons/video_icon.svg`, `icons/cube_3d.svg`, `icons/encoder.svg` - optional icons from Tabler, SVG Repo, or another clear open-source source.

## Source Guidance

- Prefer slide crops for the main lecture content.
- Prefer self-generated images for the robot/raccoon/alien prompt examples if slide crops are blurry.
- Use Pexels, Pixabay, Wikimedia Commons, Openverse, or clearly licensed Creative Commons sources for real media.
- Avoid random Google Images for public release.
- Avoid trademark-heavy logos unless they are essential. For "software", a generic code icon is safer than a TensorFlow logo.

## Attribution Tracking

Add every non-generated external asset to `assets/attribution.md` or an `assets_manifest.csv` with:

```text
filename,source_url,author,license,usage,notes
```

For CC BY assets, include title, author, source, and license. Avoid NC assets if the video may be monetized or publicly distributed with ads.
