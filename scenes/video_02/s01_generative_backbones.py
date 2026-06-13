from __future__ import annotations

from pathlib import Path
import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.v02_common import *


class V02GenerativeBackbones(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s01_generative_backbones.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        scene_start = self.time
        self.construct_intro(
            "Generative Era",
            "Text-to-image as a building block for video, 3D, and editing",
        )

        self.prompt_to_image()
        self.montage_examples()
        self.image_to_video()
        self.image_to_3d()
        self.two_backbones()
        self.text_to_image_centerpiece()
        self.hold_for_voiceover(scene_start, voiceover)
        if hasattr(self, "final_hold_group"):
            self.play(FadeOut(self.final_hold_group), run_time=0.8)

    def prompt_to_image(self):
        tag = self.section_tag("slide 4", IMAGE_BLUE).to_corner(UL, buff=0.48)
        prompt_text = "A robot cooking in the kitchen."
        empty_bar = self.prompt_bar("", width=10.2).move_to([0, 2.25, 0])
        typed = self.prompt_bar(prompt_text, width=10.2).move_to(empty_bar)
        robot_card = self.media_card(
            "Robot cooking",
            "text-to-image example",
            IMAGE_BLUE,
            width=4.65,
            height=3.25,
            asset_paths=("slides/s04_robot_cooking.png", "video2/slides/s04_robot_cooking.png"),
            kind="robot",
        ).move_to([0, -0.82, 0])
        robot_card.set_opacity(0)

        token_chips = VGroup(
            self.vector_chip("robot", TEXT_PURPLE, 1.12),
            self.vector_chip("cooking", TEXT_PURPLE, 1.38),
            self.vector_chip("kitchen", TEXT_PURPLE, 1.32),
        ).arrange(RIGHT, buff=0.16).scale(0.82)
        token_chips.move_to([0, 1.35, 0])

        guide = DashedLine(
            token_chips.get_bottom() + 0.12 * DOWN,
            robot_card[0].get_top() + 0.12 * UP,
            color=IMAGE_BLUE,
            stroke_width=2.4,
            dash_length=0.08,
        ).set_opacity(0.52)
        glow_box = SurroundingRectangle(robot_card[1], color=IMAGE_BLUE, buff=0.035, stroke_width=1.6)
        glow_box.set_fill(opacity=0)
        scan = Line(
            robot_card[1].get_left() + 0.07 * UP,
            robot_card[1].get_right() + 0.07 * UP,
            color=IMAGE_BLUE,
            stroke_width=5,
        ).set_opacity(0.58)
        scan.move_to(robot_card[1].get_top() + 0.08 * DOWN)

        rng = np.random.default_rng(15)
        particles = VGroup(*[
            Dot(
                token_chips.get_center()
                + np.array([rng.uniform(-1.8, 1.8), rng.uniform(-0.16, 0.16), 0]),
                radius=float(rng.uniform(0.012, 0.025)),
                color=self.mix_color(TEXT_PURPLE, IMAGE_BLUE, float(rng.random())),
                fill_opacity=0.9,
            )
            for _ in range(36)
        ])
        targets = VGroup(*[
            Dot(
                robot_card[1].get_center()
                + np.array([rng.uniform(-1.75, 1.75), rng.uniform(-0.72, 0.72), 0]),
                radius=0.01,
                color=IMAGE_BLUE,
                fill_opacity=0.0,
            )
            for _ in range(36)
        ])
        caption = self.takeaway("A sentence becomes a structured visual sample.", IMAGE_BLUE)
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(tag), FadeIn(empty_bar, shift=0.08 * UP), run_time=0.8)
        self.play(Transform(empty_bar, typed), run_time=1.25)
        self.play(
            LaggedStart(*[FadeIn(chip, shift=0.08 * DOWN) for chip in token_chips], lag_ratio=0.12),
            run_time=0.9,
        )
        self.play(Create(guide), FadeIn(particles), run_time=0.55)
        self.play(
            Transform(particles, targets),
            robot_card.animate.set_opacity(1),
            FadeIn(glow_box),
            run_time=1.25,
        )
        self.play(
            FadeIn(scan),
            scan.animate.move_to(robot_card[1].get_bottom() + 0.08 * UP).set_opacity(0.0),
            FadeIn(caption, shift=0.08 * UP),
            run_time=0.9,
        )
        self.play(
            FadeOut(guide),
            FadeOut(particles),
            FadeOut(glow_box),
            token_chips.animate.set_opacity(0.42),
            run_time=0.55,
        )
        self.wait(7.0)
        self.play(FadeOut(Group(tag, empty_bar, token_chips, robot_card, caption, scan)), run_time=0.9)

    def montage_examples(self):
        tag = self.section_tag("text-to-image examples", IMAGE_BLUE).to_corner(UL, buff=0.48)
        cards = Group(
            self.media_card("Robot cooking", "kitchen prompt", IMAGE_BLUE, 2.85, 2.35, ("slides/s04_robot_cooking.png",), "robot"),
            self.media_card("Robot graffiti", "brick wall prompt", NEGATIVE_ORANGE, 2.85, 2.35, ("slides/s04_robot_graffiti.png", "slides/s04_robot_graffiti.jpg"), "graffiti"),
            self.media_card("Raccoon", "formal clothes, tophat", TEXT_PURPLE, 2.85, 2.35, ("slides/s04_raccoon.png", "slides/s04_raccoon.jpg", "generated/raccoon_prompt_image.png"), "raccoon"),
            self.media_card("Alien pyramid", "hyper-real landscape", PUZZLE_GOLD, 2.85, 2.35, ("slides/s04_alien_pyramid.png",), "alien"),
        )
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.36, 0.32)).move_to([0, -0.15, 0])
        prompt = self.vector_chip("single line of text", TEXT_PURPLE, width=2.55).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tag), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(card, shift=0.12 * UP) for card in cards], lag_ratio=0.16), run_time=1.6)
        for card in cards:
            self.play(Circumscribe(card[0], color=card[0].get_stroke_color(), time_width=0.35), run_time=0.55)
        self.play(FadeIn(prompt, shift=0.08 * UP), run_time=0.7)
        self.wait(8.0)
        self.current_cards = cards
        self.play(FadeOut(VGroup(tag, prompt)), run_time=0.4)

    def image_to_video(self):
        cards = self.current_cards
        tag = self.section_tag("slide 5", IMAGE_BLUE).to_corner(UL, buff=0.48)
        background = self.media_card(
            "Lumiere-style grid",
            "temporal and spatial refinement",
            IMAGE_BLUE,
            width=5.25,
            height=2.75,
            asset_paths=("slides/s05_text_to_video_grid.png",),
            kind="video",
        ).move_to([0, 0.58, 0]).set_opacity(0.14)
        background[2].set_opacity(0.0)
        keyframes = Group(*[card.copy().scale(0.36) for card in cards])
        keyframes.arrange(RIGHT, buff=0.11).move_to([-2.35, -0.72, 0])
        strip = self.film_strip(3.65, 0.92, IMAGE_BLUE).move_to([2.45, -0.72, 0])
        flow_arrow = Arrow(
            keyframes.get_right() + 0.10 * RIGHT,
            strip.get_left() + 0.10 * LEFT,
            color=IMAGE_BLUE,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.14,
        )
        label = self.label("Text-to-Video", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([0, 2.35, 0])
        pipeline = VGroup(
            self.module("Text prompt", TEXT_PURPLE, 1.8),
            self.module("Keyframes", IMAGE_BLUE, 1.65),
            self.module("Super-resolution", PUZZLE_GOLD, 2.2),
            self.module("Video", GREEN, 1.35),
        ).arrange(RIGHT, buff=0.55).to_edge(DOWN, buff=0.42)
        arrows = VGroup(*[self.edge(pipeline[i], pipeline[i + 1], MUTED) for i in range(len(pipeline) - 1)])

        # cards is a Group (contains ImageMobject) — Transform is VMobject-only.
        # Cross-fade: shrink/fade cards out while keyframes fade in.
        self.play(FadeOut(cards, run_time=1.1), FadeIn(keyframes, run_time=1.1), FadeIn(tag), FadeIn(background), run_time=1.1)
        self.play(FadeIn(strip), GrowArrow(flow_arrow), FadeIn(label, shift=0.08 * DOWN), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(m, shift=0.06 * UP) for m in pipeline], lag_ratio=0.09),
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
            run_time=1.3,
        )
        self.play(background.animate.scale(1.02).shift(0.08 * RIGHT), strip.animate.shift(0.18 * RIGHT), run_time=1.4)
        self.wait(7.5)
        self.play(FadeOut(Group(tag, keyframes, background, strip, flow_arrow, label, pipeline, arrows)), run_time=0.9)

    def image_to_3d(self):
        tag = self.section_tag("slide 6", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        dream = self.media_card(
            "DreamFusion idea",
            "text-to-image + NeRF",
            PUZZLE_GOLD,
            width=4.55,
            height=3.25,
            asset_paths=("slides/s06_text_to_3d.png", "slides/s06_text_to_3.jpg"),
            kind="cube",
        ).move_to([-3.0, -0.05, 0])
        cube = self.cube_icon(PUZZLE_GOLD).scale(1.35).move_to([2.75, 0.15, 0])
        orbit = Circle(radius=1.25, color=PUZZLE_GOLD, stroke_opacity=0.22).move_to(cube)
        label = VGroup(
            self.label("Text-to-3D", SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_TITLE),
            self.label("Text-to-Image + NeRF as building blocks", SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.12).move_to([2.75, -1.7, 0])
        bridge = Arrow(dream.get_right(), cube.get_left(), color=PUZZLE_GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(tag), FadeIn(dream, shift=0.08 * RIGHT), run_time=0.8)
        self.play(GrowArrow(bridge), FadeIn(orbit), FadeIn(cube), FadeIn(label), run_time=1.1)
        self.play(Rotate(cube, angle=PI, about_point=cube.get_center()), orbit.animate.set_opacity(0.48), run_time=1.4)
        self.wait(8.5)
        self.play(FadeOut(Group(tag, dream, bridge, orbit, cube, label)), run_time=0.9)

    def two_backbones(self):
        tag = self.section_tag("slide 7", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        prompt = self.prompt_bar("A raccoon wearing formal clothes, wearing a tophat.", width=9.4).move_to([0, 2.25, 0]).scale(0.88)
        left_box = self.soft_box(5.9, 4.35, color=TEXT_PURPLE, fill_opacity=0.025, stroke_opacity=0.38).move_to([-3.15, -0.25, 0])
        right_box = self.soft_box(5.9, 4.35, color=IMAGE_BLUE, fill_opacity=0.025, stroke_opacity=0.38).move_to([3.15, -0.25, 0])
        left_title = self.label("Auto-regressive", SUBTITLE_SIZE, TEXT_PURPLE, font=FONT_TITLE).move_to([-3.15, 1.5, 0])
        right_title = self.label("Diffusion-based", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([3.15, 1.5, 0])

        ar_grid = VGroup()
        for r in range(6):
            for c in range(8):
                ar_grid.add(Square(side_length=0.22, stroke_color=DIM, stroke_width=0.7, fill_color=TEXT_PURPLE, fill_opacity=0.0))
        ar_grid.arrange_in_grid(rows=6, cols=8, buff=0.025).move_to([-3.15, -0.15, 0])
        filled = ar_grid.copy()
        for i, sq in enumerate(filled):
            sq.set_fill(self.mix_color(TEXT_PURPLE, PUZZLE_GOLD, (i % 8) / 7), opacity=0.46)
            sq.set_stroke(TEXT_PURPLE, opacity=0.55)
        tick = self.label("token by token", SMALL_SIZE, MUTED).move_to([-3.15, -1.78, 0])

        noise_frames = [
            self.first_asset(
                f"generated/diffusion_frames/diffuse_{pct:02d}.png",
                f"video2/generated/diffusion_frames/diffuse_{pct:02d}.png",
            )
            for pct in [0, 25, 50, 75, 100]
        ]
        if all(f is not None for f in noise_frames):
            # Use real noise-frame PNGs for a more cinematic denoising look
            img_samples = []
            for fp in noise_frames:
                img = ImageMobject(str(fp)).scale_to_fit_width(1.7)
                img.move_to([3.15, -0.12, 0])
                img_samples.append(img)
            samples = img_samples
        else:
            noise_levels = [0.95, 0.62, 0.34, 0.08, 0.0]
            samples = [self.noisy_sample(level, scale=1.2, seed=10 + i) for i, level in enumerate(noise_levels)]
            for sample in samples:
                sample.move_to([3.15, -0.12, 0])
        denoise = self.label("noise -> structure", SMALL_SIZE, MUTED).move_to([3.15, -1.78, 0])
        arrows = VGroup(
            Arrow(prompt.get_bottom(), left_box.get_top(), buff=0.16, color=TEXT_PURPLE, stroke_width=2.8),
            Arrow(prompt.get_bottom(), right_box.get_top(), buff=0.16, color=IMAGE_BLUE, stroke_width=2.8),
        )

        self.play(FadeIn(tag), FadeIn(prompt), FadeIn(left_box), FadeIn(right_box), FadeIn(left_title), FadeIn(right_title), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), FadeIn(samples[0]), run_time=0.9)
        self.play(LaggedStart(*[Transform(ar_grid[i], filled[i]) for i in range(len(ar_grid))], lag_ratio=0.015), FadeIn(tick), run_time=1.8)
        current = samples[0]
        self.add(current)
        for sample in samples[1:]:
            # Use cross-fade since samples may be ImageMobject (no align_rgbas)
            self.play(FadeOut(current, run_time=0.55), FadeIn(sample, run_time=0.55))
            self.remove(current)
            current = sample
        self.play(FadeIn(denoise), run_time=0.5)
        self.wait(14.0)
        # Use Group (not VGroup) so ImageMobject is accepted alongside VMobject
        self.play(FadeOut(Group(tag, prompt, left_box, right_box, left_title, right_title, ar_grid, current, tick, denoise, arrows)), run_time=0.9)

    def text_to_image_centerpiece(self):
        tag = self.section_tag("slide 8", IMAGE_BLUE).to_corner(UL, buff=0.48)
        center = self.module("Text-to-Image", IMAGE_BLUE, width=2.35, height=0.78).move_to(ORIGIN)
        nodes = VGroup(
            self.module("Text-to-Video", IMAGE_BLUE, 2.05).move_to([-4.0, 1.55, 0]),
            self.module("Text-to-3D", PUZZLE_GOLD, 1.75).move_to([4.0, 1.55, 0]),
            self.module("Image editing", TEXT_PURPLE, 1.9).move_to([-4.0, -1.55, 0]).set_opacity(0.52),
            self.module("Super-resolution", GREEN, 2.25).move_to([4.0, -1.55, 0]).set_opacity(0.52),
        )
        arrows = VGroup(*[
            Arrow(center.get_center(), node.get_center(), buff=0.55, color=node[0].get_stroke_color(), stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
            for node in nodes
        ])
        puzzle = VGroup(
            self.vector_chip("U-Net", PUZZLE_GOLD, 1.1),
            self.vector_chip("Diffusion", PUZZLE_GOLD, 1.45),
            self.vector_chip("CLIP", TEXT_PURPLE, 1.0),
            self.vector_chip("VQGAN", PUZZLE_GOLD, 1.25),
        ).arrange(RIGHT, buff=0.18).move_to(ORIGIN)
        next_label = self.label("Next: CLIP makes text and image meet.", SMALL_SIZE, TEXT).to_edge(DOWN, buff=0.48)

        self.play(FadeIn(tag), FadeIn(center, scale=0.9), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), LaggedStart(*[FadeIn(n, shift=0.06 * UP) for n in nodes], lag_ratio=0.1), run_time=1.4)
        self.wait(8.0)
        constellation = VGroup(center, nodes, arrows)
        self.play(FadeOut(constellation), FadeIn(puzzle), run_time=0.8)
        self.play(Circumscribe(puzzle[2], color=TEXT_PURPLE), FadeIn(next_label, shift=0.08 * UP), run_time=1.0)
        self.wait(4.0)
        self.final_hold_group = VGroup(tag, puzzle, next_label)
