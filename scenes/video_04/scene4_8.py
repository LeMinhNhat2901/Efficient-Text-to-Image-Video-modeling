import sys
import os
from manim import *

class Scene4_8(Scene):
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
                print(f"[Scene4_8] Error reading audio duration: {e}")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def load_image_safe(self, path, max_width=6, max_height=6, placeholder_color=GREEN, placeholder_text="Missing Image"):
        if os.path.exists(path):
            img = ImageMobject(path)
            img.scale_to_fit_height(max_height)
            if img.width > max_width:
                img.scale_to_fit_width(max_width)
            return img
        else:
            rect = Rectangle(width=max_width, height=max_height, color=placeholder_color, fill_opacity=0.2)
            txt = Text(placeholder_text, font_size=24, color=WHITE).move_to(rect)
            return VGroup(rect, txt)

    def draw_ar_sit_pipeline(self):
        # Build the Autoregressive Generation pipeline (Slide 36-40)
        
        # 1. Prompt Text
        prompt_box = Text('"a squirrel monkey"', font_size=24, color=WHITE)
        
        # 2. AR-SIT Box
        ar_box = RoundedRectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.3)
        ar_title = Text("AR-SIT", font_size=20, color=YELLOW).move_to(ar_box).shift(UP*0.3)
        ar_eq = MathTex(r"P(x_i \mid x_{0:i-1})", font_size=24).move_to(ar_box).shift(DOWN*0.2)
        ar_group = VGroup(ar_box, ar_title, ar_eq)
        
        # 3. Tokens
        nums = [3, 17, 7, 23, 8]
        tokens = VGroup()
        for i, n in enumerate(nums):
            sq = Square(side_length=0.4, color=WHITE, fill_opacity=0.8, fill_color=RED if i%2==0 else BLUE)
            txt = Text(str(n), font_size=16, color=BLACK).move_to(sq)
            tokens.add(VGroup(sq, txt))
        tokens.arrange(RIGHT, buff=0.1)
        
        # 4. SID
        sid_box = RoundedRectangle(width=2.5, height=1.5, color=PURPLE, fill_opacity=0.3)
        sid_txt = Text("Detokenizer\n(SID)", font_size=20).move_to(sid_box)
        sid_group = VGroup(sid_box, sid_txt)
        
        # 5. Output Image
        monkey_img = self.load_image_safe("assets/video_04/scene4_8/squirrel_monkey.png", max_width=2.5, max_height=2.5, placeholder_color=ORANGE, placeholder_text="Monkey")
        
        # Arrange horizontally (excluding prompt)
        pipeline = Group(ar_group, tokens, sid_group, monkey_img).arrange(RIGHT, buff=0.4)
        
        # Position prompt above AR-SIT
        prompt_box.next_to(ar_group, UP, buff=0.5)
        
        # Add Arrows
        a1 = Arrow(prompt_box.get_bottom(), ar_group.get_top(), buff=0.1)
        a2 = Arrow(ar_group.get_right(), tokens.get_left(), buff=0.1)
        a3 = Arrow(tokens.get_right(), sid_group.get_left(), buff=0.1)
        a4 = Arrow(sid_group.get_right(), monkey_img.get_left(), buff=0.1)
        
        return Group(prompt_box, pipeline, a1, a2, a3, a4).scale(0.85)

    def construct(self):
        self.camera.background_color = "#000000"

        # Audio 1
        title = Text("3. Spectral Image Detokenizer (SID)", font_size=40, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_1.mp3"))

        # Audio 2 - Slide 47 (Reconstruction)
        recon_img = self.load_image_safe("assets/video_04/scene4_8/multiscale_recon.png", max_width=12, max_height=6.5, placeholder_color=BLUE, placeholder_text="Multiscale Reconstruction Grid").move_to(ORIGIN).shift(DOWN*0.2)
        self.play(FadeIn(recon_img))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_2.mp3"))

        # Audio 3
        self.play(FadeOut(recon_img))
        title2 = Text("4. Coarse-to-fine Autoregressive Generation", font_size=40, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Transform(title, title2))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_3.mp3"))

        # Audio 4 & 5
        pipeline_group = self.draw_ar_sit_pipeline().move_to(ORIGIN).shift(DOWN*0.2)
        
        # Fade in AR-SIT part
        self.play(FadeIn(pipeline_group[0])) # Prompt
        self.play(GrowArrow(pipeline_group[2]), FadeIn(pipeline_group[1][0])) # a1, AR-SIT
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_4.mp3"))

        # Fade in Tokens and SID and Image
        self.play(GrowArrow(pipeline_group[3]), FadeIn(pipeline_group[1][1])) # a2, tokens
        self.play(GrowArrow(pipeline_group[4]), FadeIn(pipeline_group[1][2])) # a3, SID
        self.play(GrowArrow(pipeline_group[5]), FadeIn(pipeline_group[1][3])) # a4, Monkey img
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_5.mp3"))

        # Audio 6
        self.play(FadeOut(pipeline_group))
        m_gen = self.load_image_safe("assets/video_04/scene4_8/multiscale_gen.png", max_width=6.5, max_height=6.5, placeholder_color=PURPLE, placeholder_text="MSCOCO Generation").move_to(LEFT*3.5 + DOWN*0.2)
        c_gen = self.load_image_safe("assets/video_04/scene4_8/class_cond_gen.png", max_width=6.5, max_height=6.5, placeholder_color=RED, placeholder_text="Class Cond Generation").move_to(RIGHT*3.5 + DOWN*0.2)
        self.play(FadeIn(m_gen), FadeIn(c_gen))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_8/4_8_6.mp3"))

        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1.0)
