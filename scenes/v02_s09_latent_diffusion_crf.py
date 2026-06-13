from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


PIXEL_ORANGE = "#FF8A3D"
LATENT_GREEN = "#27E08A"
CRF_PURPLE = "#A78BFA"
HOT_RED = "#FF4081"


class V02LatentDiffusionCRF(TextPixelsScene):
    """Slides 57-60: Latent Diffusion Models and LatentCRF."""

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s09_latent_diffusion_crf.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Latent Diffusion and the CRF Shortcut",
            "Do the expensive work in a smaller space",
        )

        shots = [
            self.pixel_space_hook,
            self.timeline_ldm,
            self.encoder_to_latent,
            self.latent_denoising,
            self.conditioning_cross_attention,
            self.decoder_pipeline,
            self.latentcrf_shortcut,
            self.pairwise_higher_order,
            self.latentcrf_results,
            self.transition_to_modern_engines,
        ]
        only = os.environ.get("V02_DEBUG_SHOT")
        for shot in shots:
            if only and shot.__name__ != only:
                continue
            shot()

    def image_box(self, asset: str, width: float, height: float, color: str) -> Group:
        path = self.first_asset(asset)
        if path:
            img = ImageMobject(str(path))
            self.fit_to_box(img, width, height)
        else:
            img = self.placeholder_visual("image", width, height, color)
        frame = self.soft_box(width + 0.18, height + 0.18, color=color, fill_opacity=0.03, stroke_opacity=0.68)
        img.move_to(frame)
        return Group(frame, img)

    def latent_nodes(self, rows: int = 4, cols: int = 5, spacing: float = 0.72) -> VGroup:
        nodes = VGroup()
        for r in range(rows):
            for c in range(cols):
                node = Circle(radius=0.12, color=LATENT_GREEN, fill_color=LATENT_GREEN, fill_opacity=0.22, stroke_width=2)
                node.move_to([(c - (cols - 1) / 2) * spacing, ((rows - 1) / 2 - r) * spacing, 0])
                nodes.add(node)
        return nodes

    def pixel_space_hook(self):
        title = self.hook_question("Pixel Space is expensive.", color=PIXEL_ORANGE)
        one_pixel = Square(side_length=0.28, color=PIXEL_ORANGE, fill_color=PIXEL_ORANGE, fill_opacity=0.85)

        grid = self.pixel_grid(rows=12, cols=22, side=0.24, colors=(PIXEL_ORANGE, HOT_RED, PUZZLE_GOLD), opacity=0.22)
        grid.move_to([0, -0.25, 0])
        grid_frame = self.soft_box(5.45, 3.05, color=PIXEL_ORANGE, fill_opacity=0.02, stroke_opacity=0.38).move_to(grid)

        count = self.label("3,145,728", 36, PUZZLE_GOLD, font=FONT_CODE)
        count_label = self.label("1024 x 1024 x 3 values", SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_CODE)
        value_group = VGroup(count, count_label).arrange(DOWN, buff=0.08).move_to([0, -2.72, 0])

        robot = self.robot_icon(PIXEL_ORANGE).scale(0.58).move_to([-5.15, -1.85, 0])
        bubble = self.soft_box(2.2, 0.62, color=MUTED, fill_opacity=0.08, stroke_opacity=0.42).next_to(robot, UP, buff=0.18)
        bubble_text = self.label("Can I resign?", 14, TEXT, font=FONT_CODE).move_to(bubble)
        gpu = self.placeholder_visual("code", 1.3, 1.0, HOT_RED).move_to([5.1, -1.75, 0])
        gpu_lbl = self.label("GPU heat", SMALL_SIZE, HOT_RED, font=FONT_CODE).next_to(gpu, DOWN, buff=0.1)

        self.play(FadeIn(title), FadeIn(one_pixel), run_time=0.8)
        self.play(Transform(one_pixel, grid), FadeIn(grid_frame), run_time=1.6, rate_func=smooth)
        self.play(FadeIn(value_group), FadeIn(robot), FadeIn(bubble), FadeIn(bubble_text), FadeIn(gpu), FadeIn(gpu_lbl), run_time=1.0)
        self.play(Wiggle(gpu, scale_value=1.08), Indicate(count, color=HOT_RED), run_time=1.2)
        self.wait(5.0)
        self.fast_clear()

    def timeline_ldm(self):
        title = self.hook_question("LDM 2021: do the hard work in a smaller space.", color=LATENT_GREEN)
        names = ["Diffusion", "U-Net", "Transformers", "CLIP", "VQGAN", "DALL-E", "LDM"]
        pieces = VGroup()
        for name in names:
            color = LATENT_GREEN if name == "LDM" else DIM
            box = self.soft_box(1.45, 0.72, color=color, fill_opacity=0.06, stroke_opacity=0.6)
            txt = self.label(name, SMALL_SIZE, color if name == "LDM" else TEXT, font=FONT_CODE)
            self.fit_to_box(txt, 1.22, 0.38).move_to(box)
            pieces.add(VGroup(box, txt))
        pieces.arrange(RIGHT, buff=0.18).move_to([0, 0.2, 0])
        arrows = VGroup(*[
            Arrow(pieces[i].get_right(), pieces[i + 1].get_left(), buff=0.04, color=MUTED, stroke_width=1.8, max_tip_length_to_length_ratio=0.22)
            for i in range(len(pieces) - 1)
        ])
        subtitle = self.label("Latent Diffusion Models", 34, LATENT_GREEN, font=FONT_TITLE).move_to([0, -1.45, 0])
        note = self.takeaway("Compress first. Denoise in latent space. Decode at the end.", LATENT_GREEN).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p) for p in pieces], lag_ratio=0.1), Create(arrows), run_time=1.5)
        self.play(Circumscribe(pieces[-1], color=LATENT_GREEN), Flash(pieces[-1], color=LATENT_GREEN), FadeIn(subtitle), run_time=1.2)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(120.0)
        self.fast_clear()

    def encoder_to_latent(self):
        title = self.hook_question("Compress pixels into a smaller latent space.", color=LATENT_GREEN)
        image = self.image_box("external_57_63/high_res_image.jpg", 2.65, 2.65, PIXEL_ORANGE).move_to([-4.3, -0.2, 0])
        image_lbl = VGroup(
            self.mixed_label([("text", "Pixel Space"), ("math", r"x")], SMALL_SIZE, PIXEL_ORANGE, font=FONT_BODY),
            self.label("1024 x 1024 x 3", SMALL_SIZE, PIXEL_ORANGE, font=FONT_CODE),
        ).arrange(DOWN, buff=0.04).next_to(image, DOWN, buff=0.16)

        funnel_path = self.first_asset("icons/funnel.svg")
        funnel = SVGMobject(str(funnel_path), stroke_width=2).scale(0.9) if funnel_path else self.module("Encoder\nE", LATENT_GREEN, 1.5, 1.2)
        funnel.move_to([0, -0.15, 0])
        funnel_lbl = self.label("Encoder E", SMALL_SIZE, LATENT_GREEN, font=FONT_CODE).next_to(funnel, DOWN, buff=0.16)

        latent_img = self.image_box("generated_57_63/latent_grid_small.png", 1.6, 1.6, LATENT_GREEN).move_to([4.2, -0.1, 0])
        latent_lbl = VGroup(
            self.mixed_label([("text", "Latent Space"), ("math", r"z")], SMALL_SIZE, LATENT_GREEN, font=FONT_BODY),
            self.label("64 x 64 x 4", SMALL_SIZE, LATENT_GREEN, font=FONT_CODE),
        ).arrange(DOWN, buff=0.04).next_to(latent_img, DOWN, buff=0.16)

        arr1 = Arrow(image.get_right(), funnel.get_left(), buff=0.18, color=PIXEL_ORANGE, stroke_width=3)
        arr2 = Arrow(funnel.get_right(), latent_img.get_left(), buff=0.18, color=LATENT_GREEN, stroke_width=3)
        suitcase = self.label("same structure,\nsmaller suitcase", SMALL_SIZE, PUZZLE_GOLD, font=FONT_CODE).move_to([0, -2.55, 0])

        self.play(FadeIn(title), FadeIn(image), FadeIn(image_lbl), run_time=1.0)
        self.play(GrowArrow(arr1), FadeIn(funnel), FadeIn(funnel_lbl), run_time=0.9)
        self.play(GrowArrow(arr2), FadeIn(latent_img, shift=0.12 * RIGHT), FadeIn(latent_lbl), run_time=1.0)
        self.play(FadeIn(suitcase), Indicate(latent_img, color=LATENT_GREEN), run_time=0.8)
        self.wait(6.0)
        self.fast_clear()

    def latent_denoising(self):
        title = self.hook_question("Diffusion happens in latent space.", color=LATENT_GREEN)
        region = self.soft_box(10.7, 4.7, color=LATENT_GREEN, fill_opacity=0.035, stroke_opacity=0.45).move_to([0, -0.22, 0])
        region_lbl = self.label("Latent Space", SUBTITLE_SIZE, LATENT_GREEN, font=FONT_TITLE).move_to(region.get_top() + 0.35 * DOWN)

        sequence = ["latent_noise_00.png", "latent_noise_25.png", "latent_noise_50.png", "latent_noise_75.png", "latent_clean.png"]
        imgs = [
            self.image_box(f"generated_57_63/{name}", 1.18, 1.18, LATENT_GREEN)
            for name in sequence
        ]
        x_positions = np.linspace(-4.0, 4.0, len(imgs))
        for img, x in zip(imgs, x_positions):
            img.move_to([x, -0.4, 0])
        labels = VGroup(*[
            self.math_label(label, SMALL_SIZE, LATENT_GREEN).next_to(img, DOWN, buff=0.12)
            for label, img in zip([r"z_T", r"z_{75}", r"z_{50}", r"z_{25}", r"z_0"], imgs)
        ])
        arrows = VGroup(*[
            Arrow(imgs[i].get_right(), imgs[i + 1].get_left(), buff=0.08, color=LATENT_GREEN, stroke_width=2.4)
            for i in range(len(imgs) - 1)
        ])

        unet_box = self.soft_box(2.65, 1.08, color=IMAGE_BLUE, fill_opacity=0.055, stroke_opacity=0.68)
        unet_lbl = VGroup(
            self.label("Denoising U-Net", SMALL_SIZE, IMAGE_BLUE, font=FONT_BODY),
            self.math_label(r"\varepsilon_\theta", SMALL_SIZE, IMAGE_BLUE),
        ).arrange(DOWN, buff=0.04).move_to(unet_box)
        unet = VGroup(unet_box, unet_lbl).move_to([0, 1.3, 0])
        note = self.takeaway("Denoise z, not x.", LATENT_GREEN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(region), FadeIn(region_lbl), FadeIn(unet), run_time=1.0)
        self.play(FadeIn(imgs[0]), FadeIn(labels[0]), run_time=0.6)
        for i in range(1, len(imgs)):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(imgs[i]), FadeIn(labels[i]), run_time=0.62)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(5.0)
        self.fast_clear()

    def conditioning_cross_attention(self):
        title = self.hook_question("Conditioning enters through cross-attention.", color=PUZZLE_GOLD)
        unet = self.module("Latent U-Net\nwith cross-attention", IMAGE_BLUE, 3.1, 1.35).move_to([1.1, 0.2, 0])
        qkv = VGroup(
            self.vector_chip("Q: latent features", IMAGE_BLUE, 2.2),
            self.vector_chip("K: condition", PUZZLE_GOLD, 2.2),
            self.vector_chip("V: condition", PUZZLE_GOLD, 2.2),
        ).arrange(DOWN, buff=0.15).next_to(unet, DOWN, buff=0.38)

        conds = VGroup()
        for text, color in [
            ("Semantic Map", POSITIVE_GREEN),
            ("Text Prompt", TEXT_PURPLE),
            ("Representations", PUZZLE_GOLD),
            ("Images", PIXEL_ORANGE),
        ]:
            conds.add(self.vector_chip(text, color, 2.35))
        conds.arrange(DOWN, buff=0.18).move_to([-4.2, 0.1, 0])
        tau_box = self.soft_box(1.65, 0.94, color=CRF_PURPLE, fill_opacity=0.055, stroke_opacity=0.68)
        tau_lbl = VGroup(
            self.math_label(r"\tau_\theta", SMALL_SIZE, CRF_PURPLE),
            self.label("encoder", SMALL_SIZE, CRF_PURPLE, font=FONT_BODY),
        ).arrange(DOWN, buff=0.03).move_to(tau_box)
        tau = VGroup(tau_box, tau_lbl).move_to([-1.45, 0.1, 0])
        arrs = VGroup(
            Arrow(conds.get_right(), tau.get_left(), buff=0.1, color=CRF_PURPLE, stroke_width=2.4),
            Arrow(tau.get_right(), unet.get_left(), buff=0.1, color=PUZZLE_GOLD, stroke_width=2.8),
        )
        prompt = self.prompt_bar('"a blue Porsche"', width=4.4, color=TEXT_PURPLE).move_to([-4.2, 2.35, 0])
        attention_beam = CurvedArrow(prompt.get_right(), qkv[1].get_left(), angle=-0.35, color=PUZZLE_GOLD, stroke_width=2.6)

        self.play(FadeIn(title), FadeIn(prompt), FadeIn(unet), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(c) for c in conds], lag_ratio=0.12), FadeIn(tau), Create(arrs), run_time=1.5)
        self.play(FadeIn(qkv), Create(attention_beam), run_time=1.0)
        self.play(Indicate(qkv[0], color=IMAGE_BLUE), Indicate(qkv[1], color=PUZZLE_GOLD), Indicate(qkv[2], color=PUZZLE_GOLD), run_time=1.3)
        self.wait(5.0)
        self.fast_clear()

    def decoder_pipeline(self):
        title = self.hook_question("Decoder D opens the compressed dream back into pixels.", color=LATENT_GREEN)
        x = self.image_box("external_57_63/high_res_image.jpg", 1.35, 1.35, PIXEL_ORANGE).move_to([-5.0, 1.05, 0])
        enc = self.module("E", LATENT_GREEN, 0.78, 0.72).move_to([-3.25, 1.05, 0])
        z = self.image_box("generated_57_63/latent_grid_small.png", 1.0, 1.0, LATENT_GREEN).move_to([-1.65, 1.05, 0])
        zt = self.image_box("generated_57_63/latent_noise_00.png", 1.0, 1.0, LATENT_GREEN).move_to([-1.65, -1.05, 0])
        z0 = self.image_box("generated_57_63/latent_clean.png", 1.0, 1.0, LATENT_GREEN).move_to([1.65, -1.05, 0])
        dec = self.module("D", LATENT_GREEN, 0.78, 0.72).move_to([3.25, -1.05, 0])
        out = self.image_box("external_57_63/blue_porsche.jpg", 1.35, 1.35, IMAGE_BLUE).move_to([5.0, -1.05, 0])

        labels = VGroup(
            self.math_label(r"x", SMALL_SIZE, PIXEL_ORANGE).next_to(x, DOWN, buff=0.08),
            self.math_label(r"z", SMALL_SIZE, LATENT_GREEN).next_to(z, DOWN, buff=0.08),
            self.math_label(r"z_T", SMALL_SIZE, LATENT_GREEN).next_to(zt, DOWN, buff=0.08),
            self.math_label(r"z_0", SMALL_SIZE, LATENT_GREEN).next_to(z0, DOWN, buff=0.08),
            self.math_label(r"\hat{x}", SMALL_SIZE, IMAGE_BLUE).next_to(out, DOWN, buff=0.08),
        )
        arrows = VGroup(
            Arrow(x.get_right(), enc.get_left(), buff=0.08, color=PIXEL_ORANGE),
            Arrow(enc.get_right(), z.get_left(), buff=0.08, color=LATENT_GREEN),
            Arrow(zt.get_right(), z0.get_left(), buff=0.12, color=LATENT_GREEN),
            Arrow(z0.get_right(), dec.get_left(), buff=0.08, color=LATENT_GREEN),
            Arrow(dec.get_right(), out.get_left(), buff=0.08, color=IMAGE_BLUE),
        )
        formula = self.math_label(
            r"x \to E \to z \qquad z_T \to \cdots \to z_0 \qquad z_0 \to D \to \hat{x}",
            30, TEXT,
        ).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(x), FadeIn(enc), FadeIn(z), Create(arrows[:2]), FadeIn(labels[:2]), run_time=1.2)
        self.play(FadeIn(zt), FadeIn(z0), Create(arrows[2]), FadeIn(labels[2:4]), run_time=1.0)
        self.play(FadeIn(dec), FadeIn(out), Create(arrows[3:]), FadeIn(labels[4]), Indicate(out, color=IMAGE_BLUE), run_time=1.2)
        self.play(FadeIn(formula), run_time=0.8)
        self.wait(5.0)
        self.fast_clear()

    def latentcrf_shortcut(self):
        title = self.hook_question("Even latent denoising still has many steps.", color=CRF_PURPLE)
        nodes = VGroup()
        labels = VGroup()
        for i in range(11):
            node = Circle(radius=0.16, color=LATENT_GREEN, fill_color=LATENT_GREEN, fill_opacity=0.14, stroke_width=2)
            node.move_to([-5.0 + i, 0.7, 0])
            tex = r"z_T" if i == 0 else (r"z_0" if i == 10 else rf"z_{{{50 - i}}}")
            label = self.math_label(tex, 18, LATENT_GREEN).next_to(node, DOWN, buff=0.1)
            nodes.add(node)
            labels.add(label)
        arrows = VGroup(*[
            Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.04, color=DIM, stroke_width=2, max_tip_length_to_length_ratio=0.32)
            for i in range(10)
        ])
        walker = self.robot_icon(MUTED).scale(0.38).move_to(nodes[2].get_center() + 0.65 * UP)
        bubble = self.label("Are we there yet?", 15, MUTED, font=FONT_CODE).next_to(walker, UP, buff=0.14)

        bypass = CurvedArrow(nodes[3].get_center(), nodes[8].get_center(), angle=-0.72, color=CRF_PURPLE, stroke_width=4)
        crf = self.module("Light-weight\nLatentCRF inference", CRF_PURPLE, 3.1, 1.0).move_to([0, -1.5, 0])
        note = self.takeaway("Replace several LDM inference iterations with CRF inference.", CRF_PURPLE).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(nodes), FadeIn(labels), Create(arrows), run_time=1.25)
        self.play(FadeIn(walker), FadeIn(bubble), run_time=0.6)
        self.play(nodes[4:8].animate.set_opacity(0.22), arrows[4:8].animate.set_opacity(0.22), Create(bypass), FadeIn(crf), run_time=1.2)
        self.play(FadeIn(note), Indicate(crf, color=CRF_PURPLE), run_time=0.8)
        self.wait(6.0)
        self.fast_clear()

    def pairwise_higher_order(self):
        title = self.hook_question("LatentCRF uses local and group-level consistency.", color=CRF_PURPLE)
        nodes = self.latent_nodes(rows=4, cols=5, spacing=0.7).move_to([-2.8, -0.1, 0])
        edges = VGroup()
        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes):
                if j <= i:
                    continue
                dist = np.linalg.norm(a.get_center() - b.get_center())
                if dist < 0.78:
                    edges.add(Line(a.get_center(), b.get_center(), color=CRF_PURPLE, stroke_width=1.6, stroke_opacity=0.52))
        bad_edge = Line(nodes[6].get_center(), nodes[7].get_center(), color=HOT_RED, stroke_width=4)
        group_box = SurroundingRectangle(VGroup(nodes[7], nodes[8], nodes[12], nodes[13], nodes[14]), color=PUZZLE_GOLD, buff=0.18, stroke_width=2.8)
        left_label = self.label("Pairwise:\nlocal consistency", SUBTITLE_SIZE, CRF_PURPLE, font=FONT_TITLE).move_to([2.55, 0.85, 0])
        right_label = self.label("Higher-order:\ngroup-level structure", SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_TITLE).move_to([2.55, -1.0, 0])
        before = self.image_box("generated_57_63/latentcrf_before.png", 1.2, 1.2, HOT_RED).move_to([-5.2, -2.45, 0])
        after = self.image_box("generated_57_63/latentcrf_after.png", 1.2, 1.2, LATENT_GREEN).move_to([-3.45, -2.45, 0])
        arr = Arrow(before.get_right(), after.get_left(), buff=0.1, color=LATENT_GREEN, stroke_width=2.6)

        self.play(FadeIn(title), FadeIn(nodes), run_time=0.9)
        self.play(Create(edges), FadeIn(left_label), run_time=1.0)
        self.play(Create(bad_edge), bad_edge.animate.set_color(LATENT_GREEN), run_time=1.0)
        self.play(Create(group_box), FadeIn(right_label), run_time=0.9)
        self.play(FadeIn(before), GrowArrow(arr), FadeIn(after), run_time=0.9)
        self.wait(6.0)
        self.fast_clear()

    def latentcrf_results(self):
        title = self.hook_question("LatentCRF: 33% faster, visually comparable.", color=LATENT_GREEN)
        assets = [
            ("flower_peonies.jpg", "peonies"),
            ("blue_porsche.jpg", "blue Porsche"),
            ("raccoon_formal.jpg", "formal raccoon"),
            ("cat_portrait.jpg", "cat portrait"),
        ]
        cards = Group()
        for fname, label in assets:
            top = self.image_box(f"external_57_63/{fname}", 1.45, 1.08, LATENT_GREEN)
            bot = self.image_box(f"external_57_63/{fname}", 1.45, 1.08, IMAGE_BLUE).set_opacity(0.78)
            pair = Group(top, bot).arrange(DOWN, buff=0.12)
            lbl = self.label(label, 15, TEXT, font=FONT_CODE).next_to(pair, DOWN, buff=0.08)
            cards.add(Group(pair, lbl))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.36)).move_to([-2.2, -0.18, 0])
        row_labels = VGroup(
            self.label("LatentCRF", SMALL_SIZE, LATENT_GREEN, font=FONT_CODE),
            self.label("Full LDM", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE),
        ).arrange(DOWN, buff=0.52).move_to([-5.45, 0.38, 0])

        meter = VGroup(
            self.label("Full LDM", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE),
            Rectangle(width=2.6, height=0.26, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.55),
            self.label("100%", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE),
            self.label("LatentCRF", SMALL_SIZE, LATENT_GREEN, font=FONT_CODE),
            Rectangle(width=1.74, height=0.26, color=LATENT_GREEN, fill_color=LATENT_GREEN, fill_opacity=0.72),
            self.label("67%", SMALL_SIZE, LATENT_GREEN, font=FONT_CODE),
        )
        meter[0].move_to([2.8, 0.8, 0]); meter[1].next_to(meter[0], DOWN, buff=0.14, aligned_edge=LEFT); meter[2].next_to(meter[1], RIGHT, buff=0.18)
        meter[3].move_to([2.8, -0.15, 0]); meter[4].next_to(meter[3], DOWN, buff=0.14, aligned_edge=LEFT); meter[5].next_to(meter[4], RIGHT, buff=0.18)
        stopwatch = self.label("33% faster", 36, LATENT_GREEN, font=FONT_TITLE).move_to([3.85, -2.0, 0])
        caveat = self.label("without obvious quality loss", SMALL_SIZE, MUTED, font=FONT_CODE).next_to(stopwatch, DOWN, buff=0.12)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(row_labels), LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(meter), FadeIn(stopwatch), FadeIn(caveat), run_time=1.0)
        self.wait(7.0)
        self.fast_clear()

    def transition_to_modern_engines(self):
        title = self.hook_question("Still not fast enough?", color=PUZZLE_GOLD)
        chip = self.soft_box(2.4, 1.3, color=LATENT_GREEN, fill_opacity=0.08, stroke_opacity=0.75).move_to([0, 0.55, 0])
        chip_lbl = self.label("latent\nengine", SUBTITLE_SIZE, LATENT_GREEN, font=FONT_CODE).move_to(chip)
        sana = self.module("SANA", TEXT_PURPLE, 2.0, 0.82).move_to([-2.5, -1.35, 0])
        var = self.module("VAR", PUZZLE_GOLD, 2.0, 0.82).move_to([2.5, -1.35, 0])
        arr1 = Arrow(chip.get_bottom(), sana.get_top(), buff=0.08, color=TEXT_PURPLE, stroke_width=3)
        arr2 = Arrow(chip.get_bottom(), var.get_top(), buff=0.08, color=PUZZLE_GOLD, stroke_width=3)
        line = self.takeaway("Next: modern engines change the inside of the machine.", PUZZLE_GOLD).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(chip), FadeIn(chip_lbl), run_time=0.8)
        self.play(Flash(chip, color=PUZZLE_GOLD), GrowArrow(arr1), GrowArrow(arr2), FadeIn(sana), FadeIn(var), run_time=1.2)
        self.play(FadeIn(line), run_time=0.8)
        self.wait(4.0)
        self.fast_clear()
