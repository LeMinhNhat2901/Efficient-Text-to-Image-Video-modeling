from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.common.v01_common import *


class FokkerPlanckScoreScene(Part3Scene):
    TARGET_DURATION = 92.0

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "Fokker-Planck and the Score",
            "From sample motion to density flow",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.7)

        self.density_question()
        self.assemble_density_equation()
        self.velocity_reveals_score()
        self.visualize_probability_flow()
        self.hold_to_time(start, self.TARGET_DURATION)

    def density_question(self):
        question = self.hook_question("How does probability density evolve?")
        cloud = self.particle_cloud(120, 0.74, np.array([0, -0.1, 0]), FLOW_CYAN, 19, opacity=0.38)
        curve = self.density_curve(width=1.65, height=1.05, color=DIFFUSION_GOLD).move_to([0, -0.7, 0])
        label_a = self.word_row(["SDE:", "individual", "samples"], SMALL_SIZE, MUTED).move_to([-3.0, -2.35, 0])
        label_b = self.word_row(["Fokker-Planck:", "whole", "density"], SMALL_SIZE, DIFFUSION_GOLD).move_to([3.0, -2.35, 0])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(cloud), FadeIn(label_a), run_time=1.0)
        self.play(cloud.animate.set_opacity(0.16), Create(curve), FadeIn(label_b), run_time=1.5)
        self.wait(8.5)
        self.play(FadeOut(Group(question, cloud, curve, label_a, label_b)), run_time=0.5)

    def assemble_density_equation(self):
        question = self.hook_question("Drift and diffusion assemble into density evolution.")
        drift = self.display_equation(r"-\operatorname{div}(p\alpha)", width=4.35, size=32, accent=FLOW_BLUE).move_to([-3.05, 0.75, 0])
        diffusion = self.display_equation(r"\frac{\beta(t)}{2}\nabla^2p", width=4.35, size=32, accent=DIFFUSION_GOLD).move_to([3.05, 0.75, 0])
        plus = self.eq(r"+", size=42, color=TEXT).move_to([0, 0.75, 0])
        flow_eq = self.display_equation(
            r"\partial_t p=-\operatorname{div}(pv)",
            width=6.2,
            size=35,
            accent=FLOW_CYAN,
        ).move_to([0, -0.75, 0])
        note = self.word_row(
            ["Probability-flow", "view:", "density", "moves", "under", "a", "velocity", "field", "v."],
            SMALL_SIZE,
            MUTED,
            buff=0.09,
        ).to_edge(DOWN, buff=0.55)
        frame = SurroundingRectangle(flow_eq, color=FLOW_CYAN, stroke_width=2.2, buff=0.12)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(drift, shift=0.15 * RIGHT), FadeIn(diffusion, shift=0.15 * LEFT), FadeIn(plus), run_time=1.2)
        self.play(FadeTransform(VGroup(drift.copy(), diffusion.copy(), plus.copy()), flow_eq), run_time=1.2)
        self.play(Create(frame), FadeIn(note), run_time=1.0)
        self.wait(15.5)
        self.play(FadeOut(Group(question, drift, diffusion, plus, flow_eq, frame, note)), run_time=0.5)

    def velocity_reveals_score(self):
        question = self.hook_question("Inside the velocity field, the score returns.")
        main = self.display_equation(r"\partial_t p=-\operatorname{div}(pv)", width=6.0, size=34, accent=FLOW_CYAN).to_edge(UP, buff=1.1)
        v_eq = MathTex(
            r"v(x,t)",
            r"=",
            r"\alpha(x,t)",
            r"-",
            r"\frac{\beta(t)}{2}",
            r"\nabla\log p(x,t)",
            font_size=36,
            color=TEXT,
        ).move_to([0, -0.1, 0])
        v_eq[2].set_color(FLOW_BLUE)
        v_eq[4].set_color(DIFFUSION_GOLD)
        v_eq[5].set_color(SCORE_PINK)
        score_box = SurroundingRectangle(v_eq[5], color=SCORE_PINK, buff=0.08, stroke_width=2.5)
        compass = VGroup(
            Circle(radius=0.32, stroke_color=FLOW_CYAN, stroke_width=2.2),
            Arrow(ORIGIN, 0.28 * UR, buff=0, color=SCORE_PINK, stroke_width=4, max_tip_length_to_length_ratio=0.35),
        ).move_to([0, -1.25, 0])
        pulse = self.glow(compass.get_center(), SCORE_PINK, rings=5)
        note = self.takeaway("Score returns as part of the continuous flow.", SCORE_PINK).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(main), run_time=0.8)
        self.play(Write(v_eq), run_time=2.0)
        self.play(Create(score_box), Create(compass), Create(pulse), run_time=1.0)
        self.play(FadeOut(pulse), FadeIn(note, shift=0.08 * UP), run_time=0.9)
        self.wait(17.0)
        self.play(FadeOut(Group(question, main, v_eq, score_box, compass, note)), run_time=0.5)

    def visualize_probability_flow(self):
        question = self.hook_question("Fokker-Planck tells us how the whole cloud flows.")
        cloud = self.particle_cloud(100, 0.92, np.array([0, -0.05, 0]), DIFFUSION_GOLD, 41, opacity=0.32)
        contours = VGroup(
            Ellipse(width=5.2, height=2.3, stroke_color=TEXT, stroke_opacity=0.18),
            Ellipse(width=3.8, height=1.55, stroke_color=TEXT, stroke_opacity=0.28),
            Ellipse(width=2.2, height=0.9, stroke_color=DIFFUSION_GOLD, stroke_opacity=0.42),
        ).move_to([0, -0.08, 0])
        field = self.vector_field_arrows(center=ORIGIN, x_span=3.3, y_span=1.55, color=FLOW_CYAN, inward=False, opacity=0.72)
        paths, dots = self.brownian_paths(np.array([-3.2, -0.55, 0]), count=9, seed=101, color=FLOW_CYAN)
        time = VGroup(
            self.label("Forward time", SMALL_SIZE, FLOW_BLUE),
            self.eq(r"0\rightarrow 1", size=30, color=FLOW_BLUE),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.55)
        reverse = VGroup(
            self.label("Reverse?", SMALL_SIZE, REVERSE_ORANGE),
            self.eq(r"1\rightarrow 0", size=30, color=REVERSE_ORANGE),
        ).arrange(RIGHT, buff=0.18).move_to(time)

        self.play(
            FadeIn(question, shift=0.12 * DOWN),
            FadeIn(cloud),
            Create(contours),
            LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.02),
            run_time=1.8,
        )
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.04), FadeIn(dots), run_time=2.0)
        self.play(FadeIn(time), run_time=0.8)
        self.wait(11.5)
        self.play(Transform(time, reverse), field.animate.set_opacity(0.25), run_time=1.1)
        self.wait(14.1)

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
