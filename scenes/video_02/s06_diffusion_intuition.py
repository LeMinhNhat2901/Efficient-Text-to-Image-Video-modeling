from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.v02_common import *

# ── Color aliases for Diffusion theme ────────────────────────────────────────
FORWARD_COLOR = "#FF8A3D"   # NEGATIVE_ORANGE — destruction / forward process
REVERSE_CYAN  = "#00E5FF"   # restoration / reverse process
NOISE_GRAY    = "#8899AA"   # neutral noise color


class V02DiffusionIntuition(TextPixelsScene):
    """Diffusion intuition, forward/reverse, noise prediction."""

    def puzzle_piece(self, year: str, name: str, color: str) -> VGroup:
        body = self.soft_box(1.48, 0.9, color=color, fill_opacity=0.07, stroke_opacity=0.78)
        notch = Circle(radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(body.get_right())
        tab = Circle(radius=0.12, stroke_color=color, stroke_width=1.0, fill_color=color, fill_opacity=0.08).move_to(body.get_left())
        label = VGroup(
            self.label(year, 13, MUTED, font=FONT_CODE),
            Text(name, font=FONT_SUBTITLE, font_size=20, color=color, weight=BOLD, disable_ligatures=True),
        ).arrange(DOWN, buff=0.05).move_to(body)
        return VGroup(body, tab, notch, label)

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s06_diffusion_intuition.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        scene_start = self.time

        self.diffusion_intro()

        self.timeline_highlight_diffusion()
        self.hook_forward_diffusion()
        self.forward_reverse_arrows()
        self.destroy_restore_quote()
        self.training_vs_sampling_split()
        self.noise_prediction_secret()
        self.mse_loss_animation()
        self.hold_for_voiceover(scene_start, voiceover)
        if hasattr(self, "final_hold_group"):
            self.play(FadeOut(self.final_hold_group), run_time=0.8)

    def diffusion_intro(self):
        self.add_background_texture("textures/dark_grid.jpg", "textures/subtle_noise.jpg", opacity=0.025)

        title = Text(
            "Diffusion",
            font=FONT_SUBTITLE,
            font_size=56,
            color=FORWARD_COLOR,
            weight=BOLD,
            disable_ligatures=True,
        ).move_to([0, 1.55, 0])
        subtitle = self.label("The art of controlled destruction", SUBTITLE_SIZE, TEXT, font=FONT_TITLE)
        subtitle.next_to(title, DOWN, buff=0.18)

        clean_path = self.first_asset("external_40_56/cat_clean.jpg", "generated_40_56/cat_from_clean_noise_000.png")
        noise_path = self.first_asset("generated_40_56/cat_from_clean_noise_100.png", "generated_40_56/cat_noise_100.png")
        if clean_path:
            clean = ImageMobject(str(clean_path))
            self.fit_to_box(clean, 1.45, 1.45)
        else:
            clean = self.placeholder_visual("image", 1.45, 1.45, POSITIVE_GREEN)
        if noise_path:
            noise = ImageMobject(str(noise_path))
            self.fit_to_box(noise, 1.45, 1.45)
        else:
            noise = self.placeholder_visual("image", 1.45, 1.45, FORWARD_COLOR)

        clean_card = Group(
            self.soft_box(1.72, 1.72, color=POSITIVE_GREEN, fill_opacity=0.04, stroke_opacity=0.72),
            clean,
        ).move_to([-2.25, -0.95, 0])
        noise_card = Group(
            self.soft_box(1.72, 1.72, color=FORWARD_COLOR, fill_opacity=0.04, stroke_opacity=0.72),
            noise,
        ).move_to([2.25, -0.95, 0])
        arrow = Arrow(
            clean_card.get_right(), noise_card.get_left(),
            buff=0.18, color=FORWARD_COLOR, stroke_width=3.2,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow_label = self.label("add noise, step by step", SMALL_SIZE, FORWARD_COLOR, font=FONT_BODY)
        arrow_label.next_to(arrow, UP, buff=0.16)
        clean_lbl = self.math_label(r"x_0", SUBTITLE_SIZE + 4, POSITIVE_GREEN).next_to(clean_card, DOWN, buff=0.12)
        noise_lbl = self.math_label(r"x_T", SUBTITLE_SIZE + 4, FORWARD_COLOR).next_to(noise_card, DOWN, buff=0.12)

        self.play(FadeIn(title, shift=0.1 * DOWN), run_time=0.7)
        self.play(
            FadeIn(subtitle),
            FadeIn(Group(clean_card, clean_lbl)),
            run_time=0.55,
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(arrow_label),
            FadeIn(Group(noise_card, noise_lbl), shift=0.12 * RIGHT),
            run_time=0.75,
        )
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.55)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.1 — Timeline: highlight Diffusion piece (Slide 40)
    # ─────────────────────────────────────────────────────────────────────────
    def timeline_highlight_diffusion(self):
        tag = self.section_tag("slide 40", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question(
            "Text-to-image was assembled like a puzzle.", color=TEXT
        )
        title.shift(0.18 * DOWN)

        axis = Line([-5.4, -0.48, 0], [5.4, -0.48, 0], color=DIM, stroke_width=3)
        year_positions = {"2015": -4.55, "2017": -1.45, "2020": 1.25, "2021": 4.15}
        ticks = VGroup()
        years = VGroup()
        for year, x in year_positions.items():
            ticks.add(Line([x, -0.72, 0], [x, -0.24, 0], color=MUTED, stroke_width=2.2))
            years.add(self.label(year, 18, TEXT, font=FONT_CODE).move_to([x, -1.08, 0]))

        def badge(name: str, color: str, width: float = 1.5) -> VGroup:
            box = self.soft_box(width, 0.64, color=color, fill_opacity=0.075, stroke_opacity=0.82)
            label = Text(
                name,
                font=FONT_SUBTITLE,
                font_size=18,
                color=TEXT,
                weight=BOLD,
                disable_ligatures=True,
            )
            self.fit_to_box(label, width - 0.18, 0.36)
            label.move_to(box)
            return VGroup(box, label)

        groups = VGroup(
            VGroup(
                badge("U-Net", IMAGE_BLUE, 1.18).move_to([year_positions["2015"], 0.82, 0]),
                badge("Diffusion", FORWARD_COLOR, 1.62).move_to([year_positions["2015"], 0.10, 0]),
            ),
            badge("Transformers", TEXT_PURPLE, 1.95).move_to([year_positions["2017"], 0.52, 0]),
            badge("CLIP", TEXT_PURPLE, 1.12).move_to([year_positions["2020"], 0.52, 0]),
            VGroup(
                badge("VQGAN", PUZZLE_GOLD, 1.34).move_to([year_positions["2021"] - 0.95, 0.86, 0]),
                badge("DALL-E", PUZZLE_GOLD, 1.34).move_to([year_positions["2021"] + 0.45, 0.86, 0]),
                badge("LDM", POSITIVE_GREEN, 1.10).move_to([year_positions["2021"] + 1.78, 0.22, 0]),
            ),
        )
        cards = VGroup(groups[0][0], groups[0][1], groups[1], groups[2], groups[3][0], groups[3][1], groups[3][2])
        connectors = VGroup(*[
            Line(
                [card.get_center()[0], -0.48, 0],
                [card.get_center()[0], card.get_bottom()[1] - 0.05, 0],
                color=card[0].get_stroke_color(),
                stroke_width=1.45,
            ).set_opacity(0.68)
            for card in cards
        ])
        diffusion_piece = groups[0][1]
        glow = SurroundingRectangle(diffusion_piece, color=FORWARD_COLOR, buff=0.09, stroke_width=2.8)

        sub = Text(
            "Diffusion: learn to reverse destruction",
            font=FONT_SUBTITLE,
            font_size=SUBTITLE_SIZE,
            color=FORWARD_COLOR,
            weight=BOLD,
            disable_ligatures=True,
        ).to_edge(DOWN, buff=0.45)

        note = self.takeaway(
            "The forward process is simple: add noise. The reverse process is learned.",
            FORWARD_COLOR,
            width=10.2,
        ).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), Create(axis), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), FadeIn(years), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(g, shift=0.12 * UP) for g in groups], lag_ratio=0.18),
            LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.06),
            run_time=1.5,
        )
        self.play(Create(glow), FadeIn(sub, shift=0.08 * UP), Flash(diffusion_piece, color=FORWARD_COLOR), run_time=0.9)
        self.play(FadeOut(sub, shift=0.04 * DOWN), run_time=0.25)
        self.play(FadeIn(note, shift=0.05 * UP), run_time=0.45)
        self.wait(8.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.2 — Forward diffusion: cat → noise chain (Slide 41)
    # ─────────────────────────────────────────────────────────────────────────
    def hook_forward_diffusion(self):
        tag = self.section_tag("slide 41", FORWARD_COLOR).to_corner(UL, buff=0.48)
        title = self.hook_question("Forward diffusion: slowly destroy structure.", color=FORWARD_COLOR)

        noise_files = [
            ("external_40_56/cat_clean.jpg",                 "generated_40_56/cat_from_clean_noise_000.png"),
            ("generated_40_56/cat_from_clean_noise_010.png", "generated_40_56/cat_noise_10.png"),
            ("generated_40_56/cat_from_clean_noise_025.png", "generated_40_56/cat_noise_25.png"),
            ("generated_40_56/cat_from_clean_noise_050.png", "generated_40_56/cat_noise_50.png"),
            ("generated_40_56/cat_from_clean_noise_075.png", "generated_40_56/cat_noise_75.png"),
            ("generated_40_56/cat_from_clean_noise_100.png", "generated_40_56/cat_noise_100.png"),
        ]
        labels = [r"x_0", r"x_1", r"x_2", r"x_3", r"x_4", r"x_T"]
        colors = [POSITIVE_GREEN, IMAGE_BLUE, IMAGE_BLUE, NOISE_GRAY, NOISE_GRAY, FORWARD_COLOR]

        cards = Group()
        for i, (primary, fallback) in enumerate(noise_files):
            path = self.first_asset(primary, fallback)
            img_h, img_w = 1.6, 1.6
            if path:
                visual = ImageMobject(str(path))
                self.fit_to_box(visual, img_w, img_h)
            else:
                visual = self.placeholder_visual("image", img_w, img_h, colors[i])

            frame = self.soft_box(img_w + 0.22, img_h + 0.22,
                                  color=colors[i], fill_opacity=0.04, stroke_opacity=0.6)
            lbl = self.math_label(labels[i], SUBTITLE_SIZE, colors[i])
            lbl.next_to(frame, DOWN, buff=0.12)
            card = Group(frame, visual, lbl)
            cards.add(card)

        # Arrange horizontally with arrows between
        cards.arrange(RIGHT, buff=0.32).move_to([0, 0.0, 0])
        # Fit to screen
        cards.scale_to_fit_width(12.8)

        arrows = VGroup()
        for i in range(len(cards) - 1):
            arr = Arrow(
                cards[i].get_right() + 0.02 * RIGHT,
                cards[i + 1].get_left() - 0.02 * RIGHT,
                buff=0.0,
                color=FORWARD_COLOR,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.28,
            )
            arrows.add(arr)

        chain_label = self.math_label(r"x_0 \to x_1 \to x_2 \to \cdots \to x_T", SUBTITLE_SIZE, NOISE_GRAY)
        chain_label.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.18), run_time=2.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.14), run_time=1.4)
        self.play(FadeIn(chain_label, shift=0.1 * UP), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.3 — Forward vs Reverse: two curved arrows (Slide 41/43)
    # ─────────────────────────────────────────────────────────────────────────
    def forward_reverse_arrows(self):
        tag = self.section_tag("slide 41", IMAGE_BLUE).to_corner(UL, buff=0.48)

        # Left: clean cat thumbnail
        clean_path = self.first_asset(
            "external_40_56/cat_clean.jpg",
            "generated_40_56/cat_noise_00.png",
        )
        if clean_path:
            clean_vis = ImageMobject(str(clean_path)).scale_to_fit_height(2.0)
        else:
            clean_vis = self.placeholder_visual("image", 2.0, 2.0, POSITIVE_GREEN)
        clean_vis.move_to([-4.5, 0, 0])
        clean_lbl = self.mixed_label([("text", "Clean Image"), ("math", r"x_0")], SMALL_SIZE, POSITIVE_GREEN, font=FONT_BODY)
        clean_lbl.next_to(clean_vis, DOWN, buff=0.18)

        # Right: pure noise thumbnail
        noise_path = self.first_asset("generated_40_56/cat_from_clean_noise_100.png", "generated_40_56/cat_noise_100.png")
        if noise_path:
            noise_vis = ImageMobject(str(noise_path)).scale_to_fit_height(2.0)
        else:
            noise_vis = self.placeholder_visual("image", 2.0, 2.0, FORWARD_COLOR)
        noise_vis.move_to([4.5, 0, 0])
        noise_lbl = self.mixed_label([("text", "Pure Noise"), ("math", r"x_T")], SMALL_SIZE, FORWARD_COLOR, font=FONT_BODY)
        noise_lbl.next_to(noise_vis, DOWN, buff=0.18)

        # Two curved arrows
        fwd_arrow = CurvedArrow(
            [-3.2, 0.6, 0], [3.2, 0.6, 0],
            angle=-TAU / 10,
            color=FORWARD_COLOR,
            stroke_width=4,
        )
        fwd_label = self.label("Forward diffusion  (destroy)", SUBTITLE_SIZE, FORWARD_COLOR, font=FONT_TITLE)
        fwd_label.next_to(fwd_arrow, UP, buff=0.14)

        rev_arrow = CurvedArrow(
            [3.2, -0.6, 0], [-3.2, -0.6, 0],
            angle=-TAU / 10,
            color=REVERSE_CYAN,
            stroke_width=4,
        )
        rev_label = self.label("Reverse diffusion  (restore)", SUBTITLE_SIZE, REVERSE_CYAN, font=FONT_TITLE)
        rev_label.next_to(rev_arrow, DOWN, buff=0.14)

        self.play(FadeIn(tag), FadeIn(Group(clean_vis, clean_lbl)), FadeIn(Group(noise_vis, noise_lbl)), run_time=1.2)
        self.play(Create(fwd_arrow), FadeIn(fwd_label), run_time=1.0)
        self.play(Create(rev_arrow), FadeIn(rev_label), run_time=1.0)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.4 — Destroy → Restore quote (Slide 43)
    # ─────────────────────────────────────────────────────────────────────────
    def destroy_restore_quote(self):
        tag = self.section_tag("slide 43", TEXT_PURPLE).to_corner(UL, buff=0.48)

        quote_box = self.soft_box(9.0, 3.0, color=TEXT_PURPLE, fill_opacity=0.06, stroke_opacity=0.5)
        quote_box.move_to([0, 0.3, 0])
        line1 = self.label("Destroy structure slowly.", 36, FORWARD_COLOR, font=FONT_TITLE)
        line2 = self.label("Then learn to restore it.", 36, REVERSE_CYAN, font=FONT_TITLE)
        VGroup(line1, line2).arrange(DOWN, buff=0.42).move_to(quote_box)

        tagline = self.takeaway(
            "Forward process is known by design. Reverse process must be learned.",
            IMAGE_BLUE,
        ).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(quote_box), run_time=0.8)
        self.play(Write(line1), run_time=0.9)
        self.play(Write(line2), run_time=0.9)
        self.play(FadeIn(tagline, shift=0.1 * UP), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.5 — Training vs Sampling split screen (Slide 44)
    # ─────────────────────────────────────────────────────────────────────────
    def training_vs_sampling_split(self):
        tag = self.section_tag("slide 44", IMAGE_BLUE).to_corner(UL, buff=0.48)

        divider = Line([0, 3.2, 0], [0, -3.2, 0], color=DIM, stroke_width=1.2)

        # ── Left: Training ──
        left_title = self.label("Training", 28, FORWARD_COLOR, font=FONT_TITLE)
        left_title.move_to([-3.5, 2.6, 0])

        clean_path = self.first_asset(
            "external_40_56/cat_clean.jpg",
            "generated_40_56/cat_noise_00.png",
        )
        def process_chip(text: str, tex: str | None, color: str, width: float = 2.35) -> VGroup:
            box = self.soft_box(width, 0.82, color=color, fill_opacity=0.07, stroke_opacity=0.7)
            if tex:
                text_lbl = self.label(text, 14, MUTED, font=FONT_BODY)
                math_lbl = self.math_label(tex, 27, color)
                self.fit_to_box(math_lbl, width - 0.28, 0.36)
                content = VGroup(text_lbl, math_lbl).arrange(DOWN, buff=0.02).move_to(box)
            else:
                content = self.label(text, SMALL_SIZE, color, font=FONT_TITLE)
                self.fit_to_box(content, width - 0.25, 0.46)
                content.move_to(box)
            return VGroup(box, content)

        # Steps: x0 -> noisy x_t -> model -> eps_hat
        step_labels_l = [
            ("clean", r"x_0"),
            ("add noise", r"\varepsilon"),
            ("noisy", r"x_t"),
            ("U-Net", None),
            ("pred noise", r"\hat{\varepsilon}"),
        ]
        step_colors_l = [POSITIVE_GREEN, FORWARD_COLOR, NOISE_GRAY, IMAGE_BLUE, PUZZLE_GOLD]
        left_steps = VGroup()
        for (txt, tex), col in zip(step_labels_l, step_colors_l):
            left_steps.add(process_chip(txt, tex, col, width=2.18))
        left_steps.arrange(DOWN, buff=0.10).move_to([-3.5, -0.24, 0])

        left_arrows = VGroup()
        for i in range(len(left_steps) - 1):
            arr = Arrow(
                left_steps[i].get_bottom(),
                left_steps[i + 1].get_top(),
                buff=0.04,
                color=FORWARD_COLOR,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.25,
            )
            left_arrows.add(arr)

        # ── Right: Sampling ──
        right_title = self.label("Sampling", 28, REVERSE_CYAN, font=FONT_TITLE)
        right_title.move_to([3.5, 2.6, 0])

        step_labels_r = [
            ("noise", r"x_T \sim \mathcal{N}(0,I)"),
            ("denoise step", r"t=T"),
            ("denoise step", r"t=2"),
            ("denoise step", r"t=1"),
            ("image", r"x_0"),
        ]
        step_colors_r = [FORWARD_COLOR, NOISE_GRAY, NOISE_GRAY, IMAGE_BLUE, POSITIVE_GREEN]
        right_steps = VGroup()
        for (txt, tex), col in zip(step_labels_r, step_colors_r):
            right_steps.add(process_chip(txt, tex, col, width=2.72))
        right_steps.arrange(DOWN, buff=0.10).move_to([3.5, -0.24, 0])

        right_arrows = VGroup()
        for i in range(len(right_steps) - 1):
            arr = Arrow(
                right_steps[i].get_bottom(),
                right_steps[i + 1].get_top(),
                buff=0.04,
                color=REVERSE_CYAN,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.25,
            )
            right_arrows.add(arr)

        elegance_lbl = self.takeaway(
            "Training goes left→right. Sampling goes right→left. Two symmetric processes.",
            PUZZLE_GOLD,
        ).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(tag), Create(divider), run_time=0.8)
        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(s) for s in left_steps], lag_ratio=0.12),
            LaggedStart(*[FadeIn(s) for s in right_steps], lag_ratio=0.12),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in left_arrows], lag_ratio=0.12),
            LaggedStart(*[GrowArrow(a) for a in right_arrows], lag_ratio=0.12),
            run_time=1.5,
        )
        self.play(FadeIn(elegance_lbl, shift=0.1 * UP), run_time=0.8)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.6 — Noise prediction: the model predicts ε, not clean image (Slide 45)
    # ─────────────────────────────────────────────────────────────────────────
    def noise_prediction_secret(self):
        tag = self.section_tag("slide 45", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("The model predicts noise — not the clean image.", color=TEXT_PURPLE)

        # Input: noisy image + timestep
        noisy_path = self.first_asset("generated_40_56/cat_from_clean_noise_050.png", "generated_40_56/cat_noise_50.png")
        if noisy_path:
            noisy_vis = ImageMobject(str(noisy_path)).scale_to_fit_height(1.8)
        else:
            noisy_vis = self.placeholder_visual("image", 1.8, 1.8, NOISE_GRAY)
        noisy_vis.move_to([-4.6, 0, 0])
        noisy_lbl = self.mixed_label([("text", "noisy"), ("math", r"x_t")], SMALL_SIZE, NOISE_GRAY, font=FONT_BODY)
        noisy_lbl.next_to(noisy_vis, DOWN, buff=0.12)

        t_chip = self.mixed_chip([("text", "timestep"), ("math", r"t")], PUZZLE_GOLD, 1.75).move_to([-4.6, -1.8, 0])

        # U-Net block
        unet = self.module("Diffusion Model\n(U-Net)", IMAGE_BLUE, 2.8, 1.4).move_to([0, 0, 0])

        # Output: predicted noise
        pred_path = self.first_asset("generated_40_56/predicted_noise_good.png")
        if pred_path:
            pred_vis = ImageMobject(str(pred_path)).scale_to_fit_height(1.8)
        else:
            pred_vis = self.placeholder_visual("image", 1.8, 1.8, PUZZLE_GOLD)
        pred_vis.move_to([4.6, 0, 0])
        pred_lbl = self.mixed_label([("text", "pred noise"), ("math", r"\hat{\varepsilon}")], SMALL_SIZE, PUZZLE_GOLD, font=FONT_BODY)
        pred_lbl.next_to(pred_vis, DOWN, buff=0.12)

        # Arrows
        arr_in1 = Arrow([-3.6, 0, 0], unet[0].get_left(), buff=0.05, color=NOISE_GRAY, stroke_width=2.8, max_tip_length_to_length_ratio=0.2)
        arr_in2 = Arrow([-3.6, -1.8, 0], unet[0].get_bottom() + 0.1 * RIGHT, buff=0.05, color=PUZZLE_GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr_out = Arrow(unet[0].get_right(), [3.6, 0, 0], buff=0.05, color=PUZZLE_GOLD, stroke_width=2.8, max_tip_length_to_length_ratio=0.2)

        # Big text at bottom
        secret_lbl = self.mixed_label(
            [("text", "Output = predicted noise"), ("math", r"\hat{\varepsilon}_\theta(x_t,t)")],
            SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_TITLE,
        )
        self.fit_to_box(secret_lbl, 6.8, 0.45)
        secret_lbl.move_to([0, -2.42, 0])

        subtract_lbl = self.takeaway(
            "noisy image − predicted noise  ≈  slightly cleaner image",
            REVERSE_CYAN,
        ).to_edge(DOWN, buff=0.22)

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(FadeIn(Group(noisy_vis, noisy_lbl)), FadeIn(t_chip), run_time=1.0)
        self.play(FadeIn(unet), GrowArrow(arr_in1), GrowArrow(arr_in2), run_time=1.2)
        self.play(GrowArrow(arr_out), FadeIn(Group(pred_vis, pred_lbl)), run_time=1.0)
        self.play(FadeIn(secret_lbl), run_time=0.8)
        self.wait(4.0)
        self.play(FadeIn(subtract_lbl, shift=0.1 * UP), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 6.7 — MSE Loss animation (Slide 45)
    # ─────────────────────────────────────────────────────────────────────────
    def mse_loss_animation(self):
        tag = self.section_tag("slide 45", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Loss: minimize distance between true and predicted noise.", color=TEXT_PURPLE)

        # Two noise image cards (top half)
        true_path = self.first_asset("generated_40_56/true_noise.png")
        if true_path:
            true_vis = ImageMobject(str(true_path)).scale_to_fit_height(1.6)
        else:
            true_vis = self.placeholder_visual("image", 1.6, 1.6, PUZZLE_GOLD)
        true_vis.move_to([-3.5, 0.8, 0])
        true_lbl = self.mixed_label([("text", "true noise"), ("math", r"\varepsilon")], SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_BODY)
        true_lbl.next_to(true_vis, DOWN, buff=0.1)

        pred_path_bad = self.first_asset("generated_40_56/predicted_noise_bad.png")
        if pred_path_bad:
            pred_vis = ImageMobject(str(pred_path_bad)).scale_to_fit_height(1.6)
        else:
            pred_vis = self.placeholder_visual("image", 1.6, 1.6, REVERSE_CYAN)
        pred_vis.move_to([3.5, 0.8, 0])
        pred_lbl = self.mixed_label([("text", "pred noise"), ("math", r"\hat{\varepsilon}")], SUBTITLE_SIZE, REVERSE_CYAN, font=FONT_BODY)
        pred_lbl.next_to(pred_vis, DOWN, buff=0.1)

        # Formula (middle)
        try:
            formula = self.display_equation(
                r"\mathcal{L} = \| \varepsilon - \varepsilon_\theta(x_t, t) \|^2",
                plain="Loss = || eps - eps_hat(x_t, t) ||^2",
                width=7.4, size=34, accent=TEXT_PURPLE,
            ).move_to([0, 0.8, 0])
        except Exception:
            formula = self.label(
                "Loss = || eps - eps_hat(x_t, t) ||^2", 20, TEXT_PURPLE, font=FONT_CODE,
            ).move_to([0, 0.8, 0])

        # Loss counter as simple label sequence (no always_redraw issues)
        loss_stages = [
            (1.42, NEGATIVE_ORANGE),
            (0.73, NEGATIVE_ORANGE),
            (0.21, PUZZLE_GOLD),
            (0.04, POSITIVE_GREEN),
        ]

        loss_lbl0 = self.label(
            f"Loss: {loss_stages[0][0]:.2f}", 32, loss_stages[0][1], font=FONT_TITLE,
        ).move_to([0, -1.2, 0])

        check = self.label(
            "Noise prediction converged", SUBTITLE_SIZE, POSITIVE_GREEN, font=FONT_TITLE,
        ).move_to([0, -2.6, 0])

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(
            FadeIn(Group(true_vis, true_lbl)),
            FadeIn(Group(pred_vis, pred_lbl)),
            run_time=1.0,
        )
        self.play(FadeIn(formula), run_time=0.8)
        self.play(FadeIn(loss_lbl0), run_time=0.5)
        self.wait(1.2)

        # Animate loss dropping with Transform
        for val, col in loss_stages[1:]:
            new_lbl = self.label(f"Loss: {val:.2f}", 32, col, font=FONT_TITLE).move_to([0, -1.2, 0])
            self.play(Transform(loss_lbl0, new_lbl), run_time=0.6)
            self.wait(1.0)

        self.play(FadeIn(check, shift=0.1 * UP), run_time=0.8)
        self.wait(10.0)
        self.final_hold_group = Group(*self.mobjects)
