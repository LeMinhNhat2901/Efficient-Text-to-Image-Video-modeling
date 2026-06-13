from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.v02_common import *

FORWARD_COLOR = "#FF8A3D"
REVERSE_CYAN  = "#00E5FF"
NOISE_GRAY    = "#8899AA"
GUIDANCE_GOLD = "#F5C542"


class V02Guidance(TextPixelsScene):
    """Classifier Guidance, CFG, CLIP Guidance."""

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s08_guidance.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        scene_start = self.time

        self.construct_intro(
            "The Art of Steering: Guidance",
            "Classifier, Classifier-Free, and CLIP Guidance",
        )

        self.hook_many_directions()
        self.classifier_guidance_field()
        self.classifier_guidance_formula()
        self.scale_factor_slider()
        self.cfg_transition()
        self.cfg_formula()
        self.clip_guidance()
        self.guidance_summary_table()
        self.references_transition()
        self.hold_for_voiceover(scene_start, voiceover)
        if hasattr(self, "final_hold_group"):
            self.play(FadeOut(self.final_hold_group), run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.1 — Hook: one noise → many directions (Slide 52)
    # ─────────────────────────────────────────────────────────────────────────
    def hook_many_directions(self):
        tag = self.section_tag("slide 52", GUIDANCE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Noise alone can become many things.\nGuidance decides the direction.", color=GUIDANCE_GOLD)

        # Center: pure noise
        noise_path = self.first_asset("generated_40_56/cat_from_clean_noise_100.png", "generated_40_56/cat_noise_100.png")
        if noise_path:
            noise_vis = ImageMobject(str(noise_path)).scale_to_fit_height(1.8)
        else:
            noise_vis = self.placeholder_visual("image", 1.8, 1.8, NOISE_GRAY)
        noise_vis.move_to(ORIGIN)
        noise_frame = self.soft_box(2.1, 2.1, color=NOISE_GRAY, fill_opacity=0.04, stroke_opacity=0.55)
        noise_frame.move_to(ORIGIN)
        noise_lbl = self.mixed_label([("text", "noise"), ("math", r"x_T")], SMALL_SIZE, NOISE_GRAY, font=FONT_BODY).next_to(noise_frame, DOWN, buff=0.12)

        # Three output cards: tabby, lion, leopard
        output_data = [
            ("external_40_56/output_tabby_cat.jpg", "tabby cat",  IMAGE_BLUE,   [-4.5,  1.8, 0]),
            ("external_40_56/output_lion.jpg",      "lion",        PUZZLE_GOLD,  [-4.5, -1.8, 0]),
            ("external_40_56/output_leopard.jpg",   "leopard",     TEXT_PURPLE,  [4.5,   0.0, 0]),
        ]

        output_cards = []
        for path_str, label_text, col, pos in output_data:
            path = self.first_asset(path_str)
            if path:
                vis = ImageMobject(str(path)).scale_to_fit_height(1.5)
            else:
                vis = self.placeholder_visual("image", 1.5, 1.5, col)
            frame = self.soft_box(1.9, 1.9, color=col, fill_opacity=0.06, stroke_opacity=0.7)
            lbl = self.label(label_text, SMALL_SIZE, col, font=FONT_CODE)
            card = Group(frame, vis, lbl.next_to(frame, DOWN, buff=0.1))
            card.move_to(pos)
            output_cards.append((card, col))

        # Bezier curves from noise to outputs
        curves = VGroup()
        for card, col in output_cards:
            curve = CurvedArrow(
                noise_frame.get_center(),
                card[0].get_center(),
                angle=0.32 if card[0].get_center()[1] > 0 else -0.32,
                color=col,
                stroke_width=2.5,
            )
            curves.add(curve)

        # Steering wheel icon (compass circles)
        compass = VGroup(
            Circle(radius=0.55, color=GUIDANCE_GOLD, stroke_width=3),
            Arrow([0, 0.42, 0], [0, -0.42, 0], buff=0, color=GUIDANCE_GOLD, stroke_width=3, max_tip_length_to_length_ratio=0.35),
            Arrow([-0.42, 0, 0], [0.42, 0, 0], buff=0, color=PUZZLE_GOLD, stroke_width=2, max_tip_length_to_length_ratio=0.3),
            Dot(ORIGIN, radius=0.07, color=GUIDANCE_GOLD),
        ).scale(0.75).to_corner(DR, buff=0.55)
        compass_lbl = self.label("Guidance", SMALL_SIZE, GUIDANCE_GOLD, font=FONT_CODE).next_to(compass, DOWN, buff=0.1)

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(FadeIn(noise_frame), FadeIn(noise_vis), FadeIn(noise_lbl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c, _ in output_cards], lag_ratio=0.2), run_time=1.8)
        self.play(LaggedStart(*[Create(curve) for curve in curves], lag_ratio=0.2), run_time=1.8)
        self.play(FadeIn(compass), FadeIn(compass_lbl), run_time=0.8)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.2 — Classifier guidance: vector field bending toward "cats" (Slide 52)
    # ─────────────────────────────────────────────────────────────────────────
    def classifier_guidance_field(self):
        tag = self.section_tag("slide 52", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("With classifier guidance — sampling bends toward 'cats'.", color=IMAGE_BLUE)

        # Latent space 2D region
        region = RoundedRectangle(width=11, height=5.0, corner_radius=0.2,
                                  color=DIM, stroke_opacity=0.3, fill_color=BG, fill_opacity=1)
        region.move_to([0, -0.2, 0])

        # "High-probability cats" ellipse
        cats_zone = Ellipse(width=3.5, height=2.2, color=POSITIVE_GREEN, stroke_opacity=0.7, fill_color=POSITIVE_GREEN, fill_opacity=0.08)
        cats_zone.move_to([3.2, 0.8, 0])
        cats_zone_lbl = self.label('High p("cats")', SMALL_SIZE, POSITIVE_GREEN, font=FONT_CODE)
        cats_zone_lbl.move_to(cats_zone.get_center() + 1.4 * UP)

        # Random sampling path (no guidance) — dashed, meandering
        rng3 = np.random.default_rng(13)
        no_guide_pts = [np.array([-4.2, 0.0, 0])]
        for _ in range(8):
            prev = no_guide_pts[-1]
            step = np.array([0.9, rng3.uniform(-0.45, 0.45), 0])
            no_guide_pts.append(prev + step)
        no_guide_path = VMobject(color=NOISE_GRAY, stroke_width=2.0, stroke_opacity=0.6)
        no_guide_path.set_points_as_corners(no_guide_pts)
        no_guide_lbl = self.label("without guidance", SMALL_SIZE, NOISE_GRAY, font=FONT_CODE)
        no_guide_lbl.next_to(no_guide_pts[-1], DOWN, buff=0.15)

        # Guided sampling path — curves toward cats zone
        guide_pts = [np.array([-4.2, -1.2, 0])]
        targets = [
            np.array([-2.8, -0.6, 0]),
            np.array([-1.2, 0.2, 0]),
            np.array([0.8, 0.8, 0]),
            np.array([2.4, 0.9, 0]),
            np.array([3.0, 0.8, 0]),
        ]
        guide_pts.extend(targets)
        guide_path = VMobject(color=IMAGE_BLUE, stroke_width=3.2)
        guide_path.set_points_smoothly(guide_pts)
        guide_end_dot = Dot(guide_pts[-1], radius=0.12, color=POSITIVE_GREEN)
        guide_lbl = self.label("with classifier guidance", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE)
        guide_lbl.next_to(guide_pts[-1], DR, buff=0.12)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(region), run_time=1.0)
        self.play(FadeIn(cats_zone), FadeIn(cats_zone_lbl), run_time=0.8)
        self.play(Create(no_guide_path), FadeIn(no_guide_lbl), run_time=2.0)
        self.play(Create(guide_path), FadeIn(guide_lbl), FadeIn(guide_end_dot), run_time=2.5)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.3 — Classifier guidance architecture & formula (Slide 53)
    # ─────────────────────────────────────────────────────────────────────────
    def classifier_guidance_formula(self):
        tag = self.section_tag("slide 53", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Classifier gradient steers the reverse process.", color=IMAGE_BLUE)

        # Architecture diagram
        x_t_chip = self.mixed_chip([("text", "noisy"), ("math", r"x_t")], NOISE_GRAY, 2.0).move_to([-5.0, 1.0, 0])

        diff_block = self.module("Diffusion\nModel", IMAGE_BLUE, 2.2, 1.2).move_to([-1.5, 1.0, 0])
        class_block = VGroup(
            self.soft_box(2.2, 1.2, color=POSITIVE_GREEN, fill_opacity=0.055, stroke_opacity=0.68),
            VGroup(
                self.label("Classifier", SMALL_SIZE, POSITIVE_GREEN, font=FONT_BODY),
                self.math_label(r"p(y\mid x_t)", SMALL_SIZE, POSITIVE_GREEN),
            ).arrange(DOWN, buff=0.06),
        )
        class_block[1].move_to(class_block[0])
        class_block.move_to([-1.5, -1.2, 0])

        arr1 = Arrow(x_t_chip.get_right(), diff_block[0].get_left(), buff=0.05, color=NOISE_GRAY, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr2 = Arrow(x_t_chip.get_right(), class_block[0].get_left() + 0.2 * UP, buff=0.05, color=NOISE_GRAY, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)

        y_chip = self.mixed_chip([("text", "label"), ("math", r"y=\mathrm{cats}")], POSITIVE_GREEN, 2.4).move_to([-1.5, -2.8, 0])
        arr_y = Arrow(y_chip.get_top(), class_block[0].get_bottom(), buff=0.05, color=POSITIVE_GREEN, stroke_width=2.0, max_tip_length_to_length_ratio=0.2)

        grad_lbl = self.mixed_label([("text", "gradient"), ("math", r"\nabla \log p(y\mid x_t)")], SMALL_SIZE, POSITIVE_GREEN, font=FONT_BODY).move_to([2.55, -1.2, 0])
        grad_arr = Arrow(class_block[0].get_right(), grad_lbl.get_left(), buff=0.05, color=POSITIVE_GREEN, stroke_width=2.2, max_tip_length_to_length_ratio=0.25)

        # Formula
        formula = self.math_label(
            r"\mathrm{final\ direction}=f(x_t,y)+s\,\nabla\log p(y\mid x_t)",
            28, IMAGE_BLUE,
        )
        self.fit_to_box(formula, 4.7, 0.62)
        formula.move_to([3.25, 1.85, 0])
        formula_box = SurroundingRectangle(formula, color=IMAGE_BLUE, buff=0.16, stroke_width=2.2)

        s_note = self.label("s = guidance scale", SMALL_SIZE, GUIDANCE_GOLD, font=FONT_CODE).next_to(formula_box, DOWN, buff=0.18)

        self.play(FadeIn(tag), FadeIn(title), run_time=0.8)
        self.play(FadeIn(x_t_chip), FadeIn(diff_block), FadeIn(class_block), run_time=1.0)
        self.play(GrowArrow(arr1), GrowArrow(arr2), FadeIn(y_chip), GrowArrow(arr_y), run_time=1.2)
        self.play(GrowArrow(grad_arr), FadeIn(grad_lbl), run_time=0.9)
        self.play(FadeIn(formula), Create(formula_box), FadeIn(s_note), run_time=1.0)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.4 — Scale factor slider tradeoff (Slide 53)
    # ─────────────────────────────────────────────────────────────────────────
    def scale_factor_slider(self):
        tag = self.section_tag("slide 53", GUIDANCE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Guidance scale s: diversity vs. control.", color=GUIDANCE_GOLD)

        # Slider visual
        slider_bar = Rectangle(width=9.0, height=0.22, color=DIM, fill_color=DIM, fill_opacity=0.55)
        slider_bar.move_to([0, 1.2, 0])

        ticks_data = [(-3.8, "s = 0", NOISE_GRAY), (0, "s = 3", POSITIVE_GREEN), (3.8, "s = 10", FORWARD_COLOR)]
        ticks = VGroup()
        tick_lbls = VGroup()
        for x, lbl, col in ticks_data:
            tick = Line([x, 0.9, 0], [x, 1.5, 0], color=col, stroke_width=3)
            t_lbl = self.label(lbl, SUBTITLE_SIZE, col, font=FONT_CODE).move_to([x, 0.5, 0])
            ticks.add(tick)
            tick_lbls.add(t_lbl)

        # Three output cards
        card_data = [
            (-3.8, "Diverse\nless controlled",  NOISE_GRAY,     "external_40_56/output_tabby_cat.jpg"),
            (0.0,  "Balanced\nbest quality",     POSITIVE_GREEN, "external_40_56/output_tabby_cat.jpg"),
            (3.8,  "Controlled\nless flexible",  FORWARD_COLOR,  "external_40_56/output_tabby_cat.jpg"),
        ]
        cards = Group()
        for x, desc, col, path_str in card_data:
            path = self.first_asset(path_str)
            if path:
                vis = ImageMobject(str(path)).scale_to_fit_height(1.6)
            else:
                vis = self.placeholder_visual("image", 1.6, 1.6, col)
            frame = self.soft_box(2.1, 2.0, color=col, fill_opacity=0.06, stroke_opacity=0.7)
            lbl = self.label(desc, SMALL_SIZE, col, font=FONT_CODE)
            card = Group(frame, vis, lbl.next_to(frame, DOWN, buff=0.1))
            card.move_to([x, -1.8, 0])
            cards.add(card)

        # Highlight middle card as best
        best_box = SurroundingRectangle(cards[1], color=POSITIVE_GREEN, buff=0.1, stroke_width=3)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(slider_bar), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.14), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in tick_lbls], lag_ratio=0.14), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.2), run_time=1.8)
        self.play(Create(best_box), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.5 & 8.6 — CFG: ghost model, two predictions (Slide 54)
    # ─────────────────────────────────────────────────────────────────────────
    def cfg_transition(self):
        tag = self.section_tag("slide 54", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Classifier-Free Guidance: same model, two forward passes.", color=TEXT_PURPLE)

        # Limitation text
        limit_box = self.soft_box(9.0, 1.4, color=NEGATIVE_ORANGE, fill_opacity=0.06, stroke_opacity=0.6).move_to([0, 2.0, 0])
        limit_lbl = self.label(
            "⚠  Classifier guidance needs a separate classifier\n   trained on noisy images — not always convenient.",
            SMALL_SIZE, NEGATIVE_ORANGE, font=FONT_CODE,
        )
        self.fit_to_box(limit_lbl, 8.5, 1.0)
        limit_lbl.move_to(limit_box)

        # CFG: one model block, split into two ghost paths
        x_t_chip = self.mixed_chip([("text", "noisy"), ("math", r"x_t")], NOISE_GRAY, 2.0).move_to([-5.0, 0, 0])

        model_main = self.module("Diffusion Model\n(shared weights)", TEXT_PURPLE, 3.0, 1.2).move_to([0, 0, 0])

        # Two output branches
        cond_box = self.soft_box(2.8, 0.9, color=IMAGE_BLUE, fill_opacity=0.07, stroke_opacity=0.7).move_to([4.8, 1.2, 0])
        cond_lbl = VGroup(
            self.label("conditional", SMALL_SIZE, IMAGE_BLUE, font=FONT_BODY),
            self.math_label(r"f(x_t,y=\mathrm{cats})", 22, IMAGE_BLUE),
        ).arrange(DOWN, buff=0.05)
        self.fit_to_box(cond_lbl, 2.5, 0.75).move_to(cond_box)

        uncond_box = self.soft_box(2.8, 0.9, color=NOISE_GRAY, fill_opacity=0.07, stroke_opacity=0.6).move_to([4.8, -1.2, 0])
        uncond_lbl = VGroup(
            self.label("unconditional", SMALL_SIZE, NOISE_GRAY, font=FONT_BODY),
            self.math_label(r"f(x_t,\varnothing)", 22, NOISE_GRAY),
        ).arrange(DOWN, buff=0.05)
        self.fit_to_box(uncond_lbl, 2.5, 0.75).move_to(uncond_box)

        arr_in = Arrow(x_t_chip.get_right(), model_main[0].get_left(), buff=0.05, color=NOISE_GRAY, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr_cond = Arrow(model_main[0].get_right() + 0.18 * UP, cond_box.get_left(), buff=0.05, color=IMAGE_BLUE, stroke_width=2.2, max_tip_length_to_length_ratio=0.22)
        arr_uncond = Arrow(model_main[0].get_right() - 0.18 * UP, uncond_box.get_left(), buff=0.05, color=NOISE_GRAY, stroke_width=2.2, max_tip_length_to_length_ratio=0.22)

        diff_lbl = self.math_label(r"\mathrm{condition\ direction}=f(x_t,y)-f(x_t,\varnothing)", 28, GUIDANCE_GOLD)
        diff_lbl.to_edge(DOWN, buff=0.5)
        diff_box = SurroundingRectangle(diff_lbl, color=GUIDANCE_GOLD, buff=0.14, stroke_width=2.2)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(limit_box), FadeIn(limit_lbl), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(limit_box), FadeOut(limit_lbl), run_time=0.7)

        self.play(FadeIn(x_t_chip), FadeIn(model_main), GrowArrow(arr_in), run_time=1.0)
        self.play(GrowArrow(arr_cond), FadeIn(cond_box), FadeIn(cond_lbl), run_time=0.9)
        self.play(GrowArrow(arr_uncond), FadeIn(uncond_box), FadeIn(uncond_lbl), run_time=0.9)
        self.play(FadeIn(diff_lbl), Create(diff_box), run_time=1.0)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.7 — CFG formula + cyberpunk cat prompt (Slide 54)
    # ─────────────────────────────────────────────────────────────────────────
    def cfg_formula(self):
        tag = self.section_tag("slide 54", TEXT_PURPLE).to_corner(UL, buff=0.48)

        prompt_text = '"A cyberpunk cat wearing neon glasses"'
        prompt_shell = self.prompt_bar("", width=9.5, color=TEXT_PURPLE)
        prompt_shell.move_to([0, 2.5, 0])
        prompt_label = self.label("", SMALL_SIZE, TEXT, font=FONT_BODY)
        prompt_label.move_to(prompt_shell[0].get_center() + 0.08 * RIGHT)
        prompt_cursor = prompt_shell[3]

        cfg_formula = self.math_label(
            r"f(x_t,y)+s\left(f(x_t,y)-f(x_t,\varnothing)\right)",
            32, TEXT_PURPLE,
        ).move_to([0, 0.8, 0])
        cfg_box = SurroundingRectangle(cfg_formula, color=TEXT_PURPLE, buff=0.18, stroke_width=2.5)

        # Cyberpunk cat preview
        cyber_path = self.first_asset("external_40_56/cyberpunk_cat.jpg")
        if cyber_path:
            cyber_vis = ImageMobject(str(cyber_path)).scale_to_fit_height(2.2)
        else:
            cyber_vis = self.placeholder_visual("image", 2.2, 2.2, TEXT_PURPLE)
        cyber_vis.move_to([4.0, -1.0, 0])
        cyber_lbl = self.label("output: cyberpunk cat", SMALL_SIZE, TEXT_PURPLE, font=FONT_CODE)
        cyber_lbl.next_to(cyber_vis, DOWN, buff=0.1)

        # CFG scale visual
        scale_line = Arrow([-3.8, -1.2, 0], [1.5, -1.2, 0], buff=0, color=GUIDANCE_GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.12)
        scale_lbl = self.label("CFG scale  s →  larger = stronger conditioning", SMALL_SIZE, GUIDANCE_GOLD, font=FONT_CODE)
        scale_lbl.next_to(scale_line, DOWN, buff=0.15)

        takeaway = self.takeaway(
            "CFG amplifies what the condition changes — no external classifier needed.",
            POSITIVE_GREEN,
        ).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(tag), FadeIn(prompt_shell[0]), FadeIn(prompt_shell[1]), FadeIn(prompt_cursor), run_time=0.55)
        current_prompt = prompt_label
        self.add(current_prompt)
        for i in range(2, len(prompt_text) + 1, 2):
            new_prompt = self.label(prompt_text[:i], SMALL_SIZE, TEXT, font=FONT_BODY)
            self.fit_to_box(new_prompt, 8.5, 0.46)
            new_prompt.move_to(prompt_shell[0].get_center() + 0.08 * RIGHT)
            self.play(
                Transform(current_prompt, new_prompt),
                prompt_cursor.animate.next_to(new_prompt, RIGHT, buff=0.08),
                run_time=0.045,
                rate_func=linear,
            )
        self.play(FadeIn(cfg_formula), Create(cfg_box), run_time=1.0)
        self.play(FadeIn(Group(cyber_vis, cyber_lbl)), run_time=0.9)
        self.play(GrowArrow(scale_line), FadeIn(scale_lbl), run_time=0.9)
        self.play(FadeIn(takeaway, shift=0.1 * UP), run_time=0.8)
        self.wait(11.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.8 — CLIP Guidance (Slide 55)
    # ─────────────────────────────────────────────────────────────────────────
    def clip_guidance(self):
        tag = self.section_tag("slide 55", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("CLIP Guidance: steer using image-text similarity.", color=PUZZLE_GOLD)

        # Prompt
        prompt_bar = self.prompt_bar('"A cyberpunk cat"', width=6.4, color=TEXT_PURPLE)
        prompt_bar.move_to([0, 2.18, 0])

        # Text encoder
        text_enc = self.module("Text Encoder\n(CLIP)", TEXT_PURPLE, 2.4, 1.0).move_to([-3.0, 0.78, 0])
        # Image encoder
        img_enc = self.module("Image Encoder\n(CLIP)", IMAGE_BLUE, 2.4, 1.0).move_to([-3.0, -1.12, 0])

        arr_te = Arrow(prompt_bar[0].get_bottom(), text_enc[0].get_top(), buff=0.05, color=TEXT_PURPLE, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)

        noisy_path = self.first_asset("generated_40_56/cat_from_clean_noise_050.png", "generated_40_56/cat_noise_50.png")
        if noisy_path:
            noisy_vis = ImageMobject(str(noisy_path)).scale_to_fit_height(1.2)
        else:
            noisy_vis = self.placeholder_visual("image", 1.2, 1.2, NOISE_GRAY)
        noisy_vis.move_to([-5.5, -1.12, 0])
        arr_ie = Arrow(noisy_vis.get_right(), img_enc[0].get_left(), buff=0.05, color=NOISE_GRAY, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)

        # Embedding space
        embed_space = Ellipse(width=3.5, height=3.0, color=DIM, stroke_opacity=0.45, fill_color=DIM, fill_opacity=0.04)
        embed_space.move_to([3.0, -0.05, 0])
        embed_lbl = self.label("co-embedding space", SMALL_SIZE, DIM, font=FONT_CODE).next_to(embed_space, UP, buff=0.1)

        # Text vector and image vector in embedding space
        text_vec_dot = Dot([2.0, 0.85, 0], radius=0.1, color=TEXT_PURPLE)
        text_vec_lbl = self.math_label(r"c_t(y)", SMALL_SIZE, TEXT_PURPLE).next_to(text_vec_dot, UR, buff=0.06)

        img_vec_dot_start = Dot([4.2, -1.18, 0], radius=0.1, color=IMAGE_BLUE)
        img_vec_lbl = self.math_label(r"c_i(x_t)", SMALL_SIZE, IMAGE_BLUE).next_to(img_vec_dot_start, DR, buff=0.06)

        # Guidance arrow pulling image vector toward text vector
        guidance_arr = Arrow(
            img_vec_dot_start.get_center(),
            [2.3, 0.58, 0],
            buff=0,
            color=POSITIVE_GREEN,
            stroke_width=3.2,
            max_tip_length_to_length_ratio=0.25,
        )
        guidance_arr_lbl = self.label("CLIP guidance", SMALL_SIZE, POSITIVE_GREEN, font=FONT_CODE)
        guidance_arr_lbl.next_to(guidance_arr, RIGHT, buff=0.12)

        # Similarity formula
        sim_formula = self.math_label(
            r"\mathrm{similarity}=c_i(x_t)^\top c_t(y)",
            30, PUZZLE_GOLD,
        ).to_edge(DOWN, buff=0.48)

        output_path = self.first_asset("external_40_56/cyberpunk_cat.jpg")
        if output_path:
            output_vis = ImageMobject(str(output_path)).scale_to_fit_height(1.5)
        else:
            output_vis = self.placeholder_visual("image", 1.5, 1.5, PUZZLE_GOLD)
        output_vis.move_to([5.0, -2.5, 0])
        output_lbl = self.label("→ aligned output", SMALL_SIZE, PUZZLE_GOLD, font=FONT_CODE)
        output_lbl.next_to(output_vis, DOWN, buff=0.1)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(prompt_bar), run_time=1.0)
        self.play(FadeIn(text_enc), GrowArrow(arr_te), run_time=0.9)
        self.play(FadeIn(noisy_vis), FadeIn(img_enc), GrowArrow(arr_ie), run_time=0.9)
        self.play(FadeIn(embed_space), FadeIn(embed_lbl), FadeIn(text_vec_dot), FadeIn(text_vec_lbl), run_time=1.0)
        self.play(FadeIn(img_vec_dot_start), FadeIn(img_vec_lbl), run_time=0.8)
        self.wait(1.5)
        self.play(GrowArrow(guidance_arr), FadeIn(guidance_arr_lbl), run_time=1.0)
        self.play(FadeIn(sim_formula), run_time=0.8)
        self.play(FadeIn(Group(output_vis, output_lbl)), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.9 — Guidance summary table (Slides 52–55)
    # ─────────────────────────────────────────────────────────────────────────
    def guidance_summary_table(self):
        tag = self.section_tag("slides 52–55", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Three ways to steer diffusion sampling.", color=IMAGE_BLUE)

        cols = [
            ("Classifier\nGuidance", IMAGE_BLUE,
             ["External noisy-image classifier", "Label-based conditioning", "Classifier gradient"]),
            ("Classifier-Free\nGuidance", TEXT_PURPLE,
             ["Same diffusion model", "Conditional vs. unconditional", "Scale amplifies direction"]),
            ("CLIP\nGuidance", PUZZLE_GOLD,
             ["CLIP image-text similarity", "Text or image prompt", "Similarity gradient"]),
        ]

        col_groups = VGroup()
        for header, col, bullets in cols:
            box = self.soft_box(3.75, 3.55, color=col, fill_opacity=0.045, stroke_opacity=0.72)

            header_band = self.soft_box(3.2, 0.72, color=col, fill_opacity=0.09, stroke_opacity=0.7)
            header_band.move_to(box.get_top() + 0.48 * DOWN)
            h_lbl = self.label(header, SMALL_SIZE, col, font=FONT_TITLE)
            self.fit_to_box(h_lbl, 2.9, 0.52)
            h_lbl.move_to(header_band)

            bullet_rows = VGroup()
            for bullet in bullets:
                dot = Dot(radius=0.045, color=col)
                b_lbl = self.label(bullet, SMALL_SIZE, TEXT, font=FONT_BODY)
                self.fit_to_box(b_lbl, 2.82, 0.36)
                row = VGroup(dot, b_lbl).arrange(RIGHT, buff=0.14, aligned_edge=UP)
                bullet_rows.add(row)
            bullet_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            bullet_rows.move_to(box.get_center() + 0.22 * DOWN)

            col_groups.add(VGroup(box, header_band, h_lbl, bullet_rows))
        col_groups.arrange(RIGHT, buff=0.36).move_to([0, -0.28, 0])

        conclusion_box = self.soft_box(
            8.1, 0.66, color=POSITIVE_GREEN,
            fill_opacity=0.045, stroke_opacity=0.7,
        ).to_edge(DOWN, buff=0.42)
        conclusion_lbl = self.label(
            "Guidance turns denoising into conditional generation.",
            SMALL_SIZE, TEXT, font=FONT_TITLE,
        )
        self.fit_to_box(conclusion_lbl, 7.7, 0.38)
        conclusion_lbl.move_to(conclusion_box)
        conclusion = VGroup(conclusion_box, conclusion_lbl)

        self.play(FadeIn(tag), FadeIn(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in col_groups], lag_ratio=0.22), run_time=2.0)
        self.play(FadeIn(conclusion, shift=0.1 * UP), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 8.10 — References transition (Slide 56)
    # ─────────────────────────────────────────────────────────────────────────
    def references_transition(self):
        title = self.hook_question("Guidance turns a prompt into a direction.", color=IMAGE_BLUE)

        stage_specs = [
            ("Text\nprompt", TEXT_PURPLE),
            ("Guidance", GUIDANCE_GOLD),
            ("Reverse\ndiffusion", REVERSE_CYAN),
            ("Image", POSITIVE_GREEN),
        ]
        stages = VGroup()
        for label_text, col in stage_specs:
            box = self.soft_box(2.35, 1.05, color=col, fill_opacity=0.06, stroke_opacity=0.7)
            label = self.label(label_text, SUBTITLE_SIZE, col, font=FONT_TITLE)
            self.fit_to_box(label, 2.05, 0.72)
            label.move_to(box)
            stages.add(VGroup(box, label))
        stages.arrange(RIGHT, buff=0.42).move_to([0, 1.05, 0])

        arrows = VGroup()
        for left, right in zip(stages[:-1], stages[1:]):
            arrows.add(Arrow(
                left[0].get_right(),
                right[0].get_left(),
                buff=0.08,
                color=IMAGE_BLUE,
                stroke_width=2.6,
                max_tip_length_to_length_ratio=0.25,
            ))

        next_lbl = self.label(
            "Next: make the same process efficient in latent space",
            SUBTITLE_SIZE, POSITIVE_GREEN, font=FONT_TITLE,
        ).move_to([0, -0.55, 0])

        # Noise shrinks to latent grid
        noise_box = self.soft_box(1.8, 1.8, color=NOISE_GRAY, fill_opacity=0.1, stroke_opacity=0.55).move_to([0, -2.35, 0])
        noise_inner = self.pixel_grid(rows=4, cols=4, side=0.25, colors=(NOISE_GRAY, DIM)).move_to([0, -2.35, 0])
        latent_box = self.soft_box(1.0, 1.0, color=POSITIVE_GREEN, fill_opacity=0.1, stroke_opacity=0.7).move_to([0, -2.35, 0])
        latent_lbl = self.label("latent", SMALL_SIZE, POSITIVE_GREEN, font=FONT_CODE).next_to(latent_box, DOWN, buff=0.1)

        self.play(FadeIn(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s) for s in stages], lag_ratio=0.18), run_time=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.16), run_time=0.9)
        self.wait(2.1)
        self.play(FadeIn(next_lbl, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(noise_box), FadeIn(noise_inner), run_time=0.8)
        self.play(
            Transform(noise_box, latent_box),
            FadeOut(noise_inner),
            FadeIn(latent_lbl),
            run_time=1.5, rate_func=smooth,
        )
        self.wait(8.0)
        self.final_hold_group = Group(*self.mobjects)
