from pathlib import Path
import os
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class RoadmapOverview(DiffusionScene):
    TARGET_DURATION = 154.3
    NOISE_LEVELS = tuple(np.linspace(0.0, 1.0, 13))

    def construct(self):
        start = self.time
        self.camera.background_color = BG
        voiceover = Path("tts") / "outputs" / "s00_roadmap.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        self.add_background_texture("textures/subtle_noise.jpg", "textures/subtle_noise.png", opacity=0.03)

        self.cold_open()
        self.dimensional_shift_bridge()
        self.spiral_distribution()
        self.forward_reverse_map()
        self.reverse_question()
        self.title_promise()
        self.hold_to_time(start, self.TARGET_DURATION)

    def cold_open(self):
        current = self.puppy_panel(0.0).move_to(ORIGIN).scale(1.52)
        caption = self.label("Clean data: recognizable structure", BODY_SIZE, TEXT).next_to(current, DOWN, buff=0.28)

        self.play(FadeIn(current, scale=0.98), FadeIn(caption), run_time=1.3)
        self.wait(4.8)

        detail_labels = VGroup(
            self.label("eyes", SMALL_SIZE, ACCENT),
            self.label("nose", SMALL_SIZE, ACCENT_2),
            self.label("fur", SMALL_SIZE, GREEN),
            self.label("background", SMALL_SIZE, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        detail_labels.next_to(current, RIGHT, buff=0.55)
        detail_lines = VGroup(
            Line(detail_labels[0].get_left(), current.get_center() + np.array([0.25, 0.28, 0]), color=ACCENT, stroke_width=1.4),
            Line(detail_labels[1].get_left(), current.get_center() + np.array([0.04, 0.02, 0]), color=ACCENT_2, stroke_width=1.4),
            Line(detail_labels[2].get_left(), current.get_center() + np.array([-0.22, -0.28, 0]), color=GREEN, stroke_width=1.4),
            Line(detail_labels[3].get_left(), current.get_center() + np.array([0.52, -0.46, 0]), color=MUTED, stroke_width=1.2),
        )
        self.play(LaggedStart(*[FadeIn(label, shift=0.06 * LEFT) for label in detail_labels], lag_ratio=0.12), Create(detail_lines), run_time=1.5)
        self.wait(4.0)

        noise_prompt = self.label("Add a little random noise at every step.", BODY_SIZE, ACCENT_2)
        noise_prompt.to_edge(UP, buff=0.62)
        dissolving_caption = self.label("Noise slowly dissolves the image.", BODY_SIZE, MUTED).next_to(current, DOWN, buff=0.28)
        self.play(
            FadeIn(noise_prompt, shift=0.1 * DOWN),
            Transform(caption, dissolving_caption),
            detail_labels.animate.set_opacity(0.35),
            detail_lines.animate.set_opacity(0.2),
            run_time=0.9,
        )

        frame_time = 13.2 / (len(self.NOISE_LEVELS) - 1)
        for level in self.NOISE_LEVELS[1:]:
            next_panel = self.puppy_panel(level).move_to(current).scale(1.52)
            self.play(Transform(current, next_panel), run_time=frame_time)

        noise_caption = self.label("After many steps: pure noise", BODY_SIZE, ACCENT_2).next_to(current, DOWN, buff=0.28)
        entropy = self.takeaway("Forward process: controlled destruction.", ACCENT)
        entropy.to_edge(DOWN, buff=0.46)
        self.play(Transform(caption, noise_caption), FadeIn(entropy, shift=0.08 * UP), run_time=1.0)
        self.wait(5.2)

        self.play(
            FadeOut(noise_prompt),
            FadeOut(detail_labels),
            FadeOut(detail_lines),
            FadeOut(current),
            FadeOut(caption),
            FadeOut(entropy),
            run_time=1.4,
        )

    def forward_reverse_map(self):
        time_value = ValueTracker(0)
        counter = always_redraw(
            lambda: self.label(f"t = {int(time_value.get_value())}", BODY_SIZE, ACCENT_2).to_corner(DR, buff=0.48)
        )

        levels = (0.0, 0.18, 0.52, 0.88, 1.0)
        panels = Group()
        for level in levels:
            panels.add(self.puppy_panel(level).scale(0.44))
        panels.arrange(RIGHT, buff=0.33).move_to([0.05, 0.82, 0])

        arrows = VGroup(
            *[
                Arrow(
                    panels[i].get_right(),
                    panels[i + 1].get_left(),
                    buff=0.08,
                    color=ACCENT,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.18,
                )
                for i in range(len(panels) - 1)
            ]
        )
        state_labels = VGroup(
            *[
                self.compact_eq(tex, size=28, plain=plain).next_to(panel, DOWN, buff=0.2)
                for panel, tex, plain in zip(
                    panels,
                    (r"x_0", r"x_1", r"x_2", r"\cdots", r"x_T"),
                    ("x_0", "x_1", "x_2", "...", "x_T"),
                )
            ]
        )

        forward_text = self.label("Forward: designed", BODY_SIZE, ACCENT)
        reverse_text = self.label("Reverse: learned", BODY_SIZE, GREEN)
        forward_text.move_to([-2.55, -2.0, 0])
        reverse_text.move_to([2.55, -2.0, 0])
        forward_arrow = Arrow(forward_text.get_right() + 0.12 * RIGHT, reverse_text.get_left() - 0.12 * RIGHT, color=ACCENT, stroke_width=4)
        reverse_arrow = CurvedArrow(
            panels[-1].get_bottom() + 0.78 * DOWN,
            panels[0].get_bottom() + 0.78 * DOWN,
            angle=-TAU / 7,
            color=GREEN,
            stroke_width=4,
        )

        self.play(FadeIn(counter), LaggedStart(*[FadeIn(panel) for panel in panels], lag_ratio=0.08), run_time=1.8)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.12), FadeIn(state_labels), time_value.animate.set_value(4), run_time=2.4)
        self.wait(4.5)
        self.play(FadeIn(forward_text), GrowArrow(forward_arrow), run_time=1.0)
        self.wait(1.8)
        self.play(FadeIn(reverse_text), Create(reverse_arrow), run_time=1.3)
        self.wait(5.0)

        promise = self.takeaway(
            "The reverse process will look like probability, not magic.",
            ACCENT_2,
        )
        promise.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(promise, shift=0.08 * UP), run_time=1.0)
        self.wait(5.5)

        self.play(
            FadeOut(Group(panels)),
            FadeOut(VGroup(arrows, state_labels, forward_text, reverse_text, forward_arrow, reverse_arrow, promise, counter)),
            run_time=1.2,
        )

    def dimensional_shift_bridge(self):
        title = self.hook_question("An image is one point in a huge space.")
        panel = self.puppy_panel(0.0).scale(0.92).move_to([-3.9, 0.35, 0])
        panel_label = self.label("pixels", SMALL_SIZE, MUTED).next_to(panel, DOWN, buff=0.18)
        sample_pixels = VGroup(
            Square(side_length=0.16, fill_color="#1E2A35", fill_opacity=1, stroke_color=ACCENT, stroke_width=1.4).move_to(panel.get_center() + np.array([-0.33, 0.22, 0])),
            Square(side_length=0.16, fill_color="#B68B5D", fill_opacity=1, stroke_color=ACCENT_2, stroke_width=1.4).move_to(panel.get_center() + np.array([0.12, 0.02, 0])),
            Square(side_length=0.16, fill_color="#5B7F32", fill_opacity=1, stroke_color=GREEN, stroke_width=1.4).move_to(panel.get_center() + np.array([0.45, -0.32, 0])),
        )

        origin = np.array([0.65, -1.0, 0])
        r_axis = Arrow(origin, origin + 1.7 * RIGHT, buff=0, color=RED, stroke_width=3)
        g_axis = Arrow(origin, origin + 1.5 * UP, buff=0, color=GREEN, stroke_width=3)
        b_axis = Arrow(origin, origin + 1.05 * (LEFT * 0.78 + UP * 0.58), buff=0, color=ACCENT, stroke_width=3)
        rgb_axes = VGroup(r_axis, g_axis, b_axis)
        rgb_labels = VGroup(
            self.label("R", 16, RED).next_to(r_axis.get_end(), RIGHT, buff=0.08),
            self.label("G", 16, GREEN).next_to(g_axis.get_end(), UP, buff=0.08),
            self.label("B", 16, ACCENT).next_to(b_axis.get_end(), LEFT, buff=0.08),
        )
        rgb_space = VGroup(rgb_axes, rgb_labels)
        rgb_points = VGroup(
            Dot(origin + 1.08 * RIGHT + 0.42 * UP, radius=0.055, color=ACCENT),
            Dot(origin + 0.82 * RIGHT + 0.78 * UP + 0.18 * LEFT, radius=0.055, color=ACCENT_2),
            Dot(origin + 0.38 * RIGHT + 0.52 * UP + 0.24 * LEFT, radius=0.055, color=GREEN),
        )
        rgb_caption = self.label("three sampled RGB coordinates", SMALL_SIZE, TEXT).next_to(rgb_space, DOWN, buff=0.28)

        data_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.6, 1.6, 1],
            x_length=3.0,
            y_length=2.3,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.1},
        ).move_to([4.0, 0.15, 0])
        data_dot = Dot(data_axes.c2p(0.38, 0.38), radius=0.08, color=ACCENT)
        dot_label = self.label("one image = one data point", SMALL_SIZE, ACCENT).next_to(data_axes, DOWN, buff=0.18)
        arrow_to_rgb = Arrow(panel.get_right(), rgb_space.get_left(), buff=0.22, color=MUTED, stroke_width=3)
        arrow_to_point = Arrow(rgb_space.get_right(), data_axes.get_left(), buff=0.22, color=GREEN, stroke_width=3)

        self.play(FadeIn(title, shift=0.1 * DOWN), FadeIn(panel), FadeIn(panel_label), run_time=1.0)
        self.play(LaggedStart(*[Indicate(pixel, color=TEXT, scale_factor=1.35) for pixel in sample_pixels], lag_ratio=0.22), run_time=1.8)
        flying = sample_pixels.copy()
        self.add(flying)
        self.play(
            LaggedStart(
                *[Transform(flying[i], rgb_points[i]) for i in range(3)],
                lag_ratio=0.12,
            ),
            GrowArrow(arrow_to_rgb),
            FadeIn(rgb_space),
            FadeIn(rgb_caption),
            run_time=2.2,
        )
        self.wait(4.5)
        self.play(GrowArrow(arrow_to_point), FadeIn(data_axes), run_time=1.0)
        self.play(Transform(flying, VGroup(data_dot.copy(), data_dot.copy(), data_dot.copy())), FadeIn(data_dot), FadeIn(dot_label), run_time=1.4)
        self.wait(7.0)
        self.play(FadeOut(Group(title, panel, panel_label, sample_pixels, flying, arrow_to_rgb, rgb_space, rgb_caption, arrow_to_point, data_axes, data_dot, dot_label)), run_time=1.1)

    def title_promise(self):
        title = self.scene_title(
            "Mathematics of Diffusion",
            "Markov Chains and the Reverse Process",
        )
        keywords = VGroup(
            self.section_tag("Markov chains", ACCENT),
            self.section_tag("Bayes rule", ACCENT_2),
            self.section_tag("learning the reverse step", GREEN),
        ).arrange(RIGHT, buff=0.45)
        keywords.next_to(title, DOWN, buff=0.58)
        keywords.shift(0.18 * DOWN)

        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(item, shift=0.06 * UP) for item in keywords], lag_ratio=0.18), run_time=1.4)
        self.wait(6.0)
        self.play(FadeOut(VGroup(title, keywords)), run_time=0.9)

    def spiral_distribution(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=7.2,
            y_length=4.6,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.2},
        ).move_to([0.8, 0.0, 0])
        tag = self.section_tag("data as points", ACCENT).to_corner(UL, buff=0.42)
        self.play(FadeIn(tag), Create(axes), run_time=1.6)

        spiral_frames = self.load_spiral_frames()
        dots = self.dots_from_points(spiral_frames[0] if spiral_frames is not None else None, seed=8).move_to(axes.get_center())
        self.play(LaggedStart(*[FadeIn(dot, scale=0.6) for dot in dots], lag_ratio=0.01), run_time=4.2)
        ordered = self.label("t = 0: an ordered spiral distribution", SMALL_SIZE, ACCENT)
        ordered.next_to(axes, DOWN, buff=0.2)
        self.play(FadeIn(ordered), run_time=0.8)
        self.wait(8.0)

        t_label = self.label("Forward process: add noise step by step", BODY_SIZE, TEXT)
        t_label.to_edge(UP, buff=0.55)
        self.play(FadeIn(t_label, shift=0.1 * DOWN), run_time=0.9)
        if spiral_frames is not None:
            frame_indices = np.linspace(1, len(spiral_frames) - 1, 7, dtype=int)
            for frame_index in frame_indices:
                next_dots = self.dots_from_points(spiral_frames[frame_index]).move_to(axes.get_center())
                self.play(Transform(dots, next_dots), run_time=8.5 / len(frame_indices))
        else:
            noisy = self.noise_cloud_like(dots, seed=18)
            noisy.move_to(axes.get_center())
            self.play(Transform(dots, noisy), run_time=8.5)
        noisy_label = self.label("t = T: a high-entropy noise cloud", SMALL_SIZE, ACCENT_2)
        noisy_label.next_to(axes, DOWN, buff=0.2)
        self.play(Transform(ordered, noisy_label), run_time=1.0)
        self.wait(8.0)

        self.play(FadeOut(VGroup(tag, axes, dots, ordered, t_label)), run_time=1.4)

    def reverse_question(self):
        question = self.hook_question("Can we run this process backward?")
        noise = self.gaussian_cloud(count=150, width=2.1, height=1.35, seed=33, color=ACCENT_2).move_to([-3.6, 0.25, 0])
        spiral = self.spiral_points(seed=34).scale(0.92).move_to([3.6, 0.25, 0])
        arrow = CurvedArrow(noise.get_right(), spiral.get_left(), angle=-TAU / 7, color=GREEN, stroke_width=5)
        labels = VGroup(
            self.label("unstructured noise", SMALL_SIZE, ACCENT_2).next_to(noise, DOWN, buff=0.2),
            self.label("high-probability data region", SMALL_SIZE, GREEN).next_to(spiral, DOWN, buff=0.2),
        )
        heart = self.takeaway("Reverse learns a path back to structure.", GREEN)
        heart.to_edge(DOWN, buff=0.46)

        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)
        self.play(FadeIn(noise), FadeIn(labels[0]), run_time=1.0)
        self.play(Create(arrow), FadeIn(spiral), FadeIn(labels[1]), run_time=2.2)
        self.play(FadeIn(heart, shift=0.08 * UP), run_time=1.0)
        self.wait(16.0)
        self.play(FadeOut(VGroup(question, noise, spiral, arrow, labels, heart)), run_time=0.9)

    def puppy_panel(self, noise_level: float) -> Group:
        frame_asset = self.noise_frame_asset(noise_level)
        asset = self.puppy_asset()
        uses_precomputed_frame = frame_asset is not None
        if frame_asset is not None:
            base = ImageMobject(str(frame_asset)).scale_to_fit_height(2.42)
            noise = VGroup()
        elif asset is not None:
            base = ImageMobject(str(asset)).scale_to_fit_height(3.0)
            noise = self.procedural_noise_overlay(noise_level)
        else:
            base = self.puppy_placeholder()
            noise = self.procedural_noise_overlay(noise_level)

        if not uses_precomputed_frame:
            base.set_opacity(max(0.08, 1.0 - 0.86 * noise_level))
        frame = RoundedRectangle(width=3.75, height=2.65, corner_radius=0.08, stroke_color=DIM, stroke_width=1.2)
        return Group(frame, base, noise)

    def puppy_asset(self) -> Path | None:
        for name in ("puppy.jpg", "puppy.png", "puppy.jpeg"):
            candidate = Path("assets") / name
            if candidate.exists():
                return candidate
        return None

    def noise_frame_asset(self, noise_level: float) -> Path | None:
        index = min(
            range(len(self.NOISE_LEVELS)),
            key=lambda i: abs(self.NOISE_LEVELS[i] - noise_level),
        )
        frame = Path("assets") / "generated" / "noise_frames" / f"puppy_noise_{index:02d}.png"
        return frame if frame.exists() else None

    def procedural_noise_overlay(self, noise_level: float) -> VGroup:
        rng = np.random.default_rng(int(1000 * noise_level) + 3)
        noise = VGroup()
        count = int(18 + 170 * noise_level)
        for _ in range(count):
            x = rng.uniform(-1.72, 1.72)
            y = rng.uniform(-1.12, 1.12)
            dot = Square(
                side_length=float(rng.uniform(0.025, 0.07)),
                stroke_width=0,
                fill_color=self.mix_color(ACCENT_2, TEXT, float(rng.random())),
                fill_opacity=float(0.12 + 0.82 * noise_level),
            ).move_to([x, y, 0])
            noise.add(dot)
        return noise

    def puppy_placeholder(self) -> VGroup:
        head = Circle(radius=0.62, color=TEXT, stroke_width=3, fill_color="#E8C28B", fill_opacity=1)
        ear_l = Circle(radius=0.25, color="#9B6B3E", fill_color="#9B6B3E", fill_opacity=1).move_to([-0.48, 0.45, 0])
        ear_r = Circle(radius=0.25, color="#9B6B3E", fill_color="#9B6B3E", fill_opacity=1).move_to([0.48, 0.45, 0])
        eye_l = Dot([-0.22, 0.12, 0], radius=0.04, color=BLACK)
        eye_r = Dot([0.22, 0.12, 0], radius=0.04, color=BLACK)
        nose = Dot([0, -0.08, 0], radius=0.055, color=BLACK)
        mouth = Arc(radius=0.18, start_angle=210 * DEGREES, angle=120 * DEGREES, color=BLACK, stroke_width=2).shift(0.18 * DOWN)
        body = RoundedRectangle(width=1.35, height=0.75, corner_radius=0.2, stroke_color=TEXT, fill_color="#E8C28B", fill_opacity=1)
        body.next_to(head, DOWN, buff=-0.1)
        return VGroup(body, ear_l, ear_r, head, eye_l, eye_r, nose, mouth)

    def spiral_points(self, seed: int = 0) -> VGroup:
        rng = np.random.default_rng(seed)
        dots = VGroup()
        count = 130
        for i in range(count):
            t = 0.25 + 3.9 * i / count
            r = 0.18 + 0.22 * t
            x = r * np.cos(2.25 * t) + rng.normal(0, 0.035)
            y = r * np.sin(2.25 * t) + rng.normal(0, 0.035)
            dots.add(Dot([x, y, 0], radius=0.022, color=ACCENT, fill_opacity=0.82))
        return dots

    def noise_cloud_like(self, reference: VGroup, seed: int = 0) -> VGroup:
        rng = np.random.default_rng(seed)
        dots = VGroup()
        for _ in reference:
            x, y = rng.normal(0, 0.82, size=2)
            dots.add(Dot([x, y, 0], radius=0.022, color=self.mix_color(ACCENT, ACCENT_2, float(rng.random())), fill_opacity=0.62))
        return dots

    def load_spiral_frames(self) -> np.ndarray | None:
        path = Path("assets") / "generated" / "spiral_frames" / "spiral_diffusion.npy"
        if path.exists():
            return np.load(path)
        return None

    def dots_from_points(self, points: np.ndarray | None, seed: int = 0) -> VGroup:
        if points is None:
            return self.spiral_points(seed=seed)
        rng = np.random.default_rng(seed + 88)
        dots = VGroup()
        for x, y in points:
            mix = float(min(1.0, max(0.0, 0.5 + 0.25 * rng.normal())))
            dots.add(
                Dot(
                    [float(x), float(y), 0],
                    radius=0.022,
                    color=self.mix_color(ACCENT, ACCENT_2, mix),
                    fill_opacity=0.72,
                )
            )
        return dots
