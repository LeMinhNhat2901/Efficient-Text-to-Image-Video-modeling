from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.part3_common import *


class ReverseDistributionScene(Part3Scene):
    TARGET_DURATION = 88.9

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "Reverse in Distribution",
            "The model reverses probability, not physical time",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.7)

        self.forward_spreads_out()
        self.pause_and_reveal_score()
        self.reverse_field_inward()
        self.reverse_of_reverse()
        self.hold_to_time(start, self.TARGET_DURATION)

    def forward_spreads_out(self):
        question = self.hook_question("Forward process: data to noise")
        data = self.particle_cloud(80, 0.32, np.array([0, 0.0, 0]), FLOW_CYAN, 11, opacity=0.72)
        noise = self.particle_cloud(80, 1.15, np.array([0, 0.0, 0]), FLOW_CYAN, 12, opacity=0.34)
        field = self.vector_field_arrows(center=ORIGIN, x_span=3.2, y_span=1.55, color=FLOW_BLUE, spread=True, opacity=0.65)
        label = self.word_row(["Forward", "process:", "data", "->", "noise"], SUBTITLE_SIZE, FLOW_BLUE, font=FONT_TITLE).to_edge(DOWN, buff=0.55)
        curve_a = self.density_curve(width=0.72, height=1.25, color=DIFFUSION_GOLD).move_to([0, -1.0, 0])
        curve_b = self.density_curve(width=1.85, height=0.72, color=DIFFUSION_GOLD).move_to([0, -1.0, 0])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(data), LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.02), Create(curve_a), FadeIn(label), run_time=1.6)
        self.play(Transform(data, noise), Transform(curve_a, curve_b), run_time=2.2)
        self.wait(5.8)
        self.play(FadeOut(Group(question, data, field, label, curve_a)), run_time=0.5)

    def pause_and_reveal_score(self):
        question = self.hook_question("Freeze time. What could make the density go backward?")
        cloud = self.particle_cloud(90, 1.1, np.array([0, -0.05, 0]), MUTED, 18, opacity=0.28)
        score_arrows = self.vector_field_arrows(center=ORIGIN, x_span=3.1, y_span=1.5, color=SCORE_PINK, inward=True, opacity=0.82)
        text = self.word_row(["Reverse", "in", "distribution"], SECTION_SIZE, REVERSE_ORANGE, font=FONT_TITLE, buff=0.16).move_to([0, 1.85, 0])
        note = self.word_row(["Not", "a", "perfect", "physical", "rewind", "of", "each", "sample", "path."], SMALL_SIZE, MUTED).to_edge(DOWN, buff=0.55)
        citation = self.label("Time reversal viewpoint: Anderson, 1982", SMALL_SIZE, DIM).next_to(note, UP, buff=0.2)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(cloud), run_time=0.8)
        self.play(cloud.animate.set_opacity(0.16), FadeIn(text), LaggedStart(*[GrowArrow(a) for a in score_arrows], lag_ratio=0.025), run_time=1.8)
        self.play(FadeIn(note), FadeIn(citation), run_time=0.9)
        self.wait(11.0)
        self.play(FadeOut(Group(question, cloud, score_arrows, text, note, citation)), run_time=0.5)

    def reverse_field_inward(self):
        question = self.hook_question("The score bends the reverse flow toward structure.")
        forward = self.vector_field_arrows(center=ORIGIN, x_span=3.1, y_span=1.5, color=FLOW_BLUE, spread=True, opacity=0.35)
        reverse = self.vector_field_arrows(center=ORIGIN, x_span=3.1, y_span=1.5, color=REVERSE_ORANGE, inward=True, opacity=0.86)
        cloud = self.particle_cloud(78, 1.08, np.array([0, -0.15, 0]), DIFFUSION_GOLD, 33, opacity=0.42)
        target = self.particle_cloud(78, 0.42, np.array([0, -0.15, 0]), REVERSE_ORANGE, 34, opacity=0.7)
        eq = self.display_equation(
            r"d\bar X=\left[\cdots-\beta\nabla\log p\right]dt+\sqrt{\beta}\,d\bar W",
            width=8.5,
            size=30,
            accent=REVERSE_ORANGE,
        ).to_edge(DOWN, buff=0.52)
        theorem_box = self.soft_box(4.35, 0.96, color=SCORE_PINK, fill_opacity=0.055, stroke_opacity=0.58)
        theorem_title = self.word_row(["Anderson", "1982"], SMALL_SIZE, SCORE_PINK, font=FONT_BODY, weight=BOLD)
        theorem_body = self.word_row(["reverse", "exists", "in", "distribution"], SMALL_SIZE, TEXT, buff=0.09)
        theorem = VGroup(theorem_box, VGroup(theorem_title, theorem_body).arrange(DOWN, buff=0.12).move_to(theorem_box))
        theorem.move_to([2.45, 1.55, 0])
        label = self.word_row(["score-dependent", "force"], SMALL_SIZE, SCORE_PINK, buff=0.1).next_to(theorem, DOWN, buff=0.14)
        theorem.set_z_index(20)
        label.set_z_index(21)
        eq.set_z_index(20)

        self.play(
            FadeIn(question, shift=0.12 * DOWN),
            LaggedStart(*[GrowArrow(a) for a in forward], lag_ratio=0.02),
            FadeIn(cloud),
            run_time=1.4,
        )
        self.play(forward.animate.set_opacity(0.14), LaggedStart(*[GrowArrow(a) for a in reverse], lag_ratio=0.02), FadeIn(theorem), FadeIn(label), run_time=1.8)
        self.play(Transform(cloud, target), FadeIn(eq), run_time=2.0)
        self.wait(25.7)
        self.play(FadeOut(Group(question, forward, reverse, cloud, eq, theorem, label)), run_time=0.5)

    def reverse_of_reverse(self):
        question = self.hook_question("Learned breadcrumbs guide probability back to structure.")
        noise = self.particle_cloud(90, 0.9, np.array([-3.05, 0.0, 0]), MUTED, 51, opacity=0.26)
        structure = self.particle_cloud(90, 0.34, np.array([3.05, 0.0, 0]), REVERSE_ORANGE, 52, opacity=0.68)
        structure_contours = VGroup(
            Ellipse(width=2.0, height=1.0, stroke_color=REVERSE_ORANGE, stroke_opacity=0.36),
            Ellipse(width=1.25, height=0.58, stroke_color=DIFFUSION_GOLD, stroke_opacity=0.46),
        ).move_to([3.05, 0.0, 0])
        path = VMobject(color=REVERSE_ORANGE, stroke_width=4.0, stroke_opacity=0.9)
        points = [
            np.array([-3.15, -0.1, 0]),
            np.array([-2.05, 0.55, 0]),
            np.array([-0.72, -0.32, 0]),
            np.array([0.68, 0.28, 0]),
            np.array([1.85, -0.22, 0]),
            np.array([3.0, 0.05, 0]),
        ]
        path.set_points_smoothly(points)
        crumbs = VGroup(*[Dot(p, radius=0.06, color=DIFFUSION_GOLD) for p in points[1:-1]])
        traveler = Dot(points[0], radius=0.09, color=REVERSE_ORANGE)
        arrows = VGroup(
            *[
                Arrow(points[i], points[i + 1], buff=0.12, color=REVERSE_ORANGE, stroke_width=2.8, max_tip_length_to_length_ratio=0.18)
                for i in range(len(points) - 1)
            ]
        )
        note = self.word_row(["One", "tiny", "motion", "at", "a", "time,", "the", "cloud", "returns", "toward", "structure."], SMALL_SIZE, MUTED)
        note.to_edge(DOWN, buff=0.55)
        take = self.takeaway("Reverse is a learned distributional flow.", REVERSE_ORANGE).next_to(note, UP, buff=0.22)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(noise), FadeIn(structure_contours), FadeIn(structure), run_time=1.1)
        self.play(Create(path), LaggedStart(*[FadeIn(c, scale=0.7) for c in crumbs], lag_ratio=0.12), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), FadeIn(take), run_time=1.2)
        self.play(MoveAlongPath(traveler, path), FadeIn(note), run_time=2.8)
        self.wait(19.8)

    def word_row(
        self,
        words: list[str],
        size: int,
        color: str,
        font: str = FONT_BODY,
        weight=NORMAL,
        buff: float = 0.1,
    ) -> VGroup:
        row = VGroup(*[Text(word, font=font, font_size=size, color=color, weight=weight) for word in words])
        row.arrange(RIGHT, buff=buff)
        return row
