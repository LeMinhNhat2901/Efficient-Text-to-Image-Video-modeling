# Needed External Assets

Use this as a shopping list for assets that can improve the video without making the main explanations depend on copyrighted slide images.

## High Priority

- `assets/images/clean_sample.png`
  - A public-domain, self-made, or clearly licensed clean sample image.
  - Can replace `assets/puppy.jpg` if the puppy image license is unclear.

- `assets/icons/neural_network.png`
  - Used in Scene 8 training loop as the neural-network block when present.
  - Prefer a simple open-source image with attribution.

- `assets/icons/Warning.svg`
  - For later failure-case scenes.

- `assets/sounds/tick.mp3`
  - Used as a subtle tick/click for telescoping cancellation when present.

## Optional

- `assets/textures/subtle_noise.jpg`
  - Used as a very low-contrast title/opening texture when present.

- `assets/textures/dark_grid.jpg`
  - Used as a subtle background grid in the math-heavy scenes.

- `assets/images/markov_portrait.jpg`
  - Used in the Markov-history beat when present.
  - Record the source URL and license in `assets/attribution.md`.

## Not Needed For Scenes 5-8

- Hansel/Gretel hook is drawn directly in Manim as home, forest/noise, and breadcrumbs.
- Swiss roll terrain, contour lines, score compass, beta slider, MSE parabola, and training loop are all generated in code.
- No external image is required for the score-compass sequence unless you later want a cinematic background texture.

## Optional Cinematic Assets For SDE / Flow Scenes

- `assets/images/einstein_portrait.jpg`
  - Used in the Brownian-motion history bridge.
  - Prefer a public-domain or Wikimedia Commons image and record the source/license.

- `assets/images/ito_portrait.jpg`
  - Used in the stochastic-calculus / Ito bridge.
  - Prefer a public-domain or clearly licensed academic portrait.

- `assets/images/Brownian_motion_large.gif`
  - Used as a small historical/sample-path visual in the SDE bridge.

- `assets/images/oil_slick_drift.jpeg`
  - Used as a real-world drift image: oil sheen or dye moving along slow water.
  - If used, overlay Manim vector arrows on top rather than relying on the photo to explain the math.

- `assets/images/vortex_structure.png`
  - Used as a faded cinematic background behind Probability Flow ODE lines.
  - Use only as a faded cinematic background behind Manim particles/flow lines.

## Rules

- Add every external asset source/license to `assets/attribution.md`.
- Avoid Donald Duck, cartoon Hansel and Gretel, or slide images with unclear rights.
- Use external images for mood/context; keep the math explanation in Manim.
