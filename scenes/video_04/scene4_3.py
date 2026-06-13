from manim import *
import numpy as np
import os

# ============================================================
# MODERN VISUALIZATION HELPERS
# ============================================================

class LatentVolume(VGroup):
    def __init__(
        self,
        width=1.5,
        height=1.5,
        depth_layers=5,
        color=TEAL,
        **kwargs
    ):
        super().__init__(**kwargs)
        layers = VGroup()
        for i in range(depth_layers):
            rect = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_width=2,
                color=color
            )
            rect.set_fill(
                color=color,
                opacity=0.15 + i * 0.05
            )
            rect.shift(
                RIGHT * i * 0.08 +
                UP * i * 0.08
            )
            layers.add(rect)
        self.layers = layers
        self.add(layers)

class FeaturePlane(VGroup):
    def __init__(
        self,
        label="",
        color=ORANGE,
        rows=4,
        cols=4,
        size=0.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        np.random.seed(42) 
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=size,
                    stroke_width=1.0,
                    stroke_color=color,
                    color=color
                )
                sq.set_fill(
                    color=color,
                    opacity=np.random.uniform(0.15, 0.75)
                )
                sq.move_to(
                    RIGHT * c * size +
                    DOWN * r * size
                )
                cells.add(sq)
        cells.center()
        border = SurroundingRectangle(
            cells,
            color=color,
            buff=0,
            stroke_width=2
        )
        self.cells = cells
        self.border = border
        self.add(cells, border)
        
        if label:
            txt = Text(label, font_size=16, color=color).next_to(border, DOWN, buff=0.1)
            self.label = txt
            self.add(txt)

def create_trapezoid(text, is_decoder=False):
    w1, w2 = 1.0, 0.4
    h = 1.8
    if is_decoder:
        w1, w2 = w2, w1
    
    poly = Polygon(
        [-w1/2, h/2, 0],
        [w2/2, h/2, 0],
        [w2/2, -h/2, 0],
        [-w1/2, -h/2, 0],
        color=GREY_B,
        fill_color=GREY_E,
        fill_opacity=0.5
    )
    txt = Text(text, font_size=16).move_to(poly).rotate(PI/2)
    return VGroup(poly, txt)

def create_projection_net():
    box = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.1, color=WHITE)
    txt = Text("Projection\nnetwork", font_size=12, line_spacing=0.8).move_to(box)
    return VGroup(box, txt)

def create_jellyfish_frames(path="assets/video_04/scene4_3/jellyfish.png"):
    if os.path.exists(path):
        img = ImageMobject(path).scale_to_fit_height(1.8)
        frames = Group(*[img.copy().shift(RIGHT * i * 0.2 + UP * i * 0.2) for i in range(3)])
    else:
        frames = Group(*[RoundedRectangle(width=2.4, height=1.8, color=PURPLE, fill_opacity=0.3).shift(RIGHT * i * 0.2 + UP * i * 0.2) for i in range(3)])
    return frames

def create_four_plane_block():
    bg = RoundedRectangle(width=1.6, height=1.6, corner_radius=0.15, color=YELLOW, stroke_width=2)
    bg.set_fill(color=YELLOW, opacity=0.05)
    grid = VGroup(
        Square(side_length=0.4, color=ORANGE, fill_opacity=0.7),
        Square(side_length=0.4, color=ORANGE, fill_opacity=0.7),
        Square(side_length=0.4, color=PURPLE, fill_opacity=0.7),
        Square(side_length=0.4, color=BLUE, fill_opacity=0.7)
    ).arrange_in_grid(rows=2, cols=2, buff=0.1).move_to(bg)
    
    group = VGroup(bg, grid)
    txt = Text("Four-plane", font_size=18).next_to(bg, DOWN, buff=0.15)
    return VGroup(group, txt)


# ============================================================
# SCENE 2.3
# ============================================================

class Scene4_3(Scene):
    """Scene 2.3 – Deep Dive into Factorization
    Strictly follows the 3-part script and CVPR Slide visualizations.
    """

    def safe_add_sound(self, file_path: str):
        if os.path.exists(file_path):
            self.add_sound(file_path)
            try:
                from moviepy import AudioFileClip
                audio = AudioFileClip(file_path)
                dur = audio.duration
                audio.close()
                return dur, self.renderer.time
            except Exception as e:
                print(f"[Scene4_3] Error reading audio duration: {e}")
        else:
            print(f"[Scene4_3] Warning: Audio file {file_path} not found.")
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
        # PART 1: Slide 12 - Tri-plane Factorization
        # -----------------------------------------------------------------

        title = Text("Tri-plane Factorization", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # --- Tier 1 (Top Row): Factorization (Left to Right) ---
        in_frames = create_jellyfish_frames()
        encoder = create_trapezoid("Encoder", False)
        vol1 = LatentVolume(width=1.8, height=1.8, depth_layers=6)
        
        proj_net_group = VGroup()
        planes_group = VGroup()
        for i, c in enumerate([RED, GREEN, BLUE]):
            pnet = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.1, color=WHITE)
            ptxt = Text("Projection\nnetwork", font_size=12).move_to(pnet)
            proj_net_group.add(VGroup(pnet, ptxt))
            planes_group.add(FeaturePlane(color=c, rows=3, cols=3, size=0.25))
        
        proj_net_group.arrange(DOWN, buff=0.3)
        planes_group.arrange(DOWN, buff=0.3)

        tier1 = Group(in_frames, encoder, vol1, proj_net_group, planes_group).arrange(RIGHT, buff=0.6)
        tier1.move_to(UP * 1.0)

        # Arrows for Tier 1
        t1_arr1 = Arrow(in_frames.get_right(), encoder.get_left(), buff=0.1, color=WHITE, max_tip_length_to_length_ratio=0.1)
        t1_arr2 = Arrow(encoder.get_right(), vol1.get_left(), buff=0.1, color=WHITE, max_tip_length_to_length_ratio=0.1)
        
        proj_arrows = VGroup()
        for i in range(3):
            arr = Arrow(vol1.get_right(), proj_net_group[i].get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.08)
            p_arr = Arrow(proj_net_group[i].get_right(), planes_group[i].get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.08)
            proj_arrows.add(arr, p_arr)

        # --- Tier 2 (Bottom Row): Recomposition (Right to Left) ---
        vol2 = LatentVolume(width=1.8, height=1.8, depth_layers=6)
        decoder = create_trapezoid("Decoder", True)
        out_frames = create_jellyfish_frames()
        
        vol2.next_to(planes_group, DOWN, buff=1.5)
        decoder.next_to(vol2, LEFT, buff=0.8)
        out_frames.next_to(decoder, LEFT, buff=0.8)
        tier2 = Group(vol2, decoder, out_frames)

        # Recomposition Arrow (Downwards)
        rec_arrow = Arrow(planes_group.get_bottom(), vol2.get_top(), buff=0.2, color=WHITE, max_tip_length_to_length_ratio=0.08)
        rec_txt = Text("Recomposition", font_size=18, color=GREY_A).next_to(rec_arrow, LEFT, buff=0.2)

        # Arrows for Tier 2
        t2_arr1 = Arrow(vol2.get_left(), decoder.get_right(), buff=0.1, color=WHITE, max_tip_length_to_length_ratio=0.1)
        t2_arr2 = Arrow(decoder.get_left(), out_frames.get_right(), buff=0.1, color=WHITE, max_tip_length_to_length_ratio=0.1)

        # --- Animation Sequence ---
        audio_a_1 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3a_1.mp3")
        self.play(FadeIn(in_frames))
        self.play(GrowArrow(t1_arr1), FadeIn(encoder))
        self.play(GrowArrow(t1_arr2), FadeIn(vol1))
        self.wait_for_audio(audio_a_1)

        audio_a_2 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3a_2.mp3")
        self.play(LaggedStart(
            FadeIn(proj_arrows),
            FadeIn(proj_net_group),
            FadeIn(planes_group),
            lag_ratio=0.3
        ))
        
        xy_lbl = Text("XY Plane", font_size=18, color=RED).next_to(planes_group[0], RIGHT, buff=0.3)
        xt_lbl = Text("XT Plane", font_size=18, color=GREEN).next_to(planes_group[1], RIGHT, buff=0.3)
        yt_lbl = Text("YT Plane", font_size=18, color=BLUE).next_to(planes_group[2], RIGHT, buff=0.3)
        planes_lbls = VGroup(xy_lbl, xt_lbl, yt_lbl)
        self.play(Write(planes_lbls))
        self.wait_for_audio(audio_a_2)

        audio_a_3 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3a_3.mp3")
        self.play(GrowArrow(rec_arrow), Write(rec_txt))
        self.play(FadeIn(vol2))
        self.play(GrowArrow(t2_arr1), FadeIn(decoder))
        self.play(GrowArrow(t2_arr2), FadeIn(out_frames))
        self.wait_for_audio(audio_a_3)

        full_part1 = Group(tier1, t1_arr1, t1_arr2, proj_arrows, planes_lbls, rec_arrow, rec_txt, tier2, t2_arr1, t2_arr2)

        # -----------------------------------------------------------------
        # PART 2: Slide 13/14 - Four-plane Factorization
        # -----------------------------------------------------------------

        self.play(FadeOut(full_part1))
        
        four_title = Text("Four-plane Factorization", font_size=36, color=GREEN).to_edge(UP, buff=0.5)
        self.play(Transform(title, four_title))

        # Box 1: Factorization Elements
        vol_main = LatentVolume(width=1.8, height=1.8, depth_layers=6, color=TEAL)
        half1 = LatentVolume(width=1.8, height=1.8, depth_layers=3, color=TEAL_E).next_to(vol_main, LEFT, buff=0.2)
        half2 = LatentVolume(width=1.8, height=1.8, depth_layers=3, color=TEAL_C).next_to(vol_main, RIGHT, buff=0.2)
        
        arr_pool1 = Arrow(half1.get_bottom(), half1.get_bottom() + DOWN*1.0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        arr_pool2 = Arrow(half2.get_bottom(), half2.get_bottom() + DOWN*1.0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        pool_text = Text("Mean pooling", font_size=16, color=YELLOW).next_to(arr_pool2, RIGHT, buff=0.2)

        fp1 = FeaturePlane("Spatial 1", ORANGE, rows=3, cols=3).scale(0.8).next_to(arr_pool1, DOWN, buff=0.1)
        fp2 = FeaturePlane("Spatial 2", ORANGE, rows=3, cols=3).scale(0.8).next_to(arr_pool2, DOWN, buff=0.1)
        st_txt = Text("+ 2 Spatiotemporal Planes", font_size=16, color=BLUE_B).next_to(VGroup(fp1, fp2), DOWN, buff=0.3)

        fact_content = Group(vol_main, half1, half2, arr_pool1, arr_pool2, pool_text, fp1, fp2, st_txt)
        fact_box = SurroundingRectangle(fact_content, color=TEAL, corner_radius=0.2, fill_opacity=0.05, buff=0.4)
        # Shift down the top of fact_box slightly for title
        fact_title = Text("Factorization", font_size=20, color=TEAL).next_to(fact_box.get_top(), DOWN, buff=0.15)
        fact_group = Group(fact_box, fact_title, fact_content)

        # Box 2: Recomposition Elements
        stack_planes = VGroup(
            FeaturePlane("S1", ORANGE, rows=4, cols=4),
            FeaturePlane("S2", ORANGE, rows=4, cols=4),
            FeaturePlane("ST1", PURPLE, rows=4, cols=4),
            FeaturePlane("ST2", BLUE, rows=4, cols=4)
        ).arrange(RIGHT, buff=0.2).scale(0.8)

        p_dot = Dot(color=RED).move_to(stack_planes[1].cells.get_center())
        p_label = MathTex("P_{xy}", font_size=20, color=RED).next_to(p_dot, UP, buff=0.1)

        vec_group = VGroup(
            Rectangle(width=0.4, height=0.7, fill_color=ORANGE, fill_opacity=1),
            Rectangle(width=0.4, height=0.7, fill_color=ORANGE, fill_opacity=1),
            Rectangle(width=0.4, height=0.7, fill_color=PURPLE, fill_opacity=1),
            Rectangle(width=0.4, height=0.7, fill_color=BLUE, fill_opacity=1)
        ).arrange(DOWN, buff=0.1).next_to(stack_planes, RIGHT, buff=0.8)

        vec_labels = VGroup(
            MathTex("f^1_{xy}", font_size=18),
            MathTex("f^2_{xy}", font_size=18),
            MathTex("f_{xt}", font_size=18),
            MathTex("f_{yt}", font_size=18)
        )
        for vl, vg in zip(vec_labels, vec_group):
            vl.next_to(vg, LEFT, buff=0.15)

        extract_arrow = Arrow(p_dot.get_right(), vec_labels[1].get_left(), color=WHITE, stroke_width=2, buff=0.1, max_tip_length_to_length_ratio=0.05)

        combine_node = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1, color=WHITE).next_to(vec_group, RIGHT, buff=0.6)
        combine_text = Text("Combine", font_size=16).move_to(combine_node)
        
        pass_arrow = Arrow(vec_group.get_right(), combine_node.get_left(), color=WHITE, stroke_width=2, buff=0.1, max_tip_length_to_length_ratio=0.08)

        final_vol = LatentVolume(width=1.5, height=1.5, depth_layers=6, color=RED).next_to(combine_node, RIGHT, buff=0.6)
        vol_label = MathTex("V(x,y,t)", font_size=18, color=RED).next_to(final_vol, DOWN)
        out_arrow = Arrow(combine_node.get_right(), final_vol.get_left(), color=WHITE, stroke_width=2, buff=0.1, max_tip_length_to_length_ratio=0.08)

        rec_content = Group(stack_planes, p_dot, p_label, extract_arrow, vec_group, vec_labels, pass_arrow, combine_node, combine_text, out_arrow, final_vol, vol_label)
        rec_box = SurroundingRectangle(rec_content, color=BLUE_B, corner_radius=0.2, fill_opacity=0.05, buff=0.4)
        rec_box_title = Text("Recomposition", font_size=20, color=BLUE_B).next_to(rec_box.get_top(), DOWN, buff=0.15)
        
        rec_group = Group(rec_box, rec_box_title, rec_content)

        # Scale and position both boxes together
        rec_group.next_to(fact_group, RIGHT, buff=0.8)
        four_part = Group(fact_group, rec_group)
        four_part.scale_to_fit_width(13.0).center().shift(DOWN*0.2)

        # Now Animate everything
        audio_b_1 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3b_1.mp3")
        self.play(FadeIn(fact_box), Write(fact_title), FadeIn(vol_main))
        self.play(FadeOut(vol_main), FadeIn(half1), FadeIn(half2))
        self.wait_for_audio(audio_b_1)

        audio_b_2 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3b_2.mp3")
        self.play(GrowArrow(arr_pool1), GrowArrow(arr_pool2), Write(pool_text))
        self.play(FadeIn(fp1), FadeIn(fp2), Write(st_txt))
        self.wait_for_audio(audio_b_2)

        audio_b_3 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3b_3.mp3")
        self.play(FadeIn(rec_box), Write(rec_box_title), FadeIn(stack_planes))
        self.play(FadeIn(p_dot), Write(p_label))
        self.play(GrowArrow(extract_arrow), FadeIn(vec_group), FadeIn(vec_labels))
        self.play(GrowArrow(pass_arrow), FadeIn(combine_node), FadeIn(combine_text))
        self.play(GrowArrow(out_arrow), FadeIn(final_vol), Write(vol_label))
        self.wait_for_audio(audio_b_3)

        # -----------------------------------------------------------------
        # PART 3: Four-plane inside W.A.L.T (Slide 15)
        # -----------------------------------------------------------------
        audio_c_1 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3c_1.mp3")

        self.play(FadeOut(fact_group), FadeOut(rec_group))

        walt_title = Text("Four-plane inside W.A.L.T.", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Transform(title, walt_title))

        # WALT Pipeline
        w_in_frames = create_jellyfish_frames()
        w_enc = create_trapezoid("Encoder", False)
        w_vol1 = LatentVolume(width=1.8, height=1.8, depth_layers=6)
        w_fp = create_four_plane_block()
        w_vol2 = LatentVolume(width=1.8, height=1.8, depth_layers=6)
        w_dec = create_trapezoid("Decoder", True)
        w_out_frames = create_jellyfish_frames()

        walt_pipe = Group(w_in_frames, w_enc, w_vol1, w_fp, w_vol2, w_dec, w_out_frames).arrange(RIGHT, buff=0.4)
        walt_pipe.scale_to_fit_width(12.5).center().shift(UP*1.4)

        w_arrows = VGroup()
        for i in range(len(walt_pipe)-1):
            w_arrows.add(Arrow(walt_pipe[i].get_right(), walt_pipe[i+1].get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.08))

        self.play(FadeIn(walt_pipe), FadeIn(w_arrows))
        self.wait_for_audio(audio_c_1)

        audio_c_2 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3c_2.mp3")
        # Token illustration directly under w_fp
        token_grid = VGroup(
            Square(side_length=0.5, color=BLUE_D, fill_opacity=0.6),
            Square(side_length=0.5, color=BLUE_D, fill_opacity=0.6),
            Square(side_length=0.5, color=PURPLE_A, fill_opacity=0.6),
            Square(side_length=0.5, color=ORANGE, fill_opacity=0.6),
            Square(side_length=0.5, color=ORANGE, fill_opacity=0.6)
        ).arrange(RIGHT, buff=0.05).next_to(w_fp, DOWN, buff=0.8)
        token_lbl = MathTex("t\\times(h+w) + 2\\times h\\times w", font_size=20).next_to(token_grid, DOWN, buff=0.2)
        
        down_arrow = DoubleArrow(w_fp.get_bottom(), token_grid.get_top(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.05)

        # Diffusion Model horizontal to token grid
        diff_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.2, color=BLUE_A, fill_opacity=0.3)
        diff_txt = Text("Diffusion Model", font_size=20).move_to(diff_box)
        diff_model = VGroup(diff_box, diff_txt).next_to(token_grid, RIGHT, buff=1.0)

        to_diff_arrow = Arrow(token_grid.get_right(), diff_model.get_left(), buff=0.15, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.08)

        self.play(GrowArrow(down_arrow), FadeIn(token_grid), Write(token_lbl))
        self.play(GrowArrow(to_diff_arrow), FadeIn(diff_model))
        self.wait_for_audio(audio_c_2)

        audio_c_3 = self.safe_add_sound("tts/outputs/video_04/scene4_3/4_3c_3.mp3")
        note_txt = Text("Only modification occurs at the latent bottleneck", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.play(Write(note_txt))

        self.wait_for_audio(audio_c_3)
        self.play(FadeOut(Group(*self.mobjects)))
