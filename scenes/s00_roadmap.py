from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *
from utils.animation_helpers import staggered_fade_in


class RoadmapOverview(DiffusionScene):
    def construct(self):
        title = self.scene_title(
            "Mathematics of Diffusion",
            "A 42-minute path through discrete and continuous views",
        )
        self.play(FadeIn(title, shift=0.22 * DOWN), run_time=MED)

        headers = VGroup(
            self.label("visual", SMALL_SIZE, MUTED).move_to([LEFT_COL_X, 2.48, 0]),
            self.label("concept", SMALL_SIZE, MUTED).move_to([TITLE_COL_X, 2.48, 0]),
            self.label("key math", SMALL_SIZE, MUTED).move_to([EQ_COL_X, 2.48, 0]),
        )
        self.play(FadeIn(headers), run_time=FAST)

        row_specs = [
            ("Forward / backward", r"x_0 \leftrightarrow x_T", "x0 <-> xT"),
            ("OU and Wiener", r"dX_t,\;dW_t", "dX_t, dW_t"),
            ("Markov chain", r"x_0\to x_1\to\cdots", "x0 -> x1 -> ..."),
            ("Markov property", r"p(x_t\mid x_{t-1})", "p(xt | x_{t-1})"),
            ("Reverse chain", r"x_T\to x_{T-1}", "xT -> xT-1"),
            ("Inverse conditionals", r"\mathrm{Bayes}", "Bayes"),
            ("Learning mean", r"\mathbb{E}[Y\mid X]", "E[Y | X]"),
            ("Ito / SDE", r"f\,dt+g\,dW_t", "f dt + g dW_t"),
            ("Fokker-Planck", r"\partial_t p", "partial_t p"),
            ("Failure cases", r"\mathrm{approximation}", "approximation"),
        ]

        rows = VGroup()
        for i, (name, equation, plain) in enumerate(row_specs):
            y = 2.0 - i * 0.56
            if i in (1, 8):
                icon = self.wiener_path(length=0.88, height=0.42, steps=18, seed=20 + i, color=ACCENT_2)
            elif i in (2, 3, 4):
                icon = VGroup(*[Dot(radius=0.035, color=ACCENT) for _ in range(4)]).arrange(RIGHT, buff=0.11)
                icon.add(*[Line(icon[j].get_right(), icon[j + 1].get_left(), color=MUTED, stroke_width=1.5) for j in range(3)])
            else:
                icon = self.noisy_sample(min(0.85, i / 9), scale=0.38, seed=30 + i)
            icon.move_to([LEFT_COL_X, y, 0])

            label = self.label(name, 18, TEXT).move_to([TITLE_COL_X, y, 0]).align_to([TITLE_COL_X - 1.2, y, 0], LEFT)
            eq = self.eq(equation, size=24, plain=plain)
            if eq.width > 3.35:
                eq.scale_to_fit_width(3.35)
            eq.move_to([EQ_COL_X, y, 0]).align_to([EQ_COL_X - 1.58, y, 0], LEFT)
            rows.add(VGroup(icon, label, eq))

        self.play(staggered_fade_in(rows, lag_ratio=0.055, run_time=1.45))

        focus_box = self.soft_box(width=12.4, height=0.45, color=ACCENT, fill_opacity=0.045, stroke_opacity=0.86)
        focus_box.move_to(rows[0])
        self.play(Create(focus_box), run_time=FAST)

        for i, row in enumerate(rows):
            if i > 0:
                self.play(
                    focus_box.animate.move_to(row),
                    rows[i - 1].animate.set_opacity(0.32),
                    row.animate.set_opacity(1.0),
                    run_time=0.22,
                )
            self.wait(0.08)

        closing = self.label("We move from sample paths to probability densities, then back to sampling.", SMALL_SIZE, MUTED)
        closing.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(closing, shift=0.08 * UP), rows.animate.set_opacity(1), FadeOut(focus_box), run_time=MED)
        self.wait(0.35)
