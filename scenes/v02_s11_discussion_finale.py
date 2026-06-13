from __future__ import annotations

from pathlib import Path
import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scenes.v02_common import *


REP_GREEN = "#27E08A"
COST_RED = "#FF4081"
FUTURE_CYAN = "#00E5FF"
GOLD = "#F2C94C"


class V02DiscussionFinale(TextPixelsScene):
    """Slide 63: discussion, cost, and closing montage."""

    def construct(self):
        voiceover = Path("tts") / "outputs" / "v02_s11_discussion_finale.wav"
        if os.environ.get("MANIM_EMBED_SCENE_AUDIO") == "1" and voiceover.exists():
            self.add_sound(str(voiceover))

        self.construct_intro(
            "Discussion: What Actually Matters?",
            "Representation, scale, and the cost of generation",
        )

        self.full_machine_recap()
        self.representation_key()
        self.architecture_vs_representation()
        self.data_compute_cost()
        self.inference_cost()
        self.next_tutorials()
        self.closing_montage()

    def image_box(self, asset: str, width: float, height: float, color: str) -> Group:
        path = self.first_asset(asset)
        if path:
            img = ImageMobject(str(path))
            self.fit_to_box(img, width, height)
        else:
            img = self.placeholder_visual("image", width, height, color)
        frame = self.soft_box(width + 0.18, height + 0.18, color=color, fill_opacity=0.035, stroke_opacity=0.64)
        img.move_to(frame)
        return Group(frame, img)

    def pipeline_chip(self, text: str, color: str, width: float = 1.55) -> VGroup:
        chip = self.vector_chip(text, color, width)
        return chip

    def full_machine_recap(self):
        title = self.hook_question("The Text-to-Pixels machine is now visible.", color=FUTURE_CYAN)
        labels = [
            ("Prompt", TEXT_PURPLE),
            ("CLIP\nco-embedding", TEXT_PURPLE),
            ("Visual\nwords", GOLD),
            ("Codebook", GOLD),
            ("Transformer", IMAGE_BLUE),
            ("Diffusion", IMAGE_BLUE),
            ("Guidance", CRF_PURPLE if "CRF_PURPLE" in globals() else VIOLET),
            ("Latent\nspace", REP_GREEN),
            ("Fast\ninference", REP_GREEN),
            ("Image", FUTURE_CYAN),
        ]
        chips = VGroup(*[self.pipeline_chip(t, c, 1.45 if "\n" not in t else 1.62) for t, c in labels])
        chips.arrange(RIGHT, buff=0.13).scale(0.82).move_to([0, 0.15, 0])
        arrows = VGroup(*[
            Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.03, color=MUTED, stroke_width=1.8, max_tip_length_to_length_ratio=0.25)
            for i in range(len(chips) - 1)
        ])
        machine = self.soft_box(12.6, 2.2, color=FUTURE_CYAN, fill_opacity=0.025, stroke_opacity=0.34).move_to(chips)
        note = self.takeaway("Not one magic trick: a stack of representations and algorithms.", FUTURE_CYAN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), FadeIn(machine), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.08), Create(arrows), run_time=1.8)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(8.0)
        self.fast_clear()

    def representation_key(self):
        title = self.hook_question("Image representation is the key.", color=REP_GREEN)
        pixels = self.soft_box(3.35, 3.45, color=COST_RED, fill_opacity=0.035, stroke_opacity=0.55).move_to([-4.1, -0.1, 0])
        latent = self.soft_box(3.35, 3.45, color=REP_GREEN, fill_opacity=0.035, stroke_opacity=0.68).move_to([0, -0.1, 0])
        tokens = self.soft_box(3.35, 3.45, color=GOLD, fill_opacity=0.035, stroke_opacity=0.62).move_to([4.1, -0.1, 0])

        pixel_grid = self.pixel_grid(rows=10, cols=10, side=0.12, colors=(COST_RED, PIXEL_ORANGE if "PIXEL_ORANGE" in globals() else "#FF8A3D")).move_to(pixels.get_center() + 0.35 * UP)
        latent_cube = self.cube_icon(REP_GREEN).scale(0.9).move_to(latent.get_center() + 0.35 * UP)
        token_grid = self.pixel_grid(rows=5, cols=5, side=0.19, colors=(GOLD, TEXT_PURPLE)).move_to(tokens.get_center() + 0.35 * UP)

        text = VGroup(
            self.label("Raw Pixels\nhuge space", SMALL_SIZE, COST_RED, font=FONT_CODE).move_to(pixels.get_bottom() + 0.7 * UP),
            self.label("Latents\ncompressed structure", SMALL_SIZE, REP_GREEN, font=FONT_CODE).move_to(latent.get_bottom() + 0.7 * UP),
            self.label("Tokens\ncompact symbols", SMALL_SIZE, GOLD, font=FONT_CODE).move_to(tokens.get_bottom() + 0.7 * UP),
        )
        arrows = VGroup(
            Arrow(pixels.get_right(), latent.get_left(), buff=0.16, color=REP_GREEN, stroke_width=2.8),
            Arrow(latent.get_right(), tokens.get_left(), buff=0.16, color=GOLD, stroke_width=2.8),
        )
        note = self.takeaway("The same image can be made heavy or light by how we represent it.", REP_GREEN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(pixels), FadeIn(pixel_grid), FadeIn(text[0]), run_time=0.8)
        self.play(GrowArrow(arrows[0]), FadeIn(latent), FadeIn(latent_cube), FadeIn(text[1]), run_time=0.9)
        self.play(GrowArrow(arrows[1]), FadeIn(tokens), FadeIn(token_grid), FadeIn(text[2]), run_time=0.9)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(9.0)
        self.fast_clear()

    def architecture_vs_representation(self):
        title = self.hook_question("Architecture matters. Representation matters more.", color=TEXT)
        unet = self.module("U-Net\nDiffusion", IMAGE_BLUE, 2.4, 1.05).move_to([-3.6, 0.85, 0])
        transformer = self.module("Transformer\nDiT / AR", TEXT_PURPLE, 2.4, 1.05).move_to([-3.6, -0.95, 0])
        representation = self.module("Representation\npixels / latents / tokens", REP_GREEN, 3.35, 1.25).move_to([0.55, -0.05, 0])
        output = self.module("High-quality\ngeneration", GOLD, 2.8, 1.15).move_to([4.65, -0.05, 0])
        arrows = VGroup(
            Arrow(unet.get_right(), representation.get_left() + 0.34 * UP, buff=0.1, color=IMAGE_BLUE, stroke_width=2.6),
            Arrow(transformer.get_right(), representation.get_left() + 0.34 * DOWN, buff=0.1, color=TEXT_PURPLE, stroke_width=2.6),
            Arrow(representation.get_right(), output.get_left(), buff=0.1, color=REP_GREEN, stroke_width=3.2),
        )
        brace = Brace(representation, DOWN, color=REP_GREEN)
        brace_text = self.label("chooses the working space", SMALL_SIZE, REP_GREEN, font=FONT_CODE).next_to(brace, DOWN, buff=0.1)
        note = self.takeaway("A strong model still suffers if the working space is unnecessarily heavy.", REP_GREEN).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(unet), FadeIn(transformer), run_time=0.8)
        self.play(Create(arrows[:2]), FadeIn(representation), run_time=1.0)
        self.play(GrowArrow(arrows[2]), FadeIn(output), Create(brace), FadeIn(brace_text), run_time=1.0)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(8.0)
        self.fast_clear()

    def data_compute_cost(self):
        title = self.hook_question("The magic is not free.", color=COST_RED)
        dc = self.image_box("external_57_63/data_center.jpg", 3.25, 2.15, COST_RED).move_to([3.8, 0.7, 0])
        bill = self.soft_box(2.65, 1.25, color=COST_RED, fill_opacity=0.06, stroke_opacity=0.66).move_to([3.8, -1.6, 0])
        bill_text = self.label("GPU bill:\nplease sit down first", SMALL_SIZE, COST_RED, font=FONT_CODE).move_to(bill)

        baseline = Line([-5.2, -2.2, 0], [0.7, -2.2, 0], color=DIM, stroke_width=2)
        imagenet_bar = Rectangle(width=0.42, height=0.65, color=IMAGE_BLUE, fill_color=IMAGE_BLUE, fill_opacity=0.65).move_to([-4.15, -1.875, 0])
        laion_bar = Rectangle(width=0.72, height=3.05, color=COST_RED, fill_color=COST_RED, fill_opacity=0.65).move_to([-1.5, -0.675, 0])
        bars = VGroup(baseline, imagenet_bar, laion_bar)
        labels = VGroup(
            self.label("ImageNet\n1.2M images", SMALL_SIZE, IMAGE_BLUE, font=FONT_CODE).next_to(imagenet_bar, UP, buff=0.12),
            self.label("LAION\n5B images", SMALL_SIZE, COST_RED, font=FONT_CODE).next_to(laion_bar, UP, buff=0.12),
            self.label("Hundreds of GPU hours\nfor training", SUBTITLE_SIZE, GOLD, font=FONT_TITLE).move_to([-2.75, 2.0, 0]),
        )
        note = self.takeaway("Scale gives impressive visual results, but it also creates real cost.", COST_RED).to_edge(DOWN, buff=0.36)

        self.play(FadeIn(title), run_time=0.8)
        self.play(Create(baseline), GrowFromEdge(imagenet_bar, DOWN), FadeIn(labels[0]), run_time=0.8)
        self.play(GrowFromEdge(laion_bar, DOWN), FadeIn(labels[1]), FadeIn(labels[2]), run_time=1.0)
        self.play(FadeIn(dc), FadeIn(bill), FadeIn(bill_text), run_time=0.9)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(9.0)
        self.fast_clear()

    def inference_cost(self):
        title = self.hook_question("Training is paid once. Inference is paid every request.", color=GOLD)
        prompt = self.prompt_bar('"a cinematic city at sunset"', width=5.2, color=TEXT_PURPLE).move_to([-3.9, 1.75, 0])
        gpu = self.placeholder_visual("code", 1.5, 1.15, COST_RED).move_to([4.65, 0.35, 0])
        gpu_lbl = self.label("shared GPU service", SMALL_SIZE, COST_RED, font=FONT_CODE).next_to(gpu, DOWN, buff=0.1)
        requests = VGroup()
        rng = np.random.default_rng(7)
        for i in range(30):
            dot = Dot(radius=0.028, color=TEXT_PURPLE, fill_opacity=0.78)
            dot.move_to([-1.7 + rng.random() * 2.8, -1.85 + rng.random() * 1.55, 0])
            requests.add(dot)
        beams = VGroup(*[
            Line(dot.get_center(), gpu.get_left() + np.array([0, 0.12 * ((i % 5) - 2), 0]), color=TEXT_PURPLE, stroke_width=0.9, stroke_opacity=0.32)
            for i, dot in enumerate(requests)
        ])
        coolers = VGroup(
            self.vector_chip("LatentCRF", REP_GREEN, 1.55),
            self.vector_chip("SANA", FUTURE_CYAN, 1.25),
            self.vector_chip("VAR", GOLD, 1.12),
            self.vector_chip("MarkovGen", REP_GREEN, 1.65),
        ).arrange(RIGHT, buff=0.2).move_to([0, -2.65, 0])
        note = self.takeaway("Cut inference cost.", REP_GREEN, width=5.0).move_to([4.15, -2.65, 0])

        self.play(FadeIn(title), FadeIn(prompt), FadeIn(gpu), FadeIn(gpu_lbl), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(d) for d in requests], lag_ratio=0.02), Create(beams), run_time=1.5)
        self.play(Wiggle(gpu, scale_value=1.08), run_time=0.8)
        self.play(FadeIn(coolers), gpu.animate.set_color(REP_GREEN), FadeIn(note), run_time=1.0)
        self.wait(9.0)
        self.fast_clear()

    def next_tutorials(self):
        title = self.hook_question("The tutorial continues from these cornerstones.", color=FUTURE_CYAN)
        center = self.module("Cornerstones\nText-to-Pixels", FUTURE_CYAN, 3.0, 1.15).move_to([0, 1.15, 0])
        sadeep = self.soft_box(4.8, 1.65, color=REP_GREEN, fill_opacity=0.045, stroke_opacity=0.65).move_to([-3.0, -1.05, 0])
        ameesh = self.soft_box(4.8, 1.65, color=GOLD, fill_opacity=0.045, stroke_opacity=0.65).move_to([3.0, -1.05, 0])
        s_text = self.label("Sadeep Jayasumana\nMarkovGen and CMMD", SMALL_SIZE, REP_GREEN, font=FONT_TITLE).move_to(sadeep)
        a_text = self.label("Ameesh Makadia\nSpectral Autoencoders\nEfficient Video Generation", SMALL_SIZE, GOLD, font=FONT_TITLE).move_to(ameesh)
        arrows = VGroup(
            Arrow(center.get_bottom(), sadeep.get_top(), buff=0.08, color=REP_GREEN, stroke_width=2.6),
            Arrow(center.get_bottom(), ameesh.get_top(), buff=0.08, color=GOLD, stroke_width=2.6),
        )
        note = self.label("same theme: efficient, scalable generation", SUBTITLE_SIZE, TEXT, font=FONT_TITLE).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(title), FadeIn(center), run_time=0.8)
        self.play(Create(arrows), FadeIn(sadeep), FadeIn(ameesh), FadeIn(s_text), FadeIn(a_text), run_time=1.2)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(8.0)
        self.fast_clear()

    def closing_montage(self):
        title = self.hook_question("Text-to-Pixels Journey", color=FUTURE_CYAN)
        names = [
            ("CLIP", TEXT_PURPLE),
            ("VQGAN", GOLD),
            ("Transformers", IMAGE_BLUE),
            ("MRF", VIOLET),
            ("Muse", GOLD),
            ("Diffusion", IMAGE_BLUE),
            ("Guidance", VIOLET),
            ("LDM", REP_GREEN),
            ("LatentCRF", REP_GREEN),
            ("SANA", FUTURE_CYAN),
            ("VAR", GOLD),
        ]
        pieces = VGroup()
        for i, (name, color) in enumerate(names):
            chip = self.vector_chip(name, color, 1.42 if len(name) < 8 else 1.8)
            x = -5.4 + (i % 6) * 2.15
            y = 1.0 - (i // 6) * 1.25
            chip.move_to([x, y, 0])
            pieces.add(chip)

        road = VGroup()
        for i in range(8):
            seg = Line([-5.6 + i * 1.6, -1.75, 0], [-4.45 + i * 1.6, -1.75, 0], color=FUTURE_CYAN, stroke_width=5, stroke_opacity=0.45)
            road.add(seg)
        road_lbl = self.label("Text-to-Pixels Journey", 36, FUTURE_CYAN, font=FONT_TITLE).move_to([0, -1.18, 0])
        doors = VGroup(
            self.module("Image", FUTURE_CYAN, 1.55, 0.82),
            self.module("Video", GOLD, 1.55, 0.82),
            self.module("3D Worlds", REP_GREEN, 1.95, 0.82),
        ).arrange(RIGHT, buff=0.35).move_to([0, -2.72, 0])
        final_lines = VGroup(
            self.label("Text -> vector -> token or latent", SMALL_SIZE, MUTED, font=FONT_CODE),
            self.label("noise -> structure -> pixels", SMALL_SIZE, MUTED, font=FONT_CODE),
        ).arrange(DOWN, buff=0.12).move_to([0, 2.25, 0])
        thanks = self.label("Thank you for watching.", SUBTITLE_SIZE, TEXT, font=FONT_TITLE).move_to([0, 0.05, 0])

        self.play(FadeIn(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=0.18 * UP) for p in pieces], lag_ratio=0.06), run_time=2.0)
        self.play(Create(road), FadeIn(road_lbl), run_time=1.0)
        self.play(LaggedStart(*[p.animate.move_to(road[min(i, len(road) - 1)].get_center() + 0.48 * UP) for i, p in enumerate(pieces)], lag_ratio=0.04), run_time=1.6)
        self.play(FadeIn(doors), FadeIn(final_lines), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(pieces), FadeOut(road), FadeOut(road_lbl), FadeOut(doors), FadeOut(final_lines), FadeIn(thanks), run_time=1.2)
        self.wait(95.0)
        self.fast_clear(run_time=0.35)
