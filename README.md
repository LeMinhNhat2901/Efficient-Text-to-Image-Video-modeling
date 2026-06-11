# Mathematics of Diffusion - Manim Video Series

This repo contains the Manim source, narration workflow, and local render tools
for a visual lecture series on the mathematics of diffusion models.

Video 1 is built as fourteen scenes, from the forward Markov chain intuition to
score functions, continuous-time SDEs, Fokker-Planck density flow, numerical
solvers, and failure cases. Video 2 can now start from the same clean project
shape without mixing new work into render caches.

## Repo Layout

```text
base_scene.py              Shared scene helpers and visual language.
config.py                  Colors, typography, spacing, and global constants.
render.py                  Renders configured scenes and muxes narration when present.
scenes/                    Manim scene source files.
scripts/                   Utility scripts for precompute, TTS, muxing, and preview export.
tts/                       Narration text, generation notes, and private voice references.
assets/                    Checked-in source assets and attribution notes.
docs/                      Storyboards, equations, draft scripts, and video pipeline notes.
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
python render.py -ql
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

After rendering all low-quality scenes, stitch a full preview:

```powershell
python scripts/concat_preview.py
```

The preview is written locally under:

```text
media/videos/preview_480p15/DiffusionPrototypePreview.mp4
```

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
| 00 | `scenes/s00_roadmap.py` | `RoadmapOverview` |
| 01 | `scenes/s01_forward_ou_wiener.py` | `ForwardOUWiener` |
| 02 | `scenes/s02_markov.py` | `MarkovChainScene` |
| 03 | `scenes/s03_reverse_chain.py` | `ReverseMarkovChain` |
| 04 | `scenes/s04_score_compass.py` | `ScoreCompassScene` |
| 05 | `scenes/s05_local_linear.py` | `LocalLinearScoreScene` |
| 06 | `scenes/s06_mse_conditional_mean.py` | `MSEConditionalMeanScene` |
| 07 | `scenes/s07_training_loop.py` | `TrainingLoopScene` |
| 08 | `scenes/s08_sde_drift_diffusion.py` | `ContinuousTimeFlowScene` |
| 09 | `scenes/s09_probability_flow_ode.py` | `DriftDiffusionScene` |
| 10 | `scenes/s10_fokker_planck_score.py` | `FokkerPlanckScoreScene` |
| 11 | `scenes/s11_reverse_distribution.py` | `ReverseDistributionScene` |
| 12 | `scenes/s12_runge_kutta_solver.py` | `RungeKuttaSolverScene` |
| 13 | `scenes/s13_finale_failure.py` | `FinaleFailureScene` |

Detailed timing and visual beats are in `docs/video1_pipeline.md`.

## Starting Video 2

Suggested convention:

```text
docs/video2_outline.md
docs/video2_pipeline.md
scenes/v02_s00_<topic>.py
scenes/v02_s01_<topic>.py
tts/scripts/v02_s00_<topic>.txt
tts/scripts/v02_s01_<topic>.txt
```

When Video 2 scenes are ready, add them to the `SCENES` and `AUDIO_SCENES`
lists in `render.py`, and add their paths to `scripts/concat_preview.py` if
you want a combined preview.

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
