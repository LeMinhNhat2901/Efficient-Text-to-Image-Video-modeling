from manim import *
import os

class Scene4_1(Scene):
    """Scene 2.1 – Intro to Ameesh Makadia (Google Research)
    Implements the three sub‑segments 2.1a, 2.1b, 2.1c as described by the user.
    Audio files are expected under `assets/audio/scene2_1/` with names:
        2_1a.wav, 2_1b.wav, 2_1c.wav
    """

    # ---------------------------------------------------------------------
    # Helper methods – copy‑paste from earlier scenes for robust audio sync
    # ---------------------------------------------------------------------
    def safe_add_sound(self, file_path: str):
        """Add sound if it exists and return (duration, start_time).
        Uses pydub for reliable duration reading.
        """
        if os.path.exists(file_path):
            self.add_sound(file_path)
            try:
                from moviepy import AudioFileClip
                audio = AudioFileClip(file_path)
                dur = audio.duration
                audio.close()
                return dur, self.renderer.time
            except Exception as e:
                print(f"[Scene4_1] Error reading audio duration: {e}")
        else:
            print(f"[Scene4_1] Warning: Audio file {file_path} not found. Skipping.")
        return 0.0, self.renderer.time

    def wait_for_audio(self, audio_data):
        duration, start_time = audio_data
        elapsed = self.renderer.time - start_time
        if duration > elapsed:
            self.wait(duration - elapsed)

    # ---------------------------------------------------------------------
    # Main construct
    # ---------------------------------------------------------------------
    def construct(self):
        # -----------------------------------------------------------------
        # 2.1a – Introduce speaker & topic
        # -----------------------------------------------------------------
        audio_a = self.safe_add_sound("tts/outputs/video_04/scene4_1/4_1a.mp3")

        # Main title
        title_main = Text(
            "CVPR 2025 Tutorial: Efficient Text-to-Image/Video Modeling",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        )
        if title_main.width > config.frame_width - 1:
            title_main.scale_to_fit_width(config.frame_width - 1)

        # Speaker line
        speaker = Text(
            "Ameesh Makadia – Google Research",
            font_size=32,
            color=YELLOW,
            weight=BOLD,
        )

        # Google logo
        logo_path = "assets/video_04/scene4_1/google_logo.png"
        if os.path.exists(logo_path):
            logo = ImageMobject(logo_path)
        else:
            logo = Rectangle(width=4, height=1.5, color=GRAY)
        
        logo.height = 1.2

        # Group and center
        intro_group = Group(title_main, speaker, logo).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(Write(title_main))
        self.play(FadeIn(speaker, shift=UP))
        self.play(FadeIn(logo, shift=UP))
        self.wait_for_audio(audio_a)

        # -----------------------------------------------------------------
        # 2.1b – Three perspectives on efficiency
        # -----------------------------------------------------------------
        audio_b = self.safe_add_sound("tts/outputs/video_04/scene4_1/4_1b.mp3")

        # Fade out intro elements
        self.play(
            FadeOut(title_main),
            FadeOut(speaker),
            FadeOut(logo),
            run_time=0.8,
        )

        # New section title
        title_section = Text(
            "Different perspectives on efficiency",
            font_size=34,
            weight=BOLD,
            color=BLUE,
        ).to_edge(UP)
        self.play(Write(title_section))

        # Perspective 1 – Compression
        item1 = Text("Compression", font_size=30, weight=BOLD, color=GREEN)
        sub1 = Text(
            "More compact latent spaces → more efficient generation",
            font_size=24,
        )
        group1 = VGroup(item1, sub1).arrange(DOWN, aligned_edge=LEFT)

        # Perspective 2 – Structured representations
        item2 = Text("Structured representations", font_size=30, weight=BOLD, color=ORANGE)
        sub2 = Text(
            "Latent representation design that enables efficient modeling",
            font_size=24,
        )
        group2 = VGroup(item2, sub2).arrange(DOWN, aligned_edge=LEFT)

        # Perspective 3 – Data sparsity
        item3 = Text("Data sparsity", font_size=30, weight=BOLD, color=RED)
        sub3 = Text(
            "Generative models designed for data‑sparse settings",
            font_size=24,
        )
        group3 = VGroup(item3, sub3).arrange(DOWN, aligned_edge=LEFT)

        perspectives = VGroup(group1, group2, group3).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        perspectives.next_to(title_section, DOWN, buff=0.8)

        # Show each perspective with a gentle slide‑in
        self.play(FadeIn(group1, shift=RIGHT))
        self.wait(2)  # sync with audio cue
        self.play(FadeIn(group2, shift=RIGHT))
        self.wait(2)
        self.play(FadeIn(group3, shift=RIGHT))
        self.wait_for_audio(audio_b)

        # -----------------------------------------------------------------
        # 2.1c – Agenda
        # -----------------------------------------------------------------
        audio_c = self.safe_add_sound("tts/outputs/video_04/scene4_1/4_1c.mp3")

        # Transform three groups into a single "Agenda" box
        agenda_title = Text("Agenda", font_size=38, weight=BOLD, color=WHITE).to_edge(UP)
        self.play(
            FadeOut(title_section),
            ReplacementTransform(perspectives, agenda_title),
            run_time=1.2,
        )

        # List agenda items (from slide 6)
        part1 = Text("Part I – Compression: Factorized latent representations for video", font_size=26, color=GREEN)
        part2 = Text("Part II – Structured representations: Multiscale image generation\nwith autoregressive models", font_size=26, color=ORANGE, line_spacing=0.8)
        part3 = Text("Part III – Data sparsity: Diffusion models from a single 3D shape", font_size=26, color=RED)
        agenda_items = VGroup(part1, part2, part3).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(agenda_title, DOWN, buff=0.8)
        if agenda_items.width > config.frame_width - 1:
            agenda_items.scale_to_fit_width(config.frame_width - 1)

        # Fade in agenda items
        self.play(FadeIn(part1, shift=UP))
        self.play(FadeIn(part2, shift=UP))
        self.play(FadeIn(part3, shift=UP))
        # Highlight Part I momentarily
        self.play(Indicate(part1), run_time=1)

        self.wait_for_audio(audio_c)

        # End of scene – keep everything on screen for a moment then fade out
        self.wait(2)
        self.play(FadeOut(VGroup(agenda_title, agenda_items)), run_time=1.5)
