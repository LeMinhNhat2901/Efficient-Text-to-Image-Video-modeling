from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.common.v01_common import *


class FinaleFailureScene(Part3Scene):
    TARGET_DURATION = 113.68

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "Failure Cases and the Whole Picture",
            "Diffusion learns a probabilistic path, not magic",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(1.4)
        self.play(FadeOut(title), run_time=0.6)

        self.successful_sampling()
        self.wrong_score_failure()
        self.final_synthesis()
        self.hold_to_time(start, self.TARGET_DURATION)

    def successful_sampling(self):
        question = self.hook_question("Successful reverse path")
        noise = self.particle_cloud(95, 0.85, np.array([3.6, 0.55, 0]), DIFFUSION_GOLD, 71, opacity=0.42)
        data_path = self.first_asset("images/clean_sample.png", "images/clean_sample.jpg", "puppy.jpg")
        if data_path is not None:
            data = self.framed_image(data_path, width=1.15, height=0.85, color=FLOW_CYAN, fill_opacity=0.02)
        else:
            data = self.clean_sample(scale=0.72, color=FLOW_CYAN)
        data.move_to([-3.75, 0.55, 0])
        nodes, arrows, curve = self.breadcrumb_path(reverse=True, color=REVERSE_ORANGE)
        nodes.scale(0.78).move_to([0, -0.75, 0])
        arrows = VGroup(*[Arrow(nodes[i].get_center(), nodes[i + 1].get_center(), buff=0.11, color=REVERSE_ORANGE, stroke_width=2.5) for i in range(len(nodes) - 1)])
        label = self.word_row(["noise", "->", "cleaner", "->", "structure"], SMALL_SIZE, REVERSE_ORANGE).to_edge(DOWN, buff=0.55)
        magic = self.takeaway("When it works, noise becomes structure.", FLOW_CYAN).next_to(label, UP, buff=0.22)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.7)
        self.play(FadeIn(noise), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.35) for dot in nodes], lag_ratio=0.05), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), FadeIn(data), FadeIn(label), run_time=1.8)
        self.play(FadeIn(magic, shift=0.06 * UP), run_time=0.7)
        self.wait(16.0)
        self.play(FadeOut(Group(question, noise, data, nodes, arrows, label, magic)), run_time=0.45)

    def wrong_score_failure(self):
        question = self.hook_question("Failure case: wrong learned direction")
        good_path = self.dense_curve(REVERSE_ORANGE).scale(0.55).move_to([-2.4, 0.35, 0])
        bad_path = self.dense_curve(REVERSE_ORANGE).scale(0.55).move_to([2.25, 0.35, 0])
        bad_step_start = bad_path.point_from_proportion(0.46)
        wrong_arrow = Arrow(bad_step_start, bad_step_start + np.array([0.72, -0.82, 0]), buff=0, color=FAIL_RED, stroke_width=4.5)
        dot = Dot(bad_path.point_from_proportion(0.05), radius=0.08, color=FAIL_RED)
        distorted = self.distorted_sample().scale(0.9).move_to([4.4, -1.25, 0])
        region = Ellipse(width=2.2, height=1.05, stroke_color=DIFFUSION_GOLD, stroke_opacity=0.45, fill_color=DIFFUSION_GOLD, fill_opacity=0.06).move_to([2.25, 0.35, 0])
        note = self.word_row(["A", "precise", "solver", "can", "faithfully", "follow", "a", "bad", "compass."], SMALL_SIZE, FAIL_RED)
        note.to_edge(DOWN, buff=0.55)
        terrain = self.word_row(["safe", "probability", "terrain"], SMALL_SIZE, DIFFUSION_GOLD).move_to([2.25, 1.16, 0])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.7)
        self.play(Create(good_path), Create(region), Create(bad_path), FadeIn(dot), FadeIn(terrain), run_time=1.0)
        self.play(MoveAlongPath(dot, bad_path), run_time=1.6)
        self.play(GrowArrow(wrong_arrow), dot.animate.move_to(wrong_arrow.get_end()), bad_path.animate.set_color(FAIL_RED).set_opacity(0.55), run_time=1.0)
        self.play(FadeIn(distorted, scale=0.94), FadeIn(note), run_time=0.8)
        self.wait(26.0)
        self.play(FadeOut(Group(question, good_path, region, bad_path, dot, wrong_arrow, distorted, note, terrain)), run_time=0.45)

    def final_synthesis(self):
        question = self.hook_question("Mathematics of Diffusion")
        cards = VGroup(
            self.recap_card("Markov chains", r"x_0\rightarrow x_T", FLOW_BLUE, width=2.55),
            self.recap_card("Score", r"\nabla\log p", SCORE_PINK, width=2.1),
            self.recap_card("MSE / network", r"\mu_\theta", VIOLET, width=2.55),
            self.recap_card("Ito process", r"dX=\alpha\,dt+\sqrt{\beta}\,dW", DIFFUSION_GOLD, width=2.85, body_size=20),
            self.recap_card("Fokker-Planck", r"\partial_t p=-\operatorname{div}(pv)", FLOW_CYAN, width=2.7, body_size=20),
            self.recap_card("Solver", r"\mathrm{Euler}\,/\,\mathrm{RK4}", REVERSE_ORANGE, width=2.1, body_size=21),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.32)).move_to([0, 0.35, 0])
        final_title = self.label("Mathematics of Diffusion", TITLE_SIZE, TEXT, font=FONT_TITLE)
        subtitle = self.label("From noise to structure, through probability.", SUBTITLE_SIZE, MUTED)
        end = VGroup(final_title, subtitle).arrange(DOWN, buff=0.18).move_to([0, 0.3, 0])
        tag = self.takeaway("Forward is designed. Reverse is learned. Probability shows the way.", REVERSE_ORANGE).to_edge(DOWN, buff=0.45)
        end_screen = self.label("The End", SECTION_SIZE, TEXT, font=FONT_TITLE).move_to([0, 1.65, 0])
        idea = self.word_row(["Structure", "can", "be", "recovered", "by", "following", "probability", "geometry."], SMALL_SIZE, FLOW_CYAN)
        idea.next_to(cards, DOWN, buff=0.28)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(card, shift=0.06 * UP) for card in cards], lag_ratio=0.08), run_time=1.5)
        self.play(FadeIn(idea, shift=0.06 * UP), run_time=0.8)
        self.wait(22.0)
        self.play(FadeOut(question), FadeOut(idea), FadeTransform(cards, end), run_time=1.3)
        self.play(FadeIn(tag, shift=0.08 * UP), FadeIn(end_screen), run_time=0.9)
        self.wait(25.6)

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

    def recap_card(
        self,
        title: str,
        tex: str,
        color: str,
        width: float,
        height: float = 0.92,
        body_size: int = 22,
    ) -> VGroup:
        box = self.soft_box(width, height, color=color, fill_opacity=0.055, stroke_opacity=0.58)
        title_mob = self.label(title, SMALL_SIZE, color, font=FONT_TITLE)
        body = self.eq(tex, size=body_size, color=TEXT)
        self.fit_to_box(title_mob, width - 0.34, 0.28)
        self.fit_to_box(body, width - 0.38, 0.34)
        content = VGroup(title_mob, body).arrange(DOWN, buff=0.08).move_to(box)
        return VGroup(box, content)
