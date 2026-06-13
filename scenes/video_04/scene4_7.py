import sys
import os
from manim import *

class Scene4_7(Scene):
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
                print(f"[Scene4_7] Error reading audio duration: {e}")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def draw_haar_filters(self):
        # 2x2 Grid with full mathematical labels
        m1 = MathTex(r"\text{LL (Approximation)}", r"=", r"\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}")
        m2 = MathTex(r"\text{HL (Horizontal)}", r"=", r"\begin{bmatrix} 1 & -1 \\ 1 & -1 \end{bmatrix}")
        m3 = MathTex(r"\text{LH (Vertical)}", r"=", r"\begin{bmatrix} 1 & 1 \\ -1 & -1 \end{bmatrix}")
        m4 = MathTex(r"\text{HH (Diagonal)}", r"=", r"\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}")
        
        # Color specific parts
        m1[0].set_color(GREEN)
        m2[0].set_color(GRAY)
        m3[0].set_color(GRAY)
        m4[0].set_color(RED)
        
        group = VGroup(m1, m2, m3, m4).arrange_in_grid(rows=2, cols=2, buff=1.5).scale(0.8)
        
        lbl = Text("Haar Wavelet Transform Filters", font_size=36, color=BLUE).next_to(group, UP, buff=0.8)
        
        # Add sublabels as shown in slide 43
        lbl_one = Text("One scale", font_size=20, color=YELLOW).next_to(m1, UP, buff=0.3)
        lbl_two = Text("Two scales", font_size=20, color=YELLOW).next_to(VGroup(m2, m3, m4), DOWN, buff=0.8)
        
        return VGroup(lbl, group, lbl_one, lbl_two)

    def construct(self):
        self.camera.background_color = "#000000"

        title = Text("2. SIT Technical Innovations", font_size=40, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Audio 1
        haar_group = self.draw_haar_filters().move_to(ORIGIN).shift(DOWN*0.5)
        self.play(FadeIn(haar_group))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_1.mp3"))

        # Audio 2
        self.play(FadeOut(haar_group))
        sub1 = Text("Innovation 1: Dynamic Patch Sizing", font_size=32, color=BLUE).next_to(title, DOWN)
        self.play(Write(sub1))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_2.mp3"))

        # Audio 3
        low_freq = Rectangle(width=2, height=2, color=BLUE, fill_opacity=0.3).shift(LEFT*3)
        low_grid = VGroup(*[Square(side_length=1.0, color=WHITE) for _ in range(4)]).arrange_in_grid(rows=2, cols=2, buff=0).move_to(low_freq)
        low_lbl = Text("Low Freq (Coarse)\nPatch: 2x2", font_size=20).next_to(low_freq, DOWN)
        
        high_freq = Rectangle(width=4, height=4, color=RED, fill_opacity=0.3).shift(RIGHT*3)
        high_grid = VGroup(*[Square(side_length=0.5, color=WHITE) for _ in range(64)]).arrange_in_grid(rows=8, cols=8, buff=0).move_to(high_freq)
        high_lbl = Text("High Freq (Fine)\nPatch: 8x8", font_size=20).next_to(high_freq, DOWN)
        
        v1_group = VGroup(low_freq, low_grid, low_lbl, high_freq, high_grid, high_lbl).shift(DOWN*0.5)
        self.play(FadeIn(v1_group))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_3.mp3"))

        # Audio 4
        same_tokens = Text("Same number of tokens per scale!", font_size=32, color=GREEN).next_to(v1_group, UP, buff=0.5)
        self.play(Write(same_tokens))
        self.play(Wiggle(same_tokens))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_4.mp3"))

        # Audio 5
        self.play(FadeOut(v1_group), FadeOut(same_tokens), FadeOut(sub1))
        sub2 = Text("Innovation 2: Scale-specific Codebooks", font_size=32, color=GREEN).next_to(title, DOWN)
        self.play(Write(sub2))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_5.mp3"))

        # Audio 6
        q1 = RoundedRectangle(width=3, height=1.5, color=BLUE, fill_opacity=0.3).shift(LEFT*2.5 + DOWN*0.5)
        q1_t = Text("Coarse\nCodebook", font_size=24).move_to(q1)
        q2 = RoundedRectangle(width=3, height=1.5, color=RED, fill_opacity=0.3).shift(RIGHT*2.5 + DOWN*0.5)
        q2_t = Text("Fine Detail\nCodebook", font_size=24).move_to(q2)
        codebooks = VGroup(q1, q1_t, q2, q2_t)
        self.play(FadeIn(codebooks))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_6.mp3"))

        # Audio 7
        self.play(FadeOut(codebooks), FadeOut(sub2))
        sub3 = Text("Innovation 3: Scale-causal Self-attention", font_size=32, color=ORANGE).next_to(title, DOWN)
        self.play(Write(sub3))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_7.mp3"))

        # Audio 8
        mask = VGroup()
        colors = [GREEN if i >= j else RED for i in range(4) for j in range(4)]
        squares = [Square(side_length=0.8, color=WHITE, fill_opacity=0.6, fill_color=c) for c in colors]
        mask.add(*squares).arrange_in_grid(rows=4, cols=4, buff=0.05).move_to(ORIGIN).shift(DOWN*0.5)
        for i in range(4):
            for j in range(4):
                if i >= j:
                    txt = Text("✔", font_size=20, color=BLACK).move_to(mask[i*4+j])
                    mask.add(txt)
                else:
                    txt = Text("X", font_size=20, color=BLACK).move_to(mask[i*4+j])
                    mask.add(txt)

        self.play(FadeIn(mask))
        lbl = Text("Low freq tokens are unaffected by high freq details", font_size=24).next_to(mask, DOWN, buff=0.5)
        self.play(Write(lbl))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_7/4_7_8.mp3"))

        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1.0)
