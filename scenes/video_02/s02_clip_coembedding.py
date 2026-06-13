from __future__ import annotations

from pathlib import Path
import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.common.v02_common import *


class V02ClipCoEmbedding(TextPixelsScene):
    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s02_clip_coembedding.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))
        scene_start = self.time
        self.construct_intro(
            "CLIP and Co-Embedding",
            "How text becomes an address in visual space",
        )

        self.puzzle_timeline()
        self.image_feature_space()
        self.text_outside_space()
        self.coembedding_bridge()
        self.single_vs_two_tower()
        self.infonce_matrix()
        self.prompt_as_address()
        self.tokenization_transition()
        self.hold_for_voiceover(scene_start, voiceover)
        if hasattr(self, "final_hold_group"):
            self.play(FadeOut(self.final_hold_group), run_time=0.9)

    def puzzle_timeline(self):
        tag = self.section_tag("slides 9-10", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Text-to-image was assembled like a puzzle.", color=TEXT, width=10.4)
        title.shift(0.35 * RIGHT + 0.18 * DOWN)
        axis = Line([-5.25, -0.35, 0], [5.25, -0.35, 0], color=DIM, stroke_width=3)
        year_positions = {
            "2015": -4.65,
            "2017": -1.55,
            "2020": 1.45,
            "2021": 4.35,
        }
        ticks = VGroup()
        years = VGroup()
        for year, x in year_positions.items():
            ticks.add(Line([x, -0.58, 0], [x, -0.12, 0], color=MUTED, stroke_width=2.2))
            years.add(self.label(year, 18, TEXT, font=FONT_CODE).move_to([x, -0.92, 0]))

        def badge(name: str, color: str, width: float = 1.45) -> VGroup:
            box = self.soft_box(width, 0.58, color=color, fill_opacity=0.075, stroke_opacity=0.82)
            label = self.label(name, 18, TEXT, font=FONT_SUBTITLE)
            self.fit_to_box(label, width - 0.18, 0.34)
            label.move_to(box)
            return VGroup(box, label)

        groups = VGroup(
            VGroup(
                badge("U-Net", IMAGE_BLUE, 1.18).move_to([year_positions["2015"], 0.85, 0]),
                badge("Diffusion", IMAGE_BLUE, 1.46).move_to([year_positions["2015"], 0.18, 0]),
            ),
            badge("Transformers", TEXT_PURPLE, 1.85).move_to([year_positions["2017"], 0.52, 0]),
            badge("CLIP", TEXT_PURPLE, 1.16).move_to([year_positions["2020"], 0.52, 0]),
            VGroup(
                badge("VQGAN", PUZZLE_GOLD, 1.25).move_to([year_positions["2021"], 1.18, 0]),
                badge("DALL-E", PUZZLE_GOLD, 1.30).move_to([year_positions["2021"], 0.52, 0]),
                badge("LDM", GREEN, 1.04).move_to([year_positions["2021"], -0.14, 0]),
            ),
        )
        connectors = VGroup()
        for group in groups:
            for card in group if isinstance(group, VGroup) and len(group) > 2 else [group]:
                x = card.get_center()[0]
                connectors.add(Line([x, -0.35, 0], [x, card.get_bottom()[1] - 0.05, 0], color=card[0].get_stroke_color(), stroke_width=1.4).set_opacity(0.65))
        clip_glow = SurroundingRectangle(groups[2], color=TEXT_PURPLE, buff=0.08, stroke_width=2.6)
        note = self.takeaway("The pieces arrive at different times; CLIP gives text a visual address.", TEXT_PURPLE, width=8.7)
        note.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), Create(axis), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), FadeIn(years), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(g, shift=0.12 * UP) for g in groups], lag_ratio=0.18), LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.06), run_time=1.6)
        self.play(Create(clip_glow), FadeIn(note, shift=0.08 * UP), Flash(groups[2], color=TEXT_PURPLE), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(VGroup(tag, title, axis, ticks, years, groups, connectors, clip_glow, note)), run_time=0.9)

    def image_feature_space(self):
        tag = self.section_tag("slide 11", IMAGE_BLUE).to_corner(UL, buff=0.48)
        caption = self.label("Images with similar semantic objects are close.", SUBTITLE_SIZE, TEXT, font=FONT_TITLE)
        caption.to_edge(DOWN, buff=0.45)
        clusters = self.make_feature_clusters()
        chaos = clusters.copy()
        rng = np.random.default_rng(101)
        for dot in chaos:
            dot.move_to([rng.uniform(-5.2, 5.2), rng.uniform(-2.1, 2.0), 0])
        labels = VGroup(
            self.vector_chip("dogs / wolves", IMAGE_BLUE, 1.65).move_to([-3.45, 1.75, 0]),
            self.vector_chip("near duplicates", GREEN, 1.85).move_to([0.2, 1.85, 0]),
            self.vector_chip("sunglasses", PUZZLE_GOLD, 1.55).move_to([3.65, 1.35, 0]),
        )
        reps = Group(
            self.media_card("dog", "visual neighbor", IMAGE_BLUE, 1.25, 1.1, ("slides/img_dog.jpg",), "image").move_to([-3.85, -1.55, 0]),
            self.media_card("wolf", "nearby object", IMAGE_BLUE, 1.25, 1.1, ("slides/img_wolf.jpg",), "image").move_to([-2.65, -1.15, 0]),
            self.media_card("glasses", "shared feature", PUZZLE_GOLD, 1.4, 1.1, ("slides/img_sunglasses.jpg",), "image").move_to([3.35, -1.4, 0]),
        )
        circles = VGroup(
            Ellipse(width=2.3, height=1.45, color=IMAGE_BLUE, stroke_opacity=0.42).move_to([-3.15, -0.05, 0]),
            Ellipse(width=2.0, height=1.25, color=GREEN, stroke_opacity=0.42).move_to([0.25, 0.2, 0]),
            Ellipse(width=2.1, height=1.25, color=PUZZLE_GOLD, stroke_opacity=0.42).move_to([3.25, -0.15, 0]),
        )

        self.play(FadeIn(tag), FadeIn(chaos), run_time=1.0)
        self.play(Transform(chaos, clusters), run_time=2.2)
        self.play(Create(circles), LaggedStart(*[FadeIn(l, shift=0.05 * UP) for l in labels], lag_ratio=0.1), run_time=1.1)
        self.play(FadeIn(reps), FadeIn(caption, shift=0.08 * UP), run_time=1.0)
        self.wait(12.0)
        self.feature_space = VGroup(chaos, labels, circles)
        self.play(FadeOut(Group(tag, reps, caption)), run_time=0.4)

    def text_outside_space(self):
        left_space = self.feature_space
        self.play(left_space.animate.scale(0.68).move_to([-3.75, -0.05, 0]), run_time=0.9)
        boundary = Line([-0.15, 2.35, 0], [-0.15, -2.35, 0], color=DIM, stroke_width=2)
        question = self.label("?", 54, MUTED, font=FONT_TITLE).move_to([-0.15, 0, 0])
        language_bg = self.soft_box(4.65, 4.35, color=TEXT_PURPLE, fill_opacity=0.035, stroke_opacity=0.34).move_to([3.25, -0.05, 0])
        vision_label = self.vector_chip("Vision space", IMAGE_BLUE, 1.7).move_to([-4.9, 2.2, 0])
        language_label = self.vector_chip("Language space", TEXT_PURPLE, 2.0).move_to([3.25, 1.86, 0])
        texts = VGroup(*[
            self.vector_chip(text, TEXT_PURPLE, width=w)
            for text, w in [
                ("autonomous car", 2.0),
                ("AI", 0.85),
                ("software", 1.35),
                ("formal raccoon + tophat", 2.65),
            ]
        ]).arrange(DOWN, buff=0.26).move_to([3.25, -0.18, 0])
        note = self.label("Text is not an image. It needs a shared space.", SMALL_SIZE, TEXT).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(language_bg), Create(boundary), FadeIn(question), FadeIn(vision_label), FadeIn(language_label), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(t, shift=0.1 * LEFT) for t in texts], lag_ratio=0.14), FadeIn(note), run_time=1.3)
        self.wait(9.0)
        self.play(FadeOut(VGroup(left_space, language_bg, boundary, question, vision_label, language_label, texts, note)), run_time=0.9)

    def coembedding_bridge(self):
        tag = self.section_tag("slide 12", TEXT_PURPLE).to_corner(UL, buff=0.48)
        title = self.hook_question("CLIP builds an image-text co-embedding space.")
        bridge = self.module("CLIP / ALIGN", TEXT_PURPLE, width=2.2, height=0.78).move_to([0, 1.8, 0])
        left_nodes = Group(
            self.media_card("car", "image", IMAGE_BLUE, 1.35, 1.15, ("slides/img_autonomous_car.jpg", "slides/img_car.jpg"), "car").move_to([-4.2, 0.65, 0]),
            self.media_card("brain", "image", IMAGE_BLUE, 1.35, 1.15, ("slides/img_brain.png", "slides/img_brain.jpg"), "brain").move_to([-4.2, -0.55, 0]),
            self.media_card("code", "image", IMAGE_BLUE, 1.35, 1.15, ("slides/img_code.png", "slides/img_code.jpg"), "code").move_to([-4.2, -1.75, 0]),
        )
        right_nodes = VGroup(
            self.vector_chip("autonomous car", TEXT_PURPLE, 2.05).move_to([4.2, 0.65, 0]),
            self.vector_chip("AI", TEXT_PURPLE, 0.9).move_to([4.2, -0.55, 0]),
            self.vector_chip("software", TEXT_PURPLE, 1.35).move_to([4.2, -1.75, 0]),
        )
        embed_points = VGroup(
            Dot([-1.2, 0.25, 0], radius=0.08, color=IMAGE_BLUE),
            Dot([0.15, -0.55, 0], radius=0.08, color=IMAGE_BLUE),
            Dot([1.15, 0.22, 0], radius=0.08, color=IMAGE_BLUE),
            Dot([-0.82, 0.12, 0], radius=0.08, color=TEXT_PURPLE),
            Dot([0.42, -0.68, 0], radius=0.08, color=TEXT_PURPLE),
            Dot([0.85, 0.08, 0], radius=0.08, color=TEXT_PURPLE),
        ).shift(0.15 * DOWN)
        edges = VGroup(
            Line(embed_points[0], embed_points[3], color=POSITIVE_GREEN, stroke_width=3),
            Line(embed_points[1], embed_points[4], color=POSITIVE_GREEN, stroke_width=3),
            Line(embed_points[2], embed_points[5], color=POSITIVE_GREEN, stroke_width=3),
            DashedLine(embed_points[0], embed_points[5], color=NEGATIVE_ORANGE, stroke_width=2, dash_length=0.08).set_opacity(0.45),
        )
        space_label = VGroup(
            self.label("Image-Text Co-Embedding Space", SUBTITLE_SIZE, TEXT, font=FONT_TITLE),
            self.label("A text address for visual entities", SMALL_SIZE, MUTED),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), FadeIn(bridge), run_time=0.9)
        self.play(FadeIn(left_nodes), FadeIn(right_nodes), run_time=1.0)
        self.play(
            # Image nodes (Group) → simply fade the embed dots in; Group → Dot
            # Transform is not supported on Group (no interpolate_color).
            LaggedStart(*[FadeIn(embed_points[i], shift=0.45 * RIGHT) for i in range(3)], lag_ratio=0.1),
            # Text nodes (VGroup/VMobject) → TransformFromCopy works fine
            LaggedStart(*[TransformFromCopy(n, embed_points[i + 3]) for i, n in enumerate(right_nodes)], lag_ratio=0.1),
            run_time=1.6,
        )
        self.play(Create(edges), FadeIn(space_label, shift=0.08 * UP), run_time=1.2)
        self.wait(13.0)
        self.play(FadeOut(Group(tag, title, bridge, left_nodes, right_nodes, embed_points, edges, space_label)), run_time=0.9)

    def single_vs_two_tower(self):
        tag = self.section_tag("slide 13", IMAGE_BLUE).to_corner(UL, buff=0.48)
        title = self.hook_question("From fixed labels to open vocabulary.")
        left_panel = self.soft_box(5.75, 4.55, color=IMAGE_BLUE, fill_opacity=0.025, stroke_opacity=0.4).move_to([-3.25, -0.25, 0])
        right_panel = self.soft_box(5.75, 4.55, color=TEXT_PURPLE, fill_opacity=0.025, stroke_opacity=0.4).move_to([3.25, -0.25, 0])
        left_title = self.label("Single-tower classifier", SUBTITLE_SIZE, IMAGE_BLUE, font=FONT_TITLE).move_to([-3.25, 1.58, 0])
        right_title = self.label("Two-tower alignment", SUBTITLE_SIZE, TEXT_PURPLE, font=FONT_TITLE).move_to([3.25, 1.58, 0])

        image = self.media_card("image", "input", IMAGE_BLUE, 1.10, 0.96, ("slides/img_dog.jpg",), "image").move_to([-5.25, 0.2, 0])
        encoder = self.module("Image Encoder", IMAGE_BLUE, 1.58).move_to([-3.55, 0.2, 0])
        labels = VGroup(*[self.vector_chip(x, MUTED, 0.95).scale(0.86) for x in ["dog", "car", "cat", "airplane"]]).arrange(DOWN, buff=0.10).move_to([-1.75, 0.2, 0])
        lock = self.lock_icon(MUTED).scale(0.55).next_to(labels, DOWN, buff=0.18)
        left_arrows = VGroup(self.edge(image, encoder, IMAGE_BLUE), self.edge(encoder, labels, IMAGE_BLUE))

        img2 = self.media_card("image", "input", IMAGE_BLUE, 1.05, 0.92, ("slides/img_car.jpg", "slides/img_dog.jpg"), "image").move_to([1.35, 0.75, 0])
        txt2 = self.vector_chip("any text prompt", TEXT_PURPLE, 1.55).scale(0.9).move_to([1.35, -0.65, 0])
        img_enc = self.module("Image Encoder", IMAGE_BLUE, 1.45).move_to([3.25, 0.75, 0])
        txt_enc = self.module("Text Encoder", TEXT_PURPLE, 1.38).move_to([3.25, -0.65, 0])
        vec_i = self.vector_chip("v_image", IMAGE_BLUE, 1.05).scale(0.9).move_to([5.05, 0.75, 0])
        vec_t = self.vector_chip("v_text", TEXT_PURPLE, 1.0).scale(0.9).move_to([5.05, -0.65, 0])
        align_line = DoubleArrow(vec_i.get_bottom(), vec_t.get_top(), color=POSITIVE_GREEN, stroke_width=3, buff=0.08)
        right_arrows = VGroup(self.edge(img2, img_enc, IMAGE_BLUE), self.edge(txt2, txt_enc, TEXT_PURPLE), self.edge(img_enc, vec_i, IMAGE_BLUE), self.edge(txt_enc, vec_t, TEXT_PURPLE))
        note = self.takeaway("Open vocabulary: compare images with arbitrary descriptions.", TEXT_PURPLE)
        note.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), FadeIn(left_panel), FadeIn(right_panel), FadeIn(left_title), FadeIn(right_title), run_time=1.0)
        self.play(FadeIn(image), FadeIn(encoder), FadeIn(labels), FadeIn(lock), LaggedStart(*[GrowArrow(a) for a in left_arrows], lag_ratio=0.1), run_time=1.3)
        self.play(FadeIn(img2), FadeIn(txt2), FadeIn(img_enc), FadeIn(txt_enc), FadeIn(vec_i), FadeIn(vec_t), LaggedStart(*[GrowArrow(a) for a in right_arrows], lag_ratio=0.08), run_time=1.5)
        self.play(GrowArrow(align_line), FadeIn(note, shift=0.08 * UP), run_time=0.9)
        self.wait(18.0)
        self.play(FadeOut(Group(tag, title, left_panel, right_panel, left_title, right_title, image, encoder, labels, lock, left_arrows, img2, txt2, img_enc, txt_enc, vec_i, vec_t, right_arrows, align_line, note)), run_time=0.9)

    def infonce_matrix(self):
        tag = self.section_tag("slide 14", PUZZLE_GOLD).to_corner(UL, buff=0.48)
        title = self.hook_question("Contrastive learning: pull positives, push negatives.")
        n = 4
        cell_size = 0.58
        cells = VGroup()
        labels_left = VGroup()
        labels_top = VGroup()
        rng = np.random.default_rng(22)
        for r in range(n):
            labels_left.add(self.vector_chip(f"Image {r + 1}", IMAGE_BLUE, 1.20).scale(0.66).move_to([-2.55, 0.9 - r * cell_size, 0]))
            labels_top.add(self.vector_chip(f"Text {r + 1}", TEXT_PURPLE, 1.12).scale(0.66).move_to([-1.32 + r * cell_size, 1.62, 0]))
            for c in range(n):
                is_pos = r == c
                val = rng.uniform(0.08, 0.35) if not is_pos else rng.uniform(0.62, 0.78)
                color = POSITIVE_GREEN if is_pos else NEGATIVE_ORANGE
                square = Square(side_length=cell_size - 0.04, stroke_color=DIM, stroke_width=1.0, fill_color=color, fill_opacity=0.13 if not is_pos else 0.26)
                square.move_to([-1.33 + c * cell_size, 0.9 - r * cell_size, 0])
                txt = self.label(f"{val:.2f}", 13, TEXT, font=FONT_CODE).move_to(square)
                cells.add(VGroup(square, txt))
        matrix = VGroup(cells, labels_left, labels_top).move_to([-3.35, -0.12, 0])
        positives = VGroup(*[cells[i * n + i][0] for i in range(n)])
        formula = VGroup(
            self.display_equation(r"\max \; sim(I_i,T_i)", plain="maximize matched pairs", width=3.95, size=25, accent=POSITIVE_GREEN),
            self.display_equation(r"\min \; sim(I_i,T_j),\; i\ne j", plain="minimize mismatches", width=4.15, size=25, accent=NEGATIVE_ORANGE),
            self.display_equation(r"L=-\log\frac{\exp(sim(I_i,T_i)/\tau)}{\sum_j\exp(sim(I_i,T_j)/\tau)}", plain="InfoNCE loss", width=4.85, size=22, accent=PUZZLE_GOLD),
        ).arrange(DOWN, buff=0.22).move_to([3.55, -0.2, 0])
        pull = self.vector_chip("Pull together", POSITIVE_GREEN, 1.85).move_to([0.65, 0.78, 0])
        push = self.vector_chip("Push apart", NEGATIVE_ORANGE, 1.65).move_to([0.65, -0.05, 0])
        mid_arrow_1 = Arrow(matrix.get_right() + 0.15 * RIGHT, pull.get_left() + 0.08 * LEFT, color=POSITIVE_GREEN, stroke_width=2.2, max_tip_length_to_length_ratio=0.12)
        mid_arrow_2 = Arrow(push.get_right() + 0.08 * RIGHT, formula.get_left() + 0.15 * LEFT, color=MUTED, stroke_width=2.2, max_tip_length_to_length_ratio=0.12)
        note = self.label("Over many batches, language becomes a coordinate system for vision.", SMALL_SIZE, TEXT)
        note.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(tag), FadeIn(title, shift=0.1 * DOWN), FadeIn(matrix), run_time=1.0)
        self.play(LaggedStart(*[Indicate(p, color=POSITIVE_GREEN, scale_factor=1.16) for p in positives], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(pull, shift=0.08 * LEFT), FadeIn(push, shift=0.08 * LEFT), GrowArrow(mid_arrow_1), run_time=0.7)
        self.play(GrowArrow(mid_arrow_2), LaggedStart(*[FadeIn(f, shift=0.08 * LEFT) for f in formula], lag_ratio=0.15), FadeIn(note), run_time=1.3)
        self.wait(18.0)
        self.play(FadeOut(VGroup(tag, title, matrix, formula, pull, push, mid_arrow_1, mid_arrow_2, note)), run_time=0.9)

    def prompt_as_address(self):
        tag = self.section_tag("visual address", TEXT_PURPLE).to_corner(UL, buff=0.48)
        prompt = self.prompt_bar("A raccoon wearing formal clothes, wearing a tophat.", width=9.5).move_to([0, 2.0, 0]).scale(0.86)
        raccoon = self.media_card("raccoon", "image example", IMAGE_BLUE, 2.0, 1.65, ("slides/s04_raccoon.png", "slides/s04_raccoon.jpg", "generated/raccoon_prompt_image.png"), "raccoon").move_to([-4.5, -0.15, 0])
        text_encoder = self.module("Text Encoder", TEXT_PURPLE, 1.75).move_to([-1.7, 0.65, 0])
        image_encoder = self.module("Image Encoder", IMAGE_BLUE, 1.85).move_to([-1.7, -0.85, 0])
        vec_text = Dot([1.55, 0.38, 0], radius=0.1, color=TEXT_PURPLE)
        vec_image = Dot([1.9, -0.15, 0], radius=0.1, color=IMAGE_BLUE)
        space = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.3, 1.3, 1],
            x_length=3.6,
            y_length=2.2,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.0},
        ).move_to([2.65, -0.3, 0])
        pin = self.location_pin(POSITIVE_GREEN).scale(0.62).move_to([2.65, 0.0, 0])
        address = self.takeaway("Text becomes an address in visual space.", TEXT_PURPLE)
        address.to_edge(DOWN, buff=0.42)
        arrows = VGroup(
            Arrow(prompt.get_bottom(), text_encoder.get_top(), color=TEXT_PURPLE, stroke_width=3, buff=0.18),
            self.edge(raccoon, image_encoder, IMAGE_BLUE),
            Arrow(text_encoder.get_right(), vec_text.get_left(), color=TEXT_PURPLE, stroke_width=3, buff=0.12),
            Arrow(image_encoder.get_right(), vec_image.get_left(), color=IMAGE_BLUE, stroke_width=3, buff=0.12),
        )

        self.play(FadeIn(tag), FadeIn(prompt), FadeIn(raccoon), FadeIn(text_encoder), FadeIn(image_encoder), Create(space), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(vec_text), FadeIn(vec_image), run_time=1.5)
        self.play(vec_text.animate.move_to([2.58, 0.05, 0]), vec_image.animate.move_to([2.72, -0.05, 0]), run_time=1.1)
        self.play(FadeIn(pin, shift=0.24 * DOWN), FadeIn(address, shift=0.08 * UP), run_time=0.9)
        self.wait(13.0)
        self.address_group = Group(tag, prompt, raccoon, text_encoder, image_encoder, space, vec_text, vec_image, pin, arrows, address)

    def tokenization_transition(self):
        group = self.address_group
        image = self.media_card("visual words", "image", PUZZLE_GOLD, 3.05, 2.35, ("slides/s04_raccoon.png", "slides/s04_raccoon.jpg", "generated/raccoon_prompt_image.png"), "raccoon").move_to([-3.25, 0.2, 0])
        rows, cols = 6, 8
        grid_side = min(image[1].width / (cols + 0.45), image[1].height / (rows + 0.35))
        grid = self.pixel_grid(rows=rows, cols=cols, side=grid_side, colors=(PUZZLE_GOLD, IMAGE_BLUE, TEXT_PURPLE), opacity=0.26).move_to(image[1])
        tokens = VGroup()
        for r in range(rows):
            for c in range(cols):
                box = Square(side_length=grid_side, stroke_color=DIM, stroke_width=0.8, fill_color=PUZZLE_GOLD, fill_opacity=0.08)
                num = self.label(str(100 + 11 * r + c), 10, TEXT, font=FONT_CODE).move_to(box)
                tokens.add(VGroup(box, num))
        tokens.arrange_in_grid(rows=rows, cols=cols, buff=0.035)
        token_panel = self.soft_box(max(tokens.width + 0.45, 3.05), max(tokens.height + 0.45, 2.35), color=PUZZLE_GOLD, fill_opacity=0.035, stroke_opacity=0.62)
        token_panel.move_to([3.25, 0.2, 0])
        tokens.move_to(token_panel)
        token_title = self.label("visual token ids", 18, PUZZLE_GOLD, font=FONT_SUBTITLE)
        token_title.next_to(token_panel, UP, buff=0.14)
        image_title = self.label("image patches", 18, PUZZLE_GOLD, font=FONT_SUBTITLE)
        image_title.next_to(image[0], UP, buff=0.14)
        token_arrow = Arrow(image.get_right() + 0.18 * RIGHT, token_panel.get_left() + 0.18 * LEFT, color=PUZZLE_GOLD, stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
        question = self.label("But how do we represent an image so a model can write it out?", SUBTITLE_SIZE, TEXT, font=FONT_TITLE)
        self.fit_to_box(question, 11.6, 0.55)
        question.to_edge(UP, buff=0.55)
        next_topic = self.takeaway("Next: visual words and image tokenization.", PUZZLE_GOLD)
        next_topic.to_edge(DOWN, buff=0.38)

        # Group objects cannot be Transformed directly (VMobject only).
        # Use a cross-fade instead: fade the address group out while the
        # image card fades in, giving an equivalent dissolve effect.
        self.play(FadeOut(group, run_time=1.0), FadeIn(image, shift=0.06 * DOWN, run_time=1.0), FadeIn(image_title), run_time=1.0)
        self.play(Create(grid), run_time=0.9)
        self.play(GrowArrow(token_arrow), FadeIn(token_panel), TransformFromCopy(grid, tokens), FadeIn(token_title), FadeIn(question, shift=0.08 * DOWN), run_time=1.2)
        self.play(FadeIn(next_topic, shift=0.08 * UP), run_time=0.8)
        self.wait(8.0)
        self.final_hold_group = Group(image, image_title, grid, token_panel, tokens, token_title, token_arrow, question, next_topic)

    def puzzle_piece(self, year: str, name: str, color: str) -> VGroup:
        body = self.soft_box(1.48, 0.9, color=color, fill_opacity=0.07, stroke_opacity=0.78)
        notch = Circle(radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(body.get_right())
        tab = Circle(radius=0.12, stroke_color=color, stroke_width=1.0, fill_color=color, fill_opacity=0.08).move_to(body.get_left())
        label = VGroup(
            self.label(year, 13, MUTED, font=FONT_CODE),
            self.label(name, 16, color, font=FONT_SUBTITLE),
        ).arrange(DOWN, buff=0.05).move_to(body)
        return VGroup(body, tab, notch, label)

    def make_feature_clusters(self) -> VGroup:
        rng = np.random.default_rng(88)
        centers = [(-3.15, -0.05, IMAGE_BLUE), (0.25, 0.2, GREEN), (3.25, -0.15, PUZZLE_GOLD)]
        dots = VGroup()
        for cx, cy, color in centers:
            for _ in range(34):
                dots.add(Dot([rng.normal(cx, 0.42), rng.normal(cy, 0.28), 0], radius=float(rng.uniform(0.018, 0.035)), color=color, fill_opacity=0.67))
        return dots

    def lock_icon(self, color: str) -> VGroup:
        shackle = Arc(radius=0.22, start_angle=0, angle=PI, color=color, stroke_width=3).rotate(PI).shift(0.12 * UP)
        body = RoundedRectangle(width=0.55, height=0.42, corner_radius=0.04, color=color, fill_color=color, fill_opacity=0.08).shift(0.12 * DOWN)
        keyhole = Dot(radius=0.035, color=color).shift(0.1 * DOWN)
        return VGroup(shackle, body, keyhole)

    def location_pin(self, color: str) -> VGroup:
        outer = Circle(radius=0.28, color=color, fill_color=color, fill_opacity=0.12)
        tip = Triangle(color=color, fill_color=color, fill_opacity=0.12).scale(0.24).rotate(PI).next_to(outer, DOWN, buff=-0.06)
        core = Dot(radius=0.07, color=color).move_to(outer)
        return VGroup(tip, outer, core)
