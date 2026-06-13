import sys
import os
from manim import *

class Scene4_6(Scene):
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
                print(f"[Scene4_6] Error reading audio duration: {e}")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def draw_sit_architecture(self):
        # Build the exact diagram from Slide 42
        encoder = RoundedRectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.2)
        enc_txt = Text("Transformer\nEncoder", font_size=20).move_to(encoder)
        g_enc = VGroup(encoder, enc_txt)
        
        quantizer = RoundedRectangle(width=2.5, height=1.5, color=PURPLE, fill_opacity=0.2)
        quant_txt = Text("Quantizer", font_size=20).move_to(quantizer)
        g_quant = VGroup(quantizer, quant_txt)
        
        decoder = RoundedRectangle(width=2.5, height=1.5, color=GREEN, fill_opacity=0.2)
        dec_txt = Text("Transformer\nDecoder", font_size=20).move_to(decoder)
        g_dec = VGroup(decoder, dec_txt)
        
        # Sequence of tokens [9, 2, 8, 1, 2, 3] from Slide 42
        nums = [9, 2, 8, 1, 2, 3]
        tokens = VGroup()
        for i, n in enumerate(nums):
            sq = Square(side_length=0.4, color=WHITE, fill_opacity=0.8, fill_color=RED if i%2==0 else BLUE)
            txt = Text(str(n), font_size=16, color=BLACK).move_to(sq)
            tokens.add(VGroup(sq, txt))
        
        tokens.arrange(DOWN, buff=0.1)
        
        arch_group = VGroup(g_enc, g_quant, tokens, g_dec).arrange(RIGHT, buff=0.5)
        
        a1 = Arrow(g_enc.get_right(), g_quant.get_left(), buff=0.1)
        a2 = Arrow(g_quant.get_right(), tokens.get_left(), buff=0.1)
        a3 = Arrow(tokens.get_right(), g_dec.get_left(), buff=0.1)
        
        title = Text("Spectral image tokenizer", font_size=28, color=YELLOW).next_to(arch_group, UP, buff=0.5)
        
        return VGroup(title, arch_group, a1, a2, a3).scale(0.75)

    def draw_dwt(self):
        dwt_vis = VGroup(
            Rectangle(width=1.5, height=1.5, color=GREEN, fill_opacity=0.3),
            Rectangle(width=1.5, height=1.5, color=GRAY, fill_opacity=0.3),
            Rectangle(width=1.5, height=1.5, color=GRAY, fill_opacity=0.3),
            Rectangle(width=1.5, height=1.5, color=GRAY, fill_opacity=0.3)
        ).arrange_in_grid(rows=2, cols=2, buff=0.05)
        lbl_ll = Text("LL", font_size=24, color=WHITE).move_to(dwt_vis[0])
        lbl_hl = Text("HL", font_size=24, color=WHITE).move_to(dwt_vis[1])
        lbl_lh = Text("LH", font_size=24, color=WHITE).move_to(dwt_vis[2])
        lbl_hh = Text("HH", font_size=24, color=WHITE).move_to(dwt_vis[3])
        return VGroup(dwt_vis, lbl_ll, lbl_hl, lbl_lh, lbl_hh)

    def construct(self):
        self.camera.background_color = "#000000"

        title = Text("1. Multiscale Tokenizer Paradigm", font_size=40, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))

        flat_grid = VGroup(*[Square(side_length=0.5, color=RED) for _ in range(16)]).arrange_in_grid(rows=4, cols=4, buff=0)
        flat_lbl = Text("Flat Tokenization (ViT-VQGAN)", font_size=20).next_to(flat_grid, DOWN)
        flat_group = VGroup(flat_grid, flat_lbl).shift(LEFT*3)
        
        # Audio 1
        self.play(FadeIn(flat_group))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_1.mp3"))
        
        # Audio 2
        cross = Cross(flat_group)
        self.play(Create(cross))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_2.mp3"))
        
        # Audio 3
        multi_grid = VGroup(
            Rectangle(width=2, height=2, color=BLUE),
            Rectangle(width=1, height=1, color=GREEN).move_to(LEFT*0.5+UP*0.5),
            Rectangle(width=0.5, height=0.5, color=ORANGE).move_to(LEFT*0.75+UP*0.75)
        )
        multi_lbl = Text("Multiscale Tokenization (SIT)", font_size=20).next_to(multi_grid, DOWN)
        multi_group = VGroup(multi_grid, multi_lbl).shift(RIGHT*3)
        self.play(FadeIn(multi_group))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_3.mp3"))

        # Audio 4
        self.play(FadeOut(flat_group), FadeOut(cross), FadeOut(multi_group))
        dwt_title = Text("Discrete Wavelet Transform (DWT)", font_size=32, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(Write(dwt_title))
        dwt_g = self.draw_dwt().move_to(LEFT*4.5 + DOWN*0.5)
        self.play(FadeIn(dwt_g))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_4.mp3"))

        # Audio 5
        lbl_coarse = Text("Approximation (LL)", font_size=18, color=GREEN).next_to(dwt_g[0][0], UP)
        self.play(Write(lbl_coarse))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_5.mp3"))

        # Audio 6
        lbl_fine = Text("Sparse Details", font_size=18, color=WHITE).next_to(dwt_g[0][3], DOWN)
        self.play(Write(lbl_fine))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_6.mp3"))

        # Audio 7
        sit_arch = self.draw_sit_architecture().next_to(dwt_g, RIGHT, buff=0.5)
        arrow_out = Arrow(dwt_g.get_right(), sit_arch.get_left(), buff=0.2)
        self.play(GrowArrow(arrow_out))
        self.play(FadeIn(sit_arch[0]), FadeIn(sit_arch[1][0])) # title, enc
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_7.mp3"))

        # Audio 8
        self.play(FadeIn(sit_arch[2]), FadeIn(sit_arch[1][1])) # a1, quant
        self.play(FadeIn(sit_arch[3]), FadeIn(sit_arch[1][2])) # a2, tokens
        self.play(FadeIn(sit_arch[4]), FadeIn(sit_arch[1][3])) # a3, dec
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_6/4_6_8.mp3"))

        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1.0)
