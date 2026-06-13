from manim import *
import os

class Scene3_6(Scene):
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
        # AUDIO 1.6.1a: Intro & Title
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/1a.wav")

        title = Text("Part II: Rethinking FID as an Evaluation Metric", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))

        # Comparing Distributions images (from Slide 24)
        dist_img_path = "assets/video_03/scene3_6/slide24_distributions.png"
        if os.path.exists(dist_img_path):
            dist_img = ImageMobject(dist_img_path)
            dist_img.height = 2.5 # Control height instead of width to prevent pushing things down too much
            dist_img.next_to(title, DOWN, buff=0.2)
            self.play(FadeIn(dist_img))
        else:
            dist_placeholder = Rectangle(width=8, height=2.5, color=GRAY).next_to(title, DOWN, buff=0.2)
            dist_text = Text("[INSERT: slide24_distributions.png]", font_size=24).move_to(dist_placeholder)
            dist_img = VGroup(dist_placeholder, dist_text)
            self.play(FadeIn(dist_img))

        self.wait(1)
        self.wait_for_audio(audio_data)

        # AUDIO 1.6.1b: General Formula
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/1b.wav")

        # General Fréchet Distance Formula
        frechet_general = MathTex(
            r"\text{dist}_F^2(P,Q) := \inf_{\gamma \in \Gamma(P,Q)} \mathbb{E}_{(\mathbf{x},\mathbf{y})\sim\gamma} ||\mathbf{x} - \mathbf{y}||^2",
            font_size=32
        ).next_to(dist_img, DOWN, buff=0.3)
        
        self.play(Write(frechet_general))
        self.wait(1)
        self.wait_for_audio(audio_data)

        # AUDIO 1.6.1c: Gaussian Assumption
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/1c.wav")

        # Gaussian Formula
        frechet_gaussian = MathTex(
            r"\text{dist}_F^2(P,Q) = ||\mu_P - \mu_Q||^2 + \text{Tr}\left(\Sigma_P + \Sigma_Q - 2(\Sigma_P \Sigma_Q)^{\frac{1}{2}}\right)",
            font_size=32
        ).next_to(frechet_general, DOWN, buff=0.5)
        
        gaussian_assump_arrow = Arrow(frechet_general.get_bottom(), frechet_gaussian.get_top(), buff=0.1, color=YELLOW)
        gaussian_assump_text = Text("Under Gaussian Assumption", font_size=20, color=YELLOW).next_to(gaussian_assump_arrow, RIGHT)

        self.play(GrowArrow(gaussian_assump_arrow), Write(gaussian_assump_text))
        self.play(Write(frechet_gaussian))
        self.wait(2)
        self.wait_for_audio(audio_data)

        self.play(FadeOut(dist_img), FadeOut(frechet_general), FadeOut(gaussian_assump_arrow), FadeOut(gaussian_assump_text))
        
        # Move the remaining formula to the top, right below the title
        self.play(frechet_gaussian.animate.next_to(title, DOWN, buff=0.5))

        # AUDIO 1.6.2a: Limitation 1
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/2a.wav")

        # Highlight ImageNet Limitation
        imagenet_box = Rectangle(width=6, height=2, color=ORANGE, fill_opacity=0.1).move_to(LEFT * 3.5 + DOWN * 0.5)
        imagenet_text = Text("Limitation 1: ImageNet Features", font_size=24, color=ORANGE).move_to(imagenet_box).shift(UP * 0.5)
        imagenet_sub = Text("Trained on simple, single-object scenes.\nPoor for complex Text-to-Image models.", font_size=20).next_to(imagenet_text, DOWN)
        self.play(Create(imagenet_box), Write(imagenet_text), Write(imagenet_sub))
        self.wait_for_audio(audio_data)

        # AUDIO 1.6.2b: Limitation 2
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/2b.wav")

        # Highlight Covariance Matrix Inefficiency
        cov_box = Rectangle(width=6, height=2, color=RED, fill_opacity=0.1).move_to(RIGHT * 3.5 + DOWN * 0.5)
        cov_text = Text("Limitation 2: Covariance Matrix", font_size=24, color=RED).move_to(cov_box).shift(UP * 0.5)
        cov_sub = Text("Must estimate massive 2048x2048 matrix.\nSample inefficient & highly biased.", font_size=20).next_to(cov_text, DOWN)
        
        sigma_highlight = SurroundingRectangle(frechet_gaussian[0][-15:-1], color=RED, buff=0.1)
        
        self.play(Create(cov_box), Write(cov_text), Write(cov_sub), Create(sigma_highlight))
        self.wait(2)
        self.wait_for_audio(audio_data)

        # Fade out previous boxes AND formula to clear space
        self.play(FadeOut(imagenet_box), FadeOut(imagenet_text), FadeOut(imagenet_sub),
                  FadeOut(cov_box), FadeOut(cov_text), FadeOut(cov_sub),
                  FadeOut(frechet_gaussian), FadeOut(sigma_highlight))

        # AUDIO 1.6.3a: Gaussian Assumption False & t-SNE
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/3a.wav")

        gaussian_text = Text("Limitation 3: Gaussian Assumption is False!", font_size=36, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(Write(gaussian_text))

        # t-SNE Plot
        tsne_img_path = "assets/video_03/scene3_6/slide27_tsne.png"
        if os.path.exists(tsne_img_path):
            tsne_img = ImageMobject(tsne_img_path)
            tsne_img.height = 4.0
            tsne_img.move_to(LEFT * 3.5 + DOWN * 0.5)
            self.play(FadeIn(tsne_img))
        else:
            tsne_placeholder = Rectangle(width=4.5, height=4.0, color=GRAY).move_to(LEFT * 3.5 + DOWN * 0.5)
            tsne_text = Text("[INSERT: slide27_tsne.png]", font_size=24).move_to(tsne_placeholder)
            tsne_img = VGroup(tsne_placeholder, tsne_text)
            self.play(FadeIn(tsne_img))

        # Caption for t-SNE
        tsne_caption = Text(
            "t-SNE visualization of Inception embeddings\non the COCO 30K dataset",
            font_size=18, color=WHITE
        ).next_to(tsne_img, DOWN, buff=0.2)
        self.play(Write(tsne_caption))
        self.wait_for_audio(audio_data)

        # AUDIO 1.6.3b: Tests
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/3b.wav")

        # Statistical tests
        test1 = Text("Mardia’s Skewness Test", font_size=26)
        test2 = Text("Mardia’s Kurtosis Test", font_size=26)
        test3 = Text("Henze-Zirkler Test", font_size=26)
        tests = VGroup(test1, test2, test3).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(RIGHT * 0.8 + UP * 0.5)

        self.play(Write(tests), run_time=1.5)
        
        cross1 = Cross(test1, stroke_color=RED, stroke_width=6)
        result1 = Text("Reject (p-value 0.0)", color=RED, font_size=20).next_to(test1, RIGHT)

        cross2 = Cross(test2, stroke_color=RED, stroke_width=6)
        result2 = Text("Reject (p-value 0.0)", color=RED, font_size=20).next_to(test2, RIGHT)

        cross3 = Cross(test3, stroke_color=RED, stroke_width=6)
        result3 = Text("Reject (p-value 0.0)", color=RED, font_size=20).next_to(test3, RIGHT)

        self.play(Create(cross1), Write(result1))
        self.play(Create(cross2), Write(result2))
        self.play(Create(cross3), Write(result3))
        self.wait(1)
        self.wait_for_audio(audio_data)

        # AUDIO 1.6.3c: FID Biased
        audio_data = self.safe_add_sound("tts/outputs/video_03/scene3_6/3c.wav")

        # Big Red Cross over "FID"
        big_fid = Text("FID", font_size=72, color=GRAY, weight=BOLD).move_to(RIGHT * 1.5 + DOWN * 1.5)
        big_cross = Cross(big_fid, stroke_color=RED, stroke_width=12)
        biased_text = Text("Biased Estimator!", font_size=36, color=RED).next_to(big_fid, DOWN, buff=0.2)

        self.play(FadeIn(big_fid), Create(big_cross))
        self.play(Write(biased_text))
        self.wait(3)
        self.wait_for_audio(audio_data)
