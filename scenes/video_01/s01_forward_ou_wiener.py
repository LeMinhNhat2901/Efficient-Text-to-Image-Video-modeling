from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.base_scene import DiffusionScene
from config import *


class ForwardOUWiener(DiffusionScene):
    TARGET_DURATION = 154.2

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.035)
        title = self.scene_title(
            "The Forward Process",
            "Quantifying the destruction of structure",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(title), run_time=0.8)

        self.one_step_equation()
        self.random_walks_with_std_band()
        self.jump_formula()
        self.hold_to_time(start, self.TARGET_DURATION)

    def one_step_equation(self):
        particle = Dot(radius=0.11, color=ACCENT).move_to([-4.8, 0.65, 0])
        previous = self.compact_eq(r"X_{t-1}", size=34).next_to(particle, DOWN, buff=0.22)
        arrow = Arrow([-4.0, 0.65, 0], [-2.7, 0.65, 0], color=MUTED, stroke_width=4)
        new_particle = Dot(radius=0.11, color=ACCENT_2).move_to([-2.1, 0.65, 0])
        current = self.compact_eq(r"X_t", size=34).next_to(new_particle, DOWN, buff=0.22)

        self.play(FadeIn(particle), FadeIn(previous), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(new_particle), FadeIn(current), run_time=1.2)
        self.wait(7.0)

        eq = MathTex(
            r"X_t=",
            r"\alpha_t",
            r"X_{t-1}",
            r"+",
            r"\sqrt{\beta_t}",
            r"G",
            font_size=40,
            color=TEXT,
        )
        eq.move_to([1.05, 0.72, 0])
        self.play(Write(eq), run_time=3.2)
        self.wait(7.0)

        braces = VGroup(
            Brace(VGroup(eq[1], eq[2]), DOWN, color=ACCENT),
            Brace(VGroup(eq[4], eq[5]), DOWN, color=ACCENT_2),
        )
        alpha = self.brace_label(r"\alpha_t X_{t-1}", "shrink old signal", ACCENT)
        beta = self.brace_label(r"\sqrt{\beta_t}\,G", "add Gaussian noise", ACCENT_2)
        alpha.next_to(braces[0], DOWN, buff=0.24).set_x(braces[0].get_x())
        beta.next_to(braces[1], DOWN, buff=0.24).set_x(braces[1].get_x())

        self.play(FadeIn(braces[0]), FadeIn(alpha), run_time=1.0)
        self.wait(16.0)
        self.play(FadeIn(braces[1]), FadeIn(beta), run_time=1.0)
        self.wait(15.0)

        center = Dot(radius=0.045, color=MUTED).move_to([-3.45, -1.65, 0])
        old = Dot(radius=0.09, color=ACCENT).move_to([-4.15, -1.25, 0])
        shrunk = Dot(radius=0.09, color=ACCENT).move_to([-3.65, -1.48, 0])
        jumped = Dot(radius=0.1, color=ACCENT_2).move_to([-3.2, -1.05, 0])
        pull_arrow = Arrow(old.get_center(), shrunk.get_center(), buff=0.09, color=ACCENT, stroke_width=3)
        jitter_arrow = Arrow(shrunk.get_center(), jumped.get_center(), buff=0.09, color=ACCENT_2, stroke_width=3)
        action_label = self.label("old position, then shrink, then random jump", SMALL_SIZE, TEXT)
        action_label.next_to(center, DOWN, buff=0.22).shift(0.28 * RIGHT)
        self.play(FadeIn(center), FadeIn(old), FadeIn(action_label), run_time=0.7)
        self.play(GrowArrow(pull_arrow), Transform(old, shrunk), run_time=0.9)
        self.play(GrowArrow(jitter_arrow), Transform(old, jumped), run_time=0.9)
        self.wait(13.0)
        self.variance_circle_demo(eq, alpha, beta, braces)
        self.play(FadeOut(VGroup(particle, previous, arrow, new_particle, current, eq, alpha, beta, braces, center, old, pull_arrow, jitter_arrow, action_label)), run_time=1.2)

    def variance_circle_demo(self, eq: Mobject, alpha: Mobject, beta: Mobject, braces: Mobject):
        circle_center = np.array([4.18, -1.72, 0])
        radius = 0.82
        circle = Circle(radius=radius, color=DIM, stroke_width=2).move_to(circle_center)
        h_axis = Arrow(circle_center, circle_center + 1.14 * RIGHT, buff=0, color=ACCENT, stroke_width=3)
        v_axis = Arrow(circle_center, circle_center + 1.14 * UP, buff=0, color=RED, stroke_width=3)
        h_label = MathTex(r"\alpha_t", font_size=24, color=ACCENT).next_to(h_axis, DOWN, buff=0.08)
        v_label = MathTex(r"\sqrt{\beta_t}", font_size=24, color=RED).next_to(v_axis, LEFT, buff=0.08)
        constraint = MathTex(r"\alpha_t^2+\beta_t=1", font_size=26, color=TEXT).next_to(circle, UP, buff=0.16)
        angle = ValueTracker(12 * DEGREES)

        vector = always_redraw(
            lambda: Arrow(
                circle_center,
                circle_center + radius * np.array([np.cos(angle.get_value()), np.sin(angle.get_value()), 0]),
                buff=0,
                color=ACCENT_2,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
            )
        )
        signal_bar = always_redraw(
            lambda: Rectangle(
                width=max(0.05, 1.12 * np.cos(angle.get_value())),
                height=0.14,
                stroke_width=0,
                fill_color=ACCENT,
                fill_opacity=0.9,
            ).move_to(circle_center + 1.26 * DOWN + 0.56 * np.cos(angle.get_value()) * RIGHT).align_to(circle_center + 1.26 * DOWN, LEFT)
        )
        noise_bar = always_redraw(
            lambda: Rectangle(
                width=max(0.05, 1.12 * np.sin(angle.get_value())),
                height=0.14,
                stroke_width=0,
                fill_color=RED,
                fill_opacity=0.9,
            ).next_to(signal_bar, DOWN, buff=0.14).align_to(signal_bar, LEFT)
        )
        bar_labels = VGroup(
            self.label("signal", 13, ACCENT).next_to(signal_bar, LEFT, buff=0.12),
            self.label("noise", 13, RED).next_to(noise_bar, LEFT, buff=0.12),
        )
        note = self.label("total variance stays fixed", 15, MUTED)
        note.next_to(noise_bar, DOWN, buff=0.18).set_x(circle_center[0])

        self.play(
            eq.animate.shift(0.44 * UP),
            alpha.animate.shift(0.34 * UP),
            beta.animate.shift(0.34 * UP),
            braces.animate.shift(0.34 * UP),
            FadeIn(VGroup(circle, h_axis, v_axis, h_label, v_label, constraint, signal_bar, noise_bar, bar_labels, note)),
            GrowArrow(vector),
            run_time=1.4,
        )
        self.play(angle.animate.set_value(76 * DEGREES), run_time=10.0, rate_func=smooth)
        self.wait(18.0)
        self.play(FadeOut(VGroup(circle, h_axis, v_axis, h_label, v_label, constraint, vector, signal_bar, noise_bar, bar_labels, note)), run_time=0.9)

    def random_walks_with_std_band(self):
        title = self.hook_question("Simulation: trajectories spread as variance grows", width=11.2)
        title.to_edge(UP, buff=0.38)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-3, 3, 1],
            x_length=9.6,
            y_length=4.75,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.25},
        ).move_to([0.0, -0.05, 0])

        self.play(FadeIn(title, shift=0.12 * DOWN), Create(axes), run_time=1.2)

        ou_data = self.load_ou_paths()
        mean_line = axes.plot(lambda x: 0, x_range=[0, 10], color=MUTED, stroke_width=1.4)
        self.play(Create(mean_line), run_time=0.45)

        upper_start = axes.plot(lambda x: 0.04 + 0 * x, x_range=[0, 10], color=DIM, stroke_width=0)
        lower_start = axes.plot(lambda x: -0.04 + 0 * x, x_range=[0, 10], color=DIM, stroke_width=0)
        band_start = axes.get_area(upper_start, bounded_graph=lower_start, x_range=[0, 10], color=GREY, opacity=0.12)
        if ou_data is not None:
            xs = ou_data["xs"]
            envelope = ou_data["envelope"]
            upper = axes.plot(lambda x: float(np.interp(x, xs, envelope)), x_range=[0, 10], color=DIM, stroke_width=0)
            lower = axes.plot(lambda x: -float(np.interp(x, xs, envelope)), x_range=[0, 10], color=DIM, stroke_width=0)
        else:
            upper = axes.plot(lambda x: 0.35 + 0.23 * x, x_range=[0, 10], color=DIM, stroke_width=0)
            lower = axes.plot(lambda x: -0.35 - 0.23 * x, x_range=[0, 10], color=DIM, stroke_width=0)
        band = axes.get_area(upper, bounded_graph=lower, x_range=[0, 10], color=GREY, opacity=0.18)
        band_label = self.label("expected standard deviation", SMALL_SIZE, MUTED)
        band_label.next_to(axes, DOWN, buff=0.2)
        self.play(FadeIn(band_start), FadeIn(band_label), run_time=0.45)
        self.play(Transform(band_start, band), run_time=1.1)
        self.wait(1.2)

        particle = Dot(axes.c2p(0, 0.0), radius=0.055, color=ACCENT_2)
        pull = always_redraw(lambda: Arrow(particle.get_center() + 0.35 * UP, particle.get_center() + 0.04 * UP, buff=0, color=ACCENT_2, stroke_width=2.5, max_tip_length_to_length_ratio=0.28))
        jitter = always_redraw(lambda: Arrow(particle.get_center(), particle.get_center() + 0.28 * RIGHT + 0.18 * UP, buff=0, color=RED, stroke_width=2.5, max_tip_length_to_length_ratio=0.28))
        force_label = self.label("pull to mean + random jitter", SMALL_SIZE, TEXT)
        force_label.move_to([0, 1.72, 0])
        force_tag = self.soft_box(
            width=max(3.9, force_label.width + 0.45),
            height=0.38,
            color=DIM,
            fill_opacity=0.22,
            stroke_opacity=0.28,
        ).move_to(force_label)
        force_group = VGroup(force_tag, force_label)
        self.play(FadeIn(particle), FadeIn(pull), FadeIn(jitter), FadeIn(force_group), run_time=0.55)

        paths = VGroup()
        colors = [ACCENT, ACCENT_2, GREEN, VIOLET, RED]
        if ou_data is not None:
            xs = ou_data["xs"]
            for i, color in enumerate(colors):
                paths.add(self.path_from_arrays(axes, xs, ou_data["paths"][i], color=color))
            particle_points = [axes.c2p(float(x), float(y)) for x, y in zip(xs[::8], ou_data["particle"][::8])]
            particle_path = VMobject()
            particle_path.set_points_as_corners(particle_points)
            self.play(MoveAlongPath(particle, particle_path), run_time=1.4)
        else:
            for i, color in enumerate(colors):
                paths.add(self.random_walk_path(axes, seed=41 + i, color=color))
        self.play(LaggedStart(*[Create(path) for path in paths], lag_ratio=0.16), run_time=2.1)
        self.wait(0.8)

        note = self.label("Each line is one possible data trajectory.", SMALL_SIZE, TEXT)
        note.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(note), run_time=0.45)
        self.wait(1.4)
        self.play(FadeOut(VGroup(title, note, axes, mean_line, band_start, band_label, paths, particle, pull, jitter, force_group)), run_time=0.8)

    def jump_formula(self):
        headline = self.hook_question("Gaussian algebra lets us jump directly to any time t.")
        self.play(FadeIn(headline, shift=0.12 * DOWN), run_time=1.0)
        self.wait(2.0)

        small_steps = VGroup(*[self.chain_node(tex) for tex in [r"X_0", r"X_1", r"X_2", r"\cdots", r"X_t"]]).arrange(RIGHT, buff=0.52)
        small_steps.move_to([0, 1.0, 0])
        arrows = VGroup(*[self.small_arrow(small_steps[i], small_steps[i + 1], MUTED) for i in range(4)])
        jump = CurvedArrow(small_steps[0].get_top(), small_steps[-1].get_top(), angle=-TAU / 5, color=ACCENT_2, stroke_width=4)
        jump_label = self.label("one sampled noisy version at time t", SMALL_SIZE, ACCENT_2).next_to(jump, UP, buff=0.1)

        self.play(FadeIn(small_steps), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.09), run_time=1.6)
        self.wait(4.0)
        self.play(Create(jump), FadeIn(jump_label), run_time=1.5)

        eq = self.display_equation(
            r"X_t=\tilde{\alpha}_t X_0+\sqrt{\tilde{\beta}_t}\,G",
            width=6.7,
            size=38,
            accent=ACCENT_2,
        ).move_to([0, -0.75, 0])
        product = self.display_equation(
            r"\tilde{\alpha}_t=\prod_{i=1}^{t}\alpha_i",
            width=4.7,
            size=34,
            accent=GREEN,
        ).next_to(eq, DOWN, buff=0.25)
        self.play(FadeIn(eq, shift=0.12 * UP), run_time=1.2)
        self.wait(6.0)
        self.play(FadeIn(product, shift=0.08 * UP), run_time=1.0)
        self.wait(10.0)

        take = self.takeaway("Forward process is known. Shrink the old signal, add scheduled Gaussian noise.", ACCENT)
        take.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(take, shift=0.08 * UP), run_time=1.0)
        self.wait(8.0)

    def random_walk_path(self, axes: Axes, seed: int, color: str) -> VMobject:
        rng = np.random.default_rng(seed)
        xs = np.linspace(0, 10, 72)
        ys = [0.0]
        for i in range(1, len(xs)):
            spread = 0.05 + 0.028 * i
            ys.append(0.86 * ys[-1] + rng.normal(0, spread))
        points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
        path = VMobject(color=color, stroke_width=3)
        path.set_points_as_corners(points)
        return path

    def load_ou_paths(self):
        path = Path("assets") / "generated" / "ou_paths" / "ou_paths.npz"
        if path.exists():
            return np.load(path)
        return None

    def path_from_arrays(self, axes: Axes, xs: np.ndarray, ys: np.ndarray, color: str) -> VMobject:
        path = VMobject(color=color, stroke_width=3)
        points = [axes.c2p(float(x), float(y)) for x, y in zip(xs, ys)]
        path.set_points_as_corners(points)
        return path

    def brace_label(self, tex: str, body: str, color: str) -> VGroup:
        math = self.eq(tex, size=24, color=color)
        body_mob = self.label(body, 15, MUTED)
        group = VGroup(math, body_mob).arrange(DOWN, buff=0.08)
        if group.width > 2.3:
            group.scale_to_fit_width(2.3)
        return group
