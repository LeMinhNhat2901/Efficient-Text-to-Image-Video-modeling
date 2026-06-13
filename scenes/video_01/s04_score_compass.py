from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.base_scene import DiffusionScene
from config import *

_TERRAIN_CACHE: dict[float, ImageMobject] = {}


class ScoreCompassScene(DiffusionScene):
    TARGET_DURATION = 111.39

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "The Score Compass",
            "A local direction field for walking back from noise",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(title), run_time=0.7)

        self.breadcrumb_hook()
        self.probability_terrain_shot()
        self.score_compass_pulse()
        self.score_climb()
        self.hold_to_time(start, self.TARGET_DURATION)

    # ── Scene 1: breadcrumb hook ─────────────────────────────────────────────
    def breadcrumb_hook(self):
        question = self.hook_question("Finding the way back")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        home = self.draw_home().move_to([-4.35, 0.35, 0])
        forest = self.gaussian_cloud(
            count=150, width=1.65, height=1.15, seed=22, color=VIOLET
        ).move_to([3.6, 0.2, 0])
        forest_label = self.label("forest / noise", SMALL_SIZE, MUTED).next_to(forest, DOWN, buff=0.16)
        traveler = Dot(home.get_center() + 0.45 * RIGHT, radius=0.09, color=RED)

        path_points = [
            traveler.get_center(),
            np.array([-3.0,  0.85, 0]),
            np.array([-1.7, -0.42, 0]),
            np.array([-0.25, 0.40, 0]),
            np.array([ 1.15, -0.1, 0]),
            np.array([ 2.55,  0.32, 0]),
        ]

        # UPGRADE: gradient path — dark/violet (forest side) → bright (probability trail)
        path = VMobject(stroke_width=3.6)
        path.set_points_smoothly(path_points)
        path.set_color_by_gradient(ACCENT_2, VIOLET)

        # UPGRADE: crumbs individually coloured along the probability gradient
        crumbs = VGroup(*[
            Dot(
                p, radius=0.058,
                color=self.mix_color(ACCENT_2, VIOLET, i / max(len(path_points) - 2, 1)),
            )
            for i, p in enumerate(path_points[1:-1])
        ])

        caption = self.label(
            "In diffusion, the trail is made of probability.", SMALL_SIZE, TEXT
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(home), FadeIn(forest), FadeIn(forest_label), FadeIn(traveler), run_time=1.0)
        self.play(
            Create(path),
            MoveAlongPath(traveler, path),
            LaggedStart(*[FadeIn(c, scale=1.7) for c in crumbs], lag_ratio=0.12),
            run_time=3.4,
        )
        self.play(
            FadeIn(caption),
            crumbs.animate.set_opacity(0.95),
            forest.animate.set_opacity(0.35),
            run_time=1.0,
        )

        contour_hint = (
            self.contour_lines(scale=0.48)
            .move_to([0.0, -0.05, 0])
            .set_color(ACCENT)
            .set_opacity(0.55)
        )
        self.play(FadeTransform(crumbs.copy(), contour_hint), run_time=1.5)
        self.wait(8.0)
        self.play(
            FadeOut(Group(question, home, forest, forest_label, traveler, path, crumbs, caption, contour_hint)),
            run_time=1.0,
        )

    # ── Scene 2: probability terrain ─────────────────────────────────────────
    def probability_terrain_shot(self):
        question = self.hook_question("Probability terrain")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        terrain = self.probability_terrain(scale=1.08).move_to([0, -0.28, 0]).set_opacity(0.0)
        contours = self.contour_lines(scale=1.08).move_to(terrain).set_opacity(0.42)
        bright   = self.label("Bright = high probability", SMALL_SIZE, ACCENT_2).move_to([-3.4, -2.38, 0])
        dark     = self.label("Dark = low probability",    SMALL_SIZE, MUTED   ).move_to([ 3.25, -2.38, 0])
        manifold = self.label("Swiss roll data manifold",  SMALL_SIZE, ACCENT  ).to_corner(UL, buff=0.56)
        data_dots = self.swiss_data_dots(scale=1.08).move_to(terrain).set_z_index(2)

        y         = Dot(terrain.get_center() + np.array([2.35, 2.05, 0]), radius=0.09, color=RED).set_z_index(4)
        y_target  = terrain.get_center() + np.array([2.0, -1.04, 0])
        y_label   = self.eq(r"y", size=30, color=RED).next_to(y, DR, buff=0.12)

        dust = VGroup()
        rng  = np.random.default_rng(43)
        for _ in range(18):
            offset = np.array([rng.normal(0, 0.18), rng.normal(0, 0.12), 0])
            dust.add(Dot(
                y_target + offset,
                radius=float(rng.uniform(0.014, 0.032)),
                color=self.mix_color(RED, VIOLET, float(rng.random())),
                fill_opacity=0.68,
            ))

        self.play(
            LaggedStart(*[FadeIn(dot, scale=1.35) for dot in data_dots], lag_ratio=0.012),
            FadeIn(manifold),
            run_time=2.2,
        )
        self.add(terrain)
        terrain.set_z_index(0)
        data_dots.set_z_index(2)
        self.play(terrain.animate.set_opacity(0.94), data_dots.animate.set_opacity(0.36), run_time=1.4)

        # UPGRADE: inside-out contour reveal (innermost = index 0 first)
        self.play(
            LaggedStart(*[Create(c) for c in contours], lag_ratio=0.08),
            FadeIn(bright),
            FadeIn(dark),
            run_time=1.6,
        )
        self.play(FadeIn(y), FadeIn(y_label), run_time=0.5)
        self.play(
            y.animate.move_to(y_target),
            y_label.animate.next_to(y_target, DR, buff=0.12),
            rate_func=smooth,
            run_time=1.35,
        )
        y.move_to(y_target)
        y_label.next_to(y, DR, buff=0.12)
        self.play(
            LaggedStart(*[FadeIn(p, scale=1.7) for p in dust], lag_ratio=0.025),
            Flash(y, color=RED, flash_radius=0.42),
            run_time=0.9,
        )
        self.play(dust.animate.set_opacity(0.18), run_time=0.6)
        self.wait(12.0)
        self.play(
            FadeOut(Group(question, terrain, contours, bright, dark, manifold, data_dots, y, y_label, dust)),
            run_time=1.0,
        )

    # ── Scene 3: score compass pulse  ★ MAIN VIP UPGRADE ★ ───────────────────
    def score_compass_pulse(self):
        """
        3B1B upgrades:
          1. Richer glow (8 rings) around y
          2. Equation appears with Circumscribe highlight
          3. 4-wave expanding ripple rings
          4. RADIAL FIELD REVEAL — arrows sorted by distance from y and
             unveiled in expanding concentric waves (signature 3B1B move)
          5. Colour-coded arrows: blue (weak) → gold (strong)
          6. Indicate on local_ring to reinforce "local" concept
        """
        question = self.hook_question("The score is local")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        terrain  = self.probability_terrain(scale=1.0).move_to([-0.45, -0.2, 0])
        contours = self.contour_lines(scale=1.0).move_to(terrain).set_opacity(0.34)

        y_pos = terrain.get_center() + np.array([2.0, -1.0, 0])
        y     = Dot(y_pos, radius=0.095, color=RED)

        grad      = self.score_vec(2.0, -1.0)
        direction = grad / max(np.linalg.norm(grad), 1e-6)
        score_arrow = Arrow(
            y_pos,
            y_pos + np.array([direction[0], direction[1], 0]) * 0.95,
            buff=0.09, color=ACCENT, stroke_width=7,
            max_tip_length_to_length_ratio=0.22,
        )
        local_ring = Circle(radius=0.22, stroke_color=ACCENT, stroke_width=2.2).move_to(y)

        # Colour-coded field (arrows NOT in scene yet — FadeIn adds them)
        local_field = self.score_field_colored(scale=1.0, base_opacity=0.24).move_to(terrain)

        definition = self.display_equation(
            r"m=\nabla\log p_X(y)",
            width=4.4, size=34, accent=ACCENT_2,
        ).to_corner(UR, buff=0.55)

        note = self.label(
            "local direction of fastest increase in log-probability",
            SMALL_SIZE, TEXT,
        )
        if note.width > 4.15:
            note.scale_to_fit_width(4.15)
        note.next_to(definition, DOWN, buff=0.25).align_to(definition, RIGHT)

        local_note = self.label(
            "local, not a straight-line teleport", SMALL_SIZE, MUTED
        ).to_edge(DOWN, buff=0.5)

        # Richer glow: 8 concentric rings
        glow = self.glow_around(y, color=ACCENT, rings=8)

        # ── Phase 1: terrain + y ──────────────────────────────────────────
        self.play(FadeIn(terrain), Create(contours), run_time=1.0)
        self.play(FadeIn(y), Flash(y, color=RED, flash_radius=0.38), run_time=0.6)
        self.play(Create(glow), Create(local_ring), run_time=0.7)

        # ── Phase 2: single arrow + equation + Circumscribe ───────────────
        self.play(GrowArrow(score_arrow), run_time=0.9)
        self.play(FadeIn(definition, shift=0.08 * LEFT), run_time=0.9)
        # Circumscribe draws the viewer's eye to the equation (3B1B staple)
        self.play(Circumscribe(definition, color=ACCENT_2, time_width=0.55), run_time=1.2)

        # ── Phase 3: four expanding ripple rings ──────────────────────────
        for radius in [0.35, 0.58, 0.85, 1.18]:
            ripple = Circle(
                radius=radius, stroke_color=ACCENT,
                stroke_width=1.6, stroke_opacity=0.62,
            ).move_to(y)
            self.play(Create(ripple), FadeOut(ripple), run_time=0.38)

        # ── Phase 4: RADIAL FIELD REVEAL ─────────────────────────────────
        # Sort arrows by distance from y → naturally forms concentric rings.
        # LaggedStart over the sorted list creates the iconic "wave" unfold.
        y_center      = y.get_center()
        sorted_arrows = sorted(
            local_field,
            key=lambda a: np.linalg.norm(a.get_start() - y_center),
        )
        self.play(
            LaggedStart(
                *[FadeIn(a, scale=0.65) for a in sorted_arrows],
                lag_ratio=0.055,
            ),
            FadeOut(glow),          # glow dissolves as the full field emerges
            run_time=2.6,
        )

        # ── Phase 5: text notes + ring flash ─────────────────────────────
        self.play(FadeIn(note), FadeIn(local_note), run_time=0.8)
        # Indicate on local_ring reinforces the "local" concept visually
        self.play(
            Indicate(local_ring, color=ACCENT_2, scale_factor=1.45),
            score_arrow.animate.set_stroke(width=9),
            run_time=0.9,
        )

        self.wait(25.5)
        self.play(
            FadeOut(Group(
                question, terrain, contours, y, score_arrow,
                local_ring, local_field, definition, note, local_note,
            )),
            run_time=1.0,
        )

    # ── Scene 4: score climb  ★ MULTI-PARTICLE UPGRADE ★ ─────────────────────
    def score_climb(self):
        """
        3B1B upgrades:
          1. 4 simultaneous particles (3 satellites + main) each with a
             colour-coded TracedPath — shows convergence, not single luck
          2. Satellite paths are offset-and-converge: they all start at
             different noisy positions but arrive at the same manifold point
          3. score_field_colored replaces the monochrome background field
        """
        question = self.hook_question(
            "Small score-guided steps climb toward higher probability."
        )
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=0.9)

        terrain  = self.probability_terrain(scale=0.98).move_to([0, -0.18, 0])
        contours = self.contour_lines(scale=0.98).move_to(terrain).set_opacity(0.34)
        field    = self.score_field_colored(scale=0.98, base_opacity=0.18).move_to(terrain)
        tc       = terrain.get_center()

        # Main particle path (same anchor points as original)
        main_pts = [
            tc + np.array([2.05, -1.04, 0]),
            tc + np.array([1.52, -0.72, 0]),
            tc + np.array([1.04, -0.42, 0]),
            tc + np.array([0.58, -0.20, 0]),
            tc + np.array([0.08, -0.06, 0]),
        ]

        # Satellite configs: (start_offset, colour, dot_radius)
        # fade_factors shrink offset → all paths converge at main_pts[-1]
        sat_cfgs     = [
            (np.array([ 0.33,  0.27, 0]), ACCENT_2,  0.075),
            (np.array([-0.22, -0.19, 0]), "#FF9966",  0.070),
            (np.array([ 0.45, -0.30, 0]), "#AADDFF",  0.065),
        ]
        fade_factors = [1.0, 0.70, 0.42, 0.18, 0.03]

        def conv_path(offset_3d):
            return [main_pts[i] + offset_3d * fade_factors[i] for i in range(5)]

        all_starts   = [main_pts[0]]   + [main_pts[0] + o for o, _, _ in sat_cfgs]
        all_colors   = [RED]           + [c for _, c, _ in sat_cfgs]
        all_radii    = [0.090]         + [r for _, _, r in sat_cfgs]
        all_path_pts = [main_pts]      + [conv_path(o) for o, _, _ in sat_cfgs]

        # Build smooth VMobject paths for MoveAlongPath
        path_vms = []
        for pts in all_path_pts:
            vm = VMobject()
            vm.set_points_smoothly(pts)
            path_vms.append(vm)

        particles = VGroup(*[
            Dot(s, radius=r, color=c, fill_opacity=0.92, z_index=3)
            for s, c, r in zip(all_starts, all_colors, all_radii)
        ])

        trails = [
            TracedPath(
                p.get_center,
                stroke_color=c,
                stroke_width=2.8,
                dissipating_time=2.2,
                stroke_opacity=0.78,
            )
            for p, c in zip(particles, all_colors)
        ]

        step_arrows = VGroup(*[
            Arrow(
                main_pts[i], main_pts[i + 1],
                buff=0.08, color=ACCENT_2, stroke_width=3.4,
                max_tip_length_to_length_ratio=0.18,
            )
            for i in range(len(main_pts) - 1)
        ])
        high_label = self.label(
            "higher log-probability", SMALL_SIZE, ACCENT_2
        ).move_to([-2.7, 1.85, 0])
        take = self.takeaway("The score locally points toward higher probability.", ACCENT)
        take.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(terrain), Create(contours), FadeIn(field), run_time=1.1)
        self.play(
            LaggedStart(*[FadeIn(p, scale=1.5) for p in particles], lag_ratio=0.08),
            run_time=0.8,
        )

        for trail in trails:
            self.add(trail)

        contour_pulses = [
            contours[i].animate.set_color(ACCENT_2).set_opacity(0.72)
            for i in [3, 2, 1, 0]
        ]

        # All particles move simultaneously → convergence is the visual payoff
        self.play(
            *[MoveAlongPath(p, vm) for p, vm in zip(particles, path_vms)],
            LaggedStart(*[GrowArrow(a) for a in step_arrows], lag_ratio=0.12),
            LaggedStart(*contour_pulses, lag_ratio=0.18),
            FadeIn(high_label),
            run_time=4.5,
        )
        self.play(contours.animate.set_color(TEXT).set_opacity(0.34), run_time=0.5)
        self.wait(5.5)
        self.play(FadeIn(take, shift=0.08 * UP), run_time=1.0)
        self.wait(7.5)

        bridge = self.label(
            "Next: zoom into one small neighborhood around y.",
            SMALL_SIZE, MUTED,
        ).next_to(take, UP, buff=0.22)
        self.play(FadeIn(bridge), run_time=0.8)
        self.wait(3.0)
        self.play(
            FadeOut(Group(
                question, terrain, contours, field, particles,
                step_arrows, high_label, take, bridge,
            )),
            *[FadeOut(t) for t in trails],
            run_time=1.0,
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def draw_home(self) -> VGroup:
        body  = RoundedRectangle(
            width=1.0, height=0.72, corner_radius=0.04,
            stroke_color=ACCENT, fill_color=ACCENT, fill_opacity=0.08,
        )
        roof  = Polygon(
            [-0.62, 0.18, 0], [0, 0.72, 0], [0.62, 0.18, 0],
            color=ACCENT_2, fill_color=ACCENT_2, fill_opacity=0.18,
        )
        door  = Rectangle(
            width=0.22, height=0.38,
            stroke_color=ACCENT, fill_color=BG, fill_opacity=1,
        ).move_to([0, -0.17, 0])
        glow  = Circle(
            radius=0.74,
            stroke_color=ACCENT_2, stroke_opacity=0.25,
            fill_color=ACCENT_2, fill_opacity=0.05,
        )
        label = self.label("home", SMALL_SIZE, ACCENT).next_to(body, DOWN, buff=0.12)
        return VGroup(glow, body, roof, door, label)

    # ── probability_terrain: vectorised numpy, 400×240 ──────────────────────
    def probability_terrain(self, scale: float = 1.0) -> ImageMobject:
        """
        Vectorised numpy render — ~10× faster than the old pixel loop,
        resolution bumped to 400×240 (≈1.5× sharper on 1080p output).
        """
        cache_key = round(scale, 3)
        if cache_key in _TERRAIN_CACHE:
            return _TERRAIN_CACHE[cache_key].copy()

        W, H = 400, 240
        xs = np.linspace(-3.4, 3.4, W)
        ys = np.linspace(1.95, -1.95, H)
        XX, YY = np.meshgrid(xs, ys)

        ts     = np.linspace(0.35, 2.35, 48)
        cx_all = ts * np.cos(2.25 * ts)
        cy_all = 0.66 * ts * np.sin(2.25 * ts)

        density = np.zeros((H, W))
        for cx, cy in zip(cx_all, cy_all):
            density += np.exp(-((XX - cx) ** 2 + (YY - cy) ** 2) / 0.24)
        density = np.minimum(1.0, density / 4.0)

        bg   = np.asarray(self.hex_rgb(BG),      dtype=float)
        cyan = np.asarray(self.hex_rgb(ACCENT),   dtype=float)
        gold = np.asarray(self.hex_rgb(ACCENT_2), dtype=float)
        red  = np.asarray(self.hex_rgb(RED),      dtype=float)

        base   = bg * 0.86 + red * 0.14
        alpha1 = np.minimum(1.0, density * 1.35)[..., np.newaxis]
        color  = base + alpha1 * (cyan - base)

        blend = np.clip((density - 0.44) * 1.05, 0.0, 0.62)[..., np.newaxis]
        color = color * (1 - blend) + gold * blend

        image = np.clip(color, 0, 255).astype(np.uint8)
        mob   = ImageMobject(image)
        mob.set_opacity(0.94)
        mob.scale_to_fit_width(7.0 * scale)
        _TERRAIN_CACHE[cache_key] = mob
        return mob

    def swiss_data_dots(self, scale: float = 1.0) -> VGroup:
        dots = VGroup()
        for index, t in enumerate(np.linspace(0.35, 2.35, 92)):
            x = t * np.cos(2.25 * t)
            y = 0.66 * t * np.sin(2.25 * t)
            dots.add(Dot(
                [x, y, 0], radius=0.027,
                color=self.mix_color(ACCENT, ACCENT_2, index / 91),
                fill_opacity=0.9,
            ))
        return dots.scale(scale)

    def glow_around(self, mob: Mobject, color: str = ACCENT, rings: int = 5) -> VGroup:
        return VGroup(*[
            Circle(
                radius=0.18 + 0.09 * i,
                stroke_color=color,
                stroke_width=1.5,
                stroke_opacity=0.38 / (i + 1),
            ).move_to(mob.get_center())
            for i in range(rings)
        ])

    def hex_rgb(self, color: str) -> tuple[int, int, int]:
        text = color.lstrip("#")
        return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))

    def contour_lines(self, scale: float = 1.0) -> VGroup:
        lines = VGroup()
        for radius, opacity in [
            (0.42, 0.58), (0.72, 0.44), (1.02, 0.32), (1.32, 0.24), (1.62, 0.17)
        ]:
            curve = ParametricFunction(
                lambda t, r=radius: np.array([
                    r * t * np.cos(2.25 * t),
                    r * t * np.sin(2.25 * t) * 0.66,
                    0,
                ]),
                t_range=[0.25, 2.2, 0.03],
                color=TEXT,
                stroke_width=1.15,
            ).set_opacity(opacity)
            lines.add(curve)
        return lines.scale(scale)

    def score_field(self, scale: float = 1.0, opacity: float = 0.38) -> VGroup:
        """Original monochrome field — kept for compatibility."""
        arrows = VGroup()
        for x in np.linspace(-2.75, 2.75, 7):
            for y in np.linspace(-1.45, 1.45, 5):
                grad = self.score_vec(x, y)
                norm = np.linalg.norm(grad)
                if norm < 0.08:
                    continue
                direction = grad / norm
                length = min(0.42, 0.15 + 0.18 * norm)
                start = np.array([x, y, 0])
                end   = start + length * np.array([direction[0], direction[1], 0])
                arrows.add(
                    Arrow(start, end, buff=0, color=ACCENT, stroke_width=2.3,
                          max_tip_length_to_length_ratio=0.24).set_opacity(opacity)
                )
        return arrows.scale(scale)

    # ── NEW: colour-coded score field ────────────────────────────────────────
    def score_field_colored(self, scale: float = 1.0, base_opacity: float = 0.24) -> VGroup:
        """
        Denser 9×6 grid.  Arrows coloured blue (ACCENT, weak score)
        → gold (ACCENT_2, strong score) by normalised magnitude.
        Stroke width also scales with magnitude for extra depth.
        """
        arrow_data = []
        for x in np.linspace(-2.75, 2.75, 9):
            for y in np.linspace(-1.45, 1.45, 6):
                grad = self.score_vec(x, y)
                norm = np.linalg.norm(grad)
                if norm < 0.08:
                    continue
                direction = grad / norm
                length = min(0.44, 0.12 + 0.20 * norm)
                arrow_data.append((x, y, direction, length, norm))

        if not arrow_data:
            return VGroup()

        max_mag = max(d[4] for d in arrow_data)
        arrows  = VGroup()
        for x, y, direction, length, norm in arrow_data:
            t   = min(1.0, norm / max_mag)
            col = self.mix_color(ACCENT, ACCENT_2, t)      # blue → gold
            sw  = 1.7 + 1.4 * t                             # thin → thick
            opa = base_opacity + 0.26 * t                   # dim → bright
            start = np.array([x, y, 0])
            end   = start + length * np.array([direction[0], direction[1], 0])
            arrows.add(
                Arrow(start, end, buff=0, color=col, stroke_width=sw,
                      max_tip_length_to_length_ratio=0.26).set_opacity(opa)
            )
        return arrows.scale(scale)

    def swiss_density(self, x: float, y: float) -> float:
        total = 0.0
        for t in np.linspace(0.35, 2.35, 48):
            cx = t * np.cos(2.25 * t)
            cy = 0.66 * t * np.sin(2.25 * t)
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            total += np.exp(-d2 / 0.24)
        return float(min(1.0, total / 4.0))

    def score_vec(self, x: float, y: float) -> np.ndarray:
        eps = 0.04
        p   = max(1e-4, self.swiss_density(x, y))
        dx  = (
            np.log(max(1e-4, self.swiss_density(x + eps, y)))
            - np.log(max(1e-4, self.swiss_density(x - eps, y)))
        ) / (2 * eps)
        dy  = (
            np.log(max(1e-4, self.swiss_density(x, y + eps)))
            - np.log(max(1e-4, self.swiss_density(x, y - eps)))
        ) / (2 * eps)
        return np.array([dx, dy]) / (1 + 0.16 * abs(np.log(p)))

    def beta_slider(self, tracker: ValueTracker) -> VGroup:
        rail  = self.soft_box(2.8, 0.16, color=DIM, fill_opacity=0.3)
        fill  = always_redraw(
            lambda: Rectangle(
                width=max(0.01, 2.8 * tracker.get_value()),
                height=0.16,
                stroke_width=0,
                fill_color=ACCENT_2 if tracker.get_value() < 0.4 else RED,
                fill_opacity=0.9,
            ).align_to(rail, LEFT).move_to(rail.get_left() + RIGHT * 1.4 * tracker.get_value())
        )
        label = always_redraw(
            lambda: self.eq(
                r"\beta", size=26,
                color=ACCENT_2 if tracker.get_value() < 0.4 else RED,
            ).next_to(rail, UP, buff=0.14)
        )
        return VGroup(rail, fill, label)