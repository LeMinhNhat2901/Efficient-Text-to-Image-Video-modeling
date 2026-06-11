from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import *
from scenes.s04_score_compass import ScoreCompassScene


class LocalLinearScoreScene(ScoreCompassScene):
    TARGET_DURATION = 124.27

    def math_concept_card(
        self,
        tex: str,
        body: str,
        color: str = ACCENT,
        width: float = 2.0,
        height: float = 0.78,
        tex_size: int = 24,
    ) -> VGroup:
        box = self.soft_box(width, height, color=color, fill_opacity=0.055, stroke_opacity=0.58)
        title_mob = self.eq(tex, size=tex_size, color=color)
        body_mob = self.label(body, SMALL_SIZE, MUTED)
        self.fit_to_box(title_mob, width - 0.36, 0.30)
        self.fit_to_box(body_mob, width - 0.36, 0.22)
        content = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.08).move_to(box)
        return VGroup(box, content)

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "Local Linear Approximation",
            "Turning the score compass into a small reverse step",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(title), run_time=0.7)

        self.magnifying_glass_zoom()
        self.local_reverse_formula()
        self.beta_stability()
        self.hidden_difficulty()
        self.hold_to_time(start, self.TARGET_DURATION)

    # ── Section 1: Magnifying-glass zoom ──────────────────────────────────────
    def magnifying_glass_zoom(self):
        """Script lines 1-16. Duration ~25s."""
        question = self.hook_question("Locally, the landscape becomes simple.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        # ── Left panel: terrain [-5, -1] ────────────────────────────────────
        terrain = self.probability_terrain(scale=0.78).move_to([-3.05, -0.22, 0])
        contours = self.contour_lines(scale=0.78).move_to(terrain).set_opacity(0.32)
        y_pos = terrain.get_center() + np.array([1.35, -0.7, 0])
        y = Dot(y_pos, radius=0.08, color=RED)
        y_glow = self.glow_around(y, color=RED, rings=5)
        lens = Circle(radius=0.62, stroke_color=ACCENT_2, stroke_width=3).move_to(y)
        handle = Line(
            lens.get_corner(DR),
            lens.get_corner(DR) + np.array([0.48, -0.48, 0]),
            color=ACCENT_2, stroke_width=4,
        )

        # ── Right panel: zoom view [0.2, 5.1] ──────────────────────────────
        zoom_box = self.soft_box(
            4.95, 3.05, color=ACCENT, fill_opacity=0.03, stroke_opacity=0.68
        ).move_to([2.65, -0.2, 0])
        plane = NumberPlane(
            x_range=[-2.1, 2.1, 0.5], y_range=[-1.2, 1.2, 0.4],
            x_length=4.35, y_length=2.45,
            background_line_style={"stroke_color": DIM, "stroke_width": 1, "stroke_opacity": 0.42},
            axis_config={"stroke_color": DIM, "stroke_width": 1.2},
        ).move_to(zoom_box)

        local_lines = VGroup(*[
            Line(
                zoom_box.get_center() + np.array([-1.95, -0.82 + 0.24 * i, 0]),
                zoom_box.get_center() + np.array([1.95, -0.25 + 0.24 * i, 0]),
                color=self.mix_color(ACCENT, TEXT, 0.35), stroke_width=1.25,
            ).set_opacity(0.7)
            for i in range(7)
        ])

        curve_segment = ParametricFunction(
            lambda t: zoom_box.get_center() + np.array([1.55 * t, 0.36 * np.sin(1.5 * t) + 0.26 * t, 0]),
            t_range=[-1.0, 1.0, 0.03], color=ACCENT_2, stroke_width=4,
        )
        tangent = Line(
            zoom_box.get_center() + np.array([-1.55, -0.42, 0]),
            zoom_box.get_center() + np.array([1.55, 0.42, 0]),
            color=ACCENT, stroke_width=4,
        )
        # Label below zoom box, clear of everything
        tangent_label = self.label("curve -> tangent line", SMALL_SIZE, ACCENT)
        tangent_label.next_to(zoom_box, DOWN, buff=0.18)

        # Score arrow inside zoom panel — arrow points right and slightly up
        local_y = Dot(zoom_box.get_center() + np.array([-0.65, -0.2, 0]), radius=0.075, color=RED)
        local_y_glow = self.glow_around(local_y, color=RED, rings=4)
        grad = Arrow(
            local_y.get_center(),
            local_y.get_center() + np.array([1.15, 0.35, 0]),
            buff=0.08, color=ACCENT, stroke_width=5,
        )
        # Label UP of arrow — ensure it stays inside zoom box
        grad_label = self.eq(r"\nabla\log p_X(y)", size=24, color=ACCENT)
        grad_label.next_to(grad, UP, buff=0.10)
        if grad_label.get_top()[1] > zoom_box.get_top()[1] - 0.1:
            grad_label.next_to(local_y, UR, buff=0.12)

        # ── Animations ───────────────────────────────────────────────────────
        self.play(FadeIn(terrain), Create(contours), FadeIn(y), run_time=1.1)
        self.play(Create(y_glow), run_time=0.5)
        self.play(Create(lens), Create(handle), run_time=0.8)
        zoom_link = VGroup(
            Line(lens.get_right(), zoom_box.get_left() + 0.52 * UP, color=ACCENT_2, stroke_width=1.5),
            Line(lens.get_right(), zoom_box.get_left() + 0.52 * DOWN, color=ACCENT_2, stroke_width=1.5),
        ).set_opacity(0.72)
        self.play(FadeIn(zoom_box), FadeIn(plane), Create(zoom_link), run_time=1.0)
        self.play(
            LaggedStart(*[Create(line) for line in local_lines], lag_ratio=0.08),
            FadeOut(zoom_link),
            run_time=1.1,
        )
        self.play(Create(curve_segment), run_time=0.8)
        self.play(
            ReplacementTransform(curve_segment, tangent),
            FadeIn(tangent_label), run_time=1.0,
        )
        self.play(Circumscribe(tangent, color=ACCENT, time_width=0.6), run_time=0.9)
        self.play(
            FadeIn(local_y), Create(local_y_glow), GrowArrow(grad), run_time=1.0,
        )
        self.play(FadeIn(grad_label), run_time=0.5)
        self.play(Indicate(grad, color=ACCENT_2, scale_factor=1.3), run_time=0.9)
        self.wait(14.5)

        self.play(
            FadeOut(Group(
                question, terrain, contours, y, y_glow, lens, handle,
                zoom_box, plane, local_lines, tangent, tangent_label,
                local_y, local_y_glow, grad, grad_label,
            )),
            run_time=1.0,
        )

    # ── Section 2: Local reverse formula ──────────────────────────────────────
    def local_reverse_formula(self):
        """
        Script lines 17-34. Duration ~35s.
        Layout: geometry far-LEFT, formula TOP-RIGHT, concept cards BOTTOM.
        Strict separation ensures zero overlap.
        """
        question = self.hook_question("The score becomes a reverse mean step.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        # ── LEFT geometry (x ≈ -4.0) — tight cluster ──────────────────────
        y_center = np.array([-4.0, -0.5, 0])
        y = Dot(y_center, radius=0.10, color=RED)
        y_glow = self.glow_around(y, color=RED, rings=4)
        # y label: directly below
        y_label = self.eq(r"y", size=30, color=TEXT).next_to(y, DOWN, buff=0.14)

        # score arrow: up-right from y
        score_end = y_center + np.array([1.35, 0.62, 0])
        score = Arrow(y_center, score_end, buff=0.08, color=ACCENT, stroke_width=5)
        # score label: MathTex avoids SVG-empty bug with very short Text strings
        score_label = MathTex(r"\nabla\log p", font_size=22, color=ACCENT)
        score_label.next_to(score.get_end(), UP, buff=0.10)

        # beta arrow: shorter version of score, same direction
        beta_end = y_center + np.array([0.75, 0.35, 0])
        beta_step = Arrow(y_center, beta_end, buff=0.08, color=ACCENT_2, stroke_width=6)

        # mu dot at tip of beta arrow, label to the LEFT of mu (avoids score)
        mu = Dot(beta_end, radius=0.10, color=GREEN)
        mu_glow = self.glow_around(mu, color=GREEN, rings=4)
        mu_label = self.eq(r"\mu", size=28, color=GREEN).next_to(mu, LEFT, buff=0.14)

        # ── Formula box: top-centre/right (y = 1.60) ──────────────────────
        formula_mob = MathTex(
            r"\mu(X\mid y)",
            r"\approx",
            r"y",
            r"+\beta\,",
            r"\nabla\log p_X(y)",
            font_size=32,
        )
        formula_mob[0].set_color(GREEN)
        formula_mob[2].set_color(RED)
        formula_mob[3].set_color(ACCENT_2)
        formula_mob[4].set_color(ACCENT)
        formula_box = self.soft_box(7.2, 0.78, color=GREEN, fill_opacity=0.055, stroke_opacity=0.62)
        formula_box.move_to([1.2, 1.60, 0])
        formula_mob.move_to(formula_box)
        formula = VGroup(formula_box, formula_mob)

        # ── Concept cards: bottom strip (y = -1.80) ────────────────────────
        # Scale card widths so they stay within frame width
        parts = VGroup(
            self.math_concept_card(r"\mu(X\mid y)", "mean", GREEN, width=2.30, height=0.78, tex_size=24),
            self.math_concept_card(r"y", "current point", RED, width=1.72, height=0.78, tex_size=25),
            self.math_concept_card(r"\beta", "step size", ACCENT_2, width=1.58, height=0.78, tex_size=25),
            self.math_concept_card(r"\nabla\log p_X(y)", "score direction", ACCENT, width=2.48, height=0.78, tex_size=21),
        ).arrange(RIGHT, buff=0.13)
        parts.move_to([1.0, -1.80, 0])
        if parts.width > 10.5:
            parts.scale_to_fit_width(10.5)

        theorem = self.label(
            "Local linear approx. for small Gaussian perturbation",
            SMALL_SIZE, MUTED,
        ).to_edge(DOWN, buff=0.28)
        if theorem.width > 11.5:
            theorem.scale_to_fit_width(11.5)

        # ── Phase 1: y + score direction ──────────────────────────────────
        self.play(FadeIn(y), Create(y_glow), FadeIn(y_label), run_time=0.7)
        self.play(GrowArrow(score), FadeIn(score_label), run_time=0.9)

        # ── Phase 2: beta arrow + formula ──────────────────────────────────
        self.play(TransformFromCopy(score, beta_step), FadeIn(formula_box), run_time=1.0)
        self.play(Write(formula_mob[0]), run_time=0.45)
        self.play(Write(formula_mob[1]), run_time=0.28)
        self.play(Write(formula_mob[2]), run_time=0.28)
        self.play(Write(formula_mob[3]), run_time=0.32)
        self.play(Write(formula_mob[4]), run_time=0.45)
        self.play(Circumscribe(formula, color=ACCENT_2, time_width=0.55), run_time=1.1)
        self.play(FadeIn(mu), Create(mu_glow), FadeIn(mu_label), run_time=0.8)

        # ── Phase 3: concept cards ─────────────────────────────────────────
        self.play(
            LaggedStart(*[FadeIn(card, shift=0.06 * UP) for card in parts], lag_ratio=0.15),
            FadeIn(theorem),
            run_time=1.2,
        )
        for card in parts:
            self.play(Indicate(card, color=ACCENT_2, scale_factor=1.06), run_time=0.38)

        self.wait(22.0)

        self.play(
            FadeOut(Group(
                question, y, y_glow, y_label,
                score, score_label, beta_step,
                mu, mu_glow, mu_label,
                formula, parts, theorem,
            )),
            run_time=1.0,
        )

    # ── Section 3: Beta stability ──────────────────────────────────────────────
    def beta_stability(self):
        """
        Script lines 35-52. Duration ~30s.
        Slider: all elements in one VGroup, positioned RIGHT of terrain.
        beta_num is a static DecimalNumber updated via ChangeDecimalToValue.
        Point reset done with smooth FadeOut/FadeIn — no hard jump.
        """
        question = self.hook_question("Beta controls whether the local step stays trustworthy.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        terrain = self.probability_terrain(scale=0.82).move_to([-1.85, -0.2, 0])
        contours = self.contour_lines(scale=0.82).move_to(terrain).set_opacity(0.28)
        tc = terrain.get_center()

        point_start = tc + np.array([1.62, -0.82, 0])
        small_end   = tc + np.array([1.0,  -0.48, 0])
        large_end   = tc + np.array([-0.75, 1.05, 0])

        point = Dot(point_start, radius=0.09, color=RED)
        point_glow = self.glow_around(point, color=RED, rings=4)
        trust_region = Circle(
            radius=0.36,
            stroke_color=GREEN,
            stroke_width=1.8,
            stroke_opacity=0.72,
            fill_color=GREEN,
            fill_opacity=0.055,
        ).move_to(small_end)

        small = Arrow(point_start, small_end, buff=0.08, color=GREEN, stroke_width=5)
        large = CurvedArrow(point_start, large_end, angle=-TAU / 8, color=RED, stroke_width=4)

        # ── Two slider states — swap on transition to avoid always_redraw bugs ─
        slider_x, slider_y = 3.8, 0.6

        def make_slider(beta_val: float, fill_color: str) -> VGroup:
            """Returns a complete VGroup: [label_row, track], where fill sits inside rail."""
            sym  = MathTex(r"\beta =", font_size=22, color=MUTED)
            num  = DecimalNumber(beta_val, num_decimal_places=2, font_size=22,
                                 color=fill_color)
            row  = VGroup(sym, num).arrange(RIGHT, buff=0.10)
            rail = self.soft_box(2.6, 0.16, color=DIM, fill_opacity=0.3)
            bar  = Rectangle(
                width=max(0.02, 2.6 * beta_val), height=0.16,
                stroke_width=0, fill_color=fill_color, fill_opacity=0.92,
            )
            bar.move_to(rail.get_left() + RIGHT * bar.width / 2)
            track = VGroup(rail, bar)
            grp = VGroup(row, track).arrange(DOWN, buff=0.14)
            grp.move_to([slider_x, slider_y, 0])
            return grp

        slider_small = make_slider(0.18, ACCENT_2)
        slider_large = make_slider(0.72, RED)

        stable = self.label("small beta: stable", SMALL_SIZE, GREEN)
        overshoot = self.label("large beta: overshoot", SMALL_SIZE, RED)
        stable.next_to(slider_small[1], DOWN, buff=0.22)
        overshoot.move_to(stable)

        trail = TracedPath(point.get_center, stroke_color=GREEN, stroke_width=2.4, dissipating_time=1.8)

        # ── Build scene ──────────────────────────────────────────────────
        self.play(FadeIn(terrain), Create(contours), FadeIn(point), Create(point_glow), run_time=1.0)
        self.play(FadeIn(slider_small), FadeIn(trust_region, scale=0.82), run_time=0.7)
        self.add(trail)

        # Small step
        self.play(
            GrowArrow(small),
            point.animate.move_to(small_end),
            point_glow.animate.move_to(small_end),
            FadeIn(stable),
            run_time=1.8,
        )
        self.play(Indicate(stable, color=GREEN, scale_factor=1.08), run_time=0.7)
        self.wait(9.5)

        # Reset: smooth fade — swap slider states, no hard jump
        self.remove(trail)
        point2 = Dot(point_start, radius=0.09, color=RED)
        point_glow2 = self.glow_around(point2, color=RED, rings=4)

        self.play(
            FadeOut(small), FadeOut(stable), FadeOut(trust_region),
            FadeOut(point), FadeOut(point_glow),
            run_time=0.5,
        )
        self.play(
            FadeIn(point2), FadeIn(point_glow2),
            ReplacementTransform(slider_small, slider_large),
            run_time=0.8,
        )

        # Large step
        self.play(
            Create(large),
            point2.animate.move_to(large_end),
            point_glow2.animate.move_to(large_end),
            FadeIn(overshoot),
            run_time=1.5,
        )
        self.play(Flash(large.get_end(), color=RED, flash_radius=0.38), run_time=0.5)
        self.play(Indicate(overshoot, color=RED, scale_factor=1.08), run_time=0.7)
        self.wait(13.8)

        self.play(
            FadeOut(Group(
                question, terrain, contours,
                point2, point_glow2, large,
                slider_large, overshoot,
            )),
            run_time=1.0,
        )

    # ── Section 4: Hidden difficulty ──────────────────────────────────────────
    def hidden_difficulty(self):
        """
        Script lines 53-68. Duration ~27s.
        Layout: formula top, score=? mid-left, image_space mid-right,
                dim_label below image_space, bridge bottom strip.
        """
        question = self.hook_question("The formula hides the hard part.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        # ── Formula (top, y = 1.55) ────────────────────────────────────
        formula_mob = MathTex(
            r"\mu(X\mid y)",
            r"\approx y+\beta\,",
            r"\nabla\log p_X(y)",
            font_size=33,
        )
        formula_mob[0].set_color(GREEN)
        formula_mob[2].set_color(ACCENT)
        formula_box = self.soft_box(7.4, 0.78, color=ACCENT, fill_opacity=0.055, stroke_opacity=0.62)
        formula_box.move_to([0, 1.55, 0])
        formula_mob.move_to(formula_box)
        formula = VGroup(formula_box, formula_mob)

        # ── score=? (mid-left, x ≈ -2.8, y ≈ 0.2) ────────────────────
        score_unknown_eq = MathTex(r"\text{score} = ?", font_size=32, color=RED)
        score_box = self.soft_box(3.0, 0.72, color=RED, fill_opacity=0.06, stroke_opacity=0.72)
        score_box.move_to([-2.8, 0.15, 0])
        score_unknown_eq.move_to(score_box)
        score_unknown = VGroup(score_box, score_unknown_eq)

        # Cross-out over score term in formula
        def make_cross():
            dl = formula_mob[2].get_corner(DL) + np.array([-0.05, -0.05, 0])
            ur = formula_mob[2].get_corner(UR) + np.array([0.05,  0.05, 0])
            return Line(dl, ur, color=RED, stroke_width=3)

        # ── Image space (mid-right, x ≈ 2.8, y ≈ -0.2) ───────────────
        image_space = self.soft_box(
            4.6, 2.1, color=VIOLET, fill_opacity=0.055, stroke_opacity=0.68
        ).move_to([2.8, -0.25, 0])

        rng = np.random.default_rng(5)
        pixels = VGroup(*[
            Square(
                side_length=0.055, stroke_width=0,
                fill_color=self.mix_color(ACCENT, VIOLET, float(rng.random())),
                fill_opacity=0.55,
            ).move_to(
                image_space.get_center() + np.array([
                    float(rng.uniform(-2.1, 2.1)),
                    float(rng.uniform(-0.88, 0.88)), 0,
                ])
            )
            for _ in range(100)
        ])
        # Label BELOW box — never overlaps pixels inside box
        dim_label = self.label("1,000,000-dim image space", SMALL_SIZE, VIOLET)
        dim_label.next_to(image_space, DOWN, buff=0.14)

        # ── Bridge (bottom strip) ──────────────────────────────────────
        bridge = self.takeaway("This is where learning enters.", ACCENT_2)
        bridge.to_edge(DOWN, buff=0.25)

        # Guard: dim_label must not overlap bridge
        if dim_label.get_bottom()[1] < bridge.get_top()[1] + 0.08:
            dim_label.next_to(image_space, DOWN, buff=0.06)

        # ── Phase 1: formula ──────────────────────────────────────────
        self.play(FadeIn(formula_box), Write(formula_mob), run_time=1.2)
        self.play(Circumscribe(formula_mob[2], color=RED, time_width=0.6), run_time=1.1)

        # ── Phase 2: score_unknown ─────────────────────────────────────
        self.play(FadeTransform(formula_mob[2].copy(), score_unknown), run_time=1.0)
        self.play(Indicate(score_unknown_eq, color=RED, scale_factor=1.18), run_time=0.8)

        # ── Phase 3: image space ───────────────────────────────────────
        self.play(FadeIn(image_space), FadeIn(dim_label), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.7) for p in pixels], lag_ratio=0.005),
            run_time=1.8,
        )
        cross = make_cross()
        self.play(Create(cross), run_time=0.5)

        # ── Phase 4: punchline ─────────────────────────────────────────
        self.play(GrowFromCenter(bridge), run_time=0.9)
        self.wait(16.5)

        self.play(
            FadeOut(Group(
                question, formula, cross,
                score_unknown, image_space, pixels, dim_label, bridge,
            )),
            run_time=1.0,
        )
