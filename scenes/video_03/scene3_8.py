from manim import *
import os

class Scene3_8(Scene):
    def safe_add_sound(self, file_path):
        if os.path.exists(file_path):
            self.add_sound(file_path)
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(file_path)
                return audio.duration_seconds, self.renderer.time
            except Exception as e:
                print(f"Error reading audio duration: {e}")
        else:
            print(f"Warning: Audio file {file_path} not found. Skipping.")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)

    def construct(self):
        # AUDIO 1.8.1a: Conclusion text
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_8/1a.wav")

        title = Text("Conclusion", font_size=48, weight=BOLD, color=BLUE).to_edge(UP, buff=1.0)
        
        line = Underline(title, color=WHITE)
        self.play(Write(title), Create(line))
        self.wait(0.5)

        # Bullet points matching Slide 32 exactly
        blist = BulletedList(
            "Discrete token models integrate seamlessly with Large Language Models.",
            "MarkovGen demonstrates that MRF-based prediction is incredibly fast.",
            "FID is flawed; CMMD is a robust, unbiased evaluation metric.",
            font_size=28,
            buff=1.0
        ).shift(DOWN * 0.2)

        for item in blist:
            self.play(FadeIn(item, shift=RIGHT * 0.5), run_time=1.5)
            self.wait(1.0)

        self.wait(2)
        self.wait_for_audio(audio_data)

        # AUDIO 1.8.1b: Transition
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_8/1b.wav")

        # Transition text to Ameesh (Removed "Part III")
        transition_box = Rectangle(width=10, height=1.5, color=GREEN, fill_opacity=0.1).to_edge(DOWN, buff=0.8)
        next_text1 = Text("Next up:", font_size=24, color=YELLOW, weight=BOLD).move_to(transition_box).shift(UP * 0.2)
        next_text2 = Text("Latent Representations & Video Factorization with Ameesh Makadia", font_size=20, color=WHITE).next_to(next_text1, DOWN)

        self.play(Create(transition_box), Write(next_text1), Write(next_text2))
        self.wait(3)
        self.wait_for_audio(audio_data)
        
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)
