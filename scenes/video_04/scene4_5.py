from manim import *
import os
import random

class Scene4_5(Scene):
    def safe_add_sound(self, file_path):
        if os.path.exists(file_path):
            self.add_sound(file_path)
            try:
                from moviepy import AudioFileClip
                audio = AudioFileClip(file_path)
                dur = audio.duration
                audio.close()
                return dur, self.renderer.time
            except Exception as e:
                print(f"[Scene4_5] Error reading audio duration: {e}")
        else:
            print(f"[Scene4_5] Warning: Audio file {file_path} not found.")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def construct(self):
        # ==========================================
        # CHUNK 1: Paradigm Shift
        # ==========================================
        audio_1 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_1.mp3")

        title = Text("Part II: Multiscale image generation with AR models", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # 3 boxes: Diffusion (Noise), AR (Black), Masked (Black)
        box_size = 2.5
        box_diff = Rectangle(width=box_size, height=box_size, fill_color=GREY, fill_opacity=1, color=WHITE)
        
        # Add static noise to diffusion box
        dots = VGroup(*[Dot(radius=0.03, color=random.choice([WHITE, LIGHT_GREY, DARK_GREY, RED, BLUE, GREEN])).move_to(
            box_diff.get_center() + RIGHT * random.uniform(-box_size/2+0.1, box_size/2-0.1) + UP * random.uniform(-box_size/2+0.1, box_size/2-0.1)
        ) for _ in range(800)])
        diff_group = Group(box_diff, dots)

        box_ar = Rectangle(width=box_size, height=box_size, fill_color=BLACK, fill_opacity=1, color=WHITE)
        box_masked = Rectangle(width=box_size, height=box_size, fill_color=BLACK, fill_opacity=1, color=WHITE)

        def create_token_grid(box, is_masked=False):
            grid = VGroup()
            rows, cols = 8, 8
            w = box.width / cols
            h = box.height / rows
            for i in range(rows):
                for j in range(cols):
                    if is_masked and random.random() < 0.35:
                        color = DARK_GREY
                    else:
                        color = random.choice([RED_E, BLUE_E, GREEN_E, YELLOW_E, PURPLE_E, TEAL_E])
                    sq = Rectangle(width=w*0.85, height=h*0.85, fill_color=color, fill_opacity=1, stroke_width=0)
                    sq.move_to(box.get_top() + LEFT * box.width/2 + RIGHT * (j + 0.5) * w + DOWN * (i + 0.5) * h)
                    grid.add(sq)
            return Group(box, grid)

        ar_group = create_token_grid(box_ar, is_masked=False)
        masked_group = create_token_grid(box_masked, is_masked=True)

        boxes = Group(diff_group, ar_group, masked_group).arrange(RIGHT, buff=0.8).shift(UP * 0.5)

        lbl_diff = Text("Diffusion models", font_size=20).next_to(diff_group, DOWN)
        lbl_ar = Text("Autoregressive models", font_size=20).next_to(ar_group, DOWN)
        lbl_masked = Text("Masked models", font_size=20).next_to(masked_group, DOWN)

        self.play(FadeIn(boxes), run_time=3.0)
        self.wait(2)
        self.play(Write(lbl_diff), Write(lbl_ar), Write(lbl_masked), run_time=2.0)

        brace = Brace(Group(lbl_ar, lbl_masked), DOWN)
        brace_txt = brace.get_text("Language Models").scale(0.8).set_color(BLUE)

        self.wait(3)
        self.play(GrowFromCenter(brace), Write(brace_txt), run_time=2.0)
        
        self.wait_for_audio(audio_1)

        # ==========================================
        # CHUNK 2: The AR Trend
        # ==========================================
        audio_2 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_2.mp3")

        self.play(FadeOut(Group(diff_group, lbl_diff, masked_group, lbl_masked, brace, brace_txt)))
        
        # Move the ar_group to the left and scale slightly
        target_ar_group = ar_group.copy().scale(1.2).to_edge(LEFT, buff=1.0).shift(DOWN*0.5)
        new_lbl_ar = Text("Autoregressive models", font_size=24).next_to(target_ar_group, DOWN)
        
        self.play(
            Transform(ar_group, target_ar_group),
            Transform(lbl_ar, new_lbl_ar),
            run_time=2.0
        )

        trend_txt = Text("Recent Trend:\nBorrowing from LLMs", font_size=32, color=BLUE, line_spacing=1.2)
        trend_txt.next_to(Group(target_ar_group, new_lbl_ar), RIGHT, buff=0.8).align_to(target_ar_group, UP).shift(DOWN*0.2)
        self.play(FadeIn(trend_txt, shift=DOWN))

        list_group = VGroup(
            Text("• LlamaGen", font_size=26),
            Text("• VAR", font_size=26),
            Text("• Open-MAGVIT2", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(trend_txt, DOWN, buff=0.6).align_to(trend_txt, LEFT)

        self.play(Write(list_group), run_time=4.0)
        self.wait_for_audio(audio_2)

        # ==========================================
        # CHUNK 3: Raster Scan Drawback
        # ==========================================
        audio_3 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_3.mp3")

        self.play(FadeOut(Group(ar_group, lbl_ar, trend_txt, list_group)))

        # Load the user's ar_drawback image and place it in center
        img_scene = ImageMobject("assets/video_04/scene4_5/ar_drawback.png")
        img_scene.height = 4.5
        img_scene.move_to(ORIGIN).shift(DOWN * 0.3)
        
        # Add a white frame to match the screenshot
        frame = Rectangle(width=img_scene.width, height=img_scene.height, color=WHITE, stroke_width=4).move_to(img_scene)
        
        self.play(FadeIn(img_scene), FadeIn(frame), run_time=1.5)

        # Create black grid covering the image
        rows, cols = 10, 12
        w = img_scene.width / cols
        h = img_scene.height / rows
        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                sq = Rectangle(width=w, height=h, fill_color=BLACK, fill_opacity=1, stroke_width=1, stroke_color=DARK_GREY)
                sq.move_to(frame.get_top() + LEFT * (img_scene.width/2) + RIGHT * (j + 0.5) * w + DOWN * (i + 0.5) * h)
                grid.add(sq)
        
        self.add(grid)

        # Animate first part of the grid fading out VERY SLOWLY
        half_idx = int(len(grid) * 0.35) # Stop at 35%
        self.play(
            AnimationGroup(*[FadeOut(sq) for sq in grid[:half_idx]], lag_ratio=0.15),
            run_time=8.0
        )
        self.wait_for_audio(audio_3)

        # ==========================================
        # CHUNK 4: Drawback Emphasis
        # ==========================================
        audio_4 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_4.mp3")
        
        cross = Cross(frame, stroke_color=RED, stroke_width=8).scale(0.8)
        drawback_txt = Text("Drawback: Poor global context", font_size=36, color=RED, weight=BOLD).next_to(frame, UP, buff=0.5)
        
        self.play(Create(cross), Write(drawback_txt), run_time=2.0)
        self.wait(2)
        
        # Highlight top-left corner
        corner_rect = Rectangle(width=img_scene.width*0.4, height=img_scene.height*0.4, color=YELLOW, stroke_width=6)
        corner_rect.move_to(frame.get_top() + LEFT * (img_scene.width/2) + RIGHT * corner_rect.width/2 + DOWN * corner_rect.height/2)
        self.play(Create(corner_rect), run_time=2.0)

        self.wait_for_audio(audio_4)

        # ==========================================
        # CHUNK 5: The Multiscale Solution
        # ==========================================
        audio_5 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_5.mp3")

        sol_txt = Text("Solution: Multiscale (coarse-to-fine) tokenization", font_size=32, color=GREEN).next_to(title, DOWN, buff=0.5)
        self.play(
            FadeOut(cross), FadeOut(drawback_txt), FadeOut(corner_rect), FadeOut(grid[half_idx:]),
            Group(img_scene, frame).animate.scale(0.6).to_edge(LEFT, buff=1.0),
            Write(sol_txt),
            run_time=2.0
        )
        
        # Simulate coarse-to-fine
        coarse_rect = Rectangle(width=img_scene.width, height=img_scene.height, color=WHITE, fill_color=GREY, fill_opacity=0.9).move_to(img_scene)
        coarse_txt = Text("16x16 Coarse Map", font_size=24).move_to(coarse_rect)
        self.play(FadeIn(coarse_rect), Write(coarse_txt))
        self.wait(1)
        self.play(FadeOut(coarse_rect), FadeOut(coarse_txt))
        
        fine_rect = Rectangle(width=img_scene.width, height=img_scene.height, color=WHITE, fill_color=GREY, fill_opacity=0.4).move_to(img_scene)
        fine_txt = Text("64x64 Fine Details", font_size=24).move_to(fine_rect)
        self.play(FadeIn(fine_rect), Write(fine_txt))
        self.wait(1)
        self.play(FadeOut(fine_rect), FadeOut(fine_txt))

        self.wait_for_audio(audio_5)

        # ==========================================
        # CHUNK 6: VAR & VQ-VAE-2 Pipelines
        # ==========================================
        audio_6 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_6.mp3")

        self.play(FadeOut(img_scene), FadeOut(frame), FadeOut(sol_txt), FadeOut(title))

        title2 = Text("Multiscale Tokenizers", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title2))

        var_img = ImageMobject("assets/video_04/scene4_5/var_pipeline.png")
        vq_img = ImageMobject("assets/video_04/scene4_5/vqvae2_pipeline.png")
        
        # Scale to fit horizontally but keep them reasonable
        var_img.height = 3.5
        vq_img.height = 2.5
        
        pipes = Group(var_img, vq_img).arrange(RIGHT, buff=0.8).shift(DOWN*0.5)
        if pipes.width > 13.0:
            pipes.scale_to_fit_width(13.0)
        
        lbl_var = Text("VAR Pipeline", font_size=24, color=BLUE).next_to(var_img, UP)
        lbl_vq = Text("VQ-VAE-2 Pipeline", font_size=24, color=TEAL).next_to(vq_img, UP)

        self.play(FadeIn(pipes), run_time=3.0)
        self.play(Write(lbl_var), Write(lbl_vq))
        
        # Highlight Top-level and bottom level on VQ-VAE
        vq_hl = Rectangle(width=vq_img.width*0.8, height=vq_img.height*0.8, color=YELLOW).move_to(vq_img)
        self.play(Create(vq_hl), run_time=1.5)
        self.play(FadeOut(vq_hl))

        self.wait_for_audio(audio_6)

        # ==========================================
        # CHUNK 7: Residual Design
        # ==========================================
        audio_7 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_7.mp3")

        res_txt = Text("Residual Design: Conditioning on coarse scales", font_size=32, color=GREEN).next_to(title2, DOWN, buff=0.3)
        self.play(Write(res_txt))
        
        # Highlight VAR next scale prediction
        var_hl = Rectangle(width=var_img.width*0.5, height=var_img.height*0.4, color=RED).move_to(var_img).shift(UP*0.5)
        self.play(Create(var_hl), run_time=1.5)
        self.play(FadeOut(var_hl))

        self.wait_for_audio(audio_7)

        # ==========================================
        # CHUNK 8: Tokenizing Wavelets - SIT
        # ==========================================
        audio_8 = self.safe_add_sound("tts/outputs/video_04/scene4_5/4_5_8.mp3")

        self.play(FadeOut(pipes), FadeOut(lbl_var), FadeOut(lbl_vq), FadeOut(res_txt))

        sit_title = Text("Tokenizing Discrete Wavelet Transforms", font_size=36, color=BLUE).shift(UP)
        sit_sub = Text("SIT (Spectral Image Tokenizer, 2024)", font_size=28, color=TEAL).next_to(sit_title, DOWN, buff=0.5)

        self.play(Write(sit_title), run_time=2.0)
        self.wait(1)
        self.play(FadeIn(sit_sub, shift=UP))

        self.wait_for_audio(audio_8)

        self.play(FadeOut(Group(*self.mobjects)))
