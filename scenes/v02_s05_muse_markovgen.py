from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


class V02MuseMarkovgen(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s05_muse_markovgen.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Muse, Speed, and the Return of MRFs",
            "Parallel Decoding and Structured Refinement",
        )

        self.sequential_vs_parallel()
        self.muse_speed_highlight()
        self.consistency_tradeoff()
        self.mrf_factor_graph()
        self.unary_cost()
        self.pairwise_cost()
        self.energy_minimization()
        self.speedup_stopwatch()
        self.diffusion_transition()

    def sequential_vs_parallel(self):
        tag = self.section_tag("slide 35", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("From sequential prediction to masked parallel decoding.")
        
        left_box = self.soft_box(5.8, 4.4, color=IMAGE_BLUE, fill_opacity=0.02, stroke_opacity=0.4).move_to([-3.1, -0.2, 0])
        right_box = self.soft_box(5.8, 4.4, color=PUZZLE_GOLD, fill_opacity=0.02, stroke_opacity=0.4).move_to([3.1, -0.2, 0])
        
        left_title = self.label("Autoregressive (Sequential)", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([-3.1, 1.6, 0])
        right_title = self.label("Masked Parallel (Muse)", SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_TITLE).move_to([3.1, 1.6, 0])
        self.fit_to_box(left_title, 5.1, 0.36)
        self.fit_to_box(right_title, 5.1, 0.36)
        
        # Grid 1: Autoregressive (sequential fill)
        grid_ar = VGroup()
        for r in range(4):
            for c in range(4):
                box = Square(side_length=0.45, stroke_color=IMAGE_BLUE, stroke_width=1.0, fill_color=IMAGE_BLUE, fill_opacity=0)
                grid_ar.add(box)
        grid_ar.arrange_in_grid(rows=4, cols=4, buff=0.05).move_to([-3.1, -0.2, 0])
        
        # Grid 2: Parallel Masked
        grid_parallel = VGroup()
        for r in range(4):
            for c in range(4):
                # Initially masked (filled with DIM background)
                box = Square(side_length=0.45, stroke_color=PUZZLE_GOLD, stroke_width=1.0, fill_color=DIM, fill_opacity=0.4)
                grid_parallel.add(box)
        grid_parallel.arrange_in_grid(rows=4, cols=4, buff=0.05).move_to([3.1, -0.2, 0])
        
        lbl_ar = self.label("Slow (O(N) steps)", 13, IMAGE_BLUE, font=FONT_CODE).next_to(grid_ar, DOWN, buff=0.25)
        lbl_parallel = self.label("Fast (O(1) iterations)", 13, PUZZLE_GOLD, font=FONT_CODE).next_to(grid_parallel, DOWN, buff=0.25)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(left_box), FadeIn(left_title), FadeIn(right_box), FadeIn(right_title), run_time=1.2)
        self.play(FadeIn(grid_ar), FadeIn(grid_parallel), FadeIn(lbl_ar), FadeIn(lbl_parallel), run_time=1.0)
        self.wait(2.0)
        
        # Animate Autoregressive fill one-by-one
        ar_anims = []
        for box in grid_ar:
            ar_anims.append(box.animate.set_fill(IMAGE_BLUE, opacity=0.67))
        self.play(LaggedStart(*ar_anims, lag_ratio=0.1), run_time=2.5)
        
        # Animate Parallel fill in chunks
        # Round 1: unmask 4 random cells
        rng = np.random.default_rng(99)
        indices = list(range(16))
        rng.shuffle(indices)
        
        self.play(
            *[grid_parallel[idx].animate.set_fill(POSITIVE_GREEN, opacity=0.6).set_stroke(POSITIVE_GREEN) for idx in indices[:5]],
            run_time=0.6
        )
        self.wait(0.3)
        # Round 2: unmask 6 more
        self.play(
            *[grid_parallel[idx].animate.set_fill(POSITIVE_GREEN, opacity=0.6).set_stroke(POSITIVE_GREEN) for idx in indices[5:11]],
            run_time=0.6
        )
        self.wait(0.3)
        # Round 3: unmask remaining
        self.play(
            *[grid_parallel[idx].animate.set_fill(POSITIVE_GREEN, opacity=0.6).set_stroke(POSITIVE_GREEN) for idx in indices[11:]],
            run_time=0.6
        )
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def muse_speed_highlight(self):
        tag = self.section_tag("slide 35", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Muse 3B: High-fidelity generation in a fraction of time.", color=TEXT)
        
        # Large speed indicator
        speed_lbl = self.label("10x FASTER", 72, POSITIVE_GREEN, font=FONT_TITLE).move_to([0, 0.4, 0])
        speed_sub = self.label("than Parti 3B / Imagen 3B on TPUv4", SUBTITLE_SIZE, TEXT).next_to(speed_lbl, DOWN, buff=0.2)
        
        tpu_chip = self.soft_box(4.95, 1.24, color=PUZZLE_GOLD, fill_opacity=0.075, stroke_opacity=0.78).move_to([0, -1.85, 0])
        tpu_lbl = VGroup(
            self.label("Masked Generative", 24, PUZZLE_GOLD, font=FONT_BODY),
            self.label("Transformers", 22, PUZZLE_GOLD, font=FONT_BODY),
        ).arrange(DOWN, buff=0.075)
        self.fit_to_box(tpu_lbl, 4.35, 0.86)
        tpu_lbl.move_to(tpu_chip.get_center() + 0.02 * UP)
        
        self.play(FadeIn(tag), FadeIn(title), run_time=1.0)
        self.play(Write(speed_lbl), run_time=1.0)
        self.play(FadeIn(speed_sub), FadeIn(tpu_chip), FadeIn(tpu_lbl), run_time=1.0)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def consistency_tradeoff(self):
        tag = self.section_tag("slide 38", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Fewer decoding steps accelerate generation, but hurt consistency.")
        
        # 3 columns representation
        # 1. Full Muse (high steps)
        col1 = self.media_card("Full Muse (24 steps)", "Clean & Consistent", IMAGE_BLUE, 3.25, 2.35, ("external_16_39/sydney_opera_house.jpg",), "image").move_to([-4.25, 0, 0])
        
        # 2. Early Exit (fewer steps)
        col2 = self.media_card("Early Exit Muse (4 steps)", "Artifacts & Mistakes", NEGATIVE_ORANGE, 3.25, 2.35, ("generated/sydney_imperfect_tokens.png",), "image").move_to([0, 0, 0])
        
        # 3. MarkovGen (fewer steps + MRF)
        col3 = self.media_card("MarkovGen (4 steps + MRF)", "Corrected Structure", POSITIVE_GREEN, 3.25, 2.35, ("generated/sydney_fixed_tokens.png",), "image").move_to([4.25, 0, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(col1), run_time=1.2)
        self.wait(4.0)
        self.play(FadeIn(col2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeIn(col3), run_time=1.0)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def mrf_factor_graph(self):
        tag = self.section_tag("slide 36", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("MarkovGen: resolving local inconsistencies with MRFs.")
        
        # MRF grid formulation
        grid = VGroup()
        for r in range(3):
            for c in range(3):
                # Variable nodes (circles)
                node = Circle(radius=0.18, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.1, stroke_width=2.0)
                node.move_to([(c - 1) * 1.5, (1 - r) * 1.5 - 0.4, 0])
                grid.add(node)
                
        # Connect variables with edges containing Factor Nodes (squares)
        edges = VGroup()
        factors = VGroup()
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                if c < 2: # Horizontal factor
                    start_p = grid[idx].get_center()
                    end_p = grid[idx + 1].get_center()
                    mid_p = (start_p + end_p) / 2
                    factor = Square(side_length=0.18, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.6).move_to(mid_p)
                    factors.add(factor)
                    edges.add(Line(start_p, mid_p, color=DIM, stroke_width=1.5))
                    edges.add(Line(mid_p, end_p, color=DIM, stroke_width=1.5))
                if r < 2: # Vertical factor
                    start_p = grid[idx].get_center()
                    end_p = grid[idx + 3].get_center()
                    mid_p = (start_p + end_p) / 2
                    factor = Square(side_length=0.18, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.6).move_to(mid_p)
                    factors.add(factor)
                    edges.add(Line(start_p, mid_p, color=DIM, stroke_width=1.5))
                    edges.add(Line(mid_p, end_p, color=DIM, stroke_width=1.5))
                    
        energy_lbl = self.display_equation(
            r"E(x) = \sum_{i} \theta_i(x_i) + \sum_{i, j \in \mathcal{N}} \theta_{ij}(x_i, x_j)",
            plain="E(x) = sum unary_cost(x_i) + sum pairwise_cost(x_i, x_j)",
            width=7.5,
            size=24,
            accent=PUZZLE_GOLD
        ).move_to([0, 1.8, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(grid), Create(edges), FadeIn(factors), run_time=1.5)
        self.play(FadeIn(energy_lbl), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def unary_cost(self):
        tag = self.section_tag("slide 37", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Unary Cost: classifier probability penalty.")
        
        # Draw single token node representation zoom
        token_node = Circle(radius=0.72, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.1, stroke_width=3).move_to([-3.5, 0.2, 0])
        token_lbl = self.math_label(r"X_i", 28, IMAGE_BLUE).move_to(token_node)
        
        # Histogram showing label probability distribution
        prob_chart = VGroup()
        labels = ["dog", "car", "sky", "tree"]
        rng = np.random.default_rng(66)
        for i, l in enumerate(labels):
            h = 0.3 if i != 1 else 1.8 # "car" is high, others low
            bar = Rectangle(width=0.4, height=h, fill_color=TEXT_PURPLE, fill_opacity=0.7, stroke_color=TEXT_PURPLE)
            bar_lbl = self.label(l, 11, TEXT, font=FONT_CODE).next_to(bar, DOWN, buff=0.1)
            prob_chart.add(VGroup(bar, bar_lbl))
        prob_chart.arrange(RIGHT, buff=0.2).move_to([2.0, 0.4, 0])
        # align bottoms
        for item in prob_chart:
            item[0].align_to(prob_chart[0][0], DOWN)
            
        formula = self.display_equation(
            r"\psi_i(x_i = l) = -\log p(X_i = l \mid I_{\text{masked}})",
            plain="cost(X_i = l) = -logit_i(l)",
            width=6.0,
            size=22,
            accent=TEXT_PURPLE
        ).move_to([-3.5, -2.0, 0])
        
        takeaway_lbl = self.takeaway("Penalizes labels that conflict with the neural network predictions.", TEXT_PURPLE)
        takeaway_lbl.to_edge(DOWN, buff=0.38)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(token_node), FadeIn(token_lbl), run_time=1.2)
        self.play(FadeIn(prob_chart), run_time=1.0)
        self.play(FadeIn(formula), run_time=0.8)
        self.wait(4.0)
        
        # Turn token node red to simulate penalty on selecting low probability label (e.g. tree)
        low_prob_marker = SurroundingRectangle(prob_chart[3], color=NEGATIVE_ORANGE, buff=0.05)
        self.play(Create(low_prob_marker), token_node.animate.set_stroke(color=NEGATIVE_ORANGE).set_fill(NEGATIVE_ORANGE, opacity=0.18), run_time=1.0)
        self.play(FadeIn(takeaway_lbl), run_time=0.8)
        self.wait(10.0)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def pairwise_cost(self):
        tag = self.section_tag("slide 37", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Pairwise Cost: local neighbor compatibility penalty.")
        
        # Two neighboring nodes
        node_a = Circle(radius=0.62, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.1, stroke_width=2.5).move_to([-2.5, 0.2, 0])
        lbl_a = self.math_label(r"X_i", 26, IMAGE_BLUE).move_to(node_a)
        
        node_b = Circle(radius=0.62, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.1, stroke_width=2.5).move_to([2.5, 0.2, 0])
        lbl_b = self.math_label(r"X_j", 26, IMAGE_BLUE).move_to(node_b)
        
        # Connecting edge factor
        connection = Line(node_a.get_right(), node_b.get_left(), color=DIM, stroke_width=2)
        factor = Square(side_length=0.4, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.6).move_to([0, 0.2, 0])
        factor_lbl = self.math_label(r"\psi", 22, BG, plain="psi").move_to(factor)
        
        formula = self.display_equation(
            r"\psi_{ij}(x_i = l, x_j = m) = -C(l, m) \cdot s(i, j)",
            plain="cost(X_i = l, X_j = m) = -c(l,m) * s(i,j)",
            width=7.5,
            size=22,
            accent=TEXT_PURPLE
        ).move_to([0, -1.6, 0])
        
        desc = self.takeaway("Penalizes inconsistent neighbors (e.g. water texture right next to dog fur).", TEXT_PURPLE)
        desc.to_edge(DOWN, buff=0.35)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(node_a), FadeIn(lbl_a), FadeIn(node_b), FadeIn(lbl_b), Create(connection), FadeIn(factor), FadeIn(factor_lbl), run_time=1.5)
        self.play(FadeIn(formula), run_time=0.8)
        self.wait(5.0)
        
        # Turn edge and factor red indicating incompatibility
        self.play(
            connection.animate.set_color(NEGATIVE_ORANGE).set_stroke(width=4),
            factor.animate.set_color(NEGATIVE_ORANGE),
            run_time=0.9
        )
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def energy_minimization(self):
        tag = self.section_tag("slide 36", POSITIVE_GREEN).to_corner(UL, buff=0.48)
        title = self.hook_question("Energy minimization refines local token structure.")
        
        # Energy landscape graph (simple parabola representation)
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-0.2, 2.5, 1],
            x_length=6.0,
            y_length=3.5,
            axis_config={"color": DIM, "stroke_width": 1.0},
            tips=False
        ).move_to([-3.0, -0.4, 0])
        
        curve = axes.plot(lambda x: 0.5 * x**2 + 0.1, x_range=[-2, 2], color=PUZZLE_GOLD, stroke_width=2.5)
        
        # Dot starting high
        ball = Dot(axes.c2p(-1.8, 0.5 * (-1.8)**2 + 0.1), radius=0.12, color=NEGATIVE_ORANGE)
        
        # 3x3 Token grid on right
        grid = VGroup()
        for r in range(3):
            for c in range(3):
                # Put some red (inconsistent) tokens initially
                col = NEGATIVE_ORANGE if (r + c) % 2 == 1 else POSITIVE_GREEN
                box = Square(side_length=0.6, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.1)
                grid.add(box)
        grid.arrange_in_grid(rows=3, cols=3, buff=0.08).move_to([3.0, -0.4, 0])
        
        desc = self.takeaway("Belief Propagation or Graph Cuts find the lowest energy layout.", POSITIVE_GREEN)
        desc.to_edge(DOWN, buff=0.35)
        
        self.play(FadeIn(tag), FadeIn(title), Create(axes), Create(curve), FadeIn(ball), FadeIn(grid), run_time=1.5)
        self.wait(3.0)
        
        # Slide ball down and fix grid colors to green
        self.play(
            ball.animate.move_to(axes.c2p(0, 0.1)).set_color(POSITIVE_GREEN),
            *[box.animate.set_color(POSITIVE_GREEN).set_fill(POSITIVE_GREEN, opacity=0.1) for box in grid],
            run_time=2.2,
            rate_func=smooth
        )
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def speedup_stopwatch(self):
        tag = self.section_tag("slide 38", POSITIVE_GREEN).to_corner(UL, buff=0.48)
        title = self.hook_question("Speedup over Muse without quality loss.")
        
        # Visual clocks
        clock_muse = VGroup(
            Circle(radius=0.9, color=IMAGE_BLUE, stroke_width=3),
            Line([0,0,0], [0, 0.68, 0], color=IMAGE_BLUE, stroke_width=2.5).rotate(-PI/3, about_point=[0,0,0])
        ).move_to([-3.2, 0.4, 0])
        lbl_m = self.label("Muse: 442.05 ms", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).next_to(clock_muse, DOWN, buff=0.3)
        
        clock_markov = VGroup(
            Circle(radius=0.9, color=POSITIVE_GREEN, stroke_width=3),
            Line([0,0,0], [0, 0.68, 0], color=POSITIVE_GREEN, stroke_width=2.5).rotate(-2*PI/3, about_point=[0,0,0])
        ).move_to([3.2, 0.4, 0])
        lbl_mg = self.label("MarkovGen: 281.03 ms", SUBTITLE_SIZE, POSITIVE_GREEN, font=FONT_TITLE).next_to(clock_markov, DOWN, buff=0.3)
        
        speedup = self.label("~1.5x Speedup", 36, POSITIVE_GREEN, font=FONT_TITLE).move_to([0, 1.8, 0])
        desc = self.takeaway("Decodes only 4 parallel steps, using local MRF inference to correct errors.", POSITIVE_GREEN)
        desc.to_edge(DOWN, buff=0.35)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(clock_muse), FadeIn(lbl_m), FadeIn(clock_markov), FadeIn(lbl_mg), run_time=1.5)
        self.play(
            Rotate(clock_muse[1], angle=-2*PI, about_point=clock_muse[0].get_center(), run_time=2.2),
            Rotate(clock_markov[1], angle=-1.3*2*PI, about_point=clock_markov[0].get_center(), run_time=1.4),
        )
        self.play(FadeIn(speedup), FadeIn(desc), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def diffusion_transition(self):
        tag = self.section_tag("transition", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Text-to-Pixels: moving from discrete tokens to continuous noise.")
        
        # Autoregressive backbone block vs Diffusion backbone block from s01
        ar_block = self.module("Autoregressive / Token-based\n(VQGAN + Transformers)", TEXT_PURPLE, 3.8, 1.3).move_to([-3.4, 0.6, 0])
        diff_block = self.module("Diffusion-based\n(U-Net + Denoisers)", IMAGE_BLUE, 3.8, 1.3).move_to([3.4, 0.6, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(ar_block), FadeIn(diff_block), run_time=1.2)
        self.wait(5.0)
        
        # AR block dims out
        self.play(
            ar_block.animate.set_opacity(0.18),
            Indicate(diff_block, color=IMAGE_BLUE),
            run_time=1.5
        )
        self.wait(3.0)
        
        # Create token grid and dissolve to noise
        grid = self.pixel_grid(rows=6, cols=6, side=0.34, colors=(IMAGE_BLUE, TEXT_PURPLE, PUZZLE_GOLD)).move_to([0, -1.8, 0])
        self.play(FadeIn(grid), run_time=0.8)
        self.wait(2.0)
        
        # Dissolve grid cells: transform grid cells into small noise dots, then fade out
        rng = np.random.default_rng(101)
        noise_dots = VGroup()
        for cell in grid:
            dot = Dot(cell.get_center() + rng.uniform(-0.15, 0.15, 3), radius=0.02, color=DIM)
            noise_dots.add(dot)
            
        text_next = self.takeaway("Next stop: Diffusion Models", IMAGE_BLUE).move_to([0, -1.8, 0])
        
        self.play(
            FadeOut(grid),
            FadeIn(noise_dots),
            run_time=1.0
        )
        self.play(
            FadeOut(noise_dots),
            FadeIn(text_next, shift=0.15*UP),
            run_time=1.0
        )
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
