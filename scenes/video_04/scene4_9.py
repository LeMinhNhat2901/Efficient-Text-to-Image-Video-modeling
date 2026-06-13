import sys
import os
from manim import *

class Scene4_9(Scene):
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
                print(f"[Scene4_9] Error reading audio duration: {e}")
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

    def draw_text_guided_pipeline(self, prompt_text, image_path, text_color):
        # 1. Prompt Text
        prompt_box = Text(prompt_text, font_size=20, color=text_color)
        
        # 2. AR-SIT Box
        ar_box = RoundedRectangle(width=2.0, height=1.2, color=BLUE, fill_opacity=0.3)
        ar_title = Text("AR-SIT", font_size=20, color=YELLOW).move_to(ar_box)
        ar_group = VGroup(ar_box, ar_title)
        
        # 3. Tokens [9, 2, 4, 2, 8, 1, 2, 3] from Slide 50
        nums = [9, 2, 4, 2, 8, 1, 2, 3]
        tokens = VGroup()
        for i, n in enumerate(nums):
            sq = Square(side_length=0.35, color=WHITE, fill_opacity=0.8, fill_color=RED if i%2==0 else BLUE)
            txt = Text(str(n), font_size=14, color=BLACK).move_to(sq)
            tokens.add(VGroup(sq, txt))
        tokens.arrange(RIGHT, buff=0.1)
        
        # 4. SIT Box
        sit_box = RoundedRectangle(width=2.0, height=1.2, color=PURPLE, fill_opacity=0.3)
        sit_txt = Text("SIT", font_size=20).move_to(sit_box)
        sit_group = VGroup(sit_box, sit_txt)
        
        # 5. Output Image
        out_img = self.load_image_safe(image_path, max_width=3.0, max_height=2.5, placeholder_color=ORANGE, placeholder_text="Generated Image")
        
        # Arrange horizontally (excluding prompt)
        pipeline = Group(ar_group, tokens, sit_group, out_img).arrange(RIGHT, buff=0.3)
        
        # Position prompt above AR-SIT
        prompt_box.next_to(ar_group, UP, buff=0.5)
        
        # Add Arrows
        a1 = Arrow(prompt_box.get_bottom(), ar_group.get_top(), buff=0.1)
        a2 = Arrow(ar_group.get_right(), tokens.get_left(), buff=0.1)
        a3 = Arrow(tokens.get_right(), sit_group.get_left(), buff=0.1)
        a4 = Arrow(sit_group.get_right(), out_img.get_left(), buff=0.1)
        
        return Group(prompt_box, pipeline, a1, a2, a3, a4).scale(0.9)

    def construct(self):
        self.camera.background_color = "#000000"

        # Audio 1
        title = Text("5. Evaluation & Applications", font_size=40, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_1.mp3"))

        # Audio 2 - Introduce Upsampling
        sub1 = Text("Text-Guided Upsampling 16x16 -> 256x256", font_size=32, color=BLUE).next_to(title, DOWN)
        self.play(Write(sub1))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_2.mp3"))

        # Audio 3 - Show AR-SIT part of Upsampling
        pipeline_up = self.draw_text_guided_pipeline('"a cupcake on a red\\ncheckered tablecloth"', "assets/video_04/scene4_9/text_guided_up.png", BLUE).move_to(ORIGIN).shift(DOWN*0.5)
        self.play(FadeIn(pipeline_up[0])) # Prompt
        self.play(GrowArrow(pipeline_up[2]), FadeIn(pipeline_up[1][0])) # a1, AR-SIT
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_3.mp3"))

        # Audio 4 - Show Output Image of Upsampling
        self.play(GrowArrow(pipeline_up[3]), FadeIn(pipeline_up[1][1])) # a2, tokens
        self.play(GrowArrow(pipeline_up[4]), FadeIn(pipeline_up[1][2])) # a3, SIT
        self.play(GrowArrow(pipeline_up[5]), FadeIn(pipeline_up[1][3])) # a4, Image
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_4.mp3"))

        # Audio 5 - Introduce Editing
        self.play(FadeOut(pipeline_up), FadeOut(sub1))
        sub2 = Text("Text-Guided Localized Editing", font_size=32, color=ORANGE).next_to(title, DOWN)
        self.play(Write(sub2))
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_5.mp3"))

        # Audio 6 - Show AR-SIT part of Editing
        pipeline_edit = self.draw_text_guided_pipeline('"a close up of a dog face"', "assets/video_04/scene4_9/text_guided_edit.png", ORANGE).move_to(ORIGIN).shift(DOWN*0.5)
        self.play(FadeIn(pipeline_edit[0])) # Prompt
        self.play(GrowArrow(pipeline_edit[2]), FadeIn(pipeline_edit[1][0])) # a1, AR-SIT
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_6.mp3"))

        # Audio 7 - Show Output Image of Editing
        self.play(GrowArrow(pipeline_edit[3]), FadeIn(pipeline_edit[1][1])) # a2, tokens
        self.play(GrowArrow(pipeline_edit[4]), FadeIn(pipeline_edit[1][2])) # a3, SIT
        self.play(GrowArrow(pipeline_edit[5]), FadeIn(pipeline_edit[1][3])) # a4, Image
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_7.mp3"))

        # Audio 8 - THE NEW OUTRO
        self.play(FadeOut(pipeline_edit), FadeOut(sub2), FadeOut(title))
        outro_title = Text("Conclusion", font_size=60, color=BLUE).move_to(UP*1.0)
        outro_sub = Text("The Future of Autoregressive Vision Models", font_size=40, color=WHITE).next_to(outro_title, DOWN, buff=0.5)
        self.play(Write(outro_title))
        self.play(FadeIn(outro_sub))
        
        thank_you = Text("Thank you for watching & See you next time!", font_size=36, color=YELLOW).next_to(outro_sub, DOWN, buff=1.5)
        self.play(Write(thank_you))
        
        self.wait_for_audio(self.safe_add_sound("tts/outputs/video_04/scene4_9/4_9_8.mp3"), min_wait=5.0)

        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1.0)
