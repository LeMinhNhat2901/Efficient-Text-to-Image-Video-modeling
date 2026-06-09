from __future__ import annotations

import hashlib
import math
import re
import random
import shutil
from pathlib import Path

import numpy as np
from manim import *
from manim.utils.color import ManimColor

from config import *


class DiffusionScene(MovingCameraScene):
    """Shared style and small visual primitives for the diffusion video."""

    _latex_available = shutil.which("latex") is not None

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def scene_title(self, text: str, subtitle: str | None = None) -> VGroup:
        title = Text(text, font_size=TITLE_SIZE, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        if subtitle is None:
            return VGroup(title)
        sub = Text(subtitle, font_size=SMALL_SIZE, color=MUTED)
        sub.next_to(title, DOWN, buff=0.12)
        return VGroup(title, sub)

    def label(self, text: str, size: int = BODY_SIZE, color: str = TEXT) -> Text:
        return Text(text, font_size=size, color=color)

    def eq(self, tex: str, size: int = EQ_SIZE, color: str = TEXT, plain: str | None = None) -> Mobject:
        if DiffusionScene._latex_available:
            try:
                return MathTex(tex, font_size=size, color=color)
            except Exception:
                DiffusionScene._latex_available = False
        try:
            return self._mathtext_svg(tex, size=size, color=color)
        except Exception:
            pass
        fallback = plain or self._tex_to_readable_text(tex)
        return Text(fallback, font_size=max(12, int(size * 0.58)), color=color)

    def _mathtext_svg(self, tex: str, size: int = EQ_SIZE, color: str = TEXT) -> SVGMobject:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        cache_dir = Path("assets") / "equations"
        cache_dir.mkdir(parents=True, exist_ok=True)
        math = self._mathtext_compatible(tex)
        digest = hashlib.sha1(f"{math}|{size}|{color}".encode("utf-8")).hexdigest()[:16]
        svg_path = cache_dir / f"eq_{digest}.svg"

        if not svg_path.exists():
            fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
            fig.patch.set_alpha(0)
            fig.text(
                0,
                0,
                f"${math}$",
                color=color,
                fontsize=max(8, size),
                fontfamily="serif",
                math_fontfamily="cm",
            )
            fig.savefig(svg_path, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.015)
            plt.close(fig)

        mob = SVGMobject(str(svg_path))
        mob.set_color(color)
        return mob

    def _mathtext_compatible(self, tex: str) -> str:
        text = tex.strip()
        text = text.replace(r"\text{learned reverse}", r"\mathrm{learned\;reverse}")
        text = text.replace(r"\text{true reverse}", r"\mathrm{true\;reverse}")
        text = re.sub(r"\\text\{([^{}]+)\}", lambda m: r"\mathrm{" + m.group(1).replace(" ", r"\;") + "}", text)
        text = text.replace(r"\boldsymbol", r"\mathbf")
        text = text.replace(r"\mathbb{E}", r"\mathbb{E}")
        return text

    def display_equation(
        self,
        tex: str,
        plain: str | None = None,
        width: float = 7.0,
        size: int = EQ_SIZE,
        color: str = TEXT,
        accent: str = ACCENT,
    ) -> VGroup:
        equation = self.eq(tex, size=size, color=color, plain=plain)
        if equation.width > width - 0.65:
            equation.scale_to_fit_width(width - 0.65)
        box = self.soft_box(
            width=max(width, equation.width + 0.55),
            height=max(0.72, equation.height + 0.45),
            color=accent,
            fill_opacity=0.055,
            stroke_opacity=0.42,
        )
        equation.move_to(box)
        return VGroup(box, equation)

    def fit_to_box(self, mob: Mobject, max_width: float, max_height: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def compact_eq(self, tex: str, size: int = 26, color: str = TEXT, plain: str | None = None) -> Mobject:
        label = Text(plain or self._compact_math_text(tex), font_size=max(12, int(size * 0.62)), color=color)
        return self.fit_to_box(label, max_width=0.72, max_height=0.34)

    def _compact_math_text(self, tex: str) -> str:
        text = self._tex_to_readable_text(tex)
        text = text.replace("{", "").replace("}", "")
        return text.replace(" ", "")

    def section_tag(self, text: str, color: str = ACCENT) -> VGroup:
        dot = Dot(radius=0.055, color=color)
        label = Text(text.upper(), font_size=SMALL_SIZE, color=color, weight=BOLD)
        return VGroup(dot, label).arrange(RIGHT, buff=0.12)

    def top_left_tag(self, text: str, color: str = ACCENT) -> VGroup:
        tag = self.section_tag(text, color)
        tag.to_edge(LEFT, buff=0.34)
        tag.shift(2.55 * UP)
        return tag

    def _tex_to_readable_text(self, tex: str) -> str:
        text = tex

        text = re.sub(r"\\sqrt\{([^{}]+)\}", r"sqrt(\1)", text)
        text = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", text)

        def unwrap_command(match: re.Match[str]) -> str:
            return match.group(1)

        for command in (r"mathbf", r"boldsymbol", r"mathcal", r"mathbb"):
            text = re.sub(rf"\\{command}\{{([^{{}}]+)\}}", unwrap_command, text)

        replacements = {
            r"\rightarrow": "->",
            r"\to": "->",
            r"\left": "",
            r"\right": "",
            r"\quad": " ",
            r"\,": " ",
            r"\sqrt": "sqrt",
            r"\frac": "frac",
            r"\partial": "d",
            r"\nabla": "grad",
            r"\cdot": ".",
            r"\sim": "~",
            r"\ldots": "...",
            r"\dots": "...",
            r"\epsilon": "epsilon",
            r"\theta": "theta",
            r"\beta": "beta",
            r"\alpha": "alpha",
            r"\sigma": "sigma",
            r"\mu": "mu",
            r"\prod": "prod",
            r"\mathbb": "",
            r"\mathcal": "",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"\^\{([^{}]+)\}", r"^\1", text)
        text = re.sub(r"_\{([^{}]+)\}", r"_\1", text)
        text = text.replace("{", "").replace("}", "")
        return " ".join(text.replace("\\", "").split())

    def mix_color(self, color_a: str, color_b: str, alpha: float) -> ManimColor:
        return ManimColor(color_a).interpolate(ManimColor(color_b), alpha)

    def soft_box(
        self,
        width: float,
        height: float,
        color: str = DIM,
        fill_opacity: float = 0.18,
        stroke_opacity: float = 0.5,
    ) -> RoundedRectangle:
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_width=1.2,
            stroke_color=color,
            stroke_opacity=stroke_opacity,
            fill_color=color,
            fill_opacity=fill_opacity,
        )

    def clean_sample(self, scale: float = 1.0, color: str = ACCENT) -> VGroup:
        circle = Circle(radius=0.42 * scale, color=color, stroke_width=5)
        core = Dot(radius=0.055 * scale, color=ACCENT_2)
        slash = Line(
            circle.get_left() + 0.13 * RIGHT,
            circle.get_right() - 0.13 * RIGHT,
            color=color,
            stroke_width=4,
        )
        slash.rotate(0.7)
        return VGroup(circle, slash, core)

    def noisy_sample(self, noise_level: float, scale: float = 1.0, seed: int = 1) -> VGroup:
        rng = random.Random(seed)
        base = self.clean_sample(scale=scale, color=self.mix_color(ACCENT, MUTED, noise_level))
        base.set_opacity(max(0.12, 1.0 - 0.72 * noise_level))
        dots = VGroup()
        count = int(10 + 70 * noise_level)
        radius = 0.58 * scale
        for _ in range(count):
            x = rng.uniform(-radius, radius)
            y = rng.uniform(-radius, radius)
            if x * x + y * y > radius * radius * 1.15:
                continue
            dot = Dot(
                point=np.array([x, y, 0.0]),
                radius=rng.uniform(0.010, 0.024) * scale,
                color=self.mix_color(ACCENT_2, TEXT, rng.random()),
                fill_opacity=rng.uniform(0.35, 0.9),
            )
            dots.add(dot)
        return VGroup(base, dots)

    def gaussian_cloud(
        self,
        count: int = 120,
        width: float = 2.2,
        height: float = 1.5,
        seed: int = 0,
        color: str = ACCENT_2,
    ) -> VGroup:
        rng = np.random.default_rng(seed)
        dots = VGroup()
        for x, y in rng.normal(size=(count, 2)):
            point = np.array([0.28 * width * x, 0.28 * height * y, 0])
            radius = float(rng.uniform(0.012, 0.026))
            dots.add(Dot(point=point, radius=radius, color=color, fill_opacity=0.55))
        return dots

    def wiener_path(
        self,
        length: float = 4.8,
        height: float = 1.3,
        steps: int = 55,
        seed: int = 0,
        color: str = ACCENT,
    ) -> VMobject:
        rng = np.random.default_rng(seed)
        xs = np.linspace(-length / 2, length / 2, steps)
        increments = rng.normal(scale=0.25, size=steps)
        ys = np.cumsum(increments)
        ys = ys - ys[0]
        max_abs = max(0.001, float(np.max(np.abs(ys))))
        ys = ys / max_abs * height / 2
        points = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        path = VMobject(color=color, stroke_width=3)
        path.set_points_as_corners(points)
        return path

    def chain_node(self, text: str, color: str = ACCENT) -> VGroup:
        disk = Circle(radius=0.35, stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
        label = self.compact_eq(text, size=26, color=TEXT)
        label.move_to(disk)
        return VGroup(disk, label)

    def beta_bar(self, value: ValueTracker, width: float = 4.8) -> VGroup:
        box = self.soft_box(width=width, height=0.2, color=DIM, fill_opacity=0.25)
        fill = always_redraw(
            lambda: Rectangle(
                width=max(0.001, width * value.get_value()),
                height=0.2,
                stroke_width=0,
                fill_color=ACCENT_2,
                fill_opacity=0.95,
            ).align_to(box, LEFT).move_to(box.get_left() + RIGHT * width * value.get_value() / 2)
        )
        label = always_redraw(
            lambda: self.label(
                f"beta_t = {value.get_value():.2f}",
                size=SMALL_SIZE,
                color=ACCENT_2,
            ).next_to(box, UP, buff=0.15)
        )
        return VGroup(box, fill, label)

    def small_arrow(self, start: Mobject, end: Mobject, color: str = MUTED) -> Arrow:
        return Arrow(
            start.get_right(),
            end.get_left(),
            buff=0.12,
            color=color,
            stroke_width=2.8,
            max_tip_length_to_length_ratio=0.16,
        )

    def pulse(self, mob: Mobject, color: str = ACCENT_2):
        return Succession(
            mob.animate.set_color(color).scale(1.06),
            mob.animate.set_color(TEXT).scale(1 / 1.06),
        )
