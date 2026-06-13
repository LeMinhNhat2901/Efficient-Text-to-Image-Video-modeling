from manim import *
import os

class Scene4_4(Scene):
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
                print(f"[Scene4_4] Error reading audio duration: {e}")
        else:
            print(f"[Scene4_4] Warning: Audio file {file_path} not found.")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def construct(self):
        # -----------------------------------------------------------------
        # Khúc 2.4a_1: Tiêu đề & Bảng Reconstruction
        # -----------------------------------------------------------------
        audio_a_1 = self.safe_add_sound("tts/outputs/video_04/scene4_4/4_4a_1.mp3")

        title = Text("Reconstruction & Generation Quality", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Reconstruction Table (Full)
        recon_table = Table(
            [
                ["W.A.L.T.", "26.27", "0.79", "0.089", "1280"],
                ["Four-plane", "25.67", "0.77", "0.104", "672"],
                ["WF-VAE", "27.86", "0.83", "0.064", "1280"],
                ["Four-plane-WF-VAE", "26.98", "0.81", "0.073", "672"],
            ],
            col_labels=[
                Text("Method"), 
                Text("PSNR↑"), 
                Text("SSIM↑"), 
                Text("LPIPS↓"), 
                Text("Seq.Len")
            ],
            include_outer_lines=True
        ).scale(0.55).shift(UP * 0.5)
        
        self.play(FadeIn(recon_table))
        self.wait_for_audio(audio_a_1)

        # -----------------------------------------------------------------
        # Khúc 2.4a_2: Nhấn mạnh kết quả
        # -----------------------------------------------------------------
        audio_a_2 = self.safe_add_sound("tts/outputs/video_04/scene4_4/4_4a_2.mp3")
        recon_txt = Text("Comparable reconstruction metrics", font_size=24, color=GREEN).next_to(recon_table, DOWN, buff=0.5)
        recon_arrow = Arrow(recon_txt.get_top(), recon_table.get_bottom(), color=GREEN, buff=0.1)
        
        self.play(Write(recon_txt), GrowArrow(recon_arrow))
        self.wait_for_audio(audio_a_2)

        # -----------------------------------------------------------------
        # Khúc 2.4b_1: Bảng Generation
        # -----------------------------------------------------------------
        audio_b_1 = self.safe_add_sound("tts/outputs/video_04/scene4_4/4_4b_1.mp3")

        # Generation Table (FVD on UCF-101)
        gen_table = Table(
            [
                ["MAGVIT", "76", "-", "306M", "48"],
                ["MAGVIT-v2", "58", "-", "307M", "24"],
                ["W.A.L.T.", "39", "84.68", "214M", "50"],
                ["Four-plane", "38", "58.27", "214M", "50"],
            ],
            col_labels=[
                Text("Method"), 
                Text("UCF-101\n(128x128)"), 
                Text("UCF-101\n(256x256)"), 
                Text("Params"), 
                Text("Steps")
            ],
            include_outer_lines=True
        ).scale(0.55).shift(UP * 0.5)

        # Flip effect
        self.play(
            FadeOut(recon_txt), FadeOut(recon_arrow),
            ReplacementTransform(recon_table, gen_table)
        )
        self.wait_for_audio(audio_b_1)

        # -----------------------------------------------------------------
        # Khúc 2.4b_2: Khoanh tròn 58.27
        # -----------------------------------------------------------------
        audio_b_2 = self.safe_add_sound("tts/outputs/video_04/scene4_4/4_4b_2.mp3")
        # Circle 58.27 (Row 5, Col 3)
        target_cell = gen_table.get_cell((5, 3))
        circle = Ellipse(width=target_cell.width + 0.4, height=target_cell.height + 0.2, color=YELLOW)
        circle.move_to(target_cell.get_center())
        
        self.play(Create(circle))
        self.wait_for_audio(audio_b_2)

        # -----------------------------------------------------------------
        # Khúc 2.4b_3: Tốc độ Generation
        # -----------------------------------------------------------------
        audio_b_3 = self.safe_add_sound("tts/outputs/video_04/scene4_4/4_4b_3.mp3")
        cost_txt = Text("Generation Cost: 1.59s → 0.71s (>2x Faster)", font_size=28, color=BLUE).next_to(gen_table, DOWN, buff=0.8)
        self.play(Write(cost_txt))

        self.wait_for_audio(audio_b_3)
        self.play(FadeOut(Group(*self.mobjects)))
