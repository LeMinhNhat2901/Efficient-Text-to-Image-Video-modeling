from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.v02_common import *


class V02ArchitectureEvolution(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s04_architecture_evolution.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        scene_start = self.time

        self.construct_intro(
            "Architectural Evolution\nand the Ordering Problem",
            "MRFs, CNNs, Transformers, and 2D Grids",
        )

        self.timeline_transformers()
        self.mrf_local_neighborhood()
        self.cnn_hierarchical_features()
        self.transformer_long_range()
        self.conditioned_synthesis()
        self.ordering_problem()
        self.hold_for_voiceover(scene_start, voiceover)
        if hasattr(self, "final_hold_group"):
            self.play(FadeOut(self.final_hold_group), run_time=0.8)

    def timeline_transformers(self):
        tag = self.section_tag("slide 28", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Architecture trade-offs:\nlocal detail vs global coordination.", color=TEXT, width=9.4)
        title.shift(0.18 * DOWN)

        axis = Line([-5.25, -0.35, 0], [5.25, -0.35, 0], color=DIM, stroke_width=3)
        year_positions = {"MRF": -4.85, "CNN": -2.75, "2017": -0.45, "2020": 1.75, "2024": 4.45}
        tick_labels = {"MRF": "local", "CNN": "hierarchy", "2017": "attention", "2020": "patches", "2024": "MRF+"}
        ticks = VGroup()
        years = VGroup()
        for key, x in year_positions.items():
            ticks.add(Line([x, -0.58, 0], [x, -0.12, 0], color=MUTED, stroke_width=2.2))
            years.add(self.label(key, 17, TEXT, font=FONT_CODE).move_to([x, -0.92, 0]))

        def badge(name: str, color: str, width: float = 1.42) -> VGroup:
            box = self.soft_box(width, 0.58, color=color, fill_opacity=0.075, stroke_opacity=0.82)
            label = self.label(name, 18, TEXT, font=FONT_SUBTITLE)
            self.fit_to_box(label, width - 0.18, 0.34)
            label.move_to(box)
            return VGroup(box, label)

        badges = VGroup(
            badge("MRF", IMAGE_BLUE, 1.08).move_to([year_positions["MRF"], 0.52, 0]),
            badge("CNNs", IMAGE_BLUE, 1.18).move_to([year_positions["CNN"], 0.52, 0]),
            badge("Transformer", TEXT_PURPLE, 1.82).move_to([year_positions["2017"], 0.92, 0]),
            badge("ViT", TEXT_PURPLE, 1.04).move_to([year_positions["2020"], 0.52, 0]),
            VGroup(
                badge("Muse", PUZZLE_GOLD, 1.12).move_to([year_positions["2024"], 0.86, 0]),
                badge("MarkovGen", POSITIVE_GREEN, 1.62).move_to([year_positions["2024"], 0.18, 0]),
            ),
        )
        tiny_labels = VGroup(*[
            self.label(tick_labels[key], 12, MUTED, font=FONT_CODE).move_to([x, -1.25, 0])
            for key, x in year_positions.items()
        ])
        cards = VGroup(badges[0], badges[1], badges[2], badges[3], badges[4][0], badges[4][1])
        connectors = VGroup(*[
            Line([card.get_center()[0], -0.35, 0], [card.get_center()[0], card.get_bottom()[1] - 0.05, 0], color=card[0].get_stroke_color(), stroke_width=1.4).set_opacity(0.65)
            for card in cards
        ])
        tf_glow = SurroundingRectangle(badges[2], color=TEXT_PURPLE, buff=0.08, stroke_width=2.6)
        note = self.takeaway("The key jump: attention lets distant image patches coordinate directly.", TEXT_PURPLE, width=8.9)
        note.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), Create(axis), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), FadeIn(years), FadeIn(tiny_labels), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(g, shift=0.12 * UP) for g in badges], lag_ratio=0.18), LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.06), run_time=1.6)
        self.play(Create(tf_glow), FadeIn(note, shift=0.08 * UP), Flash(badges[2], color=TEXT_PURPLE), run_time=1.0)
        self.wait(10.0)

        self.play(FadeOut(VGroup(tag, title, axis, ticks, years, tiny_labels, badges, connectors, tf_glow, note)), run_time=0.8)

    def puzzle_piece(self, year: str, name: str, color: str) -> VGroup:
        body = self.soft_box(1.48, 0.9, color=color, fill_opacity=0.07, stroke_opacity=0.78)
        notch = Circle(radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(body.get_right())
        tab = Circle(radius=0.12, stroke_color=color, stroke_width=1.0, fill_color=color, fill_opacity=0.08).move_to(body.get_left())
        label = VGroup(
            self.label(year, 13, MUTED, font=FONT_CODE),
            self.label(name, 16, color, font=FONT_SUBTITLE),
        ).arrange(DOWN, buff=0.05).move_to(body)
        return VGroup(body, tab, notch, label)

    def mrf_local_neighborhood(self):
        tag = self.section_tag("slide 29", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Markov Random Fields (MRFs): local neighborhood dependency.")
        
        # Grid of nodes representing MRF
        nodes = VGroup()
        rows, cols = 4, 4
        spacing = 1.0
        for r in range(rows):
            for c in range(cols):
                node = Dot(radius=0.09, color=IMAGE_BLUE).move_to([
                    (c - (cols - 1) / 2) * spacing,
                    ((rows - 1) / 2 - r) * spacing - 0.4,
                    0
                ])
                nodes.add(node)
                
        # Neighborhood edges
        edges = VGroup()
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if c < cols - 1: # Horizontal edge
                    edges.add(Line(nodes[idx].get_center(), nodes[idx + 1].get_center(), color=DIM, stroke_width=1.5))
                if r < rows - 1: # Vertical edge
                    edges.add(Line(nodes[idx].get_center(), nodes[idx + cols].get_center(), color=DIM, stroke_width=1.5))
                    
        desc = self.takeaway("MRF optimization minimizes a energy function over local neighbors.", IMAGE_BLUE)
        desc.to_edge(DOWN, buff=0.35)
        
        energy_formula = self.display_equation(
            r"E(x) = \sum_{i} \psi_i(x_i) + \sum_{i, j \in \mathcal{N}} \psi_{ij}(x_i, x_j)",
            plain="E(x) = sum unary_cost(x_i) + sum pairwise_cost(x_i, x_j)",
            width=7.5,
            size=24,
            accent=IMAGE_BLUE
        ).move_to([0, 1.8, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(nodes), Create(edges), run_time=1.5)
        self.play(FadeIn(energy_formula), FadeIn(desc), run_time=1.0)
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def cnn_hierarchical_features(self):
        tag = self.section_tag("slide 30", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("CNNs: hierarchical local feature aggregation.")
        
        # Stacked feature maps (simulated perspective stack)
        layers = Group()
        colors = [IMAGE_BLUE, TEXT_PURPLE, PUZZLE_GOLD]
        for i, col in enumerate(colors):
            box = RoundedRectangle(width=3.2 - i*0.4, height=2.4 - i*0.3, corner_radius=0.08, color=col, stroke_opacity=0.6, fill_color=col, fill_opacity=0.05)
            box.shift(i * 0.4 * RIGHT + i * 0.3 * UP)
            layers.add(box)
        layers.move_to([-2.5, -0.4, 0])
        
        # Convolution kernel box sweeping
        kernel = Square(side_length=0.45, color=POSITIVE_GREEN, fill_color=POSITIVE_GREEN, fill_opacity=0.18, stroke_width=2)
        kernel.move_to(layers[0].get_corner(UL) + 0.35 * RIGHT + 0.3 * DOWN)
        
        desc = self.takeaway("Convolution kernels capture spatially localized, invariant patterns.", IMAGE_BLUE)
        desc.to_edge(DOWN, buff=0.35)
        
        hier_text = VGroup(
            self.label("Low-Level Features (edges, texture)", 14, IMAGE_BLUE),
            self.label("Mid-Level Features (shapes, object parts)", 14, TEXT_PURPLE),
            self.label("High-Level Features (semantic categories)", 14, PUZZLE_GOLD),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.0, 0.4, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(layers), run_time=1.2)
        self.play(FadeIn(kernel), FadeIn(hier_text), run_time=0.8)
        
        # Sweep animations
        positions = [
            layers[0].get_corner(UR) + 0.35 * LEFT + 0.3 * DOWN,
            layers[0].get_center(),
            layers[0].get_corner(DL) + 0.35 * RIGHT + 0.3 * UP,
        ]
        for pos in positions:
            self.play(kernel.animate.move_to(pos), run_time=0.8)
            
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def transformer_long_range(self):
        tag = self.section_tag("slide 31", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Transformers: long-range interactions via self-attention.")
        
        # Split image into patches
        patches_grid = VGroup()
        for r in range(3):
            for c in range(3):
                box = Square(side_length=0.6, stroke_color=IMAGE_BLUE, stroke_width=1.5, fill_color=IMAGE_BLUE, fill_opacity=0.08)
                num = self.label(f"P{r*3+c+1}", 11, TEXT, font=FONT_CODE).move_to(box)
                patches_grid.add(VGroup(box, num))
        patches_grid.arrange_in_grid(rows=3, cols=3, buff=0.06).move_to([-4.8, 0, 0])
        
        # Linear projection vectors
        vectors = VGroup()
        for i in range(9):
            vec = self.math_chip(rf"x_{{{i+1}}}", TEXT_PURPLE, 0.95).scale(0.8)
            vectors.add(vec)
        vectors.arrange(DOWN, buff=0.08).move_to([-1.8, 0, 0])
        
        # Positional embedding addition symbol
        pos_embeddings = VGroup()
        for i in range(9):
            pos = Circle(radius=0.13, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.15, stroke_width=1.2)
            lbl = self.label(f"+{i+1}", 8, PUZZLE_GOLD, font=FONT_CODE).move_to(pos)
            pos_embeddings.add(VGroup(pos, lbl))
        pos_embeddings.arrange(DOWN, buff=0.15).move_to([-0.5, 0, 0])
        
        # Transformer encoder block
        transformer_block = self.module("Transformer Encoder\n(Self-Attention Blocks)", TEXT_PURPLE, 2.6, 3.8).move_to([2.0, 0, 0])
        
        # Output attention connections representation
        out_node1 = Dot([4.5, 1.2, 0], color=TEXT_PURPLE)
        out_node2 = Dot([4.5, -1.2, 0], color=TEXT_PURPLE)
        attention_arc = CurvedArrow(out_node1.get_center(), out_node2.get_center(), angle=-TAU/6, color=POSITIVE_GREEN, stroke_width=2.5)
        attention_lbl = self.label("Attention", 11, POSITIVE_GREEN, font=FONT_CODE).next_to(attention_arc, RIGHT, buff=0.1)
        
        arrows = VGroup(
            Arrow(patches_grid.get_right(), vectors.get_left(), color=IMAGE_BLUE, stroke_width=2.5),
            Arrow(vectors.get_right(), transformer_block.get_left(), color=TEXT_PURPLE, stroke_width=2.5),
            Arrow(transformer_block.get_right(), [4.2, 0, 0], color=TEXT_PURPLE, stroke_width=2.5)
        )
        
        desc = self.takeaway("Attention bypasses spatial constraints, connecting distant tokens directly.", TEXT_PURPLE)
        desc.to_edge(DOWN, buff=0.35)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(patches_grid), run_time=1.2)
        self.play(GrowArrow(arrows[0]), FadeIn(vectors), run_time=1.0)
        self.play(FadeIn(pos_embeddings), run_time=0.6)
        self.play(GrowArrow(arrows[1]), FadeIn(transformer_block), run_time=1.0)
        self.play(GrowArrow(arrows[2]), FadeIn(out_node1), FadeIn(out_node2), Create(attention_arc), FadeIn(attention_lbl), run_time=1.2)
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def conditioned_synthesis(self):
        tag = self.section_tag("slide 32 & 34", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Conditioned Synthesis: transforming layouts into photo-realistic pixels.")
        
        # Pipeline: Condition -> Encoder -> Transformer -> Token Grid -> Decoder -> Image
        pipeline = VGroup()
        c_in = self.vector_chip("Condition\n(Depth/Semantic)", TEXT_PURPLE, 2.0).move_to([-5.2, 1.9, 0])
        c_enc = self.module("Condition\nEncoder", TEXT_PURPLE, 1.8, 0.8).move_to([-2.8, 1.9, 0])
        trans = self.module("Transformer", PUZZLE_GOLD, 1.8, 0.8).move_to([-0.4, 1.9, 0])
        grid = self.vector_chip("Token Grid", PUZZLE_GOLD, 1.3).move_to([1.8, 1.9, 0])
        dec = self.module("Decoder", IMAGE_BLUE, 1.5, 0.8).move_to([3.8, 1.9, 0])
        out_img = self.vector_chip("Output Image", IMAGE_BLUE, 1.5).move_to([5.8, 1.9, 0])
        
        edges = VGroup(
            self.edge(c_in, c_enc, TEXT_PURPLE),
            self.edge(c_enc, trans, TEXT_PURPLE),
            self.edge(trans, grid, PUZZLE_GOLD),
            self.edge(grid, dec, IMAGE_BLUE),
            self.edge(dec, out_img, IMAGE_BLUE)
        )
        
        pipeline.add(c_in, c_enc, trans, grid, dec, out_img, edges)
        
        # 4 Examples side-by-side
        # We can use our generated city maps here!
        # semantic_map_city, fake_depth_map_city, edge_map_city, lowres_city
        # Output: city_building
        ex1 = self.media_card("Depth map", "Input", TEXT_PURPLE, 2.3, 1.75, ("generated/fake_depth_map_city.png",), "image").move_to([-4.8, -1.0, 0])
        ex2 = self.media_card("Low resolution", "Input", TEXT_PURPLE, 2.3, 1.75, ("generated/lowres_city.png",), "image").move_to([-1.6, -1.0, 0])
        ex3 = self.media_card("Semantic map", "Input", TEXT_PURPLE, 2.3, 1.75, ("generated/semantic_map_city.png",), "image").move_to([1.6, -1.0, 0])
        ex4 = self.media_card("Edge map", "Input", TEXT_PURPLE, 2.3, 1.75, ("generated/edge_map_city.png",), "image").move_to([4.8, -1.0, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(pipeline), run_time=1.5)
        self.wait(5.0)
        self.play(
            LaggedStart(
                FadeIn(ex1, shift=0.15*DOWN),
                FadeIn(ex2, shift=0.15*DOWN),
                FadeIn(ex3, shift=0.15*DOWN),
                FadeIn(ex4, shift=0.15*DOWN),
                lag_ratio=0.15
            ),
            run_time=2.0
        )
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def ordering_problem(self):
        tag = self.section_tag("slide 33", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("The Ordering Problem: linearizing 2D structures.")
        
        # Left Panel: Language
        left_box = self.soft_box(5.8, 4.4, color=TEXT_PURPLE, fill_opacity=0.02, stroke_opacity=0.4).move_to([-3.1, -0.2, 0])
        left_title = self.label("Language: Natural 1D Sequence", SUBTITLE_SIZE, TEXT_PURPLE, font=FONT_TITLE).move_to([-3.1, 1.6, 0])
        self.fit_to_box(left_title, 5.1, 0.36)
        words_chain = VGroup(*[
            self.vector_chip(w, TEXT_PURPLE, 0.9).scale(0.68)
            for w in ["The", "cat", "sat", "on", "the", "mat"]
        ]).arrange(DOWN, buff=0.075).move_to([-3.1, -0.45, 0])
        word_arrows = VGroup(*[Arrow(words_chain[i].get_bottom(), words_chain[i+1].get_top(), color=TEXT_PURPLE, stroke_width=1.5, buff=0.05) for i in range(len(words_chain)-1)])
        
        # Right Panel: Images 2D
        right_box = self.soft_box(5.8, 4.4, color=IMAGE_BLUE, fill_opacity=0.02, stroke_opacity=0.4).move_to([3.1, -0.2, 0])
        right_title = self.label("Images: 2D Spatial Grid", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([3.1, 1.6, 0])
        self.fit_to_box(right_title, 5.1, 0.36)
        
        # Draw 4x4 Grid for orderings
        grid = VGroup()
        for r in range(4):
            for c in range(4):
                box = Square(side_length=0.52, stroke_color=IMAGE_BLUE, stroke_width=1, fill_color=IMAGE_BLUE, fill_opacity=0.08)
                grid.add(box)
        grid.arrange_in_grid(rows=4, cols=4, buff=0.04).move_to([3.1, -0.2, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(left_box), FadeIn(left_title), FadeIn(right_box), FadeIn(right_title), run_time=1.2)
        self.play(FadeIn(words_chain), Create(word_arrows), FadeIn(grid), run_time=1.5)
        self.wait(6.0)
        
        orders = [
            ("row-major", POSITIVE_GREEN, [r * 4 + c for r in range(4) for c in range(4)]),
            ("spiral", PUZZLE_GOLD, [0, 1, 2, 3, 7, 11, 15, 14, 13, 12, 8, 4, 5, 6, 10, 9]),
            ("random", NEGATIVE_ORANGE, [2, 13, 4, 11, 0, 6, 15, 8, 1, 10, 5, 14, 3, 12, 7, 9]),
            ("shuffle", TEXT_PURPLE, [5, 0, 10, 15, 1, 6, 11, 12, 2, 7, 8, 13, 3, 4, 9, 14]),
            ("alternate", IMAGE_BLUE, [0, 4, 8, 12, 13, 9, 5, 1, 2, 6, 10, 14, 15, 11, 7, 3]),
        ]

        current_labels = VGroup()
        current_name = VGroup()
        for idx, (name, color, order) in enumerate(orders):
            next_labels = VGroup()
            for order_idx, grid_idx in enumerate(order):
                lbl = self.label(str(order_idx + 1), 12, color, font=FONT_CODE).move_to(grid[grid_idx])
                next_labels.add(lbl)
            next_name = self.vector_chip(name, color, 1.7).move_to([3.1, -2.1, 0])

            if idx == 0:
                self.play(FadeIn(next_name), LaggedStart(*[FadeIn(l) for l in next_labels], lag_ratio=0.04), run_time=1.2)
            else:
                self.play(FadeOut(current_labels), FadeOut(current_name), run_time=0.25)
                self.play(FadeIn(next_name), LaggedStart(*[FadeIn(l) for l in next_labels], lag_ratio=0.025), run_time=0.9)
            current_labels = next_labels
            current_name = next_name
            self.wait(0.55)

        loss_panel = self.soft_box(6.35, 2.25, color=PUZZLE_GOLD, fill_opacity=0.03, stroke_opacity=0.42).move_to([0, -2.15, 0])
        loss_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=4.6,
            y_length=1.65,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.0},
        ).move_to([0, -2.35, 0])
        loss_title = self.label("Different orderings, different training curves", 14, TEXT).next_to(loss_axes, UP, buff=0.1)
        curves = VGroup()
        for i, (_, color, _) in enumerate(orders):
            offset = 0.18 * i
            curve = loss_axes.plot(
                lambda x, o=offset: 2.3 * np.exp(-0.45 * x) + 0.35 + o + 0.08 * np.sin(2 * x + o),
                x_range=[0, 5],
                color=color,
                stroke_width=2.2,
            )
            curves.add(curve)

        self.play(FadeOut(current_labels), FadeOut(current_name), run_time=0.35)
        self.play(
            FadeOut(VGroup(left_box, left_title, words_chain, word_arrows, right_box, right_title, grid)),
            FadeIn(loss_panel),
            run_time=0.6,
        )
        self.play(Create(loss_axes), FadeIn(loss_title), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.12), run_time=1.5)
        self.wait(7.0)
        self.final_hold_group = Group(*self.mobjects)
