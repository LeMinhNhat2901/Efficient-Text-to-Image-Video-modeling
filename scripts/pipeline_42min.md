# Mathematics of Diffusion - 42 Minute Pipeline

The source PDF is treated as roughly 44 slide-frames because each PDF page is 2-up. Do not copy tiny formulas from blurry frames until they are verified from a clear original slide.

## Act 0 - Roadmap

Target: 00:00-01:30

Scene file: `scenes/s00_roadmap.py`

On screen:

1. Forward / backward diffusion
2. Ornstein-Uhlenbeck and Wiener process
3. Markov chain
4. Markov property
5. Reverse Markov chain
6. Inverse conditional probabilities
7. Learning backward conditional mean
8. Ito / SDE
9. Fokker-Planck
10. Failure cases

## Act I - Forward / Backward + OU / Wiener

Target: 01:30-06:30

Scene file: `scenes/s01_forward_ou_wiener.py`

Safe equations:

```tex
\mathbf{x}_0 \rightarrow \mathbf{x}_T \sim \mathcal{N}(\mathbf{0},\mathbf{I})
```

```tex
dX_t=-\lambda X_t\,dt+\sigma\,dW_t
```

Purpose:

- Explain forward as designed corruption.
- Explain backward as learned denoising.
- Use OU for mean reversion plus noise.
- Use Wiener paths as the continuous-time noise source.

## Act II - Markov Chain

Target: 06:30-11:30

Scene file: `scenes/s02_markov.py`

Safe equations:

```tex
p(x_t\mid x_{t-1},x_{t-2},\ldots,x_0)=p(x_t\mid x_{t-1})
```

```tex
p(x_{0:T})=p(x_0)\prod_{t=1}^{T}p(x_t\mid x_{t-1})
```

Purpose:

- Show states as a chain.
- Clarify that Markov property does not mean complete independence.
- Show trajectory probability factorization.

## Act III - Reverse Markov Chain

Target: 11:30-18:00

Scene file: `scenes/s03_reverse_chain.py`

Safe equations:

```tex
p(x_{t-1}\mid x_t)=
\frac{p(x_t\mid x_{t-1})p(x_{t-1})}{p(x_t)}
```

```tex
p_\theta(x_{t-1}\mid x_t)=
\mathcal{N}\left(
\mu_\theta(x_t,t),
\Sigma_\theta(x_t,t)
\right)
```

Purpose:

- Ask whether the forward Markov chain has a useful reverse chain.
- Use Bayes rule for the exact reverse conditional.
- Explain why a learned approximation is needed.
- Present the Gaussian reverse conditional as a practical approximation.

## Remaining Acts

Act IV: learning backward conditional mean, least squares, training algorithm.

Act V: continuous stochastic processes and Ito SDE.

Act VI: Fokker-Planck, drift/no drift, Runge-Kutta, density and vector fields.

Act VII: sampling, failure cases, recap.

## Equation Rendering Rule

Use `self.display_equation(...)` for important formulas. It uses Manim `MathTex` when `latex` is available in PATH, and a readable text fallback otherwise. For final video, install LaTeX so equations match compiled PDF-style math.

