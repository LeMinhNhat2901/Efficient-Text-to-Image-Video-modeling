from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


TEXT_PURPLE = VIOLET
IMAGE_BLUE = ACCENT
POSITIVE_GREEN = GREEN
NEGATIVE_ORANGE = "#FF8A3D"
PUZZLE_GOLD = ACCENT_2


class TextPixelsScene(DiffusionScene):
    """Shared visual helpers for Video 2: text, pixels, and embedding spaces."""

    def section_tag(self, text: str, color: str = ACCENT) -> VGroup:
        """Hide production-only slide/scene markers in the rendered video."""
        normalized = text.strip().lower()
        words = normalized.replace("+", " ").replace("•", " ").split()
        if {"slide", "slides", "scene"} & set(words) or normalized == "transition":
            return VGroup()
        return super().section_tag(text, color)

    def label(self, text: str, size: int = BODY_SIZE, color: str = TEXT, font: str | None = None) -> Text:
        """Video 2 typography: larger, calmer labels with a 3b1b-like hierarchy."""
        if size <= 13:
            size = 15
        elif size <= SMALL_SIZE:
            size = 20
        elif size <= BODY_SIZE:
            size = 24

        resolved_font = font or (FONT_TITLE if size >= SUBTITLE_SIZE else FONT_BODY)
        return Text(
            text,
            font=resolved_font,
            font_size=size,
            color=color,
        )

    def construct_intro(self, title: str, subtitle: str | None = None) -> None:
        self.add_background_texture("textures/dark_grid.jpg", "textures/subtle_noise.jpg", opacity=0.025)
        title_group = self.scene_title(title, subtitle)
        self.play(FadeIn(title_group, shift=0.16 * DOWN), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(title_group), run_time=0.6)

    def fast_clear(self, run_time: float = 0.28) -> None:
        """Clear dense scenes without animating every cell or edge individually."""
        cover = Rectangle(
            width=config.frame_width + 0.2,
            height=config.frame_height + 0.2,
            stroke_width=0,
            fill_color=BG,
            fill_opacity=1,
        ).set_z_index(1000)
        old_mobjects = list(self.mobjects)
        self.add(cover)
        self.remove(*old_mobjects)
        self.play(FadeOut(cover), run_time=run_time)

    def prompt_bar(self, text: str = "", width: float = 10.3, color: str = TEXT_PURPLE) -> VGroup:
        box = self.soft_box(width, 0.84, color=color, fill_opacity=0.045, stroke_opacity=0.68)
        left_dot = Dot(radius=0.055, color=color).move_to(box.get_left() + 0.34 * RIGHT)
        label = self.label(text, SMALL_SIZE, TEXT, font=FONT_BODY)
        self.fit_to_box(label, width - 1.0, 0.46)
        label.move_to(box.get_center() + 0.08 * RIGHT)
        cursor = Line(0.24 * UP, 0.24 * DOWN, color=color, stroke_width=2.4)
        cursor.next_to(label, RIGHT, buff=0.08)
        return VGroup(box, left_dot, label, cursor)

    def pixel_grid(
        self,
        rows: int = 9,
        cols: int = 16,
        side: float = 0.33,
        colors: tuple[str, ...] = (IMAGE_BLUE, TEXT_PURPLE, PUZZLE_GOLD),
        opacity: float = 0.34,
    ) -> VGroup:
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                mix = (r * 5 + c * 3) % len(colors)
                cell = Square(
                    side_length=side,
                    stroke_width=0.45,
                    stroke_color=colors[mix],
                    stroke_opacity=0.25,
                    fill_color=colors[mix],
                    fill_opacity=opacity * (0.55 + 0.45 * ((r + c) % 3) / 2),
                )
                cell.move_to(((c - (cols - 1) / 2) * side, ((rows - 1) / 2 - r) * side, 0))
                cells.add(cell)
        return cells

    def vector_chip(self, text: str, color: str, width: float = 2.0) -> VGroup:
        box = self.soft_box(width, 0.66, color=color, fill_opacity=0.055, stroke_opacity=0.68)
        label = self.label(text, SMALL_SIZE, color, font=FONT_BODY)
        self.fit_to_box(label, width - 0.22, 0.40)
        label.move_to(box)
        return VGroup(box, label)

    def math_label(self, tex: str, size: int = BODY_SIZE, color: str = TEXT, plain: str | None = None) -> Mobject:
        try:
            return MathTex(tex, font_size=size, color=color)
        except Exception:
            return self.label(plain or tex.replace("\\", ""), size, color, font=FONT_CODE)

    def math_chip(self, tex: str, color: str, width: float = 2.0, plain: str | None = None) -> VGroup:
        box = self.soft_box(width, 0.66, color=color, fill_opacity=0.055, stroke_opacity=0.68)
        label = self.math_label(tex, SMALL_SIZE, color, plain=plain)
        self.fit_to_box(label, width - 0.24, 0.42)
        label.move_to(box)
        return VGroup(box, label)

    def mixed_label(
        self,
        parts: list[tuple[str, str] | tuple[str, str, str]],
        size: int = SMALL_SIZE,
        color: str = TEXT,
        font: str | None = None,
        buff: float = 0.08,
    ) -> VGroup:
        mobs = VGroup()
        for part in parts:
            kind, value = part[0], part[1]
            part_color = part[2] if len(part) > 2 else color
            if kind == "math":
                mob = self.math_label(value, size + 2, part_color)
            else:
                mob = self.label(value, size, part_color, font=font or FONT_BODY)
            mobs.add(mob)
        mobs.arrange(RIGHT, buff=buff)
        return mobs

    def mixed_chip(
        self,
        parts: list[tuple[str, str] | tuple[str, str, str]],
        color: str,
        width: float = 2.0,
        height: float = 0.66,
    ) -> VGroup:
        box = self.soft_box(width, height, color=color, fill_opacity=0.055, stroke_opacity=0.68)
        label = self.mixed_label(parts, SMALL_SIZE, color, font=FONT_BODY, buff=0.07)
        self.fit_to_box(label, width - 0.24, height - 0.22)
        label.move_to(box)
        return VGroup(box, label)

    def media_card(
        self,
        title: str,
        caption: str,
        color: str = IMAGE_BLUE,
        width: float = 3.0,
        height: float = 2.45,
        asset_paths: tuple[str, ...] = (),
        kind: str = "image",
    ) -> Group:
        path = self.first_asset(*asset_paths) if asset_paths else None
        frame = self.soft_box(width, height, color=color, fill_opacity=0.045, stroke_opacity=0.75)
        image_h = height - 0.84
        image_w = width - 0.28
        if path is not None:
            visual = ImageMobject(str(path))
            self.fit_to_box(visual, image_w, image_h)
        else:
            visual = self.placeholder_visual(kind, image_w, image_h, color)
        visual.move_to(frame.get_center() + 0.26 * UP)
        title_mob = self.label(title, SMALL_SIZE, color, font=FONT_BODY)
        caption_mob = self.label(caption, 14, MUTED, font=FONT_BODY)
        self.fit_to_box(title_mob, width - 0.28, 0.34)
        self.fit_to_box(caption_mob, width - 0.28, 0.27)
        labels = VGroup(title_mob, caption_mob).arrange(DOWN, buff=0.04)
        labels.move_to(frame.get_bottom() + 0.39 * UP)
        return Group(frame, visual, labels)

    def placeholder_visual(self, kind: str, width: float, height: float, color: str) -> VGroup:
        canvas = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.05,
            stroke_width=1.0,
            stroke_color=color,
            stroke_opacity=0.32,
            fill_color="#151A1E",
            fill_opacity=1,
        )
        glow = self.pixel_grid(rows=5, cols=7, side=min(width / 8.2, height / 6.2), opacity=0.18)
        glow.move_to(canvas)
        if kind == "robot":
            icon = self.robot_icon(color).scale(0.78)
        elif kind == "graffiti":
            icon = self.robot_icon(NEGATIVE_ORANGE).scale(0.62)
            wall = self.brick_texture(width * 0.72, height * 0.55).set_opacity(0.55)
            return VGroup(canvas, wall.move_to(canvas), icon.move_to(canvas))
        elif kind == "raccoon":
            icon = self.raccoon_icon(color).scale(0.68)
        elif kind == "alien":
            icon = self.pyramid_icon(color).scale(0.78)
        elif kind == "video":
            icon = self.film_strip(width * 0.78, height * 0.58, color)
        elif kind == "cube":
            icon = self.cube_icon(color).scale(0.85)
        elif kind == "brain":
            icon = self.brain_icon(color).scale(0.85)
        elif kind == "car":
            icon = self.car_icon(color).scale(0.88)
        elif kind == "code":
            icon = self.code_icon(color).scale(0.82)
        else:
            icon = self.image_icon(color).scale(0.8)
        icon.move_to(canvas)
        return VGroup(canvas, glow, icon)

    def robot_icon(self, color: str) -> VGroup:
        head = RoundedRectangle(width=0.9, height=0.62, corner_radius=0.08, color=color, fill_color=color, fill_opacity=0.1)
        eye_l = Dot([-0.2, 0.08, 0], radius=0.045, color=TEXT)
        eye_r = Dot([0.2, 0.08, 0], radius=0.045, color=TEXT)
        mouth = Line([-0.22, -0.16, 0], [0.22, -0.16, 0], color=color, stroke_width=2.4)
        antenna = VGroup(Line([0, 0.31, 0], [0, 0.55, 0], color=color), Dot([0, 0.6, 0], radius=0.045, color=PUZZLE_GOLD))
        body = RoundedRectangle(width=1.05, height=0.54, corner_radius=0.06, color=color, fill_color=color, fill_opacity=0.06)
        body.next_to(head, DOWN, buff=0.08)
        return VGroup(body, head, eye_l, eye_r, mouth, antenna)

    def raccoon_icon(self, color: str) -> VGroup:
        face = Circle(radius=0.45, color=color, fill_color=color, fill_opacity=0.08)
        mask = Ellipse(width=0.72, height=0.28, color=MUTED, fill_color=MUTED, fill_opacity=0.2).move_to(face)
        eyes = VGroup(Dot([-0.17, 0.05, 0], radius=0.035, color=TEXT), Dot([0.17, 0.05, 0], radius=0.035, color=TEXT))
        hat = VGroup(
            Rectangle(width=0.48, height=0.28, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.18).move_to([0, 0.58, 0]),
            Line([-0.42, 0.42, 0], [0.42, 0.42, 0], color=PUZZLE_GOLD, stroke_width=4),
        )
        tie = Triangle(color=TEXT_PURPLE, fill_color=TEXT_PURPLE, fill_opacity=0.2).scale(0.18).rotate(PI).move_to([0, -0.52, 0])
        return VGroup(face, mask, eyes, hat, tie)

    def pyramid_icon(self, color: str) -> VGroup:
        pyramid = Polygon([-0.66, -0.38, 0], [0.0, 0.55, 0], [0.66, -0.38, 0], color=color, fill_color=color, fill_opacity=0.12)
        sun = Circle(radius=0.16, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.18).move_to([0.5, 0.46, 0])
        horizon = Line([-0.9, -0.42, 0], [0.9, -0.42, 0], color=MUTED, stroke_width=1.6)
        beams = VGroup(*[
            Line([0, 0.55, 0], [0.48 * np.cos(a), 0.55 + 0.48 * np.sin(a), 0], color=TEXT_PURPLE, stroke_opacity=0.45)
            for a in np.linspace(0.15 * PI, 0.85 * PI, 5)
        ])
        return VGroup(beams, pyramid, sun, horizon)

    def image_icon(self, color: str) -> VGroup:
        frame = RoundedRectangle(width=1.2, height=0.78, corner_radius=0.04, color=color, fill_color=color, fill_opacity=0.06)
        mountain = Polygon([-0.48, -0.22, 0], [-0.16, 0.12, 0], [0.08, -0.08, 0], [0.36, 0.22, 0], [0.52, -0.22, 0], color=color, fill_color=color, fill_opacity=0.15)
        sun = Dot([0.34, 0.22, 0], radius=0.05, color=PUZZLE_GOLD)
        return VGroup(frame, mountain, sun)

    def cube_icon(self, color: str) -> VGroup:
        front = Square(side_length=0.62, color=color, fill_color=color, fill_opacity=0.08)
        back = Square(side_length=0.62, color=color, fill_color=color, fill_opacity=0.04).shift(0.25 * RIGHT + 0.2 * UP)
        edges = VGroup(*[Line(a, b, color=color, stroke_width=1.8) for a, b in zip(front.get_vertices(), back.get_vertices())])
        return VGroup(back, front, edges)

    def film_strip(self, width: float, height: float, color: str) -> VGroup:
        outer = RoundedRectangle(width=width, height=height, corner_radius=0.04, color=color, fill_color=color, fill_opacity=0.05)
        frames = VGroup()
        for x in np.linspace(-width * 0.32, width * 0.32, 3):
            frames.add(Rectangle(width=width * 0.2, height=height * 0.52, color=color, fill_color=color, fill_opacity=0.13).move_to([x, 0, 0]))
        holes = VGroup()
        for y in (-height * 0.36, height * 0.36):
            for x in np.linspace(-width * 0.42, width * 0.42, 7):
                holes.add(Square(side_length=0.04, stroke_width=0, fill_color=TEXT, fill_opacity=0.45).move_to([x, y, 0]))
        return VGroup(outer, frames, holes)

    def brick_texture(self, width: float, height: float) -> VGroup:
        bricks = VGroup()
        for row in range(4):
            for col in range(5):
                brick = Rectangle(
                    width=width / 5.4,
                    height=height / 5.2,
                    color=NEGATIVE_ORANGE,
                    fill_color=NEGATIVE_ORANGE,
                    fill_opacity=0.08,
                    stroke_width=0.8,
                    stroke_opacity=0.28,
                )
                brick.move_to([
                    (col - 2) * width / 5 + (0.08 if row % 2 else 0),
                    (row - 1.5) * height / 4.6,
                    0,
                ])
                bricks.add(brick)
        return bricks

    def car_icon(self, color: str) -> VGroup:
        body = RoundedRectangle(width=1.22, height=0.42, corner_radius=0.12, color=color, fill_color=color, fill_opacity=0.1)
        roof = Polygon([-0.35, 0.12, 0], [-0.18, 0.38, 0], [0.34, 0.38, 0], [0.52, 0.12, 0], color=color, fill_color=color, fill_opacity=0.08)
        wheels = VGroup(Dot([-0.38, -0.23, 0], radius=0.09, color=TEXT), Dot([0.42, -0.23, 0], radius=0.09, color=TEXT))
        rays = VGroup(*[Line([0.72, 0.2 * np.sin(a), 0], [1.0, 0.28 * np.sin(a), 0], color=color, stroke_width=1.4) for a in np.linspace(-0.8, 0.8, 5)])
        return VGroup(body, roof, wheels, rays)

    def brain_icon(self, color: str) -> VGroup:
        lobes = VGroup(*[
            Circle(radius=r, color=color, fill_color=color, fill_opacity=0.07).move_to(p)
            for r, p in [(0.23, [-0.28, 0.04, 0]), (0.28, [0.0, 0.16, 0]), (0.24, [0.3, 0.04, 0]), (0.2, [-0.05, -0.18, 0])]
        ])
        stem = Line([0.1, -0.33, 0], [0.26, -0.58, 0], color=color, stroke_width=3)
        return VGroup(lobes, stem)

    def code_icon(self, color: str) -> VGroup:
        box = RoundedRectangle(width=1.22, height=0.8, corner_radius=0.04, color=color, fill_color=color, fill_opacity=0.06)
        lines = VGroup(*[
            Line([-0.42, y, 0], [0.48 - 0.1 * (i % 2), y, 0], color=color, stroke_width=2)
            for i, y in enumerate([0.22, 0.05, -0.12, -0.29])
        ])
        return VGroup(box, lines)

    def module(self, text: str, color: str, width: float = 1.65, height: float = 0.64) -> VGroup:
        height = max(height, 0.70)
        box = self.soft_box(width, height, color=color, fill_opacity=0.055, stroke_opacity=0.68)
        label = self.label(text, SMALL_SIZE, color, font=FONT_BODY)
        self.fit_to_box(label, width - 0.22, height - 0.24)
        label.move_to(box)
        return VGroup(box, label)

    def edge(self, start: Mobject, end: Mobject, color: str = MUTED, curved: bool = False) -> Mobject:
        if curved:
            return CurvedArrow(start.get_right(), end.get_left(), angle=-TAU / 8, color=color, stroke_width=2.8)
        return Arrow(start.get_right(), end.get_left(), buff=0.1, color=color, stroke_width=2.8, max_tip_length_to_length_ratio=0.18)
