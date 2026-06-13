from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


SANA_NEON = "#00E5FF"
VAR_GOLD = "#F2C94C"
LINEAR_GREEN = "#27E08A"
HOT_PINK = "#FF4081"


class V02SanaVar(TextPixelsScene):
    """Slides 61-62: SANA and VAR."""

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s10_sana_var.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Modern Acceleration Engines",
            "SANA for diffusion, VAR for autoregression",
        )

        self.two_paths_hook()
        self.sana_redesign()
        self.deep_compression()
        self.linear_attention_curve()
        self.sana_pipeline()
        self.var_rethink_ar()
        self.var_next_scale()
        self.summary_bridge()

    def image_box(self, asset: str, width: float, height: float, color: str) -> Group:
        path = self.first_asset(asset)
        if path:
            img = ImageMobject(str(path))
            self.fit_to_box(img, width, height)
        else:
            img = self.placeholder_visual("image", width, height, color)
        frame = self.soft_box(width + 0.18, height + 0.18, color=color, fill_opacity=0.035, stroke_opacity=0.66)
        img.move_to(frame)
        return Group(frame, img)

    def speedometer(self) -> VGroup:
        arc = Arc(radius=0.92, start_angle=PI, angle=-PI, color=SANA_NEON, stroke_width=5)
        ticks = VGroup(*[
            Line([0.74 * np.cos(a), 0.74 * np.sin(a), 0], [0.9 * np.cos(a), 0.9 * np.sin(a), 0], color=MUTED, stroke_width=2)
            for a in np.linspace(PI, 0, 7)
        ])
        needle = Line([0, 0, 0], [0.62, 0.38, 0], color=VAR_GOLD, stroke_width=5)
        hub = Dot(radius=0.08, color=VAR_GOLD)
        return VGroup(arc, ticks, needle, hub)

    def two_paths_hook(self):
        title = self.hook_question("Two ways to accelerate text-to-image generation.", color=TEXT)
        left = self.soft_box(5.6, 3.7, color=SANA_NEON, fill_opacity=0.035, stroke_opacity=0.52).move_to([-3.25, -0.2, 0])
        right = self.soft_box(5.6, 3.7, color=VAR_GOLD, fill_opacity=0.035, stroke_opacity=0.52).move_to([3.25, -0.2, 0])
        left_text = self.label("Make Diffusion lighter\n-> SANA", 34, SANA_NEON, font=FONT_TITLE).move_to(left)
        right_text = self.label("Rethink Autoregression\n-> VAR", 34, VAR_GOLD, font=FONT_TITLE).move_to(right)
        meter = self.speedometer().scale(0.92).move_to([0, -2.38, 0])
        note = self.label("same goal: faster, lighter, more scalable", SMALL_SIZE, MUTED, font=FONT_CODE).next_to(meter, DOWN, buff=0.12)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(left), FadeIn(right), FadeIn(left_text), FadeIn(right_text), run_time=1.0)
        self.play(FadeIn(meter), Rotate(meter[2], angle=-0.65, about_point=meter.get_center()), FadeIn(note), run_time=1.1)
        self.wait(7.0)
        self.fast_clear()

    def two_tower_unet(self) -> VGroup:
        left = VGroup(*[
            self.soft_box(0.8 + i * 0.25, 0.42, color=IMAGE_BLUE, fill_opacity=0.07, stroke_opacity=0.55)
            for i in range(4)
        ]).arrange(DOWN, buff=0.12)
        right = left.copy()
        bridge = self.soft_box(0.9, 0.42, color=IMAGE_BLUE, fill_opacity=0.07, stroke_opacity=0.55)
        group = VGroup(left, bridge, right).arrange(RIGHT, buff=0.28)
        label = self.label("U-Net denoiser", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE).next_to(group, DOWN, buff=0.14)
        return VGroup(group, label)

    def sana_redesign(self):
        title = self.hook_question("SANA: diffusion redesigned as a Linear Diffusion Transformer.", color=SANA_NEON)
        unet = self.two_tower_unet().scale(1.05).move_to([-3.3, 0.25, 0])
        dit = VGroup()
        for i in range(5):
            block = self.module(f"DiT\nblock {i + 1}", SANA_NEON, 1.05, 0.82)
            dit.add(block)
        dit.arrange(RIGHT, buff=0.18).move_to([2.65, 0.25, 0])
        dit_title = self.label("Linear DiT", 34, SANA_NEON, font=FONT_TITLE).next_to(dit, UP, buff=0.28)
        arrow = Arrow(unet.get_right(), dit.get_left(), buff=0.2, color=SANA_NEON, stroke_width=3)
        soft_wording = self.takeaway("Not a dramatic red X: a redesigned denoising backbone.", SANA_NEON).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(unet), run_time=0.9)
        self.play(GrowArrow(arrow), unet.animate.set_opacity(0.42), FadeIn(dit), FadeIn(dit_title), run_time=1.3)
        self.play(FadeIn(soft_wording), run_time=0.8)
        self.wait(55.0)
        self.fast_clear()

    def compression_grid(self, cols: int, rows: int, side: float, color: str) -> VGroup:
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                cell = Square(side_length=side, color=color, stroke_width=0.5, fill_color=color, fill_opacity=0.16)
                cell.move_to([(c - (cols - 1) / 2) * side, ((rows - 1) / 2 - r) * side, 0])
                grid.add(cell)
        return grid

    def deep_compression(self):
        title = self.hook_question("SANA pushes latent compression deeper: 8x -> 32x.", color=LINEAR_GREEN)
        image = self.image_box("external_57_63/high_res_image.jpg", 2.0, 2.0, SANA_NEON).move_to([-5.0, 0.15, 0])
        grid8 = self.compression_grid(8, 8, 0.16, VAR_GOLD).move_to([-1.1, 0.15, 0])
        grid32 = self.compression_grid(4, 4, 0.18, LINEAR_GREEN).move_to([3.15, 0.15, 0])
        box8 = self.soft_box(2.25, 2.25, color=VAR_GOLD, fill_opacity=0.02, stroke_opacity=0.45).move_to(grid8)
        box32 = self.soft_box(1.32, 1.32, color=LINEAR_GREEN, fill_opacity=0.02, stroke_opacity=0.65).move_to(grid32)
        lbls = VGroup(
            self.label("image", SMALL_SIZE, TEXT, font=FONT_CODE).next_to(image, DOWN, buff=0.12),
            self.label("typical 8x\nmore tokens", SMALL_SIZE, VAR_GOLD, font=FONT_CODE).next_to(box8, DOWN, buff=0.15),
            self.label("SANA 32x\nfewer tokens", SMALL_SIZE, LINEAR_GREEN, font=FONT_CODE).next_to(box32, DOWN, buff=0.15),
        )
        arr1 = Arrow(image.get_right(), box8.get_left(), buff=0.12, color=VAR_GOLD, stroke_width=2.8)
        arr2 = Arrow(box8.get_right(), box32.get_left(), buff=0.12, color=LINEAR_GREEN, stroke_width=2.8)
        note = self.takeaway("Smaller latent representation means lower attention and feed-forward cost.", LINEAR_GREEN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(image), FadeIn(lbls[0]), run_time=0.8)
        self.play(GrowArrow(arr1), FadeIn(box8), FadeIn(grid8), FadeIn(lbls[1]), run_time=1.0)
        self.play(GrowArrow(arr2), FadeIn(box32), FadeIn(grid32), FadeIn(lbls[2]), run_time=1.0)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(9.0)
        self.fast_clear()

    def linear_attention_curve(self):
        title = self.hook_question("Quadratic attention grows fast. Linear attention stays tame.", color=SANA_NEON)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            x_length=6.2,
            y_length=3.8,
            axis_config={"color": DIM, "stroke_width": 1.2},
            tips=False,
        ).move_to([-2.35, -0.25, 0])
        quadratic = axes.plot(lambda x: x * x, x_range=[0, 10], color=HOT_PINK, stroke_width=3.0)
        linear = axes.plot(lambda x: 7.2 * x, x_range=[0, 10], color=LINEAR_GREEN, stroke_width=3.0)
        q_lbl = self.label("O(n^2)", SUBTITLE_SIZE, HOT_PINK, font=FONT_CODE).move_to(axes.c2p(8.0, 78))
        l_lbl = self.label("O(n)", SUBTITLE_SIZE, LINEAR_GREEN, font=FONT_CODE).move_to(axes.c2p(8.25, 46))
        n_dot_q = Dot(axes.c2p(6.8, 6.8 * 6.8), radius=0.09, color=HOT_PINK)
        n_dot_l = Dot(axes.c2p(6.8, 7.2 * 6.8), radius=0.09, color=LINEAR_GREEN)
        gpu = self.placeholder_visual("code", 1.3, 1.0, HOT_PINK).move_to([4.4, 0.7, 0])
        rocket_path = self.first_asset("icons/rocket_icon.svg")
        rocket = SVGMobject(str(rocket_path)).scale(0.55) if rocket_path else self.robot_icon(LINEAR_GREEN).scale(0.45)
        rocket.move_to([4.45, -1.15, 0])
        labels = VGroup(
            self.label("Quadratic attention", SMALL_SIZE, HOT_PINK, font=FONT_CODE).next_to(gpu, DOWN, buff=0.1),
            self.label("Linear attention", SMALL_SIZE, LINEAR_GREEN, font=FONT_CODE).next_to(rocket, DOWN, buff=0.1),
        )

        self.play(FadeIn(title), Create(axes), run_time=0.8)
        self.play(Create(quadratic), FadeIn(q_lbl), FadeIn(gpu), FadeIn(labels[0]), run_time=1.1)
        self.play(Create(linear), FadeIn(l_lbl), FadeIn(rocket), FadeIn(labels[1]), run_time=1.1)
        self.play(FadeIn(n_dot_q), FadeIn(n_dot_l), Wiggle(gpu), rocket.animate.shift(0.28 * RIGHT), run_time=1.1)
        self.wait(8.0)
        self.fast_clear()

    def sana_pipeline(self):
        title = self.hook_question("SANA combines CHI, VLM captions, 32x AE, Linear Attention, and Mix-FFN.", color=SANA_NEON)
        prompt = self.prompt_bar('"A cyberpunk cat wearing neon glasses"', width=6.2, color=TEXT_PURPLE).move_to([-3.6, 2.1, 0])
        chi = self.module("Complex Human\nInstruction", TEXT_PURPLE, 2.35, 1.0).move_to([-4.8, 0.55, 0])
        vlm = self.module("VLMs for\nimage captioning", VAR_GOLD, 2.25, 1.0).move_to([-2.2, 0.55, 0])
        ae = self.module("32x deep\ncompression AE", LINEAR_GREEN, 2.45, 1.0).move_to([0.45, 0.55, 0])
        linear = self.module("Linear Attention\n+ Mix-FFN", SANA_NEON, 2.45, 1.0).move_to([3.15, 0.55, 0])
        out = self.image_box("external_57_63/cyberpunk_cat.jpg", 1.7, 1.7, SANA_NEON).move_to([5.35, -1.35, 0])
        out_lbl = self.label("illustrative output", SMALL_SIZE, MUTED, font=FONT_CODE).next_to(out, DOWN, buff=0.1)
        blocks = VGroup(chi, vlm, ae, linear)
        arrows = VGroup(
            Arrow(chi.get_right(), vlm.get_left(), buff=0.08, color=MUTED, stroke_width=2.3),
            Arrow(vlm.get_right(), ae.get_left(), buff=0.08, color=MUTED, stroke_width=2.3),
            Arrow(ae.get_right(), linear.get_left(), buff=0.08, color=MUTED, stroke_width=2.3),
            Arrow(linear.get_right(), out.get_left(), buff=0.08, color=SANA_NEON, stroke_width=2.8),
        )
        citation = self.label("Xie et al., ICLR 2025", SMALL_SIZE, MUTED, font=FONT_CODE).to_corner(DR, buff=0.45)

        self.play(FadeIn(title), FadeIn(prompt), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.16), Create(arrows[:3]), run_time=1.5)
        self.play(GrowArrow(arrows[3]), FadeIn(out), FadeIn(out_lbl), FadeIn(citation), run_time=1.0)
        self.wait(10.0)
        self.fast_clear()

    def var_rethink_ar(self):
        title = self.hook_question("VAR changes the autoregressive question.", color=VAR_GOLD)
        text_ar = self.soft_box(3.6, 3.1, color=TEXT_PURPLE, fill_opacity=0.035, stroke_opacity=0.55).move_to([-4.0, -0.1, 0])
        img_ar = self.soft_box(3.6, 3.1, color=HOT_PINK, fill_opacity=0.035, stroke_opacity=0.55).move_to([0, -0.1, 0])
        var_box = self.soft_box(3.6, 3.1, color=VAR_GOLD, fill_opacity=0.045, stroke_opacity=0.72).move_to([4.0, -0.1, 0])
        text_lines = VGroup(
            self.label("Text AR", SUBTITLE_SIZE, TEXT_PURPLE, font=FONT_TITLE),
            self.label("next-token\nprediction", SMALL_SIZE, TEXT, font=FONT_CODE),
        ).arrange(DOWN, buff=0.28).move_to(text_ar)
        img_lines = VGroup(
            self.label("Image AR", SUBTITLE_SIZE, HOT_PINK, font=FONT_TITLE),
            self.label("next-image-token\nprediction", SMALL_SIZE, TEXT, font=FONT_CODE),
        ).arrange(DOWN, buff=0.28).move_to(img_ar)
        var_lines = VGroup(
            self.label("VAR", SUBTITLE_SIZE, VAR_GOLD, font=FONT_TITLE),
            self.label("next-scale /\nnext-resolution", SMALL_SIZE, TEXT, font=FONT_CODE),
        ).arrange(DOWN, buff=0.28).move_to(var_box)
        note = self.takeaway("VAR asks for the next scale, not the next token.", VAR_GOLD).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(text_ar), FadeIn(text_lines), run_time=0.7)
        self.play(FadeIn(img_ar), FadeIn(img_lines), run_time=0.7)
        self.play(FadeIn(var_box), FadeIn(var_lines), Circumscribe(var_box, color=VAR_GOLD), run_time=1.0)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(8.0)
        self.fast_clear()

    def var_next_scale(self):
        title = self.hook_question("VAR builds the whole image scale by scale.", color=VAR_GOLD)
        sizes = [16, 32, 64, 128, 256, 512]
        images = [self.image_box(f"generated_57_63/parrot_{s}.png", 3.0, 3.0, VAR_GOLD) for s in sizes]
        current = images[0].move_to([-2.4, -0.1, 0])
        label = self.label("16 x 16", SUBTITLE_SIZE, VAR_GOLD, font=FONT_CODE).next_to(current, DOWN, buff=0.16)

        ladder = VGroup()
        for i, s in enumerate(sizes):
            chip = self.vector_chip(f"r{i + 1}: {s}", VAR_GOLD if i == 0 else MUTED, 1.28)
            ladder.add(chip)
        ladder.arrange(DOWN, buff=0.13).move_to([3.45, -0.08, 0])
        big_note = self.label("coarse layout -> shapes -> details", 30, TEXT, font=FONT_TITLE).move_to([0, -2.95, 0])
        citation = self.label("Tian et al., 2024", SMALL_SIZE, MUTED, font=FONT_CODE).to_corner(DR, buff=0.45)

        self.play(FadeIn(title), FadeIn(current), FadeIn(label), FadeIn(ladder), FadeIn(citation), run_time=1.0)
        for idx, s in enumerate(sizes[1:], start=1):
            nxt = images[idx].move_to(current)
            new_label = self.label(f"{s} x {s}", SUBTITLE_SIZE, VAR_GOLD, font=FONT_CODE).next_to(current, DOWN, buff=0.16)
            self.play(
                Transform(current, nxt),
                Transform(label, new_label),
                ladder[idx - 1].animate.set_opacity(0.45),
                ladder[idx].animate.set_color(VAR_GOLD),
                run_time=0.65,
            )
        self.play(FadeIn(big_note), Flash(current, color=VAR_GOLD), run_time=0.9)
        self.wait(9.0)
        self.fast_clear()

    def summary_bridge(self):
        title = self.hook_question("Different engines, same engineering question.", color=TEXT)
        sana = self.soft_box(5.35, 3.2, color=SANA_NEON, fill_opacity=0.04, stroke_opacity=0.62).move_to([-3.0, 0.05, 0])
        var = self.soft_box(5.35, 3.2, color=VAR_GOLD, fill_opacity=0.04, stroke_opacity=0.62).move_to([3.0, 0.05, 0])
        sana_text = self.label("SANA\n32x compression\nLinear Attention\nMix-FFN", 25, SANA_NEON, font=FONT_TITLE).move_to(sana)
        var_text = self.label("VAR\nnext-scale prediction\ncoarse-to-fine image AR", 25, VAR_GOLD, font=FONT_TITLE).move_to(var)
        question = self.takeaway("How do we generate high-quality images faster and cheaper?", LINEAR_GREEN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(sana), FadeIn(var), run_time=0.8)
        self.play(FadeIn(sana_text), FadeIn(var_text), run_time=1.0)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(8.0)
        self.fast_clear()
