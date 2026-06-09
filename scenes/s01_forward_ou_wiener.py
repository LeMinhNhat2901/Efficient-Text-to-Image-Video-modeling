from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class ForwardOUWiener(DiffusionScene):
    def construct(self):
        title = self.scene_title("Act I: Forward, backward, OU, Wiener", "The first picture: data becomes noise, then we learn the way back")
        self.play(FadeIn(title, shift=0.2 * DOWN), run_time=MED)

        self.big_picture()
        self.ou_process()
        self.wiener_process()
        self.forward_backward_bridge()

    def big_picture(self):
        tag = self.top_left_tag("Forward / backward", ACCENT)
        forward = VGroup(
            self.noisy_sample(0.0, scale=0.82, seed=1),
            self.noisy_sample(0.45, scale=0.82, seed=2),
            self.gaussian_cloud(count=90, width=1.2, height=1.0, seed=3),
        ).arrange(RIGHT, buff=0.58).move_to([-3.45, 0.88, 0])
        reverse = VGroup(
            self.gaussian_cloud(count=90, width=1.2, height=1.0, seed=4, color=GREEN),
            self.noisy_sample(0.45, scale=0.82, seed=5),
            self.noisy_sample(0.0, scale=0.82, seed=6),
        ).arrange(RIGHT, buff=0.58).move_to([3.45, 0.88, 0])

        labels = VGroup(
            self.label("known forward process", SMALL_SIZE, ACCENT).next_to(forward, UP, buff=0.32),
            self.label("learned backward process", SMALL_SIZE, GREEN).next_to(reverse, UP, buff=0.32),
        )
        arrows = VGroup(
            *[self.small_arrow(forward[i], forward[i + 1], ACCENT) for i in range(2)],
            *[self.small_arrow(reverse[i], reverse[i + 1], GREEN) for i in range(2)],
        )
        eq = self.display_equation(
            r"\mathbf{x}_0 \rightarrow \mathbf{x}_T \sim \mathcal{N}(\mathbf{0},\mathbf{I})",
            plain="x0 -> xT ~ N(0, I)",
            width=5.8,
            size=30,
        ).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tag), FadeIn(labels), run_time=FAST)
        self.play(FadeIn(forward[0]), FadeIn(reverse[0]), run_time=FAST)
        for pair_index in range(2):
            self.play(
                GrowArrow(arrows[pair_index]),
                FadeIn(forward[pair_index + 1], scale=0.96),
                GrowArrow(arrows[pair_index + 2]),
                FadeIn(reverse[pair_index + 1], scale=0.96),
                run_time=MED,
            )
        self.play(FadeIn(eq, shift=0.12 * UP), run_time=MED)
        self.wait(0.45)
        self.play(FadeOut(VGroup(tag, forward, reverse, labels, arrows, eq)), run_time=MED)

    def ou_process(self):
        tag = self.top_left_tag("Ornstein-Uhlenbeck", ACCENT_2)
        axis = NumberLine(x_range=[-3, 3, 1], length=7.2, color=MUTED).move_to([0, 0.1, 0])
        center = Dot(axis.n2p(0), color=ACCENT_2)
        particle = Dot(axis.n2p(2.35), radius=0.085, color=TEXT)
        pull_arrow = always_redraw(lambda: Arrow(particle.get_center(), center.get_center(), buff=0.16, color=ACCENT_2, stroke_width=4))
        jitter = self.wiener_path(length=6.2, height=0.85, steps=70, seed=12, color=VIOLET).shift(1.25 * DOWN)
        eq = self.display_equation(
            r"dX_t=-\lambda X_t\,dt+\sigma\,dW_t",
            plain="dX_t = -lambda X_t dt + sigma dW_t",
            width=5.4,
            size=32,
            accent=ACCENT_2,
        ).to_edge(DOWN, buff=0.45)
        notes = VGroup(
            self.label("mean reversion", SMALL_SIZE, ACCENT_2),
            self.label("random forcing", SMALL_SIZE, VIOLET),
        ).arrange(RIGHT, buff=1.4).next_to(axis, UP, buff=0.55)

        self.play(FadeIn(tag), Create(axis), FadeIn(center), FadeIn(particle), GrowArrow(pull_arrow), FadeIn(notes), run_time=MED)
        self.play(particle.animate.move_to(axis.n2p(1.35)), Create(jitter), run_time=SLOW)
        self.play(particle.animate.move_to(axis.n2p(0.42)), run_time=MED)
        self.play(FadeIn(eq, shift=0.12 * UP), run_time=MED)
        self.wait(0.4)
        self.play(FadeOut(VGroup(tag, axis, center, particle, pull_arrow, jitter, eq, notes)), run_time=MED)

    def wiener_process(self):
        tag = self.top_left_tag("Wiener process", VIOLET)
        axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1.4, 1.4, 0.7],
            x_length=7.6,
            y_length=3.2,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 1.5},
        ).move_to([0, 0.2, 0])
        paths = VGroup()
        for i, color in enumerate([ACCENT, ACCENT_2, GREEN, VIOLET]):
            path = self.wiener_path(length=7.0, height=2.55, steps=70, seed=50 + i, color=color)
            path.move_to(axes.get_center()).shift(0.02 * i * UP)
            paths.add(path)
        labels = VGroup(
            self.label("W_0 = 0", SMALL_SIZE, TEXT).next_to(axes, LEFT, buff=0.25).shift(1.3 * UP),
            self.label("continuous-time noise source", SMALL_SIZE, MUTED).next_to(axes, DOWN, buff=0.22),
        )

        self.play(FadeIn(tag), Create(axes), FadeIn(labels), run_time=MED)
        self.play(LaggedStart(*[Create(path) for path in paths], lag_ratio=0.18), run_time=1.65)
        self.wait(0.35)
        self.play(FadeOut(VGroup(tag, axes, paths, labels)), run_time=MED)

    def forward_backward_bridge(self):
        tag = self.top_left_tag("Bridge to Markov chains", GREEN)
        left = self.soft_box(4.2, 1.45, color=ACCENT, fill_opacity=0.08).shift(2.65 * LEFT)
        right = self.soft_box(4.2, 1.45, color=GREEN, fill_opacity=0.08).shift(2.65 * RIGHT)
        left_text = VGroup(
            self.label("Forward process", SUBTITLE_SIZE, ACCENT),
            self.label("designed and known", SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.16).move_to(left)
        right_text = VGroup(
            self.label("Backward process", SUBTITLE_SIZE, GREEN),
            self.label("learned step by step", SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.16).move_to(right)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.32, color=TEXT, stroke_width=4)
        question = self.label("Why can both directions be handled one transition at a time?", BODY_SIZE, TEXT).to_edge(DOWN, buff=0.75)

        self.play(FadeIn(tag), FadeIn(left), FadeIn(right), FadeIn(left_text), FadeIn(right_text), GrowArrow(arrow), run_time=MED)
        self.play(FadeIn(question, shift=0.12 * UP), run_time=MED)
        self.wait(0.6)
        self.play(FadeOut(VGroup(tag, left, right, left_text, right_text, arrow, question)), run_time=MED)
