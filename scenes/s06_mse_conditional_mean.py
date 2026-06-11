from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class MSEConditionalMeanScene(DiffusionScene):
    TARGET_DURATION = 143.63

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "Why MSE Learns the Mean",
            "The best single denoising target is the conditional center of mass",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(title), run_time=0.7)

        self.network_from_question()
        self.center_of_mass_visual()
        self.parabola_loss()
        self.bridge_to_network_mean()
        self.network_absorbs_compass()
        self.hold_to_time(start, self.TARGET_DURATION)

    def network_from_question(self):
        question = self.hook_question("If score is too hard to compute, learn a denoising function.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        unknown = self.display_equation(r"\text{score}=?", width=3.5, size=34, accent=RED).move_to([-3.0, 0.65, 0])
        network = self.neural_network_block().scale(1.05).move_to([0.15, 0.45, 0])
        input_label = self.eq(r"(y,t)", size=30, color=TEXT).next_to(network, LEFT, buff=0.58)
        output = self.display_equation(r"f_\theta(y,t)", width=3.4, size=34, accent=VIOLET).next_to(network, RIGHT, buff=0.5)
        arrows = VGroup(
            Arrow(input_label.get_right(), network.get_left(), buff=0.18, color=ACCENT, stroke_width=3.5),
            Arrow(network.get_right(), output.get_left(), buff=0.18, color=VIOLET, stroke_width=3.5),
        )
        note = self.label("The theorem tells us what this optimal denoising function should be.", SMALL_SIZE, MUTED).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(unknown), run_time=0.8)
        self.play(FadeTransform(unknown.copy(), network), FadeIn(input_label), FadeIn(output), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.6)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(8.0)
        self.play(FadeOut(Group(question, unknown, network, input_label, output, arrows, note)), run_time=1.0)

    def center_of_mass_visual(self):
        question = self.hook_question("Best single prediction under MSE = conditional mean")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        y_box = self.soft_box(1.25, 0.82, color=RED, fill_opacity=0.04, stroke_opacity=0.72).move_to([0, 1.78, 0])
        y_label = self.eq(r"y", size=36, color=RED).move_to(y_box)
        samples = VGroup()
        sample_points = [
            (-1.7, 0.2), (-1.15, -0.35), (-0.6, 0.45), (-0.18, -0.18),
            (0.35, 0.18), (0.78, -0.45), (1.2, 0.36), (1.65, -0.1),
        ]
        base = np.array([0, -0.4, 0])
        for i, (x, yv) in enumerate(sample_points):
            dot = Dot(base + np.array([x, yv, 0]), radius=0.075, color=self.mix_color(ACCENT, GREEN, i / 8))
            samples.add(dot)
        mean_point = np.mean([sample.get_center() for sample in samples], axis=0)
        left_pos = np.array([-1.85, -0.82 + 0.18 * np.sin(-1.85), 0])
        right_pos = np.array([1.75, -0.82 + 0.18 * np.sin(1.75), 0])
        balanced_pos = np.array([mean_point[0], -0.82 + 0.18 * np.sin(mean_point[0]), 0])
        pred = Dot(left_pos, radius=0.09, color=RED)

        def spring_group(origin: np.ndarray, color: str = RED) -> VGroup:
            return VGroup(*[
                Line(origin, sample.get_center(), color=color, stroke_width=1.25, stroke_opacity=0.32)
                for sample in samples
            ])

        springs = always_redraw(
            lambda: VGroup(
                *[
                    Line(
                        pred.get_center(),
                        sample.get_center(),
                        color=self.mix_color(MUTED, ACCENT_2, i / max(1, len(samples) - 1)),
                        stroke_width=1.15,
                        stroke_opacity=0.18 + 0.22 * (i / max(1, len(samples) - 1)),
                    )
                    for i, sample in enumerate(samples)
                ]
            )
        )
        mean = Dot(mean_point, radius=0.12, color=ACCENT_2)
        rings = VGroup(*[Circle(radius=0.19 + 0.12 * i, stroke_color=ACCENT_2, stroke_width=1.4).move_to(mean).set_opacity(0.55 - 0.12 * i) for i in range(3)])
        label = self.eq(r"\mathbb{E}[X\mid Y=y]", size=31, color=ACCENT_2).next_to(mean, DOWN, buff=0.16)
        beam = Line([-2.1, -1.35, 0], [2.1, -1.35, 0], color=DIM, stroke_width=4)
        fulcrum = Triangle(color=DIM, fill_color=DIM, fill_opacity=0.35).scale(0.18).rotate(PI).move_to([mean_point[0], -1.58, 0])
        balance_note = self.label("balanced at the conditional center of mass", SMALL_SIZE, ACCENT_2).next_to(beam, DOWN, buff=0.22)
        caption = self.label("many possible cleaner states could explain the same y", SMALL_SIZE, MUTED).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(y_box), FadeIn(y_label), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(sample, scale=1.25) for sample in samples], lag_ratio=0.06), FadeIn(caption), run_time=1.4)
        self.play(FadeIn(springs), FadeIn(pred), Create(beam), FadeIn(fulcrum), run_time=0.8)
        self.play(pred.animate.move_to(right_pos), beam.animate.rotate(-6 * DEGREES, about_point=fulcrum.get_center()), run_time=1.6)
        self.play(pred.animate.move_to(balanced_pos).set_color(ACCENT_2), beam.animate.rotate(6 * DEGREES, about_point=fulcrum.get_center()), run_time=1.6)
        glow = VGroup(*[Circle(radius=0.22 + 0.1 * i, stroke_color=ACCENT_2, stroke_width=1.2, stroke_opacity=0.28 / (i + 1)).move_to(mean) for i in range(5)])
        self.play(FadeIn(mean, scale=1.4), Create(rings), Create(glow), FadeIn(label), FadeIn(balance_note), run_time=1.0)
        self.wait(22.0)
        self.play(FadeOut(Group(question, y_box, y_label, samples, springs, pred, mean, rings, glow, label, beam, fulcrum, balance_note, caption)), run_time=1.0)

    def parabola_loss(self):
        question = self.hook_question("The MSE minimum sits at the conditional mean.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        axes = Axes(
            x_range=[-2.8, 2.8, 1],
            y_range=[0, 4.4, 1],
            x_length=6.25,
            y_length=2.9,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.4},
        ).move_to([-1.05, -0.18, 0])
        mu_x = 0.55
        parabola = axes.plot(lambda x: 0.55 + 0.72 * (x - mu_x) ** 2, x_range=[-2.0, 2.55], color=ACCENT_2, stroke_width=4)
        ball = Dot(axes.c2p(-1.72, 3.25), radius=0.09, color=RED)
        optimum = Dot(axes.c2p(mu_x, 0.55), radius=0.1, color=GREEN)
        loss = self.display_equation(
            r"L(f_\theta)=\mathbb{E}\left[|f_\theta(y)-x|^2\right]",
            width=6.4,
            size=31,
            accent=ACCENT_2,
        ).move_to([3.2, 1.25, 0])
        theorem = self.display_equation(
            r"f^*(y)=\mathbb{E}[X\mid Y=y]=\mu(X\mid y)",
            width=6.35,
            size=31,
            accent=GREEN,
        ).move_to([3.2, -0.52, 0])
        note = self.label("In ideal conditions, the optimal function is the conditional mean.", SMALL_SIZE, TEXT)
        note.to_edge(DOWN, buff=0.5)

        self.play(Create(axes), Create(parabola), FadeIn(loss), run_time=1.3)
        self.play(FadeIn(ball), run_time=0.5)
        self.play(MoveAlongPath(ball, parabola), run_time=2.3, rate_func=smooth)
        ball.move_to(optimum)
        self.play(FadeIn(optimum, scale=1.35), FadeIn(theorem), FadeIn(note), run_time=1.3)
        self.wait(52.5)
        self.play(FadeOut(Group(question, axes, parabola, ball, optimum, loss, theorem, note)), run_time=1.0)

    def bridge_to_network_mean(self):
        question = self.hook_question("In practice, the network approximates the reverse mean.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        ideal = self.display_equation(r"f^*(y)=\mathbb{E}[X\mid Y=y]", width=4.35, size=31, accent=GREEN).move_to([-3.25, 1.0, 0])
        approx = self.display_equation(r"\mu_\theta(y,t)\approx\mathbb{E}[X_{t-1}\mid X_t=y]", width=5.75, size=28, accent=VIOLET).move_to([2.45, 1.0, 0])
        arrow = Arrow(ideal.get_right(), approx.get_left(), buff=0.24, color=VIOLET, stroke_width=4)
        noisy = self.chain_node(r"x_t=y", color=RED).move_to([1.45, -1.25, 0])
        cleaner = self.chain_node(r"x_{t-1}", color=GREEN).move_to([-1.45, -1.25, 0])
        reverse = Arrow(noisy.get_left(), cleaner.get_right(), buff=0.08, color=GREEN, stroke_width=4)
        caveat = VGroup(
            *[self.label(word, SMALL_SIZE, MUTED) for word in ["Approximation", "only:", "not", "exact."]]
        ).arrange(RIGHT, buff=0.12)
        caveat.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(ideal), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(approx), run_time=1.2)
        self.play(FadeIn(noisy), FadeIn(cleaner), GrowArrow(reverse), FadeIn(caveat), run_time=1.2)
        self.wait(13.0)
        self.play(FadeOut(Group(question, ideal, approx, arrow, noisy, cleaner, reverse, caveat)), run_time=1.0)

    def network_absorbs_compass(self):
        question = self.hook_question("The network absorbs many local compass directions.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        field = VGroup()
        for i, y in enumerate(np.linspace(-1.45, 1.45, 6)):
            start = np.array([-4.9, y, 0])
            end = start + np.array([0.72 + 0.08 * np.cos(i), 0.18 * np.sin(i), 0])
            field.add(Arrow(start, end, buff=0, color=ACCENT, stroke_width=3.0, max_tip_length_to_length_ratio=0.22))
        particles = VGroup(*[Dot(a.get_end(), radius=0.05, color=ACCENT_2) for a in field])
        network = self.neural_network_block().scale(1.15).move_to([0, 0, 0])
        output = self.display_equation(r"\mu_\theta(y,t)", width=3.6, size=34, accent=VIOLET).move_to([4.2, 0.2, 0])
        out_arrow = Arrow(network.get_right(), output.get_left(), buff=0.2, color=VIOLET, stroke_width=4)
        direction = Arrow(output.get_bottom(), output.get_bottom() + np.array([0.8, -0.45, 0]), buff=0.08, color=GREEN, stroke_width=4)
        take_words = VGroup(
            *[
                Text(word, font=FONT_SUBTITLE, font_size=SMALL_SIZE, color=TEXT, weight=BOLD, disable_ligatures=True)
                for word in ["MSE", "learns", "the", "conditional", "mean.", "Network", "approximates", "it."]
            ]
        ).arrange(RIGHT, buff=0.105)
        take_box = self.soft_box(
            width=max(10.8, take_words.width + 0.7),
            height=max(0.56, take_words.height + 0.28),
            color=VIOLET,
            fill_opacity=0.075,
            stroke_opacity=0.62,
        )
        take_words.move_to(take_box)
        take = VGroup(take_box, take_words)
        take.to_edge(DOWN, buff=0.38)

        self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.06), run_time=1.2)
        self.play(FadeIn(network, scale=0.96), run_time=0.9)
        self.play(LaggedStart(*[p.animate.move_to(network.get_center()).set_opacity(0.0) for p in particles], lag_ratio=0.05), field.animate.set_opacity(0.18), run_time=1.5)
        self.play(network.animate.set_color(VIOLET), GrowArrow(out_arrow), FadeIn(output), GrowArrow(direction), run_time=1.2)
        self.play(FadeIn(take, shift=0.08 * UP), run_time=1.0)
        self.wait(10.0)
        self.play(FadeOut(Group(question, field, particles, network, output, out_arrow, direction, take)), run_time=1.0)

    def neural_network_block(self) -> Group:
        asset = self.first_asset("icons/neural_network.svg", "icons/neural_network.png")
        if asset is not None:
            box = self.soft_box(2.15, 1.22, color=VIOLET, fill_opacity=0.055, stroke_opacity=0.72)
            icon = ImageMobject(str(asset))
            self.fit_to_box(icon, 1.72, 0.9)
            icon.move_to(box)
            icon.set_opacity(0.92)
            label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.11)
            return Group(box, icon, label)

        box = self.soft_box(2.15, 1.22, color=VIOLET, fill_opacity=0.06, stroke_opacity=0.72)
        layers = VGroup()
        for x, count in [(-0.58, 3), (0, 4), (0.58, 3)]:
            layers.add(VGroup(*[Dot([x, (i - (count - 1) / 2) * 0.2, 0], radius=0.032, color=VIOLET) for i in range(count)]))
        edges = VGroup()
        for left, right in zip(layers[:-1], layers[1:]):
            for a in left:
                for b in right:
                    edges.add(Line(a.get_center(), b.get_center(), color=DIM, stroke_width=0.7))
        label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.11)
        return Group(box, edges, layers, label)
