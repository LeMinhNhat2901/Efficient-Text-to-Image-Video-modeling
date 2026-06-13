from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


class V02VqganVisualWords(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s03_vqgan_visual_words.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Visual Vocabulary and Quantization",
            "VQGAN, Codebooks, and Image Tokenization",
        )

        self.timeline_spotlight()
        self.visual_words_patches()
        self.clustering_feature_space()
        self.search_and_generation()
        self.image_tokenization()
        self.vqgan_key_idea()
        self.two_stage_training()
        self.codebook_quantization()
        self.codebook_losses()
        self.perceptual_gan_loss()

    def timeline_spotlight(self):
        tag = self.section_tag("slide 16", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Quantizing continuous images into discrete visual words.", color=TEXT, width=10.8)
        title.shift(0.34 * RIGHT + 0.18 * DOWN)

        axis = Line([-5.25, -0.35, 0], [5.25, -0.35, 0], color=DIM, stroke_width=3)
        year_positions = {"2015": -4.65, "2017": -1.55, "2020": 1.35, "2021": 4.25}
        ticks = VGroup()
        years = VGroup()
        for year, x in year_positions.items():
            ticks.add(Line([x, -0.58, 0], [x, -0.12, 0], color=MUTED, stroke_width=2.2))
            years.add(self.label(year, 18, TEXT, font=FONT_CODE).move_to([x, -0.92, 0]))

        def badge(name: str, color: str, width: float = 1.42) -> VGroup:
            box = self.soft_box(width, 0.58, color=color, fill_opacity=0.075, stroke_opacity=0.82)
            label = self.label(name, 18, TEXT, font=FONT_SUBTITLE)
            self.fit_to_box(label, width - 0.18, 0.34)
            label.move_to(box)
            return VGroup(box, label)

        groups = VGroup(
            VGroup(
                badge("U-Net", IMAGE_BLUE, 1.16).move_to([year_positions["2015"], 0.85, 0]),
                badge("Diffusion", IMAGE_BLUE, 1.46).move_to([year_positions["2015"], 0.18, 0]),
            ),
            badge("Transformers", TEXT_PURPLE, 1.86).move_to([year_positions["2017"], 0.52, 0]),
            badge("CLIP", TEXT_PURPLE, 1.12).move_to([year_positions["2020"], 0.52, 0]),
            VGroup(
                badge("VQGAN", PUZZLE_GOLD, 1.30).move_to([year_positions["2021"], 1.18, 0]),
                badge("DALL-E", PUZZLE_GOLD, 1.30).move_to([year_positions["2021"], 0.52, 0]),
                badge("LDM", GREEN, 1.02).move_to([year_positions["2021"], -0.14, 0]),
            ),
        )
        cards = VGroup()
        for group in groups:
            for card in group if isinstance(group, VGroup) and len(group) > 2 else [group]:
                cards.add(card)
        connectors = VGroup(*[
            Line([card.get_center()[0], -0.35, 0], [card.get_center()[0], card.get_bottom()[1] - 0.05, 0], color=card[0].get_stroke_color(), stroke_width=1.4).set_opacity(0.65)
            for card in cards
        ])
        vqgan_glow = SurroundingRectangle(groups[3][0], color=PUZZLE_GOLD, buff=0.08, stroke_width=2.6)
        note = self.takeaway("VQGAN is the bridge: images become codebook tokens a transformer can model.", PUZZLE_GOLD, width=9.2)
        note.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), Create(axis), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), FadeIn(years), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(g, shift=0.12 * UP) for g in groups], lag_ratio=0.18), LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.06), run_time=1.6)
        self.play(Create(vqgan_glow), FadeIn(note, shift=0.08 * UP), Flash(groups[3][0], color=PUZZLE_GOLD), run_time=1.0)
        self.wait(12.0)

        self.play(FadeOut(VGroup(tag, title, axis, ticks, years, groups, connectors, vqgan_glow, note)), run_time=0.8)

    def visual_words_patches(self):
        tag = self.section_tag("slide 17", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("Small visual parts carry semantic information.")
        
        # Two main images
        dog_card = self.media_card("Dog image", "continuous signal", IMAGE_BLUE, 3.3, 2.65, ("external_16_39/dog_main.jpg",), kind="image").move_to([-3.4, 0.2, 0])
        car_card = self.media_card("Red car image", "continuous signal", IMAGE_BLUE, 3.3, 2.65, ("external_16_39/red_car_main.jpg",), kind="car").move_to([3.4, 0.2, 0])
        
        def image_point(card: Group, u: float, v: float) -> np.ndarray:
            visual = card[1]
            return np.array([
                visual.get_left()[0] + u * visual.width,
                visual.get_top()[1] - v * visual.height,
                0.0,
            ])

        patches_data = [
            ("dog_eye_patch.png", image_point(dog_card, 0.38, 0.25), [-5.6, -1.8, 0], "eye"),
            ("dog_nose_patch.png", image_point(dog_card, 0.50, 0.39), [-3.8, -1.8, 0], "nose"),
            ("dog_ear_patch.png", image_point(dog_card, 0.22, 0.31), [-2.0, -1.8, 0], "ear"),
            ("car_wheel_patch.png", image_point(car_card, 0.47, 0.71), [2.0, -1.8, 0], "wheel"),
            ("car_edge_patch.png", image_point(car_card, 0.41, 0.58), [3.8, -1.8, 0], "edge"),
            ("road_texture_patch.png", image_point(car_card, 0.45, 0.88), [5.6, -1.8, 0], "road"),
        ]
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(dog_card), FadeIn(car_card), run_time=1.2)
        self.wait(8.0)

        # Lens effect
        lens = Circle(radius=0.42, color=PUZZLE_GOLD, stroke_width=2.5)
        lens.move_to(patches_data[0][1])
        self.play(Create(lens), run_time=0.6)

        # Extraction loop
        lens_anims = []
        for i, (fname, scan_pos, target_pos, label_text) in enumerate(patches_data):
            # Move lens to patch
            if i > 0:
                self.play(lens.animate.move_to(scan_pos), run_time=0.5)
            
            # Draw a patch duplicate card
            img_path = self.first_asset(f"patches/{fname}")
            if img_path and img_path.exists():
                patch_img = ImageMobject(str(img_path))
                self.fit_to_box(patch_img, 0.9, 0.9)
            else:
                patch_img = Square(side_length=0.9, color=PUZZLE_GOLD, fill_color=PUZZLE_GOLD, fill_opacity=0.2)
            
            patch_box = self.soft_box(1.0, 1.0, color=PUZZLE_GOLD, fill_opacity=0, stroke_opacity=0.7)
            patch_group = Group(patch_box, patch_img).move_to(scan_pos)
            
            # Animate patch flying out
            self.play(
                FadeIn(patch_group),
                patch_group.animate.move_to(target_pos).scale(0.85),
                run_time=0.8
            )
            
            # Label below patch
            lbl = self.label(label_text, 12, MUTED, font=FONT_CODE).next_to(patch_group, DOWN, buff=0.1)
            self.add(lbl)
            
        self.play(FadeOut(lens), run_time=0.5)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def clustering_feature_space(self):
        tag = self.section_tag("slide 18", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Cluster centers = prototype visual words")
        
        # 2D feature space axes
        space = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7.5,
            y_length=4.5,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.0},
        ).move_to([0, -0.2, 0])
        
        # 4 Cluster centers
        centers = [
            [-2.2, 0.8, 0, "Word #12", POSITIVE_GREEN],
            [1.8, 1.0, 0, "Word #42", POSITIVE_GREEN],
            [-1.5, -1.1, 0, "Word #94", POSITIVE_GREEN],
            [1.5, -0.9, 0, "Word #138", POSITIVE_GREEN],
        ]
        
        # Generate scattered dots representing patches
        rng = np.random.default_rng(2026)
        dots = VGroup()
        target_positions = []
        for cx, cy, _, _, col in centers:
            for _ in range(15):
                dx = rng.normal(cx, 0.45)
                dy = rng.normal(cy, 0.45)
                dot = Dot([dx, dy, 0], radius=float(rng.uniform(0.02, 0.045)), color=IMAGE_BLUE, fill_opacity=0.6)
                dots.add(dot)
                # Keep target coordinate close to the center
                target_positions.append([rng.normal(cx, 0.15), rng.normal(cy, 0.15), 0])
                
        # Scrambled chaos dots initially
        chaos_dots = dots.copy()
        for d in chaos_dots:
            d.move_to([rng.uniform(-3.5, 3.5), rng.uniform(-2.0, 2.0), 0])
            
        self.play(FadeIn(tag), FadeIn(title), Create(space), FadeIn(chaos_dots), run_time=1.2)
        self.wait(5.0)
        
        # Gather to clusters
        gather_anims = [d.animate.move_to(target_positions[i]) for i, d in enumerate(chaos_dots)]
        self.play(
            LaggedStart(*gather_anims, lag_ratio=0.01),
            run_time=2.2
        )
        
        # Show cluster boundaries and centers
        boundaries = VGroup()
        center_markers = VGroup()
        labels = VGroup()
        for cx, cy, _, lbl_text, col in centers:
            b = Circle(radius=0.72, color=col, stroke_opacity=0.36, stroke_width=1.5).move_to([cx, cy, 0])
            m = Dot([cx, cy, 0], radius=0.08, color=col)
            l = self.vector_chip(lbl_text, col, 1.25).scale(0.65).next_to(m, UP, buff=0.15)
            boundaries.add(b)
            center_markers.add(m)
            labels.add(l)
            
        self.play(
            Create(boundaries),
            FadeIn(center_markers),
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(12.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def search_and_generation(self):
        tag = self.section_tag("slide 19", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("If we can describe an image well, we can generate it.")
        
        # 3 cards
        m_card = self.media_card("Mona Lisa", "image search", IMAGE_BLUE, 2.0, 1.6, ("external_16_39/mona_lisa.jpg",), kind="image").move_to([-4.0, 1.0, 0])
        b_card = self.media_card("Bicycle", "image search", IMAGE_BLUE, 2.0, 1.6, ("external_16_39/bicycle.jpg",), kind="image").move_to([0, 1.0, 0])
        v_card = self.media_card("Violin", "image search", IMAGE_BLUE, 2.0, 1.6, ("external_16_39/violin.jpg",), kind="image").move_to([4.0, 1.0, 0])
        
        # Histogram visual words matching each card
        hist_m = self.dummy_histogram(IMAGE_BLUE).scale(0.85).move_to([-4.0, -1.2, 0])
        hist_b = self.dummy_histogram(TEXT_PURPLE).scale(0.85).move_to([0, -1.2, 0])
        hist_v = self.dummy_histogram(PUZZLE_GOLD).scale(0.85).move_to([4.0, -1.2, 0])
        
        arrow_m = Arrow(m_card.get_bottom(), hist_m.get_top(), color=DIM, stroke_width=2)
        arrow_b = Arrow(b_card.get_bottom(), hist_b.get_top(), color=DIM, stroke_width=2)
        arrow_v = Arrow(v_card.get_bottom(), hist_v.get_top(), color=DIM, stroke_width=2)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(m_card), FadeIn(b_card), FadeIn(v_card), run_time=1.2)
        self.play(
            Create(arrow_m), Create(arrow_b), Create(arrow_v),
            FadeIn(hist_m), FadeIn(hist_b), FadeIn(hist_v),
            run_time=1.5
        )
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def dummy_histogram(self, color: str) -> VGroup:
        bars = VGroup()
        rng = np.random.default_rng(77)
        for i in range(8):
            h = rng.uniform(0.2, 1.0)
            bar = Rectangle(width=0.12, height=h, fill_color=color, fill_opacity=0.67, stroke_width=0.5, stroke_color=color)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.08)
        # align bottoms
        for b in bars:
            b.align_to(bars[0], DOWN)
        return bars

    def puzzle_piece(self, year: str, name: str, color: str) -> VGroup:
        body = self.soft_box(1.48, 0.9, color=color, fill_opacity=0.07, stroke_opacity=0.78)
        notch = Circle(radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(body.get_right())
        tab = Circle(radius=0.12, stroke_color=color, stroke_width=1.0, fill_color=color, fill_opacity=0.08).move_to(body.get_left())
        label = VGroup(
            self.label(year, 13, MUTED, font=FONT_CODE),
            self.label(name, 16, color, font=FONT_SUBTITLE),
        ).arrange(DOWN, buff=0.05).move_to(body)
        return VGroup(body, tab, notch, label)

    def image_tokenization(self):
        tag = self.section_tag("slide 20", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Image tokenization: discrete code indices grid.")
        
        # Keep the whole tokenization flow on one clean horizontal rail.
        rail = self.soft_box(12.1, 3.25, color=PUZZLE_GOLD, fill_opacity=0.025, stroke_opacity=0.32).move_to([0, -0.05, 0])
        dog_card = self.media_card("256x256x3", "Image Space", IMAGE_BLUE, 2.15, 1.78, ("external_16_39/dog_main.jpg",), kind="image").move_to([-5.0, -0.05, 0])
        
        tokenizer = self.module("Tokenizer\n(Encoder)", PUZZLE_GOLD, 1.85, 0.92).move_to([-2.55, -0.05, 0])
        
        # Grid representation
        grid_vals = [
            [9, 28, 15, 78],
            [19, 36, 27, 32],
            [8, 56, 68, 71],
            [96, 85, 49, 82]
        ]
        grid = VGroup()
        for r in range(4):
            for c in range(4):
                box = Square(side_length=0.48, stroke_color=DIM, stroke_width=0.8, fill_color=PUZZLE_GOLD, fill_opacity=0.06)
                num = self.label(str(grid_vals[r][c]), 13, TEXT, font=FONT_CODE).move_to(box)
                grid.add(VGroup(box, num))
        grid.arrange_in_grid(rows=4, cols=4, buff=0.035).move_to([0.0, -0.05, 0])
        
        detokenizer = self.module("Detokenizer\n(Decoder)", PUZZLE_GOLD, 1.95, 0.92).move_to([2.55, -0.05, 0])
        reconstructed_dog = self.media_card("256x256x3", "Reconstructed", IMAGE_BLUE, 2.15, 1.78, ("generated/dog_token_grid.png",), kind="image").move_to([5.0, -0.05, 0])
        
        arrows = VGroup(
            self.edge(dog_card, tokenizer, IMAGE_BLUE),
            self.edge(tokenizer, grid, PUZZLE_GOLD),
            self.edge(grid, detokenizer, PUZZLE_GOLD),
            self.edge(detokenizer, reconstructed_dog, IMAGE_BLUE),
        )
        
        label_text = self.takeaway("256 x 256 x 3  ->  16 x 16 token grid  ->  256 x 256 x 3", PUZZLE_GOLD)
        label_text.to_edge(DOWN, buff=0.38)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(rail), FadeIn(dog_card), FadeIn(tokenizer), run_time=1.2)
        self.play(GrowArrow(arrows[0]), run_time=0.5)
        self.play(GrowArrow(arrows[1]), FadeIn(grid), run_time=1.0)
        self.play(GrowArrow(arrows[2]), FadeIn(detokenizer), run_time=1.0)
        self.play(GrowArrow(arrows[3]), FadeIn(reconstructed_dog), run_time=1.0)
        self.play(FadeIn(label_text), run_time=0.8)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def vqgan_key_idea(self):
        tag = self.section_tag("slide 21", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("VQGAN: bridging local context and long-range relations.")
        
        # Pipeline: Image -> CNN Encoder -> Codebook -> Token Image -> CNN Decoder -> Reconstructed
        # Arrange horizontally
        img = self.vector_chip("Image", IMAGE_BLUE, 1.0).move_to([-5.2, 0.2, 0])
        enc = self.module("CNN Encoder", IMAGE_BLUE, 1.6).move_to([-3.4, 0.2, 0])
        quant = self.module("Codebook\nQuantizer", PUZZLE_GOLD, 1.6, 0.8).move_to([-1.2, 0.2, 0])
        tokens = self.vector_chip("Token Grid", PUZZLE_GOLD, 1.4).move_to([1.1, 0.2, 0])
        dec = self.module("CNN Decoder", IMAGE_BLUE, 1.6).move_to([3.1, 0.2, 0])
        recon = self.vector_chip("Reconstructed", IMAGE_BLUE, 1.7).move_to([5.2, 0.2, 0])
        
        # Transformer block above
        transformer = self.module("Transformer", TEXT_PURPLE, 2.0, 0.8).move_to([1.1, 1.9, 0])
        cond_input = self.vector_chip("Condition\n(Text/Depth)", TEXT_PURPLE, 1.6).move_to([-1.2, 1.9, 0])
        
        edges = VGroup(
            self.edge(img, enc, IMAGE_BLUE),
            self.edge(enc, quant, IMAGE_BLUE),
            self.edge(quant, tokens, PUZZLE_GOLD),
            self.edge(tokens, dec, IMAGE_BLUE),
            self.edge(dec, recon, IMAGE_BLUE),
            Arrow(cond_input.get_right(), transformer.get_left(), color=TEXT_PURPLE, stroke_width=2.5),
            DoubleArrow(transformer.get_bottom(), tokens.get_top(), color=TEXT_PURPLE, stroke_width=2.5)
        )
        
        takeaways = VGroup(
            self.label("CNNs learn local, context-rich visual parts.", color=IMAGE_BLUE, font=FONT_TITLE),
            self.label("Transformers model long-range interactions between parts.", color=TEXT_PURPLE, font=FONT_TITLE)
        ).arrange(DOWN, buff=0.15).scale(0.85).to_edge(DOWN, buff=0.4)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(img), FadeIn(enc), FadeIn(quant), FadeIn(tokens), FadeIn(dec), FadeIn(recon), run_time=1.5)
        self.play(LaggedStart(*[Create(e) for e in edges[:5]], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(cond_input), FadeIn(transformer), Create(edges[5]), Create(edges[6]), run_time=1.0)
        self.play(FadeIn(takeaways), run_time=0.9)
        self.wait(15.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def two_stage_training(self):
        tag = self.section_tag("slide 22", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("VQGAN training has two decoupled phases.")
        
        left_box = self.soft_box(5.8, 4.4, color=IMAGE_BLUE, fill_opacity=0.02, stroke_opacity=0.4).move_to([-3.1, -0.2, 0])
        right_box = self.soft_box(5.8, 4.4, color=TEXT_PURPLE, fill_opacity=0.02, stroke_opacity=0.4).move_to([3.1, -0.2, 0])
        
        left_title = self.label("Stage 1: Reconstruction", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([-3.1, 1.6, 0])
        right_title = self.label("Stage 2: Conditional Generation", SUBTITLE_SIZE, TEXT_PURPLE, font=FONT_TITLE).move_to([3.1, 1.6, 0])
        
        left_desc = VGroup(
            self.label("- Learn Encoder (E), Decoder (D), Codebook (Z)", 14, TEXT),
            self.label("- Optimize VQ loss + perceptual/GAN loss", 14, TEXT),
            self.label("- Goal: Compress images to rich discrete tokens", 14, TEXT)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.1, -0.2, 0])
        
        right_desc = VGroup(
            self.label("- Freeze Encoder, Decoder, and Codebook", 14, TEXT),
            self.label("- Train Autoregressive Transformer on grids", 14, TEXT),
            self.label("- Goal: Predict next token given conditions", 14, TEXT)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.1, -0.2, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(left_box), FadeIn(left_title), run_time=1.0)
        self.play(FadeIn(left_desc), run_time=0.8)
        self.wait(5.0)
        self.play(FadeIn(right_box), FadeIn(right_title), run_time=1.0)
        self.play(FadeIn(right_desc), run_time=0.8)
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def codebook_quantization(self):
        tag = self.section_tag("slides 23-24", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Codebook lookup: nearest neighbor quantization.")
        
        # ẑ_ij vector from encoder
        z_vector = self.math_chip(r"\hat{z}_{ij}", IMAGE_BLUE, 1.72).move_to([-4.0, 0.4, 0])
        z_caption = self.label("Encoder latent", 13, MUTED, font=FONT_BODY).next_to(z_vector, DOWN, buff=0.08)
        
        # Codebook Z box on right
        codebook_box = self.soft_box(3.45, 4.35, color=PUZZLE_GOLD, fill_opacity=0.05, stroke_opacity=0.7).move_to([3.5, 0.18, 0])
        codebook_lbl = self.label("Codebook Z", SUBTITLE_SIZE, PUZZLE_GOLD, font=FONT_TITLE).move_to([3.5, 1.94, 0])
        
        # Codebook slots
        slots = VGroup()
        for i, val in enumerate([r"z_1", r"z_2", r"z_3", r"\cdots", r"z_K"]):
            col = POSITIVE_GREEN if i == 1 else DIM
            slot = self.math_chip(val, col, 1.18).scale(0.85)
            if i == 1:
                nearest = self.label("nearest", 12, POSITIVE_GREEN, font=FONT_BODY)
                nearest.next_to(slot, RIGHT, buff=0.12)
                slot = VGroup(slot, nearest)
            slots.add(slot)
        slots.arrange(DOWN, buff=0.16).move_to([3.5, 0.25, 0])
        
        # Distance measurements lines
        lines = VGroup(
            DashedLine(z_vector.get_right(), slots[0].get_left(), color=NEGATIVE_ORANGE, stroke_width=1.5),
            Line(z_vector.get_right(), slots[1].get_left(), color=POSITIVE_GREEN, stroke_width=3),
            DashedLine(z_vector.get_right(), slots[2].get_left(), color=NEGATIVE_ORANGE, stroke_width=1.5)
        )
        
        formula = self.display_equation(
            r"z_q = q(\hat{z}_{ij}) = \arg\min_{z_k \in Z} || \hat{z}_{ij} - z_k ||_2^2",
            plain="z_q = argmin || z_hat - z_k ||",
            width=6.0,
            size=24,
            accent=PUZZLE_GOLD
        ).move_to([-4.0, -1.8, 0])
        
        token_id = self.vector_chip("Token label = 42", POSITIVE_GREEN, 2.2).move_to([3.5, -1.65, 0])
        arrow_token = Arrow(slots[1].get_bottom(), token_id.get_top(), color=POSITIVE_GREEN, stroke_width=2.5)

        self.play(FadeIn(tag), FadeIn(title), FadeIn(z_vector), FadeIn(z_caption), FadeIn(codebook_box), FadeIn(codebook_lbl), FadeIn(slots), run_time=1.5)
        self.play(FadeIn(formula), run_time=0.8)
        self.play(Create(lines[0]), Create(lines[2]), run_time=0.6)
        self.play(Create(lines[1]), Indicate(slots[1], color=POSITIVE_GREEN), run_time=1.0)
        self.play(GrowArrow(arrow_token), FadeIn(token_id), run_time=0.8)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def codebook_losses(self):
        tag = self.section_tag("slide 25", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Codebook losses: stability and reconstruction.")
        
        # Loss formula
        loss_eq = self.display_equation(
            r"\mathcal{L}_{\text{VQ}} = ||x - \hat{x}||^2 + ||\text{sg}[E(x)] - z_q||_2^2 + \beta ||\text{sg}[z_q] - E(x)||_2^2",
            plain="L_VQ = ||x - x_hat||^2 + ||sg[E(x)] - z_q||^2 + beta ||sg[z_q] - E(x)||^2",
            width=11.2,
            size=24,
            accent=PUZZLE_GOLD
        ).move_to([0, 1.2, 0])
        
        # Explainers
        exp_recon = self.takeaway("1. Reconstruction Loss: Keeps reconstructed image sharp/faithful.", IMAGE_BLUE, width=10.0).move_to([0, -0.4, 0])
        exp_code = self.takeaway("2. Codebook Loss: Pulls codebook entries towards encoder outputs.", PUZZLE_GOLD, width=10.0).move_to([0, -1.3, 0])
        exp_commit = self.takeaway("3. Commitment Loss: Stops encoder outputs from fluctuating too much.", TEXT_PURPLE, width=10.0).move_to([0, -2.2, 0])
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(loss_eq), run_time=1.2)
        self.wait(6.0)
        
        # Sequentially highlight terms and introduce explanations
        self.play(Indicate(loss_eq[1][0][:6], color=IMAGE_BLUE), FadeIn(exp_recon), run_time=1.2) # x-x_hat term
        self.wait(4.0)
        self.play(Indicate(loss_eq[1][0][6:19], color=PUZZLE_GOLD), FadeIn(exp_code), run_time=1.2) # sg[E(x)]-zq term
        self.wait(4.0)
        self.play(Indicate(loss_eq[1][0][19:], color=TEXT_PURPLE), FadeIn(exp_commit), run_time=1.2) # sg[zq]-E(x) term
        self.wait(12.0)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def perceptual_gan_loss(self):
        tag = self.section_tag("slide 26", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("Perceptual + GAN loss -> sharper, realistic reconstructions.")
        
        # Real vs Reconstructed image cards
        real_card = self.media_card("Real image (x)", "Original", IMAGE_BLUE, 2.2, 1.8, ("external_16_39/red_car_main.jpg",), kind="image").move_to([-4.5, 1.0, 0])
        recon_card = self.media_card("Reconstructed", "Blurry initial state", PUZZLE_GOLD, 2.2, 1.8, ("generated/car_token_grid.png",), kind="image").move_to([-1.5, 1.0, 0])
        
        # Discriminator (D)
        discriminator = self.module("Discriminator (D)\n(Adversarial Judge)", TEXT_PURPLE, 2.4, 1.0).move_to([2.8, 1.0, 0])
        
        arrows = VGroup(
            Arrow(real_card.get_right(), discriminator.get_left(), color=IMAGE_BLUE, stroke_width=2),
            Arrow(recon_card.get_right(), discriminator.get_left(), color=PUZZLE_GOLD, stroke_width=2),
        )
        
        # Balance scale represented visually.
        scale_beam = Line([-3.0, -1.8, 0], [3.0, -1.8, 0], color=DIM, stroke_width=4)
        scale_fulcrum = Polygon([-0.2, -2.1, 0], [0.2, -2.1, 0], [0, -1.8, 0], color=DIM, fill_color=DIM, fill_opacity=0.6)
        scale_left = self.vector_chip("Generator (Decoder)", IMAGE_BLUE, 2.4).move_to([-3.0, -1.2, 0])
        scale_right = self.vector_chip("Discriminator", TEXT_PURPLE, 2.4).move_to([3.0, -1.2, 0])
        scale = VGroup(scale_beam, scale_fulcrum, scale_left, scale_right)
        
        takeaway_label = self.takeaway("GAN loss penalises blurry details, enforcing crisp edges.", TEXT_PURPLE)
        takeaway_label.to_edge(DOWN, buff=0.38)
        
        self.play(FadeIn(tag), FadeIn(title), FadeIn(real_card), FadeIn(recon_card), FadeIn(discriminator), Create(arrows), run_time=1.5)
        self.wait(5.0)
        self.play(FadeIn(scale), run_time=1.0)
        self.wait(5.0)
        
        # Sharpening: replace the recon card visual with a sharp version (cross-fade image card visual only)
        sharp_card = self.media_card("Reconstructed", "Sharper results", POSITIVE_GREEN, 2.2, 1.8, ("external_16_39/red_car_main.jpg",), kind="car").move_to([-1.5, 1.0, 0])
        
        self.play(
            FadeOut(recon_card),
            FadeIn(sharp_card),
            FadeIn(takeaway_label),
            run_time=1.5
        )
        self.wait(10.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
