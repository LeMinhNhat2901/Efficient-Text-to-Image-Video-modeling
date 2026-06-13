# Mathematics of Diffusion - Manim Video Series

This repo contains the Manim source, narration workflow, and local render tools
for a visual lecture series on the mathematics of diffusion models.

Video 1 is built as fourteen scenes, from the forward Markov chain intuition to
score functions, continuous-time SDEs, Fokker-Planck density flow, numerical
solvers, and failure cases. Video 2 explores generative backbones and diffusion architectures. Video 3 and Video 4 contain scenes from the CVPR 2025 tutorial on efficient text-to-image generation.

## Repo Layout

```text
base_scene.py              (Moved to scenes/common/base_scene.py)
config.py                  Colors, typography, spacing, and global constants.
render.py                  Renders configured scenes and muxes narration when present.
scenes/
  ├── common/              Shared visual language and configs.
  ├── video_01/            Video 1 source files.
  ├── video_02/            Video 2 source files.
  ├── video_03/            Video 3 source files (CVPR Tutorial Part 3).
  └── video_04/            Video 4 source files (CVPR Tutorial Part 4).
scripts/                   Utility scripts for precompute, TTS, muxing, and preview export.
tts/                       Narration text, generation notes, and private voice references.
assets/                    Checked-in source assets and attribution notes.
docs/                      Pipeline notes and documentation.
media/                     Local Manim output. Ignored by git.
tmp_review_frames/         Local frame grabs for visual review. Ignored by git.
```

Keep `scripts/` for executable tooling. Put planning notes, outlines, scripts,
and long scene timing notes in `docs/`.

## Setup

Install FFmpeg and a LaTeX distribution first. On Windows, MiKTeX or TeX Live
works for Manim `MathTex`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Quick checks:

```powershell
python -c "import manim; print(manim.__version__)"
ffmpeg -version
latex --version
```

## Render

Render one scene:

```powershell
python render.py -ql --scene RoadmapOverview
```

Render all configured Video 1 scenes:

```powershell
python render.py --video 1 -ql
```

Render Video 3 scenes:

```powershell
python render.py --video 3 -ql
```

Use `-qm` for a medium check and `-qh` for a final-quality render:

```powershell
python render.py -qm
python render.py -qh
```

When layout/caching gets stale:

```powershell
python render.py -ql --disable-caching
```

`render.py` also tries to mux matching narration from `tts/outputs/*.wav` after
each scene render. If an audio file is missing, it leaves the silent render in
place and continues.

## Preview

After rendering all low-quality scenes, stitch a full preview (Video 1 only):

```powershell
python scripts/concat_preview.py
```

The preview is written locally under:

```text
media/videos/preview_480p15/DiffusionPrototypePreview.mp4
```

## Stitch Full Videos

To concatenate all rendered scenes of a specific video (e.g., Video 3) into a single, complete video file with audio:

```powershell
python scripts/stitch_video.py --video 3 -qm --output Tutorial_Part3.mp4
```

This uses `ffmpeg` to securely copy and concatenate the streams without re-encoding, generating the final stitched video in the project root.

`media/` is ignored by git because it contains generated render output and
Manim cache files.

## Precomputed Visual Data

These optional generated assets make a few scenes smoother. Scenes still have
fallbacks when the generated files are absent.

```powershell
python scripts/precompute_noise_frames.py
python scripts/precompute_spiral_diffusion_frames.py
python scripts/precompute_ou_paths.py
```

Generated files are written to `assets/generated/`, which is ignored by git.

## Narration / TTS

Use a separate `chatterbox` environment for voice generation. Do not install the
Chatterbox stack into the Manim render environment because it has a different
Torch/Numpy dependency profile.

```powershell
conda activate chatterbox
python scripts/generate_chatterbox_tts.py --dry-run
python scripts/generate_chatterbox_tts.py --input tts/scripts --output-dir tts/outputs --device cuda
```

See `tts/README.md` for presets, voice references, splitting the full narration
file, and troubleshooting.

## Video 1 Scenes

| Order | File | Class |
| ---: | --- | --- |
| 00 | `scenes/video_01/s00_roadmap.py` | `RoadmapOverview` |
| 01 | `scenes/video_01/s01_forward_ou_wiener.py` | `ForwardOUWiener` |
| 02 | `scenes/video_01/s02_markov.py` | `MarkovChainScene` |
| 03 | `scenes/video_01/s03_reverse_chain.py` | `ReverseMarkovChain` |
| 04 | `scenes/video_01/s04_score_compass.py` | `ScoreCompassScene` |
| 05 | `scenes/video_01/s05_local_linear.py` | `LocalLinearScoreScene` |
| 06 | `scenes/video_01/s06_mse_conditional_mean.py` | `MSEConditionalMeanScene` |
| 07 | `scenes/video_01/s07_training_loop.py` | `TrainingLoopScene` |
| 08 | `scenes/video_01/s08_sde_drift_diffusion.py` | `ContinuousTimeFlowScene` |
| 09 | `scenes/video_01/s09_probability_flow_ode.py` | `DriftDiffusionScene` |
| 10 | `scenes/video_01/s10_fokker_planck_score.py` | `FokkerPlanckScoreScene` |
| 11 | `scenes/video_01/s11_reverse_distribution.py` | `ReverseDistributionScene` |
| 12 | `scenes/video_01/s12_runge_kutta_solver.py` | `RungeKuttaSolverScene` |
| 13 | `scenes/video_01/s13_finale_failure.py` | `FinaleFailureScene` |

Detailed timing and visual beats are in `docs/video1_pipeline.md`.

## Videos 3 & 4 (CVPR Tutorial)

Video 3 and 4 scenes (from the CVPR tutorial) are organized in `scenes/video_03/` and `scenes/video_04/`.
Their assets and audio are kept under `assets/video_0X/` and `tts/outputs/video_0X/`.
Since their audio fragments are natively embedded in the Manim scenes via `self.add_sound()`, `render.py` will render them with audio gracefully without needing to post-mux single `.wav` files.

## Assets

Track source/license information for non-code assets in:

```text
assets/attribution.md
```

Checked-in assets should be source materials that are hard to regenerate.
Generated assets belong in `assets/generated/`, `media/`, `tts/outputs/`, or
`tmp_review_frames/`.

## Git Hygiene

The ignore rules now keep future cache and render output out of git. If older
generated files were already tracked, remove them from the index before your
next cleanup commit:

```powershell
git rm --cached -r media assets/generated assets/equations __pycache__ scenes/__pycache__ utils/__pycache__
```

That command only untracks the generated files; it does not delete local render
output from disk.
