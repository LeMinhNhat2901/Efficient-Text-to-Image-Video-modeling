from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *

FORWARD_COLOR = "#FF8A3D"
REVERSE_CYAN  = "#00E5FF"
NOISE_GRAY    = "#8899AA"


class V02DiffusionMath(TextPixelsScene):
    """Scene 7 — Slides 46–51: Diffusion math, Markov chain, β schedule, α̅, loss, pseudocode."""

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s07_diffusion_math.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Diffusion Math: From Intuition to Formulas",
            "Markov chains, noise schedules, and the time-jump trick",
        )

        self.markov_chain_with_cats()
        self.one_step_transition()
        self.beta_schedule_curve()
        self.mean_shrink_to_zero()
        self.time_jump_shortcut()
        self.simple_loss()
        self.pseudocode_training()
        self.pseudocode_sampling()

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.1 — Markov chain with noisy cats (Slide 46)
    # ─────────────────────────────────────────────────────────────────────────
    def markov_chain_with_cats(self):
        tag = self.section_tag("slide 46", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("A Markov chain of progressively noised variables.", color=IMAGE_BLUE)

        noise_stages = [
            (("external_40_56/cat_clean.jpg", "generated_40_56/cat_from_clean_noise_000.png"), r"x_0", POSITIVE_GREEN),
            ("generated_40_56/cat_from_clean_noise_025.png", r"x_1",  IMAGE_BLUE),
            ("generated_40_56/cat_from_clean_noise_050.png", r"x_2",  NOISE_GRAY),
            ("generated_40_56/cat_from_clean_noise_075.png", "…",   NOISE_GRAY),
            ("generated_40_56/cat_from_clean_noise_100.png", r"x_T", FORWARD_COLOR),
        ]

        cards = Group()
        for path_spec, lbl_text, col in noise_stages:
            path = self.first_asset(*path_spec) if isinstance(path_spec, tuple) else self.first_asset(path_spec)
            size = 1.5
            if path:
                vis = ImageMobject(str(path)).scale_to_fit_height(size)
            else:
                vis = self.placeholder_visual("image", size, size, col)
            frame = self.soft_box(size + 0.2, size + 0.2, color=col, fill_opacity=0.04, stroke_opacity=0.55)
            lbl = self.label(lbl_text, SUBTITLE_SIZE, col, font=FONT_CODE) if lbl_text == "…" else self.math_label(lbl_text, SUBTITLE_SIZE, col)
            lbl.next_to(frame, DOWN, buff=0.1)
            cards.add(Group(frame, vis, lbl))

        cards.arrange(RIGHT, buff=0.42).move_to([0, 0.1, 0]).scale_to_fit_width(13.0)

        arrows = VGroup()
        for i in range(len(cards) - 1):
            arr = Arrow(
                cards[i].get_right() + 0.01 * RIGHT,
                cards[i + 1].get_left() - 0.01 * RIGHT,
                buff=0.0,
                color=FORWARD_COLOR,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.28,
            )
            beta_lbl = self.math_label(r"\beta_t", 18, FORWARD_COLOR)
            beta_lbl.next_to(arr, UP, buff=0.06)
            arrows.add(VGroup(arr, beta_lbl))

        desc = self.takeaway(
            "Each step adds a small amount of Gaussian noise, controlled by the schedule.",
            IMAGE_BLUE,
        ).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.18), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.14), run_time=1.4)
        self.play(FadeIn(desc, shift=0.1 * UP), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.2 — One-step transition formula (Slide 47)
    # ─────────────────────────────────────────────────────────────────────────
    def one_step_transition(self):
        tag = self.section_tag("slide 47", FORWARD_COLOR).to_corner(UL, buff=0.48)
        title = self.hook_question("One-step forward transition.", color=FORWARD_COLOR)

        try:
            formula = self.display_equation(
                r"q(x_t \mid x_{t-1}) = \mathcal{N}(x_t;\; \sqrt{1-\beta_t}\, x_{t-1},\; \beta_t \mathbf{I})",
                plain="q(x_t | x_{t-1}) = N( sqrt(1−β_t)·x_{t-1},  β_t I )",
                width=10.4, size=34, accent=FORWARD_COLOR,
            ).move_to([0, 1.1, 0])
        except Exception:
            formula = self.label(
                "q(x_t | x_{t-1}) = N( sqrt(1-β_t)·x_{t-1},  β_t·I )",
                20, FORWARD_COLOR, font=FONT_CODE,
            ).move_to([0, 1.1, 0])

        # Two parts: shrink + add noise
        part1_box = self.soft_box(5.0, 1.1, color=IMAGE_BLUE, fill_opacity=0.06, stroke_opacity=0.7).move_to([-3.0, -1.0, 0])
        part1_math = self.math_label(r"\sqrt{1-\beta_t}\,x_{t-1}", 29, IMAGE_BLUE)
        part1_text = self.label("Shrinks signal toward 0", SMALL_SIZE, IMAGE_BLUE, font=FONT_BODY)
        part1_lbl = VGroup(part1_math, part1_text).arrange(DOWN, buff=0.08)
        self.fit_to_box(part1_lbl, 4.7, 0.9)
        part1_lbl.move_to(part1_box)

        part2_box = self.soft_box(4.4, 1.1, color=FORWARD_COLOR, fill_opacity=0.06, stroke_opacity=0.7).move_to([3.2, -1.0, 0])
        part2_math = self.math_label(r"\beta_t \mathbf{I}", 29, FORWARD_COLOR)
        part2_text = self.label("Adds Gaussian noise", SMALL_SIZE, FORWARD_COLOR, font=FONT_BODY)
        part2_lbl = VGroup(part2_math, part2_text).arrange(DOWN, buff=0.08)
        self.fit_to_box(part2_lbl, 4.2, 0.9)
        part2_lbl.move_to(part2_box)

        plus_lbl = self.label("+", 32, TEXT, font=FONT_TITLE).move_to([0, -1.0, 0])

        note = self.takeaway(
            "Signal weakens. Noise grows. Two forces acting simultaneously.",
            NOISE_GRAY,
        ).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(tag), FadeIn(title), run_time=0.8)
        self.play(FadeIn(formula), run_time=1.0)
        self.play(FadeIn(part1_box), FadeIn(part1_lbl), FadeIn(plus_lbl), FadeIn(part2_box), FadeIn(part2_lbl), run_time=1.2)
        self.play(FadeIn(note, shift=0.1 * UP), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.3 — Beta schedule curve (Slide 47)
    # ─────────────────────────────────────────────────────────────────────────
    def beta_schedule_curve(self):
        tag = self.section_tag("slide 47", FORWARD_COLOR).to_corner(UL, buff=0.48)
        title = self.hook_question("Noise schedule controls each forward step.", color=FORWARD_COLOR)

        axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 0.22, 0.05],
            x_length=7.5,
            y_length=3.8,
            axis_config={"color": DIM, "stroke_width": 1.5, "include_tip": True},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            tips=True,
        ).move_to([0, -0.4, 0])

        x_lbl = self.mixed_label([("text", "timestep"), ("math", r"t")], SMALL_SIZE, DIM, font=FONT_BODY).next_to(axes.x_axis.get_right(), DR, buff=0.1)
        y_lbl = self.math_label(r"\beta_t", SMALL_SIZE, FORWARD_COLOR).next_to(axes.y_axis.get_top(), UR, buff=0.1)

        # Linear schedule: β increases from ~0.0001 to ~0.02
        schedule = axes.plot(lambda x: 0.0001 + 0.0199 * x, x_range=[0, 1], color=FORWARD_COLOR, stroke_width=3)

        # Moving dot with ValueTracker
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(t_tracker.get_value(), 0.0001 + 0.0199 * t_tracker.get_value()),
            radius=0.12,
            color=PUZZLE_GOLD,
        ))

        # Noise level indicator text
        noise_desc = always_redraw(lambda: self.label(
            f"noise level: {int(t_tracker.get_value() * 100):d}%",
            SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_CODE,
        ).to_edge(DOWN, buff=0.38))

        annot_start = self.label("Small early steps", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE).move_to([-2.4, 2.3, 0])
        annot_end = self.label("Stronger later corruption", SMALL_SIZE, FORWARD_COLOR, font=FONT_CODE).move_to([2.6, 2.3, 0])

        self.play(FadeIn(tag), FadeIn(title), Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=1.2)
        self.play(Create(schedule), run_time=1.2)
        self.play(FadeIn(dot), FadeIn(noise_desc), run_time=0.6)
        self.play(FadeIn(annot_start), FadeIn(annot_end), run_time=0.8)
        self.play(t_tracker.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.4 — Mean shrinks to zero (Slide 48)
    # ─────────────────────────────────────────────────────────────────────────
    def mean_shrink_to_zero(self):
        tag = self.section_tag("slide 48", NOISE_GRAY).to_corner(UL, buff=0.48)
        title = self.hook_question("The signal shrinks. The noise dominates.", color=NOISE_GRAY)

        axes = Axes(
            x_range=[-1, 1, 0.5], y_range=[-1, 1, 0.5],
            x_length=5.5, y_length=5.5,
            axis_config={"color": DIM, "stroke_width": 1.2},
            tips=False,
        ).move_to([0, -0.2, 0])

        rng2 = np.random.default_rng(7)
        # Initial cloud around x0 = (0.55, 0.45)
        x0_center = np.array([0.55, 0.45])

        def make_cloud(center: np.ndarray, spread: float, n: int = 40) -> VGroup:
            pts = VGroup()
            points = rng2.normal(center, spread, (n, 2))
            for p in points:
                d = Dot(axes.c2p(p[0], p[1]), radius=0.035, color=NOISE_GRAY, fill_opacity=0.55)
                pts.add(d)
            return pts

        cloud_t0 = make_cloud(x0_center, 0.05)
        x0_dot = Dot(axes.c2p(*x0_center), radius=0.1, color=POSITIVE_GREEN)
        x0_lbl = self.math_label(r"x_0", SMALL_SIZE, POSITIVE_GREEN).next_to(x0_dot, UR, buff=0.06)

        origin_dot = Dot(axes.c2p(0, 0), radius=0.09, color=FORWARD_COLOR, fill_opacity=0)
        origin_lbl = self.label("0", SMALL_SIZE, FORWARD_COLOR, font=FONT_CODE).next_to(origin_dot, DL, buff=0.06)

        gaussian_cloud = make_cloud(np.array([0, 0]), 0.32, n=80)

        final_lbl = self.math_label(r"x_T \approx \mathcal{N}(0,I)", 32, FORWARD_COLOR).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tag), FadeIn(title), Create(axes), run_time=1.0)
        self.play(FadeIn(cloud_t0), FadeIn(x0_dot), FadeIn(x0_lbl), FadeIn(origin_lbl), run_time=1.0)
        self.wait(2.0)
        # Morph cloud toward origin
        self.play(
            Transform(cloud_t0, gaussian_cloud),
            x0_dot.animate.move_to(axes.c2p(0.08, 0.06)).set_color(FORWARD_COLOR).scale(0.5),
            x0_lbl.animate.set_color(FORWARD_COLOR),
            run_time=3.5, rate_func=smooth,
        )
        self.play(FadeIn(final_lbl, shift=0.1 * UP), run_time=0.8)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.5 — Time-jump shortcut: α_t, ᾱ_t, q(x_t|x_0) (Slide 49)
    # ─────────────────────────────────────────────────────────────────────────
    def time_jump_shortcut(self):
        tag = self.section_tag("slide 49", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Training shortcut: sample any timestep directly.", color=PUZZLE_GOLD)

        # Define formulas sequentially
        formula_alpha = self.math_label(r"\alpha_t = 1-\beta_t", 30, IMAGE_BLUE).move_to([0, 1.6, 0])

        formula_abar = self.math_label(r"\bar{\alpha}_t = \alpha_1\alpha_2\cdots\alpha_t", 28, IMAGE_BLUE).move_to([0, 0.7, 0])

        try:
            formula_q = self.display_equation(
                r"q(x_t \mid x_0) = \mathcal{N}\!\left(x_t;\; \sqrt{\bar\alpha_t}\, x_0,\; (1-\bar\alpha_t)\mathbf{I}\right)",
                plain="q(x_t | x0) = N( sqrt(alpha_bar_t)*x0, (1-alpha_bar_t)*I )",
                width=10.7, size=32, accent=PUZZLE_GOLD,
            ).move_to([0, -0.4, 0])
        except Exception:
            formula_q = self.label(
                "q(x_t | x_0) = N( sqrt(alpha_bar_t)*x_0, (1-alpha_bar_t)*I )",
                18, PUZZLE_GOLD, font=FONT_CODE,
            ).move_to([0, -0.4, 0])

        formula_sample = self.math_label(
            r"x_t=\sqrt{\bar{\alpha}_t}\,x_0+\sqrt{1-\bar{\alpha}_t}\,\varepsilon",
            34, POSITIVE_GREEN,
        ).move_to([0, -1.6, 0])

        box_sample = SurroundingRectangle(formula_sample, color=POSITIVE_GREEN, buff=0.14, stroke_width=2.5)

        jump_lbl = self.takeaway(
            "No need to simulate all T steps - sample any timestep in one shot!",
            PUZZLE_GOLD,
        ).to_edge(DOWN, buff=0.35)

        # Long Markov chain → then jump arrow
        chain_small = self.math_label(r"x_0 \longrightarrow x_1 \longrightarrow x_2 \longrightarrow \cdots \longrightarrow x_T", 26, DIM).to_edge(UP, buff=0.78)
        jump_arrow = CurvedArrow([-4.2, -0.05, 0], [4.2, -0.05, 0], angle=0.42, color=PUZZLE_GOLD, stroke_width=3)
        jump_arrow_lbl = self.label("Direct jump", SMALL_SIZE, PUZZLE_GOLD, font=FONT_CODE).next_to(jump_arrow, DOWN, buff=0.08)

        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(FadeIn(chain_small), run_time=0.8)
        self.play(Create(jump_arrow), FadeIn(jump_arrow_lbl), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(jump_arrow), FadeOut(jump_arrow_lbl), FadeOut(chain_small), run_time=0.6)

        self.play(FadeIn(formula_alpha), run_time=0.9)
        self.play(FadeIn(formula_abar), run_time=0.9)
        self.play(FadeIn(formula_q), run_time=1.0)
        self.play(FadeIn(formula_sample), Create(box_sample), run_time=0.9)
        self.play(FadeIn(jump_lbl, shift=0.1 * UP), run_time=0.8)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.6 — Simple MSE loss (Slide 50)
    # ─────────────────────────────────────────────────────────────────────────
    def simple_loss(self):
        tag = self.section_tag("slide 50", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Simple objective: predict the noise.", color=TEXT_PURPLE)

        # Model diagram
        model_box = self.math_chip(r"\varepsilon_\theta(x_t,t)", TEXT_PURPLE, 3.0).move_to([0, 0.8, 0])
        input_chip1 = self.mixed_chip([("text", "noisy image"), ("math", r"x_t")], NOISE_GRAY, 2.4).move_to([-3.8, 1.4, 0])
        input_chip2 = self.mixed_chip([("text", "timestep"), ("math", r"t")], PUZZLE_GOLD, 2.0).move_to([-3.8, 0.2, 0])
        target_chip = self.mixed_chip([("text", "true noise"), ("math", r"\varepsilon")], PUZZLE_GOLD, 2.0).move_to([3.8, 0.8, 0])

        arr_i1 = Arrow(input_chip1.get_right(), model_box[0].get_left() + 0.18 * UP, buff=0.05, color=NOISE_GRAY, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)
        arr_i2 = Arrow(input_chip2.get_right(), model_box[0].get_left() - 0.18 * UP, buff=0.05, color=PUZZLE_GOLD, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)
        arr_out = Arrow(model_box[0].get_right(), target_chip.get_left(), buff=0.05, color=TEXT_PURPLE, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)
        arr_out_lbl = self.label("predict", SMALL_SIZE, TEXT_PURPLE, font=FONT_CODE).next_to(arr_out, UP, buff=0.06)

        try:
            loss_eq = self.display_equation(
                r"\mathcal{L}_{\text{simple}} = \mathbb{E}\!\left[\, \|\varepsilon - \varepsilon_\theta(x_t, t)\|^2 \,\right]",
                plain="L_simple = E[ || ε − ε_θ(x_t, t) ||² ]",
                width=8.8, size=34, accent=TEXT_PURPLE,
            ).move_to([0, -1.4, 0])
        except Exception:
            loss_eq = self.label(
                "L_simple  =  E[ ||ε − ε_θ(x_t, t)||² ]",
                22, TEXT_PURPLE, font=FONT_CODE,
            ).move_to([0, -1.4, 0])

        # Color annotations
        eps_note = self.mixed_label([("math", r"\varepsilon"), ("text", "- true noise")], SMALL_SIZE, PUZZLE_GOLD, font=FONT_BODY).move_to([-2.5, -2.8, 0])
        pred_note = self.mixed_label([("math", r"\varepsilon_\theta"), ("text", "- predicted")], SMALL_SIZE, REVERSE_CYAN, font=FONT_BODY).move_to([2.5, -2.8, 0])

        self.play(FadeIn(tag), FadeIn(title), run_time=0.8)
        self.play(FadeIn(model_box), FadeIn(input_chip1), FadeIn(input_chip2), FadeIn(target_chip), run_time=1.0)
        self.play(GrowArrow(arr_i1), GrowArrow(arr_i2), GrowArrow(arr_out), FadeIn(arr_out_lbl), run_time=1.2)
        self.play(FadeIn(loss_eq), run_time=1.0)
        self.play(FadeIn(eps_note), FadeIn(pred_note), run_time=0.8)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.7 — Training pseudocode (Slide 51)
    # ─────────────────────────────────────────────────────────────────────────
    def pseudocode_training(self):
        tag = self.section_tag("slide 51", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Algorithm 1 — Training loop.", color=IMAGE_BLUE)

        steps = [
            ("1.", r"\text{sample } x_0 \text{ from data distribution}", POSITIVE_GREEN),
            ("2.", "sample t uniformly from {1, ..., T}", PUZZLE_GOLD),
            ("3.", r"\text{sample } \varepsilon \sim \mathcal{N}(0,I)", NOISE_GRAY),
            ("4.", r"x_t=\sqrt{\bar{\alpha}_t}x_0+\sqrt{1-\bar{\alpha}_t}\varepsilon", FORWARD_COLOR),
            ("5.", r"\text{update } \theta \text{ to predict } \varepsilon", IMAGE_BLUE),
        ]

        code_box = self.soft_box(11.0, 4.8, color=IMAGE_BLUE, fill_opacity=0.04, stroke_opacity=0.5).move_to([0, -0.3, 0])
        loop_title = self.label("Training loop:", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE)
        loop_title.next_to(code_box, UP, buff=0.1)

        step_mobs = VGroup()
        for num, text, col in steps:
            num_lbl = self.label(num, SUBTITLE_SIZE, DIM, font=FONT_CODE)
            text_lbl = self.math_label(text, SUBTITLE_SIZE + 2, col) if ("\\" in text or "x_" in text) else self.label(text, SUBTITLE_SIZE, col, font=FONT_CODE)
            self.fit_to_box(text_lbl, 9.3, 0.48)
            row = VGroup(num_lbl, text_lbl).arrange(RIGHT, buff=0.25)
            step_mobs.add(row)
        step_mobs.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        step_mobs.move_to(code_box)

        # Highlight step 5 (key: predict noise)
        highlight5 = SurroundingRectangle(step_mobs[-1], color=IMAGE_BLUE, buff=0.12, stroke_width=2.5)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(code_box), FadeIn(loop_title), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=0.08 * RIGHT) for s in step_mobs], lag_ratio=0.18), run_time=2.5)
        self.play(Create(highlight5), run_time=0.8)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    # ─────────────────────────────────────────────────────────────────────────
    # Shot 7.8 — Sampling pseudocode (Slide 51)
    # ─────────────────────────────────────────────────────────────────────────
    def pseudocode_sampling(self):
        tag = self.section_tag("slide 51", REVERSE_CYAN).to_corner(UL, buff=0.48)
        title = self.hook_question("Algorithm 2 — Sampling loop.", color=REVERSE_CYAN)

        steps = [
            ("1.", r"\text{start from pure noise: } x_T \sim \mathcal{N}(0,I)", FORWARD_COLOR),
            ("2.", "for t = T, T-1, ..., 1:", DIM),
            ("3.", r"\text{predict noise: } \hat{\varepsilon}=\varepsilon_\theta(x_t,t)", NOISE_GRAY),
            ("4.", r"x_{t-1}=\mathrm{reverse}(x_t,\hat{\varepsilon},t)", REVERSE_CYAN),
            ("5.", r"\text{return } x_0 \text{ (generated image)}", POSITIVE_GREEN),
        ]

        code_box = self.soft_box(11.0, 4.8, color=REVERSE_CYAN, fill_opacity=0.04, stroke_opacity=0.5).move_to([0, -0.3, 0])
        loop_title = self.label("Sampling loop:", SUBTITLE_SIZE, REVERSE_CYAN, font=FONT_TITLE)
        loop_title.next_to(code_box, UP, buff=0.1)

        step_mobs = VGroup()
        for num, text, col in steps:
            num_lbl = self.label(num, SUBTITLE_SIZE, DIM, font=FONT_CODE)
            text_lbl = self.math_label(text, SUBTITLE_SIZE + 2, col) if ("\\" in text or "x_" in text) else self.label(text, SUBTITLE_SIZE, col, font=FONT_CODE)
            self.fit_to_box(text_lbl, 9.3, 0.48)
            row = VGroup(num_lbl, text_lbl).arrange(RIGHT, buff=0.25)
            step_mobs.add(row)
        step_mobs.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        step_mobs.move_to(code_box)

        # Counter running backward
        t_counter = self.math_label(r"t=T", 36, PUZZLE_GOLD).to_corner(UR, buff=0.55)

        # Noise images decreasing
        reverse_paths = [
            self.first_asset("generated_40_56/cat_from_clean_reverse_00_noise.png", "generated_40_56/reverse_00_noise.png"),
            self.first_asset("generated_40_56/cat_from_clean_reverse_01_less_noise.png", "generated_40_56/reverse_01_less_noise.png"),
            self.first_asset("generated_40_56/cat_from_clean_reverse_02_shape.png", "generated_40_56/reverse_02_shape.png"),
            self.first_asset("generated_40_56/cat_from_clean_reverse_04_final.png", "generated_40_56/reverse_04_final.png"),
        ]
        reverse_images = [
            ImageMobject(str(path)).scale_to_fit_height(1.4) if path else self.placeholder_visual("image", 1.4, 1.4, FORWARD_COLOR)
            for path in reverse_paths
        ]
        vis_noise = reverse_images[0]
        vis_noise.to_corner(UR, buff=0.55).shift(1.2 * DOWN)
        for img in reverse_images[1:]:
            img.move_to(vis_noise)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(code_box), FadeIn(loop_title), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=0.08 * RIGHT) for s in step_mobs], lag_ratio=0.18), run_time=2.5)
        self.play(FadeIn(t_counter), FadeIn(vis_noise), run_time=0.8)

        # Animate counter going backwards
        for t_val, next_img in zip([r"t=T-1", r"t=T/2", r"t=1"], reverse_images[1:]):
            t_new = self.math_label(t_val, 36, PUZZLE_GOLD).to_corner(UR, buff=0.55)
            self.play(Transform(t_counter, t_new), Transform(vis_noise, next_img), run_time=0.7)
            self.wait(0.5)
        self.wait(9.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

