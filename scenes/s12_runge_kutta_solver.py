from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.part3_common import *


class RungeKuttaSolverScene(Part3Scene):
    TARGET_DURATION = 114.81

    def construct(self):
        start = self.time
        self.p3_background()
        title = self.part3_title(
            "Numerical Solvers",
            "Euler and Runge-Kutta approximate continuous trajectories",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.7)

        self.continuous_vs_computer_steps()
        self.euler_one_step()
        self.rk4_scouts()
        self.three_layer_comparison()
        self.network_provides_field()
        self.hold_to_time(start, self.TARGET_DURATION)

    def exact_curve(self, color: str = TEXT, opacity: float = 0.45) -> ParametricFunction:
        return ParametricFunction(
            lambda t: np.array([
                -4.2 + 8.4 * t,
                -1.0 + 1.45 * np.sin(PI * t) + 0.2 * np.sin(3 * PI * t),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=color,
            stroke_width=4,
            stroke_opacity=opacity,
        )

    def continuous_vs_computer_steps(self):
        question = self.hook_question("Computers cannot take infinitely small steps.")
        curve = self.exact_curve(TEXT, 0.38)
        dot = Dot(curve.point_from_proportion(0.06), radius=0.085, color=REVERSE_ORANGE)
        labels = VGroup(
            self.label("ideal continuous trajectory", SMALL_SIZE, MUTED).next_to(curve, UP, buff=0.25),
            self.label("finite samples only", SMALL_SIZE, REVERSE_ORANGE).to_edge(DOWN, buff=0.55),
        )
        ticks = VGroup(*[Dot(curve.point_from_proportion(t), radius=0.04, color=REVERSE_ORANGE) for t in np.linspace(0.08, 0.92, 8)])

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(curve), FadeIn(dot), FadeIn(labels[0]), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in ticks], lag_ratio=0.08), FadeIn(labels[1]), run_time=1.2)
        self.wait(8.0)
        self.play(FadeOut(Group(question, curve, dot, labels, ticks)), run_time=0.5)

    def euler_one_step(self):
        question = self.hook_question("Euler: one look, one step.")
        curve = self.exact_curve(TEXT, 0.32)
        y0 = curve.point_from_proportion(0.18)
        tangent_end = y0 + np.array([1.18, 0.9, 0])
        euler_end = y0 + np.array([1.65, 1.25, 0])
        true_near = curve.point_from_proportion(0.38)
        arrow = Arrow(y0, tangent_end, buff=0, color=FAIL_RED, stroke_width=4.2)
        step = Line(y0, euler_end, color=FAIL_RED, stroke_width=4)
        error = DashedLine(euler_end, true_near, color=FAIL_RED, stroke_width=2.5, dash_length=0.08)
        ydot = Dot(y0, radius=0.085, color=FAIL_RED)
        new_dot = Dot(euler_end, radius=0.075, color=FAIL_RED)
        eq = self.display_equation(r"y_{n+1}=y_n+h f(t_n,y_n)", width=6.2, size=32, accent=FAIL_RED).to_edge(DOWN, buff=0.52)
        label = self.label("Explicit Euler", SUBTITLE_SIZE, FAIL_RED, font=FONT_TITLE).move_to([-3.15, 1.85, 0])
        note = self.label("If the curve bends, one slope can drift away.", SMALL_SIZE, MUTED).next_to(eq, UP, buff=0.22)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(curve), FadeIn(ydot), FadeIn(label), run_time=1.0)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(Create(step), FadeIn(new_dot), FadeIn(eq), run_time=1.1)
        self.play(Create(error), FadeIn(note), run_time=0.8)
        self.wait(21.5)
        self.play(FadeOut(Group(question, curve, ydot, arrow, step, new_dot, error, eq, label, note)), run_time=0.5)

    def rk4_scouts(self):
        question = self.hook_question("Runge-Kutta sends out several slope scouts.")
        curve = self.exact_curve(TEXT, 0.28)
        base = curve.point_from_proportion(0.22)
        scouts = VGroup(
            Arrow(base, base + np.array([0.7, 0.32, 0]), buff=0, color=FLOW_CYAN, stroke_width=3.2),
            Arrow(base + np.array([0.45, 0.18, 0]), base + np.array([1.12, 0.52, 0]), buff=0, color=GREEN, stroke_width=3.2),
            Arrow(base + np.array([0.54, 0.28, 0]), base + np.array([1.22, 0.72, 0]), buff=0, color=VIOLET, stroke_width=3.2),
            Arrow(base + np.array([1.02, 0.62, 0]), base + np.array([1.62, 1.02, 0]), buff=0, color=FAIL_RED, stroke_width=3.2),
        )
        colors = [FLOW_CYAN, GREEN, VIOLET, FAIL_RED]
        labels = VGroup(*[self.eq(fr"k_{i}", size=25, color=colors[i - 1]).next_to(scouts[i - 1], UP, buff=0.05) for i in range(1, 5)])
        avg = Arrow(base, base + np.array([1.38, 0.74, 0]), buff=0, color=REVERSE_ORANGE, stroke_width=5)
        avg_label = self.label("weighted average", SMALL_SIZE, REVERSE_ORANGE).next_to(avg, DOWN, buff=0.12)
        eq = self.display_equation(
            r"y_{n+1}=y_n+\frac{h}{6}(k_1+2k_2+2k_3+k_4)",
            width=7.7,
            size=31,
            accent=REVERSE_ORANGE,
        ).to_edge(DOWN, buff=0.52)
        side = self.word_row(["start", "middle", "middle", "end"], SMALL_SIZE, MUTED, buff=0.52)
        side.next_to(eq, UP, buff=0.22)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(curve), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in scouts], lag_ratio=0.18), FadeIn(labels), run_time=1.8)
        self.play(GrowArrow(avg), FadeIn(avg_label), FadeIn(eq), FadeIn(side), run_time=1.2)
        self.wait(26.0)
        self.play(FadeOut(Group(question, curve, scouts, labels, avg, avg_label, eq, side)), run_time=0.5)

    def three_layer_comparison(self):
        question = self.hook_question("Euler drifts away. RK4 stays close.")
        exact = self.exact_curve(TEXT, 0.36)
        euler_points = [
            exact.point_from_proportion(0.05),
            np.array([-2.6, -0.1, 0]),
            np.array([-1.1, 1.1, 0]),
            np.array([0.6, 1.85, 0]),
            np.array([2.25, 1.72, 0]),
        ]
        rk_points = [exact.point_from_proportion(t) + np.array([0.04 * np.sin(20 * t), -0.03, 0]) for t in np.linspace(0.05, 0.82, 5)]
        euler = VMobject(color=FAIL_RED, stroke_width=4)
        euler.set_points_as_corners(euler_points)
        rk = VMobject(color=REVERSE_ORANGE, stroke_width=4)
        rk.set_points_smoothly(rk_points)
        e_error = DashedLine(euler_points[-1], exact.point_from_proportion(0.82), color=FAIL_RED, dash_length=0.08)
        rk_error = DashedLine(rk_points[-1], exact.point_from_proportion(0.82), color=REVERSE_ORANGE, dash_length=0.06)
        legend = VGroup(
            self.label("exact", SMALL_SIZE, TEXT),
            self.label("Euler", SMALL_SIZE, FAIL_RED),
            self.label("RK4", SMALL_SIZE, REVERSE_ORANGE),
        ).arrange(RIGHT, buff=0.34).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(Create(exact), run_time=0.9)
        self.play(Create(euler), Create(rk), FadeIn(legend), run_time=2.2)
        self.play(Create(e_error), Create(rk_error), run_time=0.8)
        self.wait(10.0)
        self.play(FadeOut(Group(question, exact, euler, rk, e_error, rk_error, legend)), run_time=0.5)

    def network_provides_field(self):
        question = self.hook_question("The model learns the direction. The solver decides the step.")
        f_eq = self.display_equation(r"f(t,y)", width=2.4, size=35, accent=FLOW_CYAN).move_to([-4.0, 0.85, 0])
        net = self.neural_network_block().scale(1.05).move_to([-1.3, 0.85, 0])
        input_label = self.eq(r"(y,t)", size=30, color=TEXT).next_to(net, LEFT, buff=0.48)
        output = self.display_equation(r"\text{learned score / vector field}", width=4.6, size=25, accent=VIOLET).next_to(net, RIGHT, buff=0.42)
        solver = self.concept_card("Euler / RK4", "finite stepping rule", REVERSE_ORANGE, width=2.9, height=1.1).move_to([1.4, -1.05, 0])
        path = self.dense_curve(REVERSE_ORANGE).scale(0.42).move_to([4.35, -1.05, 0])
        arrows = VGroup(
            Arrow(input_label.get_right(), net.get_left(), buff=0.15, color=FLOW_CYAN, stroke_width=3),
            Arrow(net.get_right(), output.get_left(), buff=0.15, color=VIOLET, stroke_width=3),
            Arrow(output.get_bottom(), solver.get_top(), buff=0.15, color=REVERSE_ORANGE, stroke_width=3),
            Arrow(solver.get_right(), path.get_left(), buff=0.18, color=REVERSE_ORANGE, stroke_width=3),
        )
        sample = Dot(path.point_from_proportion(0.02), radius=0.075, color=REVERSE_ORANGE)
        take = self.takeaway("The model learns geometry. The solver walks it.", REVERSE_ORANGE).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(f_eq), run_time=0.7)
        self.play(FadeTransform(f_eq.copy(), net), FadeOut(f_eq), FadeIn(input_label), GrowArrow(arrows[0]), run_time=1.2)
        self.play(GrowArrow(arrows[1]), FadeIn(output), GrowArrow(arrows[2]), FadeIn(solver), run_time=1.3)
        self.play(GrowArrow(arrows[3]), Create(path), FadeIn(sample), run_time=1.0)
        self.play(MoveAlongPath(sample, path), FadeIn(take), run_time=2.8)
        self.wait(18.4)

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
