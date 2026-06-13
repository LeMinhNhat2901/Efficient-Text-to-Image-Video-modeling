from manim import *
import wave
import os

def get_audio_duration(file_path):
    if not os.path.exists(file_path): return 5.0 # fallback
    with wave.open(file_path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

class Scene3_1_Plus(Scene):
    def construct(self):
        # =======================================================
        # ⏱️ Khúc 1.1+a: Token hóa hình ảnh (Image Tokenization)
        # =======================================================
        audio1 = "tts/outputs/video_03/scene3_1_plus/1.wav"
        self.add_sound(audio1)
        dur1 = get_audio_duration(audio1)
        
        title1 = Text("Image Tokenization", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title1), run_time=1.0)
        self.wait(10.0)
        
        # Flowchart: 256x256x3 -> Tokenizer -> 16x16
        t_input = Text("256 x 256 x 3", font_size=28)
        box_tok = Rectangle(width=2.5, height=1.0, color=WHITE)
        t_tok = Text("Tokenizer", font_size=24).move_to(box_tok.get_center())
        t_output = Text("16 x 16", font_size=28)
        
        box_group = VGroup(box_tok, t_tok)
        flow_group = VGroup(t_input, box_group, t_output).arrange(RIGHT, buff=1.0).move_to(UP * 2.0)
        
        arr1 = Arrow(t_input.get_right(), box_group.get_left(), buff=0.1)
        arr2 = Arrow(box_group.get_right(), t_output.get_left(), buff=0.1)
        
        self.play(Write(t_input), run_time=1.0)
        self.play(GrowArrow(arr1), FadeIn(box_group), run_time=1.0)
        self.play(GrowArrow(arr2), Write(t_output), run_time=1.0)
        self.wait(10.0)
        
        # Load ảnh sơ đồ ViT-VQGAN
        img_dogs = ImageMobject("assets/video_03/scene3_1_plus/tokenization_dogs.png")
        img_dogs.height = 4.0
        img_dogs.move_to(DOWN * 1.0)
        self.play(FadeIn(img_dogs), run_time=1.5)
        
        self.wait(max(0, dur1 - 25.5))
        
        # =======================================================
        # ⏱️ Khúc 1.1+b: Parti - Giải mã tuần tự (Sequential Decoding)
        # =======================================================
        audio2 = "tts/outputs/video_03/scene3_1_plus/2.wav"
        self.add_sound(audio2)
        dur2 = get_audio_duration(audio2)
        
        self.play(
            FadeOut(img_dogs), FadeOut(flow_group), FadeOut(arr1), FadeOut(arr2),
            run_time=1.0
        )
        
        title2 = Text("Parti (Autoregressive)", font_size=40, color=BLUE).to_edge(UP)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.wait(5.0)
        
        # Ảnh Parti flamingo
        img_parti = ImageMobject("assets/video_03/scene3_1_plus/parti_flamingo.png")
        img_parti.width = 12.0
        img_parti.move_to(DOWN * 0.5)
        
        self.play(FadeIn(img_parti), run_time=1.0)
        self.wait(max(0, dur2 - 8.0))
        
        # =======================================================
        # ⏱️ Khúc 1.1+c: Muse - Giải mã song song (Parallel Decoding)
        # =======================================================
        audio3 = "tts/outputs/video_03/scene3_1_plus/3.wav"
        self.add_sound(audio3)
        dur3 = get_audio_duration(audio3)
        
        self.play(FadeOut(img_parti), run_time=1.0)
        
        title3 = Text("Muse (Parallel Decoding)", font_size=40, color=BLUE).to_edge(UP)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.wait(5.0)
        
        # Ảnh Muse flamingo
        img_muse = ImageMobject("assets/video_03/scene3_1_plus/muse_flamingo.png")
        img_muse.width = 12.0
        img_muse.move_to(DOWN * 0.5)
        
        # Hiệu ứng hiện ra (tượng trưng cho song song refine)
        self.play(FadeIn(img_muse), run_time=2.0)
        self.wait(5.0)
        
        speed_text = Text("Muse 3B is 10x faster than Parti 3B", font_size=32, color=YELLOW)
        speed_text.to_edge(DOWN, buff=0.5)
        
        self.play(Write(speed_text), run_time=1.0)
        self.play(Wiggle(speed_text), run_time=1.5)
        
        self.wait(max(0, dur3 - 16.5))
