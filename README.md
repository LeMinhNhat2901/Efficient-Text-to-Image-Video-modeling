# Diffusion Models Manim Prototype

Prototype scenes for a visual lecture on the mathematics of diffusion models.

## Setup

Install Manim, LaTeX, and ffmpeg first. Then from the workspace root:

```powershell
python -m pip install -r requirements.txt
```

Quick environment checks:

```powershell
python -c "import manim; print(manim.__version__)"
ffmpeg -version
latex --version
```

## Render

Render one prototype scene:

```powershell
manim -ql scenes/s01_forward_ou_wiener.py ForwardOUWiener
```

Render all current prototype scenes:

```powershell
python render.py -ql
```

Force a clean preview render after code/layout edits:

```powershell
python render.py -ql --disable-caching
```

Use `-qm` for a medium check and `-qh` for the 1080p final.

Expected final render flow:

```powershell
python render.py -ql
python render.py -qm
python render.py -qh
```

## Current Scenes

- `RoadmapOverview`: 10-row roadmap for the 42-minute pipeline.
- `ForwardOUWiener`: forward/backward intuition plus OU and Wiener process visuals.
- `MarkovChainScene`: Markov chain intuition, Markov property, and factorization.
- `ReverseMarkovChain`: reverse-chain question, Bayes inversion, and Gaussian approximation.

## Next Build Order

1. Learning backward conditional mean with least-square intuition.
2. Training algorithm and noise prediction formulation.
3. Continuous stochastic process / Ito SDE.
4. Fokker-Planck distribution evolution.
5. Runge-Kutta, density/vector-field visuals, and failure cases.

## Equation Rendering

Equations render in this order:

1. Manim `MathTex` if a LaTeX distribution is installed and `latex` is available in `PATH`.
2. Cached SVG math via Matplotlib mathtext in `assets/equations/`.
3. Plain text only if both math renderers fail.

For the final submission, installing MiKTeX or TeX Live is still ideal, but the SVG math fallback is designed to look much closer to compiled LaTeX than ordinary text.
