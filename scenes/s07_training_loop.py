from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class TrainingLoopScene(DiffusionScene):
    TARGET_DURATION = 111.33

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "Training the Reverse Step",
            "Algorithm, backward Gaussian, and learned breadcrumbs",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(title), run_time=0.7)

        self.training_machine_layout()
        self.correct_training_step()
        self.loss_meter_decreases()
        self.backward_gaussian()
        self.sampling_breadcrumbs()
        self.sde_teaser()
        self.hold_to_time(start, self.TARGET_DURATION)

    def training_machine_layout(self):
        question = self.hook_question("Training: corrupt, predict, compare, update.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        divider = Line(UP * 2.7, DOWN * 2.7, color=DIM, stroke_width=1.2)
        left_title = self.label("Training loop", SUBTITLE_SIZE, ACCENT, font=FONT_TITLE).move_to([-3.45, 2.15, 0])
        right_title = self.label("Sampling", SUBTITLE_SIZE, MUTED, font=FONT_TITLE).move_to([3.45, 2.15, 0]).set_opacity(0.35)
        machine_shell = self.soft_box(5.65, 4.25, color=ACCENT, fill_opacity=0.025, stroke_opacity=0.46).move_to([-3.48, -0.32, 0])
        gears = VGroup(
            self.gear_icon(ACCENT).scale(0.52).move_to(machine_shell.get_corner(UL) + np.array([0.34, -0.32, 0])),
            self.gear_icon(VIOLET).scale(0.43).move_to(machine_shell.get_corner(DR) + np.array([-0.34, 0.32, 0])),
        ).set_opacity(0.75)
        modules = VGroup(
            self.module_box("choose t", ACCENT).move_to([-5.0, 0.8, 0]),
            self.module_box(r"x_{t-1}", GREEN).move_to([-3.65, 0.8, 0]),
            self.module_box("inject", RED).move_to([-2.3, 0.8, 0]),
            self.module_box(r"y=x_t", RED).move_to([-4.35, -0.55, 0]),
            self.module_box(r"\mu_\theta(y,t)", VIOLET, width=1.75).move_to([-2.55, -0.55, 0]),
            self.module_box("loss", ACCENT_2).move_to([-3.45, -1.85, 0]),
        )
        noise_particles = VGroup()
        rng = np.random.default_rng(21)
        for _ in range(18):
            noise_particles.add(
                Dot(
                    modules[2].get_center() + np.array([rng.normal(0, 0.22), rng.normal(0, 0.15), 0]),
                    radius=float(rng.uniform(0.014, 0.03)),
                    color=RED,
                    fill_opacity=0.72,
                )
            )
        staircase = VGroup()
        stair_points = [np.array([2.1 + 0.55 * i, 1.0 - 0.34 * i, 0]) for i in range(6)]
        for i, point in enumerate(stair_points):
            dot = Dot(point, radius=0.055, color=self.mix_color(RED, ACCENT_2, i / 5), fill_opacity=0.45)
            staircase.add(dot)
            if i:
                staircase.add(Arrow(stair_points[i - 1], point, buff=0.09, color=ACCENT_2, stroke_width=1.7, max_tip_length_to_length_ratio=0.18).set_opacity(0.35))
        arrows = VGroup(
            Arrow(modules[0].get_right(), modules[1].get_left(), buff=0.08, color=ACCENT, stroke_width=2.6),
            Arrow(modules[1].get_right(), modules[2].get_left(), buff=0.08, color=RED, stroke_width=2.6),
            Arrow(modules[2].get_bottom(), modules[3].get_top(), buff=0.1, color=RED, stroke_width=2.6),
            Arrow(modules[3].get_right(), modules[4].get_left(), buff=0.1, color=VIOLET, stroke_width=2.6),
            Arrow(modules[4].get_bottom(), modules[5].get_top(), buff=0.1, color=ACCENT_2, stroke_width=2.6),
        )
        update = CurvedArrow(modules[5].get_right(), modules[4].get_bottom(), angle=TAU / 7, color=ACCENT_2, stroke_width=3)

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), FadeIn(machine_shell), FadeIn(gears), FadeIn(staircase), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=0.05 * UP) for m in modules], lag_ratio=0.08), run_time=1.3)
        self.play(FadeIn(noise_particles), run_time=0.35)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08),
            LaggedStart(*[p.animate.move_to(modules[3].get_center() + 0.18 * np.array([np.cos(i), np.sin(i), 0])).set_opacity(0.0) for i, p in enumerate(noise_particles)], lag_ratio=0.02),
            Create(update),
            gears.animate.rotate(PI / 4),
            run_time=1.5,
        )
        self.wait(12.0)
        self.play(FadeOut(Group(question, divider, left_title, right_title, machine_shell, gears, modules, noise_particles, staircase, arrows, update)), run_time=1.0)

    def correct_training_step(self):
        question = self.hook_question("The target is the cleaner previous state, not necessarily x_0.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        top = VGroup(
            self.display_equation(r"y=\alpha_t x+\sqrt{\beta_t}\epsilon", width=5.0, size=30, accent=RED),
            self.display_equation(r"\hat{x}=\mu_\theta(y,t)", width=3.75, size=31, accent=VIOLET),
            self.display_equation(r"\left|\mu_\theta(y,t)-x\right|^2", width=4.45, size=31, accent=ACCENT_2),
        ).arrange(DOWN, buff=0.35).move_to([3.35, 0.15, 0])
        x_node = self.chain_node(r"x\sim X_{t-1}", color=GREEN).move_to([-4.4, 0.65, 0])
        y_node = self.chain_node(r"y=x_t", color=RED).move_to([-2.0, 0.65, 0])
        net = self.neural_network_block().scale(0.82).move_to([-0.1, 0.65, 0])
        pred = self.chain_node(r"\hat{x}", color=VIOLET).move_to([1.55, 0.65, 0])
        injector_noise = VGroup()
        rng = np.random.default_rng(31)
        for _ in range(24):
            injector_noise.add(Dot(x_node.get_center() + np.array([rng.normal(0, 0.22), rng.normal(0, 0.18), 0]), radius=float(rng.uniform(0.012, 0.028)), color=RED, fill_opacity=0.7))
        arrows = VGroup(
            Arrow(x_node.get_right(), y_node.get_left(), buff=0.1, color=RED, stroke_width=3),
            Arrow(y_node.get_right(), net.get_left(), buff=0.1, color=ACCENT, stroke_width=3),
            Arrow(net.get_right(), pred.get_left(), buff=0.1, color=VIOLET, stroke_width=3),
        )
        note = self.word_row(["Noise", "prediction", "is", "another", "common", "formulation."], SMALL_SIZE, MUTED)
        note.to_edge(DOWN, buff=0.55)
        target = self.eq(r"\text{target: }x\sim X_{t-1}", size=25, color=GREEN).next_to(x_node, DOWN, buff=0.22)

        self.play(FadeIn(x_node), FadeIn(target), run_time=0.7)
        self.play(FadeIn(injector_noise), run_time=0.3)
        self.play(
            GrowArrow(arrows[0]),
            LaggedStart(*[p.animate.move_to(y_node.get_center() + 0.28 * np.array([np.cos(i), np.sin(i), 0])).set_opacity(0.0) for i, p in enumerate(injector_noise)], lag_ratio=0.012),
            FadeIn(y_node),
            FadeIn(top[0]),
            run_time=1.0,
        )
        self.play(GrowArrow(arrows[1]), FadeIn(net), run_time=0.8)
        self.play(GrowArrow(arrows[2]), FadeIn(pred), FadeIn(top[1]), run_time=0.9)
        self.play(FadeIn(top[2]), FadeIn(note), run_time=0.9)
        self.wait(6.0)
        self.play(FadeOut(Group(question, top, x_node, y_node, net, pred, arrows, injector_noise, note, target)), run_time=1.0)

    def loss_meter_decreases(self):
        question = self.hook_question("Repeated updates make the reverse mean more reliable.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        net = self.neural_network_block().scale(0.95).move_to([-2.7, 0.4, 0])
        target = Dot([2.2, 0.4, 0], radius=0.1, color=GREEN)
        pred = Dot([0.7, -0.85, 0], radius=0.1, color=RED)
        target_label = self.eq(r"x_{t-1}", size=30, color=GREEN).next_to(target, UP, buff=0.14)
        pred_label = self.eq(r"\mu_\theta(y,t)", size=28, color=VIOLET).next_to(pred, DOWN, buff=0.16)
        meter = self.loss_meter(fill=0.85, color=RED).move_to([2.55, -1.55, 0])
        update = CurvedArrow(meter.get_left(), net.get_bottom(), angle=-TAU / 6, color=ACCENT_2, stroke_width=3.2)
        wall = self.brick_wall().move_to([3.65, 0.34, 0])
        bad_arrow = Arrow(pred.get_right(), wall.get_left(), buff=0.1, color=RED, stroke_width=4)
        wrong = VGroup(
            self.label("wrong way:", SMALL_SIZE, RED),
            self.label("through that wall", SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.08).next_to(wall, DOWN, buff=0.18)
        aligned = Arrow(pred.get_right(), target.get_left(), buff=0.12, color=GREEN, stroke_width=4)

        self.play(FadeIn(net), FadeIn(target), FadeIn(target_label), FadeIn(pred), FadeIn(pred_label), FadeIn(meter), run_time=1.0)
        self.play(FadeIn(wall), GrowArrow(bad_arrow), FadeIn(wrong, shift=0.08 * UP), run_time=1.1)
        self.wait(8.0)
        self.play(FadeOut(wall), FadeOut(bad_arrow), FadeOut(wrong), run_time=0.6)
        for end, fill, color, label in [
            (np.array([1.15, -0.35, 0]), 0.55, ACCENT_2, "epoch 2"),
            (np.array([1.75, 0.12, 0]), 0.28, GREEN, "epoch 3"),
            (np.array([2.08, 0.32, 0]), 0.16, GREEN, "many updates"),
        ]:
            new_meter = self.loss_meter(fill=fill, color=color).move_to(meter)
            epoch = self.label(label, SMALL_SIZE, color).next_to(meter, UP, buff=0.5)
            self.play(pred.animate.move_to(end), Transform(meter, new_meter), Create(update), FadeIn(epoch), run_time=1.15)
            self.play(FadeOut(update), FadeOut(epoch), run_time=0.35)
        self.play(GrowArrow(aligned), pred_label.animate.next_to(pred, DOWN, buff=0.16), run_time=1.0)
        self.wait(7.0)
        self.play(FadeOut(Group(question, net, target, target_label, pred, pred_label, meter, aligned)), run_time=1.0)

    def backward_gaussian(self):
        question = self.hook_question("After training, each reverse transition is modeled as a Gaussian.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        xt = self.chain_node(r"x_t", color=RED).move_to([-3.65, 0.35, 0])
        net = self.neural_network_block().scale(0.82).move_to([-1.2, 0.35, 0])
        mean = Dot([1.0, 0.35, 0], radius=0.1, color=ACCENT_2)
        mean_label = self.eq(r"\mu_{\theta,t}(x_t)", size=29, color=ACCENT_2)
        ellipse = Ellipse(width=1.35, height=0.72, stroke_color=ACCENT_2, fill_color=ACCENT_2, fill_opacity=0.08, stroke_opacity=0.65).move_to(mean)
        sample = Dot([1.45, 0.08, 0], radius=0.07, color=GREEN)
        eq = self.display_equation(
            r"p_\theta(x_{t-1}\mid x_t)=\mathcal{N}\left(x_{t-1};\mu_{\theta,t}(x_t),\beta_t I\right)",
            width=9.0,
            size=29,
            accent=ACCENT_2,
        ).to_edge(DOWN, buff=0.52)
        labels = VGroup(
            self.word_row(["learned", "mean"], SMALL_SIZE, ACCENT_2, buff=0.16),
            self.word_row(["forward", "variance"], SMALL_SIZE, MUTED, buff=0.16),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.75, 0.52, 0])
        arrows = VGroup(
            Arrow(xt.get_right(), net.get_left(), buff=0.1, color=ACCENT, stroke_width=3),
            Arrow(net.get_right(), mean.get_left(), buff=0.12, color=ACCENT_2, stroke_width=3),
        )

        self.play(FadeIn(xt), FadeIn(net), GrowArrow(arrows[0]), run_time=0.8)
        mean_label.next_to(ellipse, UP, buff=0.18)
        self.play(GrowArrow(arrows[1]), FadeIn(mean), FadeIn(mean_label), Create(ellipse), FadeIn(sample), run_time=1.2)
        self.play(FadeIn(eq), FadeIn(labels), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(Group(question, xt, net, mean, mean_label, ellipse, sample, eq, labels, arrows)), run_time=1.0)

    def sampling_breadcrumbs(self):
        question = self.hook_question("Sampling follows learned Gaussian breadcrumbs back from noise.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        noise = self.gaussian_cloud(count=125, width=1.28, height=0.95, seed=77, color=ACCENT_2).move_to([4.15, 0.4, 0])
        data = self.clean_sample(scale=0.72, color=ACCENT).move_to([-4.15, 0.4, 0])
        path_points = [
            np.array([3.65, 0.38, 0]),
            np.array([2.65, 0.92, 0]),
            np.array([1.45, 0.22, 0]),
            np.array([0.25, 0.67, 0]),
            np.array([-1.0, -0.06, 0]),
            np.array([-2.32, 0.55, 0]),
            np.array([-3.45, 0.36, 0]),
        ]
        path = VMobject(color=GREEN, stroke_width=4)
        path.set_points_smoothly(path_points)
        ellipses = VGroup(*[Ellipse(width=0.7, height=0.36, stroke_color=ACCENT_2, stroke_opacity=0.48, fill_color=ACCENT_2, fill_opacity=0.06).move_to(p) for p in path_points[1:-1]])
        crumbs = VGroup(*[Dot(p, radius=0.065, color=ACCENT_2) for p in path_points[1:-1]])
        traveler = Dot(path_points[0], radius=0.095, color=RED)
        chain = self.display_equation(r"x_T\rightarrow x_{T-1}\rightarrow x_{T-2}\rightarrow\cdots", width=7.4, size=31, accent=GREEN).to_edge(DOWN, buff=0.58)
        note = VGroup(
            self.word_row(["Not", "an", "exact", "rewind", "of", "one", "image."], SMALL_SIZE, MUTED),
            self.word_row(["A", "learned", "path", "toward", "high-probability", "data."], SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.08).next_to(chain, UP, buff=0.22)

        self.play(FadeIn(noise), FadeIn(data), run_time=0.9)
        self.play(Create(path), LaggedStart(*[Create(e) for e in ellipses], lag_ratio=0.1), LaggedStart(*[FadeIn(c, scale=1.35) for c in crumbs], lag_ratio=0.1), run_time=1.8)
        self.play(FadeIn(traveler), FadeIn(chain), run_time=0.7)
        self.play(MoveAlongPath(traveler, path), run_time=3.4)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(18.5)
        self.play(FadeOut(Group(question, noise, data, path, ellipses, crumbs, traveler, chain, note)), run_time=1.0)

    def sde_teaser(self):
        question = self.hook_question("What if the steps become continuous?")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        axis = Line([-4.5, 0.4, 0], [4.5, 0.4, 0], color=DIM, stroke_width=2)
        ticks_sparse = VGroup(*[Line([x, 0.25, 0], [x, 0.55, 0], color=ACCENT_2, stroke_width=2) for x in np.linspace(-4.0, 4.0, 7)])
        ticks_dense = VGroup(*[Line([x, 0.28, 0], [x, 0.52, 0], color=ACCENT, stroke_width=1.6) for x in np.linspace(-4.0, 4.0, 25)])
        discrete = self.display_equation(r"x_T\rightarrow x_{T-1}\rightarrow\cdots\rightarrow x_0", width=7.5, size=31, accent=ACCENT_2).move_to([0, 1.35, 0])
        dt = self.display_equation(r"\Delta t\rightarrow 0", width=3.2, size=34, accent=ACCENT).move_to([0, -0.85, 0])
        curve = ParametricFunction(lambda t: np.array([-4.0 + 8.0 * t, -1.95 + 0.45 * np.sin(2 * PI * t), 0]), t_range=[0, 1, 0.02], color=ACCENT, stroke_width=4)
        teaser_words = self.word_row(["Next:", "stochastic", "differential", "equations."], SMALL_SIZE, TEXT, weight=BOLD, buff=0.11)
        teaser_box = self.soft_box(
            width=max(10.8, teaser_words.width + 0.75),
            height=max(0.56, teaser_words.height + 0.28),
            color=ACCENT,
            fill_opacity=0.075,
            stroke_opacity=0.62,
        )
        teaser_words.move_to(teaser_box)
        teaser = VGroup(teaser_box, teaser_words).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(discrete), Create(axis), FadeIn(ticks_sparse), run_time=1.0)
        self.play(Transform(ticks_sparse, ticks_dense), FadeIn(dt), run_time=1.3)
        self.play(Create(curve), FadeIn(teaser, shift=0.08 * UP), run_time=1.5)
        self.wait(8.0)
        self.play(FadeOut(Group(question, axis, ticks_sparse, discrete, dt, curve, teaser)), run_time=1.0)

    def module_box(self, text: str, color: str, width: float = 1.15) -> VGroup:
        box = self.soft_box(width, 0.58, color=color, fill_opacity=0.055, stroke_opacity=0.72)
        if text.startswith("\\") or "_" in text:
            label = self.eq(text, size=23, color=color)
        else:
            label = self.label(text, SMALL_SIZE, color)
        self.fit_to_box(label, width - 0.18, 0.34)
        label.move_to(box)
        return VGroup(box, label)

    def word_row(
        self,
        words: list[str],
        size: int = SMALL_SIZE,
        color: str = MUTED,
        weight: str = NORMAL,
        buff: float = 0.095,
    ) -> VGroup:
        return VGroup(
            *[
                Text(word, font=FONT_SUBTITLE, font_size=size, color=color, weight=weight, disable_ligatures=True)
                for word in words
            ]
        ).arrange(RIGHT, buff=buff)

    def gear_icon(self, color: str) -> VGroup:
        ring = Circle(radius=0.28, stroke_color=color, stroke_width=2.2)
        hub = Circle(radius=0.09, stroke_color=color, fill_color=color, fill_opacity=0.18, stroke_width=1.5)
        teeth = VGroup()
        for angle in np.linspace(0, TAU, 8, endpoint=False):
            tooth = Rectangle(width=0.055, height=0.16, stroke_width=0, fill_color=color, fill_opacity=0.42)
            tooth.move_to(0.34 * np.array([np.cos(angle), np.sin(angle), 0]))
            tooth.rotate(angle)
            teeth.add(tooth)
        return VGroup(teeth, ring, hub)

    def loss_meter(self, fill: float = 0.78, color: str = RED) -> VGroup:
        box = self.soft_box(2.5, 0.38, color=DIM, fill_opacity=0.28)
        bar = Rectangle(width=2.35 * fill, height=0.22, stroke_width=0, fill_color=color, fill_opacity=0.92)
        bar.align_to(box, LEFT).shift(RIGHT * 0.08)
        label = self.label("loss", SMALL_SIZE, color).next_to(box, UP, buff=0.14)
        return VGroup(box, bar, label)

    def brick_wall(self) -> VGroup:
        bricks = VGroup()
        for row in range(4):
            for col in range(3):
                brick = Rectangle(
                    width=0.34,
                    height=0.16,
                    stroke_width=1.0,
                    stroke_color=RED,
                    fill_color=RED,
                    fill_opacity=0.14,
                )
                brick.move_to(np.array([0.18 * (row % 2) + 0.37 * (col - 1), 0.18 * (row - 1.5), 0]))
                bricks.add(brick)
        frame = self.soft_box(1.38, 0.9, color=RED, fill_opacity=0.02, stroke_opacity=0.34)
        label = self.label("wall", SMALL_SIZE, RED).next_to(frame, UP, buff=0.08)
        return VGroup(frame, bricks, label)

    def neural_network_block(self) -> Group:
        asset = self.first_asset("icons/neural_network.svg", "icons/neural_network.png")
        if asset is not None:
            box = self.soft_box(2.1, 1.18, color=VIOLET, fill_opacity=0.055, stroke_opacity=0.72)
            icon = ImageMobject(str(asset))
            self.fit_to_box(icon, 1.7, 0.88)
            icon.move_to(box)
            icon.set_opacity(0.92)
            label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.11)
            return Group(box, icon, label)

        box = self.soft_box(2.1, 1.18, color=VIOLET, fill_opacity=0.06, stroke_opacity=0.72)
        layers = VGroup()
        for x, count in [(-0.58, 3), (0, 4), (0.58, 3)]:
            layer = VGroup(*[Dot([x, (i - (count - 1) / 2) * 0.2, 0], radius=0.032, color=VIOLET) for i in range(count)])
            layers.add(layer)
        edges = VGroup()
        for left, right in zip(layers[:-1], layers[1:]):
            for a in left:
                for b in right:
                    edges.add(Line(a.get_center(), b.get_center(), color=DIM, stroke_width=0.7))
        label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.11)
        return Group(box, edges, layers, label)
