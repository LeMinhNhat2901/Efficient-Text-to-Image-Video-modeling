from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.common.v01_common import *


class DriftDiffusionScene(Part3Scene):
    TARGET_DURATION = 98.69

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "Oil Slick: Drift and Diffusion",
            "One force moves probability, the other spreads it",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.7)

        self.split_screen_setup()
        self.drift_only()
        self.pure_diffusion()
        self.merge_ito_process()
        self.hold_to_time(start, self.TARGET_DURATION)

    def split_screen_setup(self):
        question = self.hook_question("A density changes because it moves and because it spreads.")
        divider = Line(UP * 2.75, DOWN * 2.75, color=DIM, stroke_width=1.4)
        left_title = self.label("Drift only", SUBTITLE_SIZE, FLOW_BLUE, font=FONT_TITLE).move_to([-3.45, 2.15, 0])
        right_title = self.label("Pure diffusion", SUBTITLE_SIZE, DIFFUSION_GOLD, font=FONT_TITLE).move_to([3.45, 2.15, 0])
        left_blob = self.oil_blob().scale(0.72).move_to([-3.45, 0.2, 0])
        right_blob = self.oil_blob().scale(0.72).move_to([3.45, 0.2, 0])
        move_label = self.label("moves", SMALL_SIZE, FLOW_BLUE).move_to([-3.45, -1.65, 0])
        spread_label = self.label("spreads", SMALL_SIZE, DIFFUSION_GOLD).move_to([3.45, -1.65, 0])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), FadeIn(left_blob), FadeIn(right_blob), run_time=1.2)
        self.play(FadeIn(move_label), FadeIn(spread_label), run_time=0.8)
        self.wait(5.0)
        self.play(FadeOut(Group(question, divider, left_title, right_title, left_blob, right_blob, move_label, spread_label)), run_time=0.35)

    def drift_only(self):
        question = self.hook_question("Drift is deterministic transport.")
        panel = self.soft_box(5.9, 4.4, color=FLOW_BLUE, fill_opacity=0.025, stroke_opacity=0.45).move_to([-3.1, -0.12, 0])
        title = self.label("Drift only", SUBTITLE_SIZE, FLOW_BLUE, font=FONT_TITLE).next_to(panel, UP, buff=0.16)
        field = self.vector_field_arrows(center=np.array([-3.1, 0.0, 0]), x_span=2.35, y_span=1.25, color=FLOW_BLUE)
        particles = self.particle_cloud(36, 0.34, np.array([-4.4, -0.15, 0]), FLOW_CYAN, 3, opacity=0.72)
        targets = particles.copy()
        for dot in targets:
            x, y, _ = dot.get_center()
            dot.move_to(np.array([-2.1 + 0.12 * np.sin(3 * y), 0.55 * y, 0]))
        eq = self.display_equation(r"dX=\alpha(x,t)\,dt", width=4.2, size=32, accent=FLOW_BLUE).move_to([2.7, 0.95, 0])
        density_term = self.display_equation(
            r"\partial_t p=-\operatorname{div}(p\alpha)",
            width=5.4,
            size=31,
            accent=FLOW_BLUE,
        ).move_to([2.6, -0.6, 0])
        note = self.word_row(["compression", "accumulates", "mass;", "expansion", "spreads", "it"], SMALL_SIZE, MUTED)
        note.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(panel), FadeIn(title), LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.025), FadeIn(particles), run_time=1.7)
        self.play(Transform(particles, targets), FadeIn(eq), run_time=2.0)
        self.play(FadeIn(density_term, shift=0.08 * UP), FadeIn(note), run_time=1.0)
        self.wait(15.2)
        self.play(FadeOut(Group(question, panel, title, field, particles, eq, density_term, note)), run_time=0.35)

    def pure_diffusion(self):
        question = self.hook_question("Pure diffusion spreads without a guiding flow.")
        panel = self.soft_box(5.9, 4.4, color=DIFFUSION_GOLD, fill_opacity=0.025, stroke_opacity=0.45).move_to([3.1, -0.12, 0])
        title = self.label("Pure diffusion", SUBTITLE_SIZE, DIFFUSION_GOLD, font=FONT_TITLE).next_to(panel, UP, buff=0.16)
        cloud_1 = self.particle_cloud(54, 0.22, np.array([3.1, -0.05, 0]), DIFFUSION_GOLD, 5, opacity=0.74)
        cloud_2 = self.particle_cloud(54, 0.62, np.array([3.1, -0.05, 0]), DIFFUSION_GOLD, 6, opacity=0.58)
        cloud_3 = self.particle_cloud(54, 0.96, np.array([3.1, -0.05, 0]), DIFFUSION_GOLD, 7, opacity=0.44)
        curve_1 = self.density_curve(width=0.72, height=1.2, color=DIFFUSION_GOLD).scale(0.62).move_to([-2.65, -0.4, 0])
        curve_2 = self.density_curve(width=1.75, height=0.72, color=DIFFUSION_GOLD).scale(0.62).move_to([-2.65, -0.4, 0])
        eq = self.display_equation(r"dX=\sqrt{\beta(t)}\,dW", width=4.6, size=32, accent=DIFFUSION_GOLD).move_to([-2.65, 1.0, 0])
        density_term = self.display_equation(
            r"\partial_t p=\frac{\beta(t)}{2}\nabla^2p",
            width=5.2,
            size=31,
            accent=DIFFUSION_GOLD,
        ).move_to([-2.65, -1.4, 0])
        note = self.word_row(["random", "motion", "spreads", "the", "cloud", "outward"], SMALL_SIZE, MUTED)
        note.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(panel), FadeIn(title), FadeIn(cloud_1), Create(curve_1), run_time=1.2)
        self.play(Transform(cloud_1, cloud_2), Transform(curve_1, curve_2), FadeIn(eq), run_time=1.8)
        self.play(Transform(cloud_1, cloud_3), run_time=1.4)
        self.play(FadeIn(density_term), FadeIn(note), run_time=1.0)
        self.wait(14.8)
        self.play(FadeOut(Group(question, panel, title, cloud_1, curve_1, eq, density_term, note)), run_time=0.35)

    def merge_ito_process(self):
        question = self.hook_question("Drift plus diffusion gives an Ito process.")
        left_field = self.vector_field_arrows(center=np.array([-2.7, 0.25, 0]), x_span=1.7, y_span=1.0, color=FLOW_BLUE)
        right_cloud = self.particle_cloud(46, 0.64, np.array([2.7, 0.25, 0]), DIFFUSION_GOLD, 22, opacity=0.48)
        combo_field = self.vector_field_arrows(center=np.array([0, -0.38, 0]), x_span=3.15, y_span=0.95, color=FLOW_CYAN, spread=False)
        noisy_paths, endpoints = self.brownian_paths(np.array([-3.0, -0.75, 0]), count=14, seed=88, color=DIFFUSION_GOLD)
        eq_left = self.eq(r"\alpha(x,t)\,dt", size=34, color=FLOW_BLUE).move_to([-2.6, 1.7, 0])
        eq_right = self.eq(r"\sqrt{\beta(t)}\,dW", size=34, color=DIFFUSION_GOLD).move_to([2.6, 1.7, 0])
        full = self.display_equation(
            r"dX=\alpha(x,t)\,dt+\sqrt{\beta(t)}\,dW",
            width=8.1,
            size=35,
            accent=REVERSE_ORANGE,
        ).move_to([0, 1.55, 0])
        full.set_z_index(20)
        label = self.word_row(["Drift", "+", "Diffusion", "=", "Ito", "process"], SUBTITLE_SIZE, REVERSE_ORANGE, font=FONT_TITLE, buff=0.12)
        label.to_edge(DOWN, buff=0.54)
        bridge = self.word_row(["How", "does", "the", "whole", "density", "move?"], SMALL_SIZE, MUTED)
        bridge.next_to(label, UP, buff=0.2)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in left_field], lag_ratio=0.03), FadeIn(right_cloud), FadeIn(eq_left), FadeIn(eq_right), run_time=1.6)
        self.play(FadeOut(eq_left), FadeOut(eq_right), FadeIn(full, shift=0.08 * DOWN), FadeIn(combo_field), run_time=1.3)
        self.play(LaggedStart(*[Create(path) for path in noisy_paths], lag_ratio=0.04), FadeIn(endpoints), FadeIn(label), run_time=2.3)
        self.play(FadeIn(bridge), run_time=0.9)
        self.wait(32.75)

    def word_row(
        self,
        words: list[str],
        size: int = SMALL_SIZE,
        color: str = MUTED,
        font: str | None = None,
        weight: str = NORMAL,
        buff: float = 0.095,
    ) -> VGroup:
        return VGroup(
            *[
                Text(
                    word,
                    font=font or FONT_SUBTITLE,
                    font_size=size,
                    color=color,
                    weight=weight,
                    disable_ligatures=True,
                )
                for word in words
            ]
        ).arrange(RIGHT, buff=buff)
