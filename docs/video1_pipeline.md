# Mathematics of Diffusion - 42 Minute Pipeline

Source of truth: final English narration script attached in the Codex thread.

Part 1 title:

```text
Viet lai mui ten thoi gian bang Xac suat
```

Main narrative:

```text
Forward diffusion destroys structure in a controlled way.
Reverse diffusion asks whether probability can describe a path back from noise.
```

The current build locks every scene to the narration target using `TARGET_DURATION` plus `hold_to_time()`. Do not shorten these scenes when tuning effects; adjust animation timing around narration instead.

## Voice Timing Lock

| Scene | File | Target |
| --- | --- | ---: |
| 1 | `scenes/video_01/s00_roadmap.py` | 154.3s |
| 2 | `scenes/video_01/s01_forward_ou_wiener.py` | 210s |
| 3 | `scenes/video_01/s02_markov.py` | 180s |
| 4 | `scenes/video_01/s03_reverse_chain.py` | 210s |
| 5 | `scenes/video_01/s04_score_compass.py` | 180s |
| 6 | `scenes/video_01/s05_local_linear.py` | 180s |
| 7 | `scenes/video_01/s06_mse_conditional_mean.py` | 210s |
| 8 | `scenes/video_01/s07_training_loop.py` | 150s |
| 9 | `scenes/video_01/s08_sde_drift_diffusion.py` | 165s |
| 10 | `scenes/video_01/s09_probability_flow_ode.py` | 180s |
| 11 | `scenes/video_01/s10_fokker_planck_score.py` | 165s |
| 12 | `scenes/video_01/s11_reverse_distribution.py` | 165s |
| 13 | `scenes/video_01/s12_runge_kutta_solver.py` | 195s |
| 14 | `scenes/video_01/s13_finale_failure.py` | 120s |

Total scene time follows the rendered narration WAVs when they are available. Preview concat adds 0.25s gaps between scenes.

## Scene 1 - Opening Intuition

Scene file: `scenes/video_01/s00_roadmap.py`

Class: `RoadmapOverview`

Target duration: 154.3 seconds, matched to `tts/outputs/video_01/s00_roadmap.wav`.

Visual beats:

1. Start from black.
2. Show pure noise first with the label `Random noise`.
3. Ask: `Can this become an image?`
4. Transform noise backward into the clean sample image.
5. Rewind forward as a small chain: `x_0 -> x_1 -> x_2 -> ... -> x_T`.
6. Contrast `Forward: designed` with `Reverse: learned`.
7. Show the title after the hook: `Mathematics of Diffusion`.
8. Show three keywords: Markov chains, Bayes rule, learning the reverse step.
9. Draw a 2D spiral data distribution at `t = 0`.
10. Diffuse the spiral into a chaotic noise cloud at `t = T`.
11. End with the reverse question: can we run this process backward?

Implementation note:

```powershell
python scripts/precompute_noise_frames.py
python scripts/precompute_spiral_diffusion_frames.py
```

To mux the rendered preview scene with narration without relying on Manim `add_sound`:

```powershell
python scripts/mux_scene_audio.py --scene s00
```

This generates `assets/generated/noise_frames/puppy_noise_00.png` through `puppy_noise_12.png` and `assets/generated/spiral_frames/spiral_diffusion.npy`. The generated directories are ignored by git; Scene 1 can still render without them by using the procedural Manim fallback.

Track source/license information for non-code assets in `assets/attribution.md`.

Key idea:

```text
Noise increases entropy and breaks visible structure.
```

## Scene 2 - Forward Process Mathematics

Scene file: `scenes/video_01/s01_forward_ou_wiener.py`

Class: `ForwardOUWiener`

Target duration: 210 seconds.

Visual beats:

1. Keep one particle in focus.
2. Reveal the forward equation slowly.
3. Explain `\alpha_t`, `\beta_t`, and Gaussian noise `G`.
4. Show expected variance widening over time.
5. Draw five random walk paths that spread as time grows.
6. Reveal the direct jump formula from `X_0` to `X_t`.
7. Show the product definition of `\tilde{\alpha}_t`.

Implementation note:

```powershell
python scripts/precompute_ou_paths.py
```

This generates `assets/generated/ou_paths/ou_paths.npz` for the five sample paths, the widening standard-deviation band, and one highlighted particle trace.

Main equations:

```tex
X_t=\alpha_t X_{t-1}+\sqrt{\beta_t}G
```

```tex
X_t=\tilde{\alpha}_t X_0+\sqrt{\tilde{\beta}_t}G
```

```tex
\tilde{\alpha}_t=\prod_{i=1}^t \alpha_i
```

## Scene 3 - Coin Toss And Markov Property

Scene file: `scenes/video_01/s02_markov.py`

Class: `MarkovChainScene`

Target duration: 180 seconds.

Visual beats:

1. Use a Manim coin toss visual instead of copyrighted media.
2. Show that a random process can still have rules.
3. Draw the chain `x_0 -> x_1 -> ... -> x_{t-1} -> x_t -> x_{t+1}`.
4. Dim the distant past and highlight only the transition `x_{t-1} -> x_t`.
5. Reveal the Markov property after the visual.
6. Reveal the factorized joint distribution.

Main equations:

```tex
p(x_t\mid x_0,\ldots,x_{t-1})=p(x_t\mid x_{t-1})
```

```tex
p(x_{0:T})=p(x_0)\prod_{t=1}^{T}p(x_t\mid x_{t-1})
```

## Scene 4 - Telescoping And Reverse Probability

Scene file: `scenes/video_01/s03_reverse_chain.py`

Class: `ReverseMarkovChain`

Target duration: 210 seconds.

Visual beats:

1. Draw the forward chain first.
2. Dim the blue forward arrows, then grow the gold reverse arrows on the same nodes.
3. Ask whether a Markov chain has a reverse.
4. Show the forward factorization.
5. Rewrite each forward transition using Bayes' rule.
6. Substitute the fractions into the product.
7. Cancel matching marginal terms one by one with red cancellation lines.
8. Box the final reverse factorization.
9. Bridge to the neural network question: the formula is exact, but reverse conditionals are the unknown objects we must learn.

Main equations:

```tex
q(x_{0:T})=q(x_0)\prod_{t=1}^{T}q(x_t\mid x_{t-1})
```

```tex
q(x_t\mid x_{t-1})=
\frac{q(x_{t-1}\mid x_t)q(x_t)}{q(x_{t-1})}
```

```tex
q(x_{0:T})=q(x_T)\prod_{t=1}^{T}q(x_{t-1}\mid x_t)
```

## Preview Output

Current preview concat:

```text
media/videos/preview_480p15/DiffusionPrototypePreview.mp4
```

The concat script first tries FFmpeg, then falls back to PyAV/libx264 if the local FFmpeg runtime fails.

## Scene 5 - Score Compass

Scene file: `scenes/video_01/s04_score_compass.py`

Class: `ScoreCompassScene`

Target duration: 180 seconds.

Visual beats:

1. Use a short 15 to 20 second breadcrumb hook drawn in Manim: home, forest/noise, breadcrumbs.
2. Move quickly into a Swiss roll probability terrain with contour lines.
3. Drop a noisy point `y` in a low-probability region.
4. Reveal the local score compass `s(y)=\nabla\log p_X(y)`.
5. Phrase score as a local compass: at each point it points where log-probability rises fastest.
6. Show a beta step `y <- y + beta score(y)`.
7. Use a beta slider to contrast a small stable step with a large overshooting step.
8. Use the subtle/dark grid texture as background structure when present.

Main equations:

```tex
s(y)=\nabla\log p_X(y)
```

```tex
y \leftarrow y+\beta\nabla\log p_X(y)
```

## Scene 6 - Local Linear Approximation

Scene file: `scenes/video_01/s05_local_linear.py`

Class: `LocalLinearScoreScene`

Target duration: 180 seconds.

Visual beats:

1. Zoom into the probability landscape around a noisy point.
2. Use a magnifying glass to show the local region becoming nearly linear.
3. Highlight `\nabla\log p_X(y)`.
4. Bridge local score direction into the cleaner-state approximation.

Main equation:

```tex
\mu(X\mid y)\approx y+\beta\nabla\log p_X(y)
```

## Scene 7 - MSE And Conditional Mean

Scene file: `scenes/video_01/s06_mse_conditional_mean.py`

Class: `MSEConditionalMeanScene`

Target duration: 210 seconds.

Visual beats:

1. Show many possible cleaner states that could explain one noisy observation `y`.
2. Show their center of mass before showing the parabola.
3. Reveal that least squares is minimized at the conditional mean.
4. Be precise: in ideal conditions MSE is optimized by the conditional mean.
5. Bridge `f^*(y)=E[X|y]` into the learned reverse mean `\mu_\theta(y,t)`.
6. State that the neural network approximates the reverse mean, not that it finds it perfectly.

Main equations:

```tex
\mathcal{L}(f)=\mathbb{E}\|X-f(y)\|^2
```

```tex
f^*(y)=\mathbb{E}[X\mid y]
```

```tex
\mu_\theta(y,t)\approx\mathbb{E}[X_{t-1}\mid X_t=y]
```

## Scene 8 - Training Loop And Learned Breadcrumbs

Scene file: `scenes/video_01/s07_training_loop.py`

Class: `TrainingLoopScene`

Target duration: 150 seconds.

Visual beats:

1. Send score arrows into a neural network.
2. Show training loop: corrupt, predict cleaner state, compare, update.
3. Use a loss meter that decreases.
4. Show learned breadcrumbs back from noise to data.
5. Avoid saying the model predicts `x_0`; in this scene it predicts the cleaner previous state `x_{t-1}`.
6. Mention that some formulations predict noise instead.
7. End with teaser: SDE tracks samples, Fokker-Planck tracks densities.
8. Use `assets/icons/neural_network.png` when available; otherwise fall back to Manim-drawn nodes.

## Scene 9 - Breadcrumbs To Continuous Flow

Scene file: `scenes/video_01/s08_sde_drift_diffusion.py`

Class: `ContinuousTimeFlowScene`

Target duration: 165 seconds.

Visual beats:

1. Carry over learned reverse breadcrumbs from Part 2.
2. Show discrete time ticks becoming dense as `Delta t -> 0`.
3. Morph discrete Gaussian noise into Wiener noise `dW`.
4. Show random particle paths, then shift viewpoint to density evolution.
5. Transform particles into histogram bars, then a smooth density curve.
6. End by morphing the density into a Manim-drawn oil slick on a stream.

Main equation:

```tex
dX=\sqrt{\beta(t)}\,dW
```

## Scene 10 - Oil Slick: Drift And Diffusion

Scene file: `scenes/video_01/s09_probability_flow_ode.py`

Class: `DriftDiffusionScene`

Target duration: 180 seconds.

Visual beats:

1. Split the screen into `Drift only` and `Pure diffusion`.
2. Drift: particles move smoothly under a vector field.
3. Diffusion: particles spread symmetrically from random Wiener motion.
4. Show the separate density terms for drift and diffusion.
5. Merge both sides into the Ito process.

Main equations:

```tex
dX=\alpha(x,t)\,dt
```

```tex
dX=\sqrt{\beta(t)}\,dW
```

```tex
dX=\alpha(x,t)\,dt+\sqrt{\beta(t)}\,dW
```

## Scene 11 - Fokker-Planck And The Score

Scene file: `scenes/video_01/s10_fokker_planck_score.py`

Class: `FokkerPlanckScoreScene`

Target duration: 165 seconds.

Visual beats:

1. Move from individual sample paths to whole-density evolution.
2. Assemble drift and diffusion into a probability-flow density equation.
3. Reveal the velocity field `v`.
4. Highlight the score term `nabla log p(x,t)` as the returning compass.
5. Visualize a density cloud moving under a vector field.

Main equations:

```tex
\partial_t p=-\operatorname{div}(pv)
```

```tex
v(x,t)=\alpha(x,t)-\frac{\beta(t)}{2}\nabla\log p(x,t)
```

## Scene 12 - Reverse In Distribution

Scene file: `scenes/video_01/s11_reverse_distribution.py`

Class: `ReverseDistributionScene`

Target duration: 165 seconds.

Visual beats:

1. Show forward process spreading data into noise.
2. Freeze time and reveal score arrows in the noisy cloud.
3. State that reversal is in distribution, not a physical rewind of paths.
4. Dim forward arrows and grow reverse arrows that curve inward.
5. Briefly show reverse-of-reverse consistency.

Main equation:

```tex
d\bar X=\left[\cdots-\beta\nabla\log p\right]dt+\sqrt{\beta}\,d\bar W
```

## Scene 13 - Euler And Runge-Kutta Solvers

Scene file: `scenes/video_01/s12_runge_kutta_solver.py`

Class: `RungeKuttaSolverScene`

Target duration: 195 seconds.

Visual beats:

1. Show ideal continuous trajectory versus finite computer steps.
2. Euler: one slope, one straight step, visible error.
3. RK4: four slope scouts `k_1,k_2,k_3,k_4`.
4. Compare exact curve, Euler path, and RK4 path.
5. Show the neural network providing the learned score/vector field to the solver.

Main equations:

```tex
y_{n+1}=y_n+h f(t_n,y_n)
```

```tex
y_{n+1}=y_n+\frac{h}{6}(k_1+2k_2+2k_3+k_4)
```

## Scene 14 - Failure Cases And Final Synthesis

Scene file: `scenes/video_01/s13_finale_failure.py`

Class: `FinaleFailureScene`

Target duration: 120 seconds.

Visual beats:

1. Show successful sampling from noise back to structure.
2. Duplicate the path and show a wrong learned score direction.
3. Let the solver faithfully follow the wrong direction into a distorted sample.
4. Zoom out into the full pipeline: discrete, reverse learning, continuous, density, solver, failure.
5. End with `Mathematics of Diffusion` and `Forward is designed. Reverse is learned.`
