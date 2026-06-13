from __future__ import annotations

from pathlib import Path
import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


class V02TextPixelsOpening(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s00_text_pixels_opening.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        self.add_background_texture("textures/subtle_noise.jpg", "textures/dark_grid.jpg", opacity=0.03)

        self.opening_title()
        self.tutorial_route()
        self.route_to_pixels()

    def opening_title(self):
        rng = np.random.default_rng(24)
        seed = Dot(radius=0.055, color=IMAGE_BLUE).move_to(ORIGIN)
        particles = VGroup()
        for _ in range(64):
            angle = rng.uniform(0, TAU)
            radius = rng.uniform(0.25, 3.7)
            p = Dot(
                point=[radius * np.cos(angle), radius * np.sin(angle) * 0.55, 0],
                radius=rng.uniform(0.012, 0.028),
                color=self.mix_color(IMAGE_BLUE, TEXT_PURPLE, float(rng.random())),
                fill_opacity=rng.uniform(0.35, 0.9),
            )
            particles.add(p)

        title = self.label("Cornerstones of the Text-to-Pixels Journey", 40, TEXT, font=FONT_TITLE)
        self.fit_to_box(title, 12.2, 0.82)
        title.move_to([0, 0.35, 0])
        speaker = self.label("Srikumar Ramalingam - Google Research", SMALL_SIZE, MUTED)
        speaker.next_to(title, DOWN, buff=0.2)
        scan = Rectangle(width=0.12, height=1.55, stroke_width=0, fill_color=IMAGE_BLUE, fill_opacity=0.42)
        scan.move_to(title.get_left() + 0.3 * LEFT)

        self.play(FadeIn(seed, scale=1.6), run_time=0.45)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.4) for p in particles], lag_ratio=0.01),
            seed.animate.set_opacity(0),
            run_time=1.2,
        )
        self.play(Write(title), FadeIn(speaker, shift=0.08 * UP), run_time=1.4)
        self.play(scan.animate.move_to(title.get_right() + 0.4 * RIGHT), title.animate.set_color(IMAGE_BLUE), run_time=0.9)
        self.play(title.animate.set_color(TEXT), FadeOut(scan), run_time=0.35)
        self.wait(2.2)
        self.play(FadeOut(VGroup(seed, particles, title, speaker)), run_time=0.9)

    def tutorial_route(self):
        tag = self.section_tag("tutorial map", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        route = VMobject(color=DIM, stroke_width=4.0)
        points = [
            np.array([-5.6, -0.8, 0]),
            np.array([-3.6, 1.1, 0]),
            np.array([-1.15, 0.15, 0]),
            np.array([1.75, 1.0, 0]),
            np.array([4.8, -0.25, 0]),
        ]
        route.set_points_smoothly(points)
        names = [
            ("Richard Hartley", "Mathematics of Diffusion", IMAGE_BLUE),
            ("Srikumar Ramalingam", "Text-to-Pixels Journey", PUZZLE_GOLD),
            ("Sadeep Jayasumana", "MarkovGen", TEXT_PURPLE),
            ("Ameesh Makadia", "Latent Representations", GREEN),
        ]
        stations = VGroup()
        for i, (name, topic, color) in enumerate(names):
            dot = Dot(points[i], radius=0.085 if i != 1 else 0.13, color=color)
            halo = Circle(radius=0.23 if i != 1 else 0.36, color=color, stroke_opacity=0.35).move_to(dot)
            label = VGroup(
                self.label(name, 15, TEXT if i == 1 else MUTED),
                self.label(topic, 12, color),
            ).arrange(DOWN, buff=0.04)
            label.next_to(dot, UP if i % 2 else DOWN, buff=0.22)
            stations.add(VGroup(halo, dot, label))
        here = self.vector_chip("YOU ARE HERE", PUZZLE_GOLD, width=2.05)
        here.next_to(stations[1], UP, buff=0.48)

        self.play(FadeIn(tag), Create(route), run_time=1.25)
        self.play(LaggedStart(*[FadeIn(s, shift=0.06 * UP) for s in stations], lag_ratio=0.17), run_time=1.8)
        self.play(FadeIn(here, shift=0.08 * DOWN), Circumscribe(stations[1], color=PUZZLE_GOLD), run_time=1.4)
        self.wait(4.5)

        self.route_group = VGroup(tag, route, stations, here)

    def route_to_pixels(self):
        route_group = self.route_group
        pixel_grid = self.pixel_grid(rows=9, cols=16, side=0.42, opacity=0.022).move_to(ORIGIN).set_opacity(0.0)
        four_pixels = VGroup(*[
            Square(side_length=0.55, stroke_color=PUZZLE_GOLD, stroke_width=1.2, fill_color=PUZZLE_GOLD, fill_opacity=0.32).move_to(p)
            for p in [np.array([-2.1, 0.45, 0]), np.array([-0.7, 0.45, 0]), np.array([0.7, 0.45, 0]), np.array([2.1, 0.45, 0])]
        ])
        phrase = VGroup(
            self.label("Text", 38, TEXT_PURPLE, font=FONT_TITLE),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=3).scale(0.9),
            self.label("Pixels", 38, IMAGE_BLUE, font=FONT_TITLE),
        ).arrange(RIGHT, buff=0.32).move_to(ORIGIN)
        phrase.set_stroke(BG, width=3.0, opacity=0.8, background=True)
        phrase.set_z_index(3)
        phrase_panel = self.soft_box(7.8, 2.55, color=IMAGE_BLUE, fill_opacity=0.0, stroke_opacity=0.28)
        phrase_panel.set_fill("#0D1117", opacity=0.96)
        phrase_panel.move_to([0, -0.16, 0])
        phrase_panel.set_z_index(2)
        token_specs = [
            ("A", TEXT_PURPLE, 0.68),
            ("prompt", IMAGE_BLUE, 1.28),
            ("becomes", GREEN, 1.48),
            ("visual", PUZZLE_GOLD, 1.22),
            ("structure", TEXT_PURPLE, 1.62),
        ]
        tokens = VGroup()
        for text, color, width in token_specs:
            box = RoundedRectangle(
                width=width,
                height=0.48,
                corner_radius=0.06,
                stroke_width=1.4,
                stroke_color=color,
                stroke_opacity=0.92,
                fill_color=BG,
                fill_opacity=0.88,
            )
            label = self.label(text, 17, TEXT, font=FONT_BODY)
            self.fit_to_box(label, width - 0.18, 0.32)
            label.move_to(box)
            tokens.add(VGroup(box, label))
        tokens.arrange(RIGHT, buff=0.14).move_to([0, -0.9, 0])
        tokens.set_z_index(3)

        prompt = self.prompt_bar("A sentence describing a world", width=8.35)
        prompt.move_to([0, 1.42, 0]).scale(0.92)
        prompt.set_z_index(3)
        input_label = self.vector_chip("text prompt", TEXT_PURPLE, width=1.72).scale(0.82)
        input_label.next_to(prompt, UP, buff=0.18)
        input_label.set_z_index(3)

        world_frame = self.soft_box(4.25, 2.05, color=IMAGE_BLUE, fill_opacity=0.035, stroke_opacity=0.72)
        world_grid = self.pixel_grid(
            rows=5,
            cols=9,
            side=0.23,
            colors=(IMAGE_BLUE, TEXT_PURPLE, PUZZLE_GOLD, GREEN),
            opacity=0.34,
        ).move_to(world_frame)
        horizon = Line(world_frame.get_left() + 0.45 * RIGHT, world_frame.get_right() + 0.45 * LEFT, color=MUTED, stroke_width=1.4)
        horizon.shift(0.48 * DOWN)
        sun = Circle(radius=0.18, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.2)
        sun.move_to(world_frame.get_center() + np.array([0.82, 0.46, 0]))
        world = VGroup(world_frame, world_grid, horizon, sun).move_to([0, -0.74, 0])
        world.set_z_index(3)
        output_label = self.vector_chip("visual structure", IMAGE_BLUE, width=2.28).scale(0.82)
        output_label.next_to(world, DOWN, buff=0.16)
        output_label.set_z_index(3)
        final_arrow = Arrow(
            prompt.get_bottom() + 0.06 * DOWN,
            world.get_top() + 0.08 * UP,
            color=IMAGE_BLUE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        final_arrow.set_z_index(3)
        finale_panel = self.soft_box(10.25, 5.55, color=IMAGE_BLUE, fill_opacity=0.0, stroke_opacity=0.22)
        finale_panel.set_fill("#0D1117", opacity=0.96)
        finale_panel.move_to([0, 0.0, 0])
        finale_panel.set_z_index(2)
        finale = VGroup(finale_panel, input_label, prompt, final_arrow, world, output_label)

        self.play(Transform(route_group, four_pixels), run_time=1.0)
        self.play(Transform(route_group, pixel_grid.set_opacity(1.0)), run_time=1.35)
        self.play(FadeIn(phrase_panel), FadeIn(phrase, shift=0.08 * UP), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(t, shift=0.08 * UP) for t in tokens], lag_ratio=0.1), run_time=1.0)
        self.play(
            tokens.animate.shift(0.35 * RIGHT),
            phrase[1].animate.set_color(IMAGE_BLUE),
            phrase[2].animate.set_color(PUZZLE_GOLD),
            run_time=1.2,
        )
        self.wait(3.2)
        self.play(
            FadeOut(phrase),
            FadeOut(phrase_panel),
            FadeOut(tokens),
            FadeOut(route_group),
            run_time=0.9,
        )
        self.play(FadeIn(finale_panel), FadeIn(input_label, shift=0.05 * DOWN), FadeIn(prompt, shift=0.08 * DOWN), run_time=0.65)
        self.play(GrowArrow(final_arrow), FadeIn(world, shift=0.08 * UP), FadeIn(output_label, shift=0.05 * UP), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(finale), run_time=0.9)
