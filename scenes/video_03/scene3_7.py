from manim import *
import os

class Scene3_7(Scene):
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
        # AUDIO 1.7.1a: Intro
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_7/1a.wav")

        title = Text("The Solution: CMMD", font_size=44, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # Comparison Table FID vs CMMD
        col1_title = Text("FID", font_size=36, color=RED)
        col1_bullets = VGroup(
            Text("✗ Inception Embeddings", font_size=26),
            Text("✗ Incorrect normality", font_size=26),
            Text("✗ Sample inefficient", font_size=26),
            Text("✗ Biased estimator", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col1 = VGroup(col1_title, col1_bullets).arrange(DOWN, buff=0.6).shift(LEFT * 3.5 + UP * 0.5)

        col2_title = Text("CMMD", font_size=36, color=GREEN)
        col2_bullets = VGroup(
            Text("✓ Rich CLIP Embeddings", font_size=26),
            Text("✓ Distribution-free (MMD)", font_size=26),
            Text("✓ Sample efficient", font_size=26),
            Text("✓ Unbiased estimator", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col2 = VGroup(col2_title, col2_bullets).arrange(DOWN, buff=0.6).shift(RIGHT * 3.5 + UP * 0.5)

        divider = Line(UP * 2, DOWN * 2, color=WHITE)

        self.play(Write(col1_title), Write(col2_title), Create(divider))
        self.wait_for_audio(audio_data)
        
        # AUDIO 1.7.1b: Feature comparison
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_7/1b.wav")

        for b1, b2 in zip(col1_bullets, col2_bullets):
            self.play(FadeIn(b1, shift=RIGHT*0.2), FadeIn(b2, shift=RIGHT*0.2), run_time=0.6)
        
        self.wait(2)
        self.wait_for_audio(audio_data)

        self.play(
            FadeOut(col1), FadeOut(col2), FadeOut(divider), FadeOut(title)
        )

        # AUDIO 1.7.2a: Runtime efficiency
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_7/2a.wav")

        title_eval = Text("CMMD is More Efficient & Aligns with Humans", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title_eval))

        # CMMD Graph (Slide 30)
        graph_path = "assets/video_03/scene3_7/slide30_cmmd_graph.png"
        if os.path.exists(graph_path):
            cmmd_graph = ImageMobject(graph_path)
            cmmd_graph.width = 5.5 # Make graph slightly smaller to avoid overlap
            cmmd_graph.move_to(LEFT * 3.8 + DOWN * 0.5)
            self.play(FadeIn(cmmd_graph))
        else:
            graph_placeholder = Rectangle(width=5.5, height=3.5, color=GRAY).shift(LEFT * 3.8 + DOWN * 0.5)
            graph_text = Text("[INSERT: slide30_cmmd_graph.png]", font_size=20).move_to(graph_placeholder)
            cmmd_graph = VGroup(graph_placeholder, graph_text)
            self.play(FadeIn(cmmd_graph))

        # Runtime Table (Slide 31)
        runtime_table = Table(
            [["Fréchet distance", "7007.59 ± 231 ms"],
             ["MMD distance", "71.42 ± 0.67 ms"],
             ["Inception inference", "2.076 ± 0.15 ms"],
             ["CLIP inference", "1.955 ± 0.14 ms"]],
            col_labels=[Text("Operation"), Text("Time")],
            include_outer_lines=True,
            line_config={"color": WHITE}
        ).scale(0.42).shift(RIGHT * 3.5 + UP * 1.0)

        self.play(Create(runtime_table), run_time=1.5)

        hl_frechet = SurroundingRectangle(runtime_table.get_rows()[1], color=RED)
        hl_mmd = SurroundingRectangle(runtime_table.get_rows()[2], color=GREEN)
        self.play(Create(hl_frechet))
        self.play(Create(hl_mmd))
        self.wait(1)
        self.wait_for_audio(audio_data)

        # AUDIO 1.7.2b: Human Evaluation
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_7/2b.wav")

        # Human Eval Table (Slide 31)
        human_table = Table(
            [["FID", "6.9%", "93.1%"],
             ["CMMD", "92.5%", "7.5%"]],
            col_labels=[Text("Metric"), Text("Agree"), Text("Disagree")],
            include_outer_lines=True,
            line_config={"color": WHITE}
        ).scale(0.45).shift(RIGHT * 3.5 + DOWN * 2.2)

        self.play(Create(human_table), run_time=1.5)

        cmmd_agree_val = human_table.get_entries((3, 2))
        hl_human = SurroundingRectangle(cmmd_agree_val, color=YELLOW)
        self.play(Create(hl_human))
        self.play(Wiggle(cmmd_agree_val, scale_value=1.3))
        
        self.wait(3)
        self.wait_for_audio(audio_data)
