# Video 2 Slides 16-39 - Asset Shortlist Can Tai

Ket luan nhanh: khong can tai tat ca asset trong `needed_assets_v02_s16_39.md`.
Hien tai code chu yeu dung anh that, patch, va generated maps. Cac crop slide `assets/slides_16_39/*.png` gan nhu chi la reference, khong phai asset bat buoc de render dep.

## Uu Tien 1 - Nen Tai De Video Dep Hon Ro Ret

Tai thay the dung filename/path ben duoi. Nen chon anh ngang hoac gan vuong, net, it watermark, do phan giai toi thieu 1000px theo canh dai.

| Save to | Ly do can | Goi y tim/tai |
|---|---|---|
| `assets/external_16_39/dog_main.jpg` | Asset chinh cho visual words, tokenization, VQGAN. Anh hien tai rat nhe/placeholder nen len video se kem. | Dog portrait / golden retriever / clear dog face, natural light, high resolution |
| `assets/external_16_39/red_car_main.jpg` | Asset chinh cho car visual words va reconstruction/GAN beat. | Red car side view or 3/4 front view, clean road/background, high resolution |
| `assets/external_16_39/sydney_opera_house.jpg` | Asset chinh cho Muse vs MarkovGen comparison. Can anh ro de thay su khac nhau giua imperfect/fixed tokens. | Sydney Opera House waterfront, landscape, high resolution |
| `assets/external_16_39/city_building.jpg` | Nguon de tao depth/lowres/semantic/edge maps trong conditioned synthesis. | Urban street / building facade, straight lines, clear structure, high resolution |

Sau khi co 4 anh nay, minh co the tao lai cac asset phu tu dong/ban tu dong:

| Derived asset | Tao tu |
|---|---|
| `assets/patches/dog_eye_patch.png` | crop tu `dog_main.jpg` |
| `assets/patches/dog_nose_patch.png` | crop tu `dog_main.jpg` |
| `assets/patches/dog_ear_patch.png` | crop tu `dog_main.jpg` |
| `assets/patches/fur_texture_patch.png` | crop tu `dog_main.jpg` |
| `assets/patches/car_wheel_patch.png` | crop tu `red_car_main.jpg` |
| `assets/patches/car_edge_patch.png` | crop tu `red_car_main.jpg` |
| `assets/patches/road_texture_patch.png` | crop tu `red_car_main.jpg` hoac mot vung mat duong trong anh |
| `assets/generated/dog_token_grid.png` | tao tu `dog_main.jpg` |
| `assets/generated/dog_token_numbers.png` | tao tu `dog_main.jpg` |
| `assets/generated/sydney_imperfect_tokens.png` | tao tu `sydney_opera_house.jpg` |
| `assets/generated/sydney_fixed_tokens.png` | tao tu `sydney_opera_house.jpg` |
| `assets/generated/fake_depth_map_city.png` | tao tu `city_building.jpg` |
| `assets/generated/lowres_city.png` | tao tu `city_building.jpg` |
| `assets/generated/semantic_map_city.png` | tao tu `city_building.jpg` |
| `assets/generated/edge_map_city.png` | tao tu `city_building.jpg` |

## Uu Tien 2 - Nen Co Neu Muon Doan Codebook / Image Search Dep Hon

Ba anh nay dang duoc code dung trong scene VQGAN/codebook, nhung kich thuoc tren man hinh nho hon nen khong cap bach bang nhom Uu Tien 1.

| Save to | Ly do can | Goi y tim/tai |
|---|---|---|
| `assets/external_16_39/mona_lisa.jpg` | Card minh hoa image search/codebook. | Mona Lisa Wikimedia Commons public domain |
| `assets/external_16_39/bicycle.jpg` | Card minh hoa image search/codebook. | Bicycle photo, simple background, high resolution |
| `assets/external_16_39/violin.jpg` | Card minh hoa image search/codebook. | Violin photo, simple background, high resolution |

## Co The Bo Qua Luc Nay

Khong can tai/crop lai cac file nay truoc, vi scene hien tai ve lai bang Manim hoac dung visual rieng:

- `assets/slides_16_39/s17_visual_words_dog_car.png`
- `assets/slides_16_39/s18_visual_words_clustering.png`
- `assets/slides_16_39/s20_image_tokenization.png`
- `assets/slides_16_39/s22_vqgan_overview.png`
- `assets/slides_16_39/s23_codebook_token_image.png`
- `assets/slides_16_39/s25_vq_loss.png`
- `assets/slides_16_39/s26_gan_loss.png`
- `assets/slides_16_39/s30_model_hierarchy.png`
- `assets/slides_16_39/s31_vit.png`
- `assets/slides_16_39/s33_ordering_problem.png`
- `assets/slides_16_39/s34_conditioned_synthesis.png`
- `assets/slides_16_39/s35_muse.png`
- `assets/slides_16_39/s36_markovgen.png`
- `assets/slides_16_39/s37_mrf_formulation.png`
- `assets/slides_16_39/s38_speedup.png`

Ly do: neu dua crop slide vao thang video, nhin se giong doc slide hon la 3b1b. Nen giu chung lam reference thoi, con final nen dung diagram/animation ve lai.

## Quy Tac Dat File

- Ghi de dung path/filename nhu bang tren.
- Dung `.jpg` cho anh external neu duoc.
- Tranh watermark, text overlay, logo lon.
- Uu tien anh co chu the ro, background gon, contrast cao.
- Neu tai tu web, nen uu tien Wikimedia Commons, Unsplash, Pexels, Pixabay hoac source co license ro.
