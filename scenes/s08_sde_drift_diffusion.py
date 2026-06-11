from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.part3_common import *


class ContinuousTimeFlowScene(Part3Scene):
    TARGET_DURATION = 87.91

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "From Breadcrumbs to Continuous Flow",
            "Discrete reverse steps become a stochastic path",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.7)

        self.breadcrumbs_to_limit()
        self.discrete_noise_to_wiener()
        self.particles_to_density()
        self.hold_to_time(start, self.TARGET_DURATION)

    def breadcrumbs_to_limit(self):
        question = self.hook_question("What happens when reverse steps become tiny?")
        nodes, arrows, curve = self.breadcrumb_path(reverse=True, color=REVERSE_ORANGE)
        chain_eq = self.display_equation(
            r"x_T\rightarrow x_{T-1}\rightarrow x_{T-2}\rightarrow\cdots\rightarrow x_0",
            width=8.7,
            size=31,
            accent=REVERSE_ORANGE,
        ).move_to([0, 1.65, 0])
        ticks = self.time_ticks(dense=False, color=MUTED)
        dense_ticks = self.time_ticks(dense=True, color=FLOW_CYAN)
        label = self.label("Discrete reverse steps", SUBTITLE_SIZE, REVERSE_ORANGE, font=FONT_TITLE).to_edge(DOWN, buff=0.52)
        limit_label = self.label("Continuous-time limit", SUBTITLE_SIZE, FLOW_CYAN, font=FONT_TITLE).move_to(label)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(chain_eq), LaggedStart(*[FadeIn(dot, scale=1.35) for dot in nodes], lag_ratio=0.1), run_time=1.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(ticks), FadeIn(label), run_time=1.5)
        dt_text = self.display_equation(
            r"\Delta t\rightarrow\frac{\Delta t}{2}\rightarrow\frac{\Delta t}{4}\rightarrow\frac{\Delta t}{8}",
            width=6.7,
            size=29,
            accent=FLOW_CYAN,
        ).move_to([0, -1.25, 0])
        self.play(FadeIn(dt_text, shift=0.08 * UP), run_time=0.8)
        self.play(Transform(ticks, dense_ticks), Transform(label, limit_label), FadeOut(arrows), Create(curve), run_time=2.0)
        self.play(nodes.animate.set_opacity(0.28), curve.animate.set_color(FLOW_CYAN).set_stroke(width=5), run_time=1.1)
        self.wait(5.0)
        self.play(FadeOut(Group(question, chain_eq, nodes, curve, ticks, label, dt_text)), run_time=1.0)

    def discrete_noise_to_wiener(self):
        question = self.hook_question("Discrete Gaussian noise becomes Wiener noise.")
        old_eq = self.display_equation(
            r"X_t=\alpha_tX_{t-1}+\sqrt{\beta_t}G",
            width=6.6,
            size=35,
            accent=DIFFUSION_GOLD,
        ).move_to([0, 1.15, 0])
        new_eq = self.display_equation(
            r"dX=\sqrt{\beta(t)}\,dW",
            width=4.8,
            size=38,
            accent=FLOW_CYAN,
        ).move_to([0, 1.15, 0])
        wiener = self.word_row(["Wiener", "process", "increment"], SMALL_SIZE, FLOW_CYAN).next_to(new_eq, DOWN, buff=0.18)
        path, particles = self.brownian_paths(np.array([-3.1, -0.65, 0]), count=24, seed=44, color=DIFFUSION_GOLD)
        jitter_note = VGroup(
            self.word_row(["infinitesimal", "random", "fluctuations"], SMALL_SIZE, MUTED),
            self.word_row(["continuous", "motion,", "not", "nervousness"], SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.48)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(old_eq), run_time=1.0)
        noise = VGroup(*[Dot(old_eq.get_right() + 0.1 * i * LEFT + 0.1 * UP, radius=0.025, color=DIFFUSION_GOLD) for i in range(12)])
        self.play(
            LaggedStart(
                *[
                    p.animate.shift((1.2 + 0.1 * i) * DOWN + (i - 5) * 0.12 * RIGHT).set_opacity(0.0)
                    for i, p in enumerate(noise)
                ],
                lag_ratio=0.03,
            ),
            run_time=1.0,
        )
        self.play(FadeTransform(old_eq, new_eq), FadeIn(wiener), run_time=1.2)
        self.play(LaggedStart(*[Create(p) for p in path], lag_ratio=0.015), FadeIn(particles), FadeIn(jitter_note), run_time=2.5)
        self.wait(25.0)
        self.play(FadeOut(Group(question, new_eq, wiener, path, particles, noise, jitter_note)), run_time=1.0)

    def particles_to_density(self):
        question = self.hook_question("Individual paths are random. Density evolution is structured.")
        cloud_1 = self.particle_cloud(90, 0.22, np.array([-2.8, 0.1, 0]), DIFFUSION_GOLD, 11, opacity=0.72)
        cloud_2 = self.particle_cloud(90, 0.55, np.array([-1.1, -0.05, 0]), DIFFUSION_GOLD, 12, opacity=0.58)
        cloud_3 = self.particle_cloud(90, 0.92, np.array([0.6, -0.15, 0]), DIFFUSION_GOLD, 13, opacity=0.46)
        bars = self.histogram_bars(DIFFUSION_GOLD)
        curve_narrow = self.density_curve(width=0.82, height=1.35, color=DIFFUSION_GOLD)
        curve_wide = self.density_curve(width=1.85, height=0.82, color=FLOW_CYAN)
        text_1 = self.word_row(["Individual", "paths", "are", "random."], SMALL_SIZE, MUTED).move_to([-3.05, -2.35, 0])
        text_2 = self.word_row(["Density", "evolution", "is", "structured."], SMALL_SIZE, FLOW_CYAN).move_to([2.8, -2.35, 0])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(cloud_1), FadeIn(text_1), run_time=1.0)
        self.wait(5.0)
        self.play(Transform(cloud_1, cloud_2), run_time=1.5)
        self.play(Transform(cloud_1, cloud_3), run_time=1.5)
        self.wait(4.0)
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.05), run_time=1.4)
        self.wait(3.5)
        self.play(ReplacementTransform(bars, curve_narrow), FadeIn(text_2), run_time=1.3)
        self.wait(3.0)
        self.play(Transform(curve_narrow, curve_wide), cloud_1.animate.set_opacity(0.18), run_time=1.6)
        self.wait(9.7)

    def word_row(
        self,
        words: list[str],
        size: int = SMALL_SIZE,
        color: str = MUTED,
        weight: str = NORMAL,
        buff: float = 0.095,
    ) -> VGroup:
        return VGroup(
            *[
                Text(word, font=FONT_SUBTITLE, font_size=size, color=color, weight=weight, disable_ligatures=True)
                for word in words
            ]
        ).arrange(RIGHT, buff=buff)

    def transition_to_oil_stream(self):
        question = self.hook_question("What controls this density?")
        density = self.density_curve(width=1.65, height=0.95, color=DIFFUSION_GOLD).move_to([0, 0.72, 0])
        oil = self.oil_blob().move_to([0, 0.62, 0])
        streams = self.streamlines(width=10.0, count=8, color=FLOW_BLUE).move_to([0, -0.25, 0])
        particles = self.particle_cloud(40, 0.46, np.array([0, 0.52, 0]), REVERSE_ORANGE, 31, opacity=0.48)
        bridge = self.label("Oil on a slow stream: motion plus spreading.", SUBTITLE_SIZE, FLOW_CYAN, font=FONT_TITLE).to_edge(DOWN, buff=0.52)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(density), run_time=0.9)
        self.play(ReplacementTransform(density, oil), LaggedStart(*[Create(line) for line in streams], lag_ratio=0.06), run_time=1.7)
        self.play(FadeIn(particles), FadeIn(bridge, shift=0.08 * UP), run_time=1.0)
        self.play(particles.animate.shift(0.55 * RIGHT).set_opacity(0.65), oil.animate.shift(0.22 * RIGHT), run_time=2.0)
        self.wait(10.0)
        self.play(FadeOut(Group(question, oil, streams, particles, bridge)), run_time=1.0)
