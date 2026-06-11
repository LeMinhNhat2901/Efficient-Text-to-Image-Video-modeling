from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class ReverseMarkovChain(DiffusionScene):
    TARGET_DURATION = 148.99

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "Telescoping and the Reverse Probability",
            "The moment we rewrite the arrow of time",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(title), run_time=0.8)

        self.reverse_chain_question()
        self.bayes_rewrite()
        self.telescoping_expansion()
        self.final_reverse_markov()
        self.hold_to_time(start, self.TARGET_DURATION)

    def reverse_chain_question(self):
        nodes = VGroup(*[self.chain_node(tex, color=ACCENT) for tex in [r"x_0", r"x_1", r"\cdots", r"x_{T-1}", r"x_T"]])
        nodes.arrange(RIGHT, buff=0.62).move_to([0, 1.1, 0])
        forward_arrows = VGroup(*[self.small_arrow(nodes[i], nodes[i + 1], ACCENT) for i in range(len(nodes) - 1)])
        reverse_arrows = VGroup(
            *[
                Arrow(
                    nodes[i + 1].get_left(),
                    nodes[i].get_right(),
                    buff=0.08,
                    color=ACCENT_2,
                    stroke_width=3.0,
                    max_tip_length_to_length_ratio=0.18,
                )
                for i in range(len(nodes) - 1)
            ]
        )
        question = self.hook_question("Does a Markov Chain have a reverse?")
        cloud = self.gaussian_cloud(count=100, width=1.1, height=0.8, seed=111, color=ACCENT_2).move_to(nodes[-1].get_center() + 1.35 * DOWN)
        data_path = self.first_asset("images/clean_sample.png", "images/clean_sample.jpg", "puppy.jpg")
        if data_path is not None:
            data = self.framed_image(data_path, width=0.94, height=0.68, color=ACCENT, fill_opacity=0.025)
        else:
            data = self.clean_sample(scale=0.42, color=ACCENT)
        data.move_to(nodes[0].get_center() + 1.44 * DOWN)
        guides = VGroup(
            DashedLine(nodes[-1].get_bottom(), cloud.get_top(), color=ACCENT_2, stroke_width=1.5, dash_length=0.08),
            DashedLine(nodes[0].get_bottom(), data.get_top(), color=ACCENT, stroke_width=1.5, dash_length=0.08),
        )
        captions = VGroup(
            self.label("noise", SMALL_SIZE, ACCENT_2).next_to(cloud, DOWN, buff=0.12),
            self.label("data", SMALL_SIZE, ACCENT).next_to(data, DOWN, buff=0.12),
        )
        forward_label = self.label("forward chain", SMALL_SIZE, ACCENT).next_to(nodes, UP, buff=0.32)
        reverse_label = self.label("reverse arrows", SMALL_SIZE, ACCENT_2).next_to(nodes, DOWN, buff=1.15)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)
        self.play(FadeIn(nodes), FadeIn(forward_label), LaggedStart(*[GrowArrow(arrow) for arrow in forward_arrows], lag_ratio=0.1), run_time=2.0)
        self.wait(2.5)
        self.play(forward_arrows.animate.set_opacity(0.2), forward_label.animate.set_opacity(0.25), run_time=0.8)
        self.play(FadeIn(reverse_label), LaggedStart(*[GrowArrow(arrow) for arrow in reverse_arrows], lag_ratio=0.1), run_time=1.8)
        self.play(FadeIn(cloud), FadeIn(data), Create(guides), FadeIn(captions), run_time=0.8)
        self.wait(16.2)
        self.play(FadeOut(Group(question, nodes, forward_arrows, reverse_arrows, forward_label, reverse_label, cloud, data, guides, captions)), run_time=1.0)

    def bayes_rewrite(self):
        forward = self.display_equation(
            r"q(x_{0:T})=q(x_0)\prod_{t=1}^{T}q(x_t\mid x_{t-1})",
            width=8.2,
            size=34,
            accent=ACCENT,
        ).move_to([0, 1.35, 0])
        label = self.label("Start with the standard forward factorization.", SMALL_SIZE, MUTED)
        label.next_to(forward, DOWN, buff=0.2)
        self.play(FadeIn(forward, shift=0.12 * UP), FadeIn(label), run_time=1.4)
        self.wait(12.0)

        bayes_title = self.section_tag("Bayes rewrite", ACCENT_2).to_edge(LEFT, buff=0.45).shift(0.2 * UP)
        bayes = self.display_equation(
            r"q(x_t\mid x_{t-1})=\frac{q(x_{t-1}\mid x_t)\,q(x_t)}{q(x_{t-1})}",
            width=8.1,
            size=34,
            accent=ACCENT_2,
        ).move_to([0, -0.95, 0])
        self.play(FadeIn(bayes_title), FadeIn(bayes, shift=0.12 * UP), run_time=1.5)
        self.wait(15.0)
        self.play(FadeOut(VGroup(forward, label, bayes_title, bayes)), run_time=1.0)

    def telescoping_expansion(self):
        title = self.hook_question("Substitute Bayes, then expand the product.")
        self.play(FadeIn(title, shift=0.12 * DOWN), run_time=1.0)

        start_term = self.eq(r"q(x_0)", size=30)
        fractions = VGroup(
            self.fraction_block(r"q(x_0\mid x_1)\,q(x_1)", r"q(x_0)", ACCENT),
            self.fraction_block(r"q(x_1\mid x_2)\,q(x_2)", r"q(x_1)", ACCENT_2),
            self.fraction_block(r"q(x_2\mid x_3)\,q(x_3)", r"q(x_2)", GREEN),
            self.fraction_block(r"\cdots", r"\cdots", VIOLET),
            self.fraction_block(r"q(x_{T-1}\mid x_T)\,q(x_T)", r"q(x_{T-1})", RED),
        ).arrange(RIGHT, buff=0.14)
        if fractions.width > 11.4:
            fractions.scale_to_fit_width(11.4)
        fractions.move_to([0.45, 0.12, 0])

        prefix = self.eq(r"q(x_{0:T})=", size=30)
        start_term.next_to(prefix, RIGHT, buff=0.18)
        leading = VGroup(prefix, start_term).move_to([-4.15, 1.08, 0])
        times = self.eq(r"\times", size=28).next_to(start_term, RIGHT, buff=0.2)
        self.play(FadeIn(prefix), FadeIn(start_term), FadeIn(times), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(frac, shift=0.08 * UP) for frac in fractions], lag_ratio=0.12), run_time=3.4)
        self.wait(11.0)
        self.telescoping_engine_demo(fractions)

        cancel_lines = VGroup()
        highlights = VGroup()
        cancel_pairs = [
            (start_term, fractions[0][3]),
            (fractions[0][1][1], fractions[1][3]),
            (fractions[1][1][1], fractions[2][3]),
        ]
        for top_mob, bottom_mob in cancel_pairs:
            top_line = Line(top_mob.get_corner(DL), top_mob.get_corner(UR), color=RED, stroke_width=5)
            bottom_line = Line(bottom_mob.get_corner(DL), bottom_mob.get_corner(UR), color=RED, stroke_width=5)
            cancel_lines.add(VGroup(top_line, bottom_line))
            highlights.add(
                VGroup(
                    SurroundingRectangle(top_mob, color=ACCENT_2, stroke_width=2, buff=0.06),
                    SurroundingRectangle(bottom_mob, color=ACCENT_2, stroke_width=2, buff=0.06),
                )
            )
        cancel_label = self.label("Telescoping: matching factors cancel from left to right.", SMALL_SIZE, RED)
        cancel_label.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(cancel_label), run_time=0.8)
        tick_path = self.first_asset("sounds/tick.wav", "sounds/tick.mp3")
        for highlight, line_pair in zip(highlights, cancel_lines):
            self.play(Create(highlight), run_time=0.28)
            if tick_path is not None:
                self.add_sound(str(tick_path), gain=-18)
            self.play(LaggedStart(*[Create(line) for line in line_pair], lag_ratio=0.12), FadeOut(highlight), run_time=0.55)
        collapsed = self.display_equation(
            r"q(x_{0:T})=q(x_T)\prod_{t=1}^{T}q(x_{t-1}\mid x_t)",
            width=7.6,
            size=32,
            accent=RED,
        ).to_edge(DOWN, buff=0.38)
        self.play(Transform(cancel_label, self.label("What remains is the reverse factorization.", SMALL_SIZE, RED).to_edge(DOWN, buff=0.55)), run_time=0.8)
        self.play(FadeIn(collapsed, shift=0.08 * UP), run_time=1.1)
        self.wait(9.0)
        self.play(FadeOut(VGroup(title, leading, times, fractions, cancel_lines, cancel_label, collapsed)), run_time=1.2)

    def telescoping_engine_demo(self, fractions: VGroup):
        engine_label = self.label("The matching marginals lock together, then vanish.", SMALL_SIZE, ACCENT_2)
        engine_label.to_edge(DOWN, buff=0.58)
        blocks = VGroup(
            self.connector_block(r"q(x_0)", ACCENT),
            self.connector_block(r"q(x_1)", ACCENT_2),
            self.connector_block(r"q(x_2)", GREEN),
            self.connector_block(r"\cdots", VIOLET),
        ).arrange(RIGHT, buff=0.38)
        blocks.move_to([0.0, -1.55, 0])
        block_targets = blocks.copy().arrange(RIGHT, buff=-0.06).move_to(blocks)
        smoke = VGroup(
            *[
                VGroup(
                    *[
                        Circle(radius=0.045 + 0.012 * j, stroke_width=0, fill_color=TEXT, fill_opacity=0.24 - 0.035 * j)
                        .move_to(block.get_center() + np.array([0.08 * (j - 2), 0.08 * np.sin(j), 0]))
                        for j in range(5)
                    ]
                )
                for block in blocks
            ]
        )
        keep_left = MathTex(r"q(x_T)", font_size=28, color=RED).move_to(blocks.get_left() + 0.48 * LEFT + 0.02 * UP)
        keep_right = MathTex(r"\prod q(x_{t-1}\mid x_t)", font_size=27, color=RED).move_to(blocks.get_right() + 0.92 * RIGHT + 0.02 * UP)
        self.play(FadeIn(engine_label), LaggedStart(*[FadeIn(block, shift=0.06 * UP) for block in blocks], lag_ratio=0.12), run_time=1.1)
        self.play(
            LaggedStart(*[Transform(blocks[i], block_targets[i]) for i in range(len(blocks))], lag_ratio=0.08),
            run_time=1.2,
        )
        tick_path = self.first_asset("sounds/tick.wav", "sounds/tick.mp3")
        if tick_path is not None:
            self.add_sound(str(tick_path), gain=-18)
        self.play(
            LaggedStart(*[FadeIn(puff, scale=1.4) for puff in smoke], lag_ratio=0.06),
            blocks.animate.set_opacity(0.08).scale(0.92),
            FadeIn(keep_left),
            FadeIn(keep_right),
            run_time=1.2,
        )
        self.wait(1.3)
        self.play(FadeOut(VGroup(engine_label, blocks, smoke, keep_left, keep_right)), run_time=0.8)

    def connector_block(self, tex: str, color: str) -> VGroup:
        body = RoundedRectangle(
            width=1.18,
            height=0.52,
            corner_radius=0.07,
            stroke_color=color,
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=0.12,
        )
        peg = Circle(radius=0.09, stroke_color=color, stroke_width=1.2, fill_color=BG, fill_opacity=1)
        peg.next_to(body, RIGHT, buff=-0.01)
        notch = Circle(radius=0.09, stroke_color=color, stroke_width=1.2, fill_color=BG, fill_opacity=1)
        notch.next_to(body, LEFT, buff=-0.01)
        label = MathTex(tex, font_size=22, color=TEXT).move_to(body)
        return VGroup(body, peg, notch, label)

    def final_reverse_markov(self):
        final = self.display_equation(
            r"q(x_{0:T})=q(x_T)\prod_{t=1}^{T}q(x_{t-1}\mid x_t)",
            width=8.5,
            size=36,
            accent=RED,
        ).move_to([0, 0.85, 0])
        red_box = SurroundingRectangle(final, color=RED, stroke_width=3, buff=0.12)
        meaning = self.label(
            "The same joint distribution can be written in the reverse Markov direction.",
            BODY_SIZE,
            TEXT,
        )
        meaning.next_to(final, DOWN, buff=0.42)

        self.play(FadeIn(final, shift=0.16 * UP), Create(red_box), run_time=1.6)
        self.wait(11.0)
        self.play(FadeIn(meaning), run_time=1.0)
        self.wait(14.0)

        bridge = self.takeaway(
            "Learn the reverse step, then walk from noise back to data.",
            GREEN,
        )
        bridge.to_edge(DOWN, buff=0.42)
        nn = self.neural_network_block().scale(0.85).move_to([0, -2.0, 0])
        arrow = Arrow(final.get_bottom(), nn.get_top(), buff=0.25, color=GREEN, stroke_width=4)
        self.play(FadeOut(meaning), run_time=0.6)
        self.play(GrowArrow(arrow), FadeIn(nn, scale=0.96), FadeIn(bridge, shift=0.08 * UP), run_time=1.8)
        self.wait(18.0)

    def fraction_block(self, numerator: str, denominator: str, color: str) -> VGroup:
        box = self.soft_box(width=2.15, height=1.08, color=color, fill_opacity=0.035, stroke_opacity=0.45)
        if r"\," in numerator and numerator != r"\cdots":
            conditional_tex, marginal_tex = numerator.split(r"\,", 1)
            num = VGroup(
                self.eq(conditional_tex, size=22),
                self.eq(marginal_tex, size=22),
            ).arrange(RIGHT, buff=0.08)
        else:
            num = self.eq(numerator, size=22)
        num = self.fit_to_box(num, 1.9, 0.28)
        den = self.fit_to_box(self.eq(denominator, size=22), 1.9, 0.28)
        rule = Line(LEFT * 0.82, RIGHT * 0.82, color=TEXT, stroke_width=1.4)
        frac = VGroup(num, rule, den).arrange(DOWN, buff=0.06).move_to(box)
        return VGroup(box, num, rule, den)

    def neural_network_block(self) -> VGroup:
        asset = self.first_asset("icons/neural_network.svg", "icons/neural_network.png")
        if asset is not None:
            box = self.soft_box(2.55, 1.42, color=VIOLET, fill_opacity=0.045, stroke_opacity=0.72)
            if asset.suffix.lower() == ".svg":
                icon = SVGMobject(str(asset), stroke_width=2)
            else:
                icon = ImageMobject(str(asset))
            self.fit_to_box(icon, 2.12, 1.12)
            icon.move_to(box)
            label = self.label("Neural network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.12)
            return Group(box, icon, label)

        box = self.soft_box(2.35, 1.22, color=VIOLET, fill_opacity=0.06, stroke_opacity=0.72)
        layers = VGroup()
        for x, count in [(-0.65, 3), (0, 4), (0.65, 3)]:
            layer = VGroup(*[Dot([x, (i - (count - 1) / 2) * 0.22, 0], radius=0.034, color=VIOLET) for i in range(count)])
            layers.add(layer)
        edges = VGroup()
        for left, right in zip(layers[:-1], layers[1:]):
            for a in left:
                for b in right:
                    edges.add(Line(a.get_center(), b.get_center(), color=DIM, stroke_width=0.7))
        label = self.label("Neural Network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.12)
        return VGroup(box, edges, layers, label)
