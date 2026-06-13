# Video 2 Scenes 0-2 Asset Download Shortlist

Day la shortlist dung sau khi doi chieu lai code cho `v02_s00`, `v02_s01`, `v02_s02`.
Ket luan moi: ban noi dung, scene 2 can them nhom anh minh da bo sot luc truoc neu muon ban render dep, khong chi dung icon placeholder.

## Scene 0

Khong can tai anh ngoai bat buoc.

Scene 0 dung Manim particles, pixel grid va background texture co san. File `assets/external/particles_bg.mp4` trong list cu co the bo qua vi scene hien tai khong goi den video background do.

## Scene 1 - Generative Backbones

Day la nhom can uu tien cao nhat.

| Priority | Save to | Ghi chu |
|---|---|---|
| 1 | `assets/slides/s04_robot_cooking.png` | Anh AI ro net: friendly robot cooking in modern kitchen |
| 1 | `assets/slides/s04_robot_graffiti.png` | Nen dung PNG moi, ro hon file jpg hien co neu file hien tai bi mo/nho |
| 1 | `assets/slides/s04_raccoon.png` | Nen dung PNG moi, formal raccoon portrait, tophat |
| 1 | `assets/slides/s04_alien_pyramid.png` | Sci-fi alien pyramid landscape, high contrast |
| 2 | `assets/slides/s05_text_to_video_grid.png` | Crop grid text-to-video/Lumiere tu slide |
| 2 | `assets/slides/s06_text_to_3d.png` | Crop DreamFusion/text-to-3D diagram tu slide |

Code da duoc chinh de chap nhan fallback `.jpg` hien co:

- `assets/slides/s04_robot_graffiti.jpg`
- `assets/slides/s04_raccoon.jpg`
- `assets/slides/s06_text_to_3.jpg`

Nhung neu ban tai lai ban dep hon, nen dung dung ten `.png` trong bang tren.

## Scene 2 - CLIP / Co-Embedding

Nhom nay minh da bo sot trong cau tra loi truoc. Neu tai duoc, scene 2 se dep va dung y "image feature space" hon nhieu.

| Priority | Save to | Nen chon anh |
|---|---|---|
| 1 | `assets/slides/img_dog.jpg` | Dog portrait, centered, clean background |
| 1 | `assets/slides/img_wolf.jpg` | Gray wolf portrait, similar crop/style voi dog |
| 1 | `assets/slides/img_sunglasses.jpg` | Sunglasses product photo, simple background |
| 1 | `assets/slides/img_car.jpg` | Autonomous car / modern car on road |
| 2 | `assets/slides/img_autonomous_car.jpg` | Co the reuse/copy cung anh voi `img_car.jpg` neu khong muon tai them |
| 2 | `assets/slides/img_brain.png` | Brain / AI concept, nen nen trong suot hoac dark background |
| 2 | `assets/slides/img_code.png` | Dark-theme code editor screenshot |

Code da duoc chinh de scene 2 doc cac file tren khi co san. Neu file nao thieu, scene van fallback sang icon Manim.

## Khong can tai cho scenes 0-2

Nhung muc nay trong `needed_assets_v02.md` co the bo qua cho rieng scene 0-2:

- `assets/slides/s07_backbone.png`
- `assets/slides/s08_centerpiece.png`
- `assets/slides/s09_puzzle.png`
- `assets/slides/s11_feature_clusters.png`
- `assets/slides/s12_co_embedding.png`
- `assets/slides/s13_two_tower.png`
- `assets/slides/s14_clip_align.png`
- `assets/external/particles_bg.mp4`
- `assets/external/vid_dog_run.mp4`
- `assets/external/vid_astronaut.mp4`
- `assets/external/vid_northern_lights.mp4`
- `assets/external/vid_puppy.mp4`

## Icons

Khong can tai icon cho scenes 0-2 luc nay. Scene da co fallback bang Manim.

## Noise frames

Khong can tai tu ngoai. Scene 1 dung cac frame nay neu da generate:

- `assets/generated/diffusion_frames/diffuse_00.png`
- `assets/generated/diffusion_frames/diffuse_25.png`
- `assets/generated/diffusion_frames/diffuse_50.png`
- `assets/generated/diffusion_frames/diffuse_75.png`
- `assets/generated/diffusion_frames/diffuse_100.png`

Neu can tao lai:

```powershell
E:\miniconda\envs\min_ds-env\python.exe scripts\generate_v02_noise_frames.py
```

## Goi y tai nhanh

Bo toi thieu nen tai:

1. `s04_robot_cooking.png`
2. `s04_robot_graffiti.png`
3. `s04_raccoon.png`
4. `s04_alien_pyramid.png`
5. `img_dog.jpg`
6. `img_wolf.jpg`
7. `img_sunglasses.jpg`
8. `img_car.jpg`

Bo dep hon nen them:

9. `s05_text_to_video_grid.png`
10. `s06_text_to_3d.png`
11. `img_brain.png`
12. `img_code.png`
