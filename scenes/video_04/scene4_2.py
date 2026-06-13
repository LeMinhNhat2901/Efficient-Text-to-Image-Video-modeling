from manim import *
import os
import random

class Scene4_2(Scene):
    """Scene 2.2 – Part I: The Video Tokenization Bottleneck
    Covers Slides 7-11 of Ameesh Makadia's tutorial.
    """

    def safe_add_sound(self, file_path: str):
        """Uses moviepy to get precise duration for async audio sync."""
        if os.path.exists(file_path):
            self.add_sound(file_path)
            try:
                from moviepy import AudioFileClip
                audio = AudioFileClip(file_path)
                dur = audio.duration
                audio.close()
                return dur, self.renderer.time
            except Exception as e:
                print(f"[Scene4_2] Error reading audio duration: {e}")
        else:
            print(f"[Scene4_2] Warning: Audio file {file_path} not found. Skipping.")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data, min_wait=1.0):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)
        else:
            self.wait(min_wait)

    def create_2d_grid(self, rows=6, cols=6, side_length=0.25):
        """Helper to create a colorful 2D latent grid matching the slides."""
        grid = VGroup()
        colors = [BLUE_D, GREEN_D, YELLOW_D, PURPLE_D, TEAL_D, ORANGE]
        random.seed(42)
        for i in range(rows):
            for j in range(cols):
                color = random.choice(colors)
                sq = Square(side_length=side_length, fill_color=color, fill_opacity=1, stroke_color=DARK_GREY, stroke_width=0.5)
                sq.move_to(RIGHT * j * side_length + DOWN * i * side_length)
                grid.add(sq)
        grid.center()
        return grid

    def create_3d_volume(self, rows=6, cols=6, depth=6, side_length=0.25, offset=np.array([0.15, 0.15, 0])):
        """Helper to create an isometric colorful 3D volume (stacked grids)."""
        volume = VGroup()
        colors = [BLUE_D, GREEN_D, YELLOW_D, PURPLE_D, TEAL_D, ORANGE]
        random.seed(42)
        for d in range(depth):
            # Draw from back to front
            grid = VGroup()
            for i in range(rows):
                for j in range(cols):
                    color = random.choice(colors)
                    sq = Square(side_length=side_length, fill_color=color, fill_opacity=1, stroke_color=DARK_GREY, stroke_width=0.5)
                    sq.move_to(RIGHT * j * side_length + DOWN * i * side_length)
                    grid.add(sq)
            grid.center()
            # Apply offset for pseudo-3D
            grid.shift(offset * (depth - 1 - d))
            volume.add(grid)
        volume.center()
        return volume

    def create_trapezoid(self, text="Encoder", is_decoder=False):
        """Helper to create the trapezoid shapes seen in the CVPR slides."""
        width = 1.2
        h_tall = 2.5
        h_short = 1.0
        
        if is_decoder:
            pts = [[-width/2, h_short/2, 0], [width/2, h_tall/2, 0], [width/2, -h_tall/2, 0], [-width/2, -h_short/2, 0]]
        else:
            pts = [[-width/2, h_tall/2, 0], [width/2, h_short/2, 0], [width/2, -h_short/2, 0], [-width/2, -h_tall/2, 0]]
            
        poly = Polygon(*pts, fill_color=LIGHT_GREY, fill_opacity=0.2, stroke_color=WHITE, stroke_width=2)
        t = Text(text, font_size=20, color=WHITE).rotate(PI/2)
        return VGroup(poly, t)

    def create_video_stack(self, path):
        """Helper to create a stacked sequence of frames for video."""
        stack = Group()
        for i in range(3):
            if os.path.exists(path):
                img = ImageMobject(path).scale_to_fit_height(2.0)
            else:
                img = Rectangle(width=3.0, height=2.0, color=BLUE, fill_opacity=0.5)
                vid_label = Text("Jellyfish").move_to(img)
                img = Group(img, vid_label)
            # Offset from back to front
            img.shift(RIGHT * (2-i) * 0.15 + UP * (2-i) * 0.15)
            stack.add(img)
        return stack

    def construct(self):
        # -----------------------------------------------------------------
        # 2.2a – Intro to Part I
        # -----------------------------------------------------------------
        audio_a = self.safe_add_sound("tts/outputs/video_04/scene4_2/4_2a.mp3")

        title = Text("Part I: Factorized latent representations for video", font_size=36, weight=BOLD)
        if title.width > config.frame_width - 1:
            title.scale_to_fit_width(config.frame_width - 1)
        title.to_edge(UP)

        self.play(Write(title))

        intro_text = Text("Latent Generative Models", font_size=32, color=BLUE)
        self.play(FadeIn(intro_text, shift=UP))

        self.wait_for_audio(audio_a)
        self.play(FadeOut(intro_text))

        # -----------------------------------------------------------------
        # 2.2b – 2D Tokenization & Losses (Full Slide Pipeline)
        # -----------------------------------------------------------------
        audio_b = self.safe_add_sound("tts/outputs/video_04/scene4_2/4_2b.mp3")

        turtle_path = "assets/video_04/scene4_2/turtle.png"
        if os.path.exists(turtle_path):
            input_img = ImageMobject(turtle_path).scale_to_fit_height(2.0)
        else:
            input_img = Rectangle(width=3, height=2.0, color=GREEN, fill_opacity=0.5)
            input_label = Text("Turtle").move_to(input_img)
            input_img = Group(input_img, input_label)
            
        output_img = input_img.copy()

        encoder = self.create_trapezoid("Encoder", False)
        decoder = self.create_trapezoid("Decoder", True)
        grid_2d = self.create_2d_grid()

        # arrange them: Input -> Encoder -> Grid -> Decoder -> Output
        pipeline = Group(input_img, encoder, grid_2d, decoder, output_img)
        pipeline.arrange(RIGHT, buff=0.4)
        pipeline.center().shift(UP * 0.5)

        self.play(FadeIn(pipeline, shift=RIGHT))

        # Show losses
        losses_title = Text("Reconstruction Losses:", font_size=24, color=YELLOW)
        loss1 = Text("- Pixel (MSE)", font_size=20)
        loss2 = Text("- Perceptual (LPIPS)", font_size=20)
        loss3 = Text("- Discriminator (Adversarial)", font_size=20)
        losses = VGroup(losses_title, loss1, loss2, loss3).arrange(DOWN, aligned_edge=LEFT)
        losses.next_to(pipeline, DOWN, buff=0.8).shift(RIGHT * 2)

        self.play(Write(losses_title))
        self.play(FadeIn(loss1, shift=LEFT))
        self.play(FadeIn(loss2, shift=LEFT))
        self.play(FadeIn(loss3, shift=LEFT))

        self.wait_for_audio(audio_b)

        # -----------------------------------------------------------------
        # 2.2c – The Two-Stage Paradigm
        # -----------------------------------------------------------------
        audio_c = self.safe_add_sound("tts/outputs/video_04/scene4_2/4_2c.mp3")

        # Stage 1: Autoencoder Pipeline
        stage1_text = Text("Stage 1: Train Autoencoder (Learn Latent Space)", font_size=32, color=GREEN).next_to(pipeline, UP, buff=0.5)
        self.play(FadeOut(losses), Write(stage1_text))
        
        self.wait(3) # Wait for audio "Stage 1 focuses entirely on training..."
        
        # Stage 1 disappears completely
        self.play(FadeOut(pipeline), FadeOut(stage1_text))
        
        # Stage 2: Generative Model centered
        stage2_title = Text("Stage 2: Train Generative Model on Tokens", font_size=32, color=ORANGE).move_to(ORIGIN).shift(UP * 1.5)
        self.play(FadeIn(stage2_title, shift=UP))

        # Split path
        discrete_text = Text("Discrete Tokens\n(Autoregressive)", font_size=28).next_to(stage2_title, DOWN, buff=1.5).shift(LEFT * 3.5)
        continuous_text = Text("Continuous Tokens\n(Diffusion Models)", font_size=28).next_to(stage2_title, DOWN, buff=1.5).shift(RIGHT * 3.5)

        a_left = Arrow(stage2_title.get_bottom(), discrete_text.get_top(), buff=0.2, color=BLUE)
        a_right = Arrow(stage2_title.get_bottom(), continuous_text.get_top(), buff=0.2, color=RED)

        self.play(GrowArrow(a_left), FadeIn(discrete_text))
        self.play(GrowArrow(a_right), FadeIn(continuous_text))

        self.wait_for_audio(audio_c)

        # -----------------------------------------------------------------
        # 2.2d – From 2D to Video 3D (Jellyfish Stack)
        # -----------------------------------------------------------------
        audio_d = self.safe_add_sound("tts/outputs/video_04/scene4_2/4_2d.mp3")

        # Clear stage 2 stuff
        self.play(
            FadeOut(stage2_title), FadeOut(discrete_text),
            FadeOut(continuous_text), FadeOut(a_left), FadeOut(a_right)
        )

        vid_title = Text("Video Tokenization", font_size=32, color=RED).next_to(title, DOWN, buff=0.5)

        # Create Jellyfish Pipeline
        input_stack = self.create_video_stack("assets/video_04/scene4_2/jellyfish.png")
        output_stack = self.create_video_stack("assets/video_04/scene4_2/jellyfish.png")
        vid_encoder = self.create_trapezoid("Encoder", False)
        vid_decoder = self.create_trapezoid("Decoder", True)
        volume_3d = self.create_3d_volume()
        
        vid_pipeline = Group(input_stack, vid_encoder, volume_3d, vid_decoder, output_stack)
        vid_pipeline.arrange(RIGHT, buff=0.3)
        vid_pipeline.center().shift(UP * 0.5)

        self.play(FadeIn(vid_pipeline, shift=UP), Write(vid_title))

        # Dimensions H, W, T
        h_label = MathTex("H").next_to(volume_3d, LEFT, buff=0.1)
        w_label = MathTex("W").next_to(volume_3d, DOWN, buff=0.1)
        t_label = MathTex("T").next_to(volume_3d, UR, buff=0.1)

        self.play(FadeIn(h_label), FadeIn(w_label))
        self.play(FadeIn(t_label, shift=RIGHT))

        volume_group = Group(volume_3d, h_label, w_label, t_label)

        self.wait_for_audio(audio_d)

        # -----------------------------------------------------------------
        # 2.2e – The Computational Bottleneck
        # -----------------------------------------------------------------
        audio_e = self.safe_add_sound("tts/outputs/video_04/scene4_2/4_2e.mp3")

        # Focus on the bottleneck
        self.play(
            FadeOut(input_stack), FadeOut(vid_encoder), FadeOut(vid_decoder), FadeOut(output_stack), FadeOut(vid_title),
            volume_group.animate.move_to(LEFT * 3).scale(1.2),
        )

        bottleneck_formula = MathTex(r"\mathcal{O}(", "H", r"\times", "W", r"\times", "T", ")", font_size=72, color=RED)
        bottleneck_text = Text("Storage & Compute", font_size=32, color=RED_B).next_to(bottleneck_formula, DOWN)
        bottleneck_group = VGroup(bottleneck_formula, bottleneck_text).move_to(RIGHT * 2)

        self.play(Write(bottleneck_formula))
        self.play(FadeIn(bottleneck_text))

        # Wiggle T
        self.play(Wiggle(bottleneck_formula[5], scale_value=1.5, rotation_angle=0.1 * PI), run_time=2)

        # Attention text
        attention_text = Text("Self-Attention scales quadratically: ", font_size=24)
        attention_formula = MathTex(r"\mathcal{O}((HWT)^2)", font_size=32, color=ORANGE)
        attention_group = VGroup(attention_text, attention_formula).arrange(RIGHT).next_to(bottleneck_group, DOWN, buff=1)

        self.play(FadeIn(attention_group, shift=UP))

        self.wait_for_audio(audio_e)

        # Fade out
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)
