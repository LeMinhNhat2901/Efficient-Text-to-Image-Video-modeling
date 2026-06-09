from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class MarkovChainScene(DiffusionScene):
    def construct(self):
        title = self.scene_title("Act II: Markov chains", "A long trajectory becomes many local transitions")
        self.play(FadeIn(title, shift=0.2 * DOWN), run_time=MED)

        node_tex = [r"x_0", r"x_1", r"x_2", r"x_{t-1}", r"x_t", r"x_T"]
        nodes = VGroup(*[self.chain_node(tex) for tex in node_tex]).arrange(RIGHT, buff=0.52).move_to([0, 0.9, 0])
        arrows = VGroup(*[self.small_arrow(nodes[i], nodes[i + 1], MUTED) for i in range(len(nodes) - 1)])
        intro = self.label("A Markov chain is a sequence of states connected by probabilistic transitions.", BODY_SIZE, MUTED)
        intro.to_edge(DOWN, buff=0.7)

        self.play(LaggedStart(*[FadeIn(node, scale=0.94) for node in nodes], lag_ratio=0.08), run_time=MED)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.08), FadeIn(intro), run_time=MED)
        self.wait(0.35)

        property_eq = self.display_equation(
            r"p(x_t\mid x_{t-1},x_{t-2},\ldots,x_0)=p(x_t\mid x_{t-1})",
            plain="p(x_t | x_{t-1}, x_{t-2}, ..., x_0) = p(x_t | x_{t-1})",
            width=8.4,
            size=30,
        ).to_edge(DOWN, buff=0.45)
        focus = self.soft_box(width=2.25, height=1.05, color=ACCENT_2, fill_opacity=0.045, stroke_opacity=0.92)
        focus.move_to(VGroup(nodes[3], nodes[4]))
        past = VGroup(nodes[0], nodes[1], nodes[2], arrows[0], arrows[1], arrows[2])
        future = VGroup(nodes[5], arrows[4])
        keep = VGroup(nodes[3], nodes[4], arrows[3])

        self.play(FadeOut(intro), run_time=FAST)
        self.play(
            past.animate.set_opacity(0.18),
            future.animate.set_opacity(0.18),
            Create(focus),
            run_time=MED,
        )
        note = self.label("The distant past is not ignored; it is summarized by the current state.", SMALL_SIZE, MUTED)
        note.next_to(property_eq, UP, buff=0.2)
        self.play(FadeIn(property_eq, shift=0.12 * UP), FadeIn(note), run_time=MED)
        self.wait(0.55)

        factor_eq = self.display_equation(
            r"p(x_{0:T})=p(x_0)\prod_{t=1}^{T}p(x_t\mid x_{t-1})",
            plain="p(x_0:T) = p(x_0) prod_{t=1}^T p(x_t | x_{t-1})",
            width=7.1,
            size=31,
            accent=GREEN,
        ).to_edge(DOWN, buff=0.45)
        transition_pairs = VGroup()
        for i in range(4):
            pair = self.soft_box(width=1.35, height=0.72, color=GREEN, fill_opacity=0.035, stroke_opacity=0.7)
            pair.move_to(VGroup(nodes[i], nodes[i + 1]))
            transition_pairs.add(pair)

        self.play(FadeOut(property_eq), FadeOut(note), FadeOut(focus), run_time=FAST)
        self.play(
            past.animate.set_opacity(1.0),
            future.animate.set_opacity(1.0),
            LaggedStart(*[Create(pair) for pair in transition_pairs], lag_ratio=0.16),
            FadeIn(factor_eq, shift=0.12 * UP),
            run_time=MED,
        )
        self.wait(0.65)
