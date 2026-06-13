from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.base_scene import DiffusionScene
from config import *


P3_BG = "#0E1117"
FLOW_BLUE = "#2F80ED"
FLOW_CYAN = "#00E5FF"
DIFFUSION_GOLD = "#F2C94C"
REVERSE_ORANGE = "#FFB703"
SCORE_PINK = "#FF4081"
FAIL_RED = "#FF2D55"
LOW_PURPLE = "#241329"


class Part3Scene(DiffusionScene):
    """Shared Part 3 visual primitives."""

    def setup(self):
        super().setup()
        self.camera.background_color = P3_BG

    def part3_title(self, text: str, subtitle: str | None = None) -> VGroup:
        title = self.scene_title(text, subtitle)
        title.set_z_index(20)
        return title

    def p3_background(self) -> None:
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.024)

    def glow(self, center: np.ndarray, color: str, rings: int = 5, start: float = 0.18) -> VGroup:
        return VGroup(
            *[
                Circle(
                    radius=start + 0.1 * i,
                    stroke_color=color,
                    stroke_width=1.3,
                    stroke_opacity=0.32 / (i + 1),
                ).move_to(center)
                for i in range(rings)
            ]
        )

    def breadcrumb_path(self, reverse: bool = True, color: str = REVERSE_ORANGE) -> tuple[VGroup, VGroup, VMobject]:
        xs = np.linspace(-4.8, 4.8, 7)
        ys = np.array([0.8, 0.25, 0.65, -0.05, 0.28, -0.34, 0.0])
        points = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        if reverse:
            points = list(reversed(points))
        nodes = VGroup(*[Dot(p, radius=0.075, color=color) for p in points])
        arrows = VGroup(
            *[
                Arrow(points[i], points[i + 1], buff=0.12, color=color, stroke_width=2.8, max_tip_length_to_length_ratio=0.18)
                for i in range(len(points) - 1)
            ]
        )
        curve = VMobject(color=color, stroke_width=4, stroke_opacity=0.85)
        curve.set_points_smoothly(points)
        return nodes, arrows, curve

    def dense_curve(self, color: str = FLOW_CYAN) -> VMobject:
        curve = ParametricFunction(
            lambda t: np.array([
                -4.75 + 9.5 * t,
                0.1 + 0.62 * np.sin(2.2 * PI * t) + 0.18 * np.sin(8 * PI * t),
                0,
            ]),
            t_range=[0, 1, 0.015],
            color=color,
            stroke_width=4,
        )
        return curve

    def time_ticks(self, dense: bool = False, color: str = MUTED) -> VGroup:
        count = 29 if dense else 7
        ticks = VGroup()
        xs = np.linspace(-4.8, 4.8, count)
        for i, x in enumerate(xs):
            tick = Line([x, -2.15, 0], [x, -1.9, 0], color=color, stroke_width=1.6 if dense else 2.2)
            ticks.add(tick)
            if not dense:
                label = self.label(["T", "T-1", "T-2", "...", "2", "1", "0"][i], 13, MUTED).next_to(tick, DOWN, buff=0.09)
                ticks.add(label)
        return ticks

    def particle_cloud(self, count: int, spread: float, center: np.ndarray, color: str, seed: int, opacity: float = 0.65) -> VGroup:
        rng = np.random.default_rng(seed)
        dots = VGroup()
        for _ in range(count):
            offset = np.array([rng.normal(scale=spread), rng.normal(scale=0.58 * spread), 0])
            dots.add(Dot(center + offset, radius=float(rng.uniform(0.016, 0.033)), color=color, fill_opacity=opacity))
        return dots

    def brownian_paths(self, start: np.ndarray, count: int = 18, seed: int = 1, color: str = DIFFUSION_GOLD) -> tuple[VGroup, VGroup]:
        rng = np.random.default_rng(seed)
        paths = VGroup()
        endpoints = VGroup()
        for _ in range(count):
            points = [start + np.array([rng.normal(scale=0.08), rng.normal(scale=0.06), 0])]
            pos = points[0].copy()
            for step in range(7):
                drift = np.array([0.16, 0.0, 0])
                jitter = np.array([rng.normal(scale=0.18), rng.normal(scale=0.14), 0])
                pos = pos + drift + jitter
                points.append(pos.copy())
            path = VMobject(color=color, stroke_width=1.4, stroke_opacity=0.42)
            path.set_points_smoothly(points)
            paths.add(path)
            endpoints.add(Dot(points[-1], radius=0.026, color=color, fill_opacity=0.72))
        return paths, endpoints

    def density_curve(self, width: float = 1.0, height: float = 1.0, color: str = DIFFUSION_GOLD) -> VMobject:
        return ParametricFunction(
            lambda t: np.array([
                -3.2 + 6.4 * t,
                -1.1 + height * np.exp(-((t - 0.5) ** 2) / (0.035 * width)),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=color,
            stroke_width=4,
        )

    def histogram_bars(self, color: str = DIFFUSION_GOLD) -> VGroup:
        heights = [0.18, 0.32, 0.56, 0.9, 1.18, 0.9, 0.56, 0.32, 0.18]
        bars = VGroup()
        for i, h in enumerate(heights):
            bar = Rectangle(width=0.42, height=h, stroke_width=0, fill_color=color, fill_opacity=0.62)
            bar.move_to([-1.9 + i * 0.48, -1.55 + h / 2, 0])
            bars.add(bar)
        return bars

    def streamlines(self, width: float = 9.4, count: int = 7, color: str = FLOW_BLUE) -> VGroup:
        lines = VGroup()
        for j, y in enumerate(np.linspace(-1.45, 1.45, count)):
            curve = ParametricFunction(
                lambda t, yy=y, jj=j: np.array([
                    -width / 2 + width * t,
                    yy + 0.12 * np.sin(2 * PI * t + jj * 0.65),
                    0,
                ]),
                t_range=[0, 1, 0.02],
                color=color,
                stroke_width=1.8,
                stroke_opacity=0.54,
            )
            lines.add(curve)
        return lines

    def vector_field_arrows(
        self,
        center: np.ndarray = ORIGIN,
        x_span: float = 2.4,
        y_span: float = 1.5,
        color: str = FLOW_BLUE,
        inward: bool = False,
        spread: bool = False,
        opacity: float = 0.75,
    ) -> VGroup:
        arrows = VGroup()
        for x in np.linspace(-x_span, x_span, 6):
            for y in np.linspace(-y_span, y_span, 4):
                pos = center + np.array([x, y, 0])
                if inward:
                    vec = -0.22 * np.array([x, y, 0]) + np.array([0.18 * np.sin(y), -0.05 * np.cos(x), 0])
                elif spread:
                    vec = 0.2 * np.array([x, y, 0]) + np.array([0.22, 0.08 * np.sin(x), 0])
                else:
                    vec = np.array([0.38, -0.18 * y, 0])
                if np.linalg.norm(vec[:2]) < 0.03:
                    continue
                arrows.add(Arrow(pos, pos + vec, buff=0, color=color, stroke_width=2.0, max_tip_length_to_length_ratio=0.2).set_opacity(opacity))
        return arrows

    def oil_blob(self) -> VGroup:
        blobs = VGroup()
        colors = [FLOW_CYAN, DIFFUSION_GOLD, VIOLET, SCORE_PINK]
        for i, color in enumerate(colors):
            blob = Ellipse(
                width=2.25 - 0.22 * i,
                height=0.82 + 0.08 * i,
                stroke_color=color,
                fill_color=color,
                stroke_opacity=0.34,
                fill_opacity=0.12,
            )
            blob.rotate((i - 1.5) * 0.18).shift(np.array([0.12 * i, 0.04 * np.sin(i), 0]))
            blobs.add(blob)
        return blobs

    def neural_network_block(self, width: float = 2.25, height: float = 1.25) -> Group:
        asset = self.first_asset("icons/neural_network.svg", "icons/neural_network.png")
        box = self.soft_box(width, height, color=VIOLET, fill_opacity=0.055, stroke_opacity=0.72)
        if asset is not None:
            icon = ImageMobject(str(asset))
            self.fit_to_box(icon, width - 0.45, height - 0.32)
            icon.move_to(box)
            icon.set_opacity(0.9)
            label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.1)
            return Group(box, icon, label)

        layers = VGroup()
        for x, count in [(-0.55, 3), (0, 4), (0.55, 3)]:
            layers.add(VGroup(*[Dot([x, (i - (count - 1) / 2) * 0.2, 0], radius=0.032, color=VIOLET) for i in range(count)]))
        edges = VGroup()
        for left, right in zip(layers[:-1], layers[1:]):
            for a in left:
                for b in right:
                    edges.add(Line(a.get_center(), b.get_center(), color=DIM, stroke_width=0.7))
        label = self.label("network", SMALL_SIZE, VIOLET).next_to(box, DOWN, buff=0.1)
        return Group(box, edges, layers, label)

    def distorted_sample(self) -> VGroup:
        face = VGroup(
            Circle(radius=0.48, stroke_color=FAIL_RED, fill_color=FAIL_RED, fill_opacity=0.06, stroke_width=3),
            Dot([-0.18, 0.12, 0], radius=0.035, color=FAIL_RED),
            Dot([0.22, 0.02, 0], radius=0.035, color=FAIL_RED),
            Arc(radius=0.22, start_angle=0.1, angle=-PI * 0.72, color=FAIL_RED, stroke_width=3).shift(0.1 * DOWN),
        )
        glitch = VGroup(
            Line([-0.65, 0.3, 0], [0.6, 0.18, 0], color=SCORE_PINK, stroke_width=2),
            Line([-0.55, -0.18, 0], [0.7, -0.34, 0], color=FLOW_CYAN, stroke_width=2),
        )
        return VGroup(face, glitch)

