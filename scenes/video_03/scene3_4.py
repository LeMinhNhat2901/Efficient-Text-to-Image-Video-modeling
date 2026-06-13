from networkx.generators import spectral_graph_forge
from manim import *
import os

def get_image_with_fallback(path, fallback_width, fallback_height, fallback_text):
    if os.path.exists(path):
        img = ImageMobject(path)
        img.height = fallback_height # Force height to prevent oversized images causing overlaps
        return img
    else:
        rect = Rectangle(width=fallback_width, height=fallback_height, fill_color=DARK_GRAY, fill_opacity=0.8, color=WHITE)
        label = Text(f"[Image Missing]\n{fallback_text}\nPath: {path}", font_size=20, color=WHITE).move_to(rect.get_center())
        return VGroup(rect, label)

class Scene3_4(Scene):
    def construct(self):
        # =======================================================
        # ⏱️ Khúc 1.4a: The Intractability & Mean Field (0:00 - ~2:00)
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_4/1.wav")
        
        title = Text("Inference Algorithm: Intractability", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title), run_time=1.0)
        
        # Dịch công thức lên thật cao để không đè vào Manifold
        eq_prob = MathTex(
            "P(\\mathbf{X}=\\mathbf{x}|\\mathbf{I})", 
            "=", 
            "\\frac{1}{Z(\\mathbf{I})} \\exp(-E(\\mathbf{x}|\\mathbf{I}))", 
            font_size=36
        ).shift(UP * 2.5)
        
        self.play(Write(eq_prob), run_time=1.5)
        
        # Nhấn mạnh Partition Function Z
        z_box = SurroundingRectangle(eq_prob[2][0:4], color=RED)
        z_text = Text("Z requires summing over ALL combinations!", font_size=24, color=RED).next_to(z_box, DOWN)
        self.play(Create(z_box), Write(z_text), run_time=1.0)
        
        # Trực quan hóa bùng nổ tổ hợp bằng Grid 16x16
        grid = VGroup(*[Square(side_length=0.1, stroke_color=BLUE, stroke_width=1, fill_color=BLUE, fill_opacity=0.2) for _ in range(256)])
        grid.arrange_in_grid(16, 16, buff=0.02).move_to(LEFT * 3.5 + DOWN * 1.0)
        
        self.play(FadeIn(grid), run_time=1.5)
        
        highlight_sq = grid[119].copy().set_fill(YELLOW, opacity=1).set_stroke(YELLOW, 2)
        self.play(FadeIn(highlight_sq), run_time=0.5)
        
        vocab_text = Text("1 pixel = 8192 possible tokens", font_size=20, color=YELLOW).next_to(grid, RIGHT, buff=0.5).shift(UP * 1.0)
        arrow_vocab = Arrow(highlight_sq.get_right(), vocab_text.get_left(), color=YELLOW, buff=0.1)
        self.play(GrowArrow(arrow_vocab), Write(vocab_text), run_time=1.0)
        
        comb_eq = MathTex("8192 \\times 8192 \\times \\dots \\text{ (256 times)}", font_size=24).next_to(vocab_text, DOWN, buff=0.3).align_to(vocab_text, LEFT)
        comb_res = MathTex("= 8192^{256} \\rightarrow \\infty", font_size=36, color=RED).next_to(comb_eq, DOWN, buff=0.3).align_to(vocab_text, LEFT)
        
        self.play(Write(comb_eq), run_time=1.5)
        self.play(Write(comb_res), Flash(comb_res, color=RED), run_time=1.0)
        
        intractable = Text("COMPUTATIONALLY INTRACTABLE", font_size=28, color=RED, weight=BOLD).next_to(comb_res, DOWN, buff=0.5).align_to(vocab_text, LEFT)
        self.play(Write(intractable), run_time=1.0)
        self.play(Wiggle(intractable), run_time=1.0)
        
        self.wait(5.0)
        
        # Chuyển sang Mean Field
        self.play(
            FadeOut(z_box), FadeOut(z_text), FadeOut(grid), FadeOut(highlight_sq),
            FadeOut(arrow_vocab), FadeOut(vocab_text), FadeOut(comb_eq), FadeOut(comb_res), FadeOut(intractable),
            run_time=1.5
        )
        
        title2 = Text("Mean Field Approximation", font_size=40, color=BLUE).to_edge(UP)
        self.play(ReplacementTransform(title, title2), run_time=1.0)
        
        eq_approx = MathTex("\\approx", "\\prod_{i=1}^N Q_i(x_i)", font_size=36).next_to(eq_prob, RIGHT, buff=0.2)
        approx_text = Text("Fully Factorized Q", font_size=24, color=GREEN).next_to(eq_approx, DOWN)
        self.play(Write(eq_approx), Write(approx_text), run_time=1.5)
        
        # Hình vẽ Manifold 3D Native tuyệt đẹp (Thu nhỏ và đưa về góc trái dưới)
        manifold = ParametricFunction(
            lambda t: np.array([
                2.5 * np.cos(t) + 0.5 * np.cos(3*t),
                1.5 * np.sin(t) - 0.3 * np.sin(2*t),
                0
            ]),
            t_range=[0, TAU],
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2
        ).scale(0.8).move_to(DOWN * 1.5 + LEFT * 3.5)
        
        manifold_label = Text("Factorized Q\nManifold", font_size=20, color=WHITE).next_to(manifold, DOWN, buff=0.2)
        
        # Chỉnh lại tọa độ dot P và Q cho mượt, không đè lên text
        dot_p = Dot(color=RED, radius=0.15).move_to(manifold.get_center() + UP * 2.5 + LEFT * 2.5)
        label_p = Text("True P", font_size=24, color=RED).next_to(dot_p, UP, buff=0.1)
        
        dot_q = Dot(color=TEAL, radius=0.15).move_to(manifold.get_center() + RIGHT * 0.5)
        label_q = Text("Approx Q", font_size=24, color=TEAL).next_to(dot_q, RIGHT, buff=0.1)
        
        projection_arrow = Arrow(dot_p.get_center(), dot_q.get_center(), color=WHITE, buff=0.15)
        
        self.play(FadeIn(manifold), Write(manifold_label), run_time=1.5)
        self.play(FadeIn(dot_p), Write(label_p), run_time=1.0)
        self.play(GrowArrow(projection_arrow), FadeIn(dot_q), Write(label_q), run_time=1.5)
        
        # Công thức KL Divergence (Chỉnh sang phải cho cân đối)
        kl_text = Text("Minimize KL Divergence:", font_size=28, color=YELLOW).move_to(RIGHT * 3.0 + DOWN * 0.5)
        eq_kl = MathTex("D_{KL}(Q||P) = \\mathbb{E}_Q[\\log(Q) - \\log(P)]", font_size=24).next_to(kl_text, DOWN, buff=0.3)
        ref_text = Text("Ref: Krähenbühl & Koltun (2011)", font_size=16, color=LIGHT_GREY).next_to(eq_kl, DOWN, buff=0.5)
        
        self.play(Write(kl_text), Write(eq_kl), Write(ref_text), run_time=2.0)
        self.wait(27.78)
        
        # =======================================================
        # ⏱️ Khúc 1.4b: The Message Passing Algorithm (2:00 - ~4:00)
        # =======================================================
        
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        self.add_sound("tts/outputs/video_03/scene3_4/2.wav")
        
        title3 = Text("Iterative Message Passing Algorithm", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=1.0)
        
        # Native Code Block
        algo_title = Text("Algorithm 1", font_size=28, color=YELLOW, weight=BOLD)
        line1 = MathTex("Q_i(k) \\leftarrow \\text{softmax}(f_i(k))", font_size=24)
        line2 = Text("for num_iterations do", font_size=20, weight=BOLD)
        line3 = MathTex("Q_i(k) \\leftarrow \\sum_{j=1}^n \\mathbf{W}_{ij}^s Q_j(k)", font_size=28) # Spatial
        line4 = MathTex("Q_i(k) \\leftarrow \\sum_{k'=1}^V \\mathbf{W}_{kk'}^c Q_i(k')", font_size=28) # Label
        line5 = MathTex("Q_i(k) \\leftarrow Q_i(k) + f_i(k)", font_size=24)
        line6 = MathTex("Q_i(k) \\leftarrow \\text{softmax}(Q_i(k))", font_size=24)
        line7 = Text("end for", font_size=20, weight=BOLD)
        
        # Xếp các dòng lề trái
        algo_group = VGroup(algo_title, line1, line2, line3, line4, line5, line6, line7).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # Dịch chuyển (thụt lề) SAU KHI đã arrange
        for line in [line3, line4, line5, line6]:
            line.shift(RIGHT * 0.5)
            
        bg_rect = SurroundingRectangle(algo_group, color=WHITE, fill_color=BLACK, fill_opacity=0.8, buff=0.4)
        algo_block = VGroup(bg_rect, algo_group).scale(0.9).to_edge(LEFT, buff=1.0)
        
        self.play(FadeIn(bg_rect), Write(algo_group), run_time=2.0)
        
        # Native Visualization for Spatial (Depthwise Conv)
        box_spatial = SurroundingRectangle(line3, color=RED, buff=0.1)
        self.play(Create(box_spatial), run_time=0.5)
        
        grid_3x3 = VGroup(*[Square(side_length=0.4, stroke_color=RED, fill_color=RED, fill_opacity=0.2) for _ in range(9)])
        grid_3x3.arrange_in_grid(3, 3, buff=0.05).move_to(RIGHT * 3.5 + UP * 1.5)
        center_sq = grid_3x3[4].copy().set_fill(color=RED, opacity=0.8)
        self.add(center_sq)
        arrows_in = VGroup(*[Arrow(sq.get_center(), center_sq.get_center(), buff=0.1, color=WHITE, max_stroke_width_to_length_ratio=4) for i, sq in enumerate(grid_3x3) if i != 4])
        
        spatial_desc = Text("Spatial Context\n(Depthwise Conv)", font_size=20, color=RED, weight=BOLD).next_to(grid_3x3, DOWN, buff=0.3)
        self.play(FadeIn(grid_3x3), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(arr) for arr in arrows_in], lag_ratio=0.1), Write(spatial_desc), run_time=1.5)
        self.wait(10.0)
        
        # Native Visualization for Label (Pointwise Conv)
        box_label = SurroundingRectangle(line4, color=GREEN, buff=0.1)
        self.play(Create(box_label), run_time=0.5)
        
        vocab_stack = VGroup(*[Rectangle(width=1.5, height=0.2, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.2) for _ in range(6)])
        vocab_stack.arrange(UP, buff=0.05).move_to(RIGHT * 3.5 + DOWN * 2.0)
        label_arrows = VGroup(*[Arrow(rect.get_right() + RIGHT * 0.2, rect.get_right() + LEFT * 0.1, color=WHITE, max_stroke_width_to_length_ratio=4) for rect in vocab_stack])
        
        label_desc = Text("Label Context\n(1x1 Conv)", font_size=20, color=GREEN, weight=BOLD).next_to(vocab_stack, DOWN, buff=0.3)
        self.play(FadeIn(vocab_stack), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(arr) for arr in label_arrows], lag_ratio=0.1), Write(label_desc), run_time=1.5)
        
        self.wait(26.21)

        # =======================================================
        # ⏱️ Khúc 1.4c: Visualizing Token Correction
        # =======================================================
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        self.add_sound("tts/outputs/video_03/scene3_4/3.wav")
        
        title_mrf = Text("MRFs for Fast Image Generation", font_size=40, color=BLUE).to_edge(UP, buff=0.2)
        self.play(Write(title_mrf), run_time=1.0)
        self.wait(2.0)

        # Trực quan hóa Grid Tokens
        grid1 = VGroup()
        raw_data = [[4021, 2351, 743, 408], [221, 1902, 4999, 600], [420, 8001, 6421, 1213], [7495, 2001, 121, 900]]
        for r in range(4):
            for c in range(4):
                val = raw_data[r][c]
                color = RED if val in [221, 4999, 1213, 900] else LIGHT_GREY
                sq = Square(side_length=0.6, stroke_color=WHITE, stroke_width=1)
                num = Text(str(val), font_size=12, color=color)
                grp = VGroup(sq, num).move_to(RIGHT * (c * 0.6) + DOWN * (r * 0.6))
                grid1.add(grp)
        grid1.move_to(LEFT * 4.5 + DOWN * 1.5)
        label_grid1 = Tex(r"\textbf{Imperfect token image}", font_size=24).scale(0.8).set_color(WHITE).next_to(grid1, DOWN, buff=0.2)
        
        grid2 = grid1.copy().move_to(RIGHT * 4.5 + DOWN * 1.5)
        fixes = {(1, 0): 92, (1, 2): 204, (2, 3): 789, (3, 3): 800}
        for (r, c), new_val in fixes.items():
            idx = r * 4 + c
            new_num = Text(str(new_val), font_size=12, color=GREEN).move_to(grid2[idx][1].get_center())
            grid2[idx][1].become(new_num)
        label_grid2 = Tex(r"\textbf{Fixed token image}", font_size=24).scale(0.8).set_color(WHITE).next_to(grid2, DOWN, buff=0.2)

        arrow_mrf = Line(grid1.get_right() + DOWN * 0.5, grid2.get_left() + DOWN * 0.5, color=GREY, stroke_width=6).add_tip(tip_length=0.3)
        arrow_text = Tex(r"\textbf{MRF Inference}", font_size=24).scale(0.8).set_color(GREEN).next_to(arrow_mrf, DOWN, buff=0.1)
        arrow_detok1 = Arrow(grid1.get_top(), grid1.get_top() + UP * 0.6, color=GREY, stroke_width=4)
        text_detok1 = Tex(r"\textit{Detokenization}", font_size=24).scale(0.7).set_color(GREEN).next_to(arrow_detok1, LEFT, buff=0.1)
        arrow_detok2 = Arrow(grid2.get_top(), grid2.get_top() + UP * 0.6, color=GREY, stroke_width=4)
        text_detok2 = Tex(r"\textit{Detokenization}", font_size=24).scale(0.7).set_color(GREEN).next_to(arrow_detok2, RIGHT, buff=0.1)

        opera1 = get_image_with_fallback("assets/video_03/scene3_4/opera_imperfect.png", 3.0, 2.2, "Opera\nImperfect").next_to(arrow_detok1, UP, buff=0.2)
        opera2 = get_image_with_fallback("assets/video_03/scene3_4/opera_perfect.png", 3.0, 2.2, "Opera\nPerfect").next_to(arrow_detok2, UP, buff=0.2)

        self.play(FadeIn(grid1), Write(label_grid1), run_time=1.5)
        self.wait(5.0)
        self.play(GrowArrow(arrow_detok1), Write(text_detok1), run_time=1.0)
        self.play(FadeIn(opera1), run_time=1.5)
        self.wait(10.0)
        self.play(Create(arrow_mrf), Write(arrow_text), run_time=1.0)
        self.play(TransformFromCopy(grid1, grid2), Write(label_grid2), run_time=2.0)
        self.wait(8.0)
        self.play(GrowArrow(arrow_detok2), Write(text_detok2), run_time=1.0)
        self.play(FadeIn(opera2), run_time=1.5)
        self.wait(26.76)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        self.add_sound("tts/outputs/video_03/scene3_4/4.wav")
        
        title_pipe = Text("The Hybrid Generation Pipeline", font_size=40, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(title_pipe), run_time=1.0)
        self.wait(3.0)
        
        # Box 1: Prompt
        prompt = Tex(r"\textit{Text Prompt}", font_size=28).scale(0.8).set_color(WHITE).move_to(LEFT * 5.5 + UP * 0.5)
        
        # Box 2: Transformer
        box1_rect = RoundedRectangle(width=2.2, height=1.5, corner_radius=0.2, color=WHITE)
        box1_text = Tex("Transformer", "Model", "(e.g. Muse)", font_size=26).arrange(DOWN, buff=0.1).set_color(WHITE).move_to(box1_rect.get_center())
        box1 = VGroup(box1_rect, box1_text).move_to(LEFT * 2.5 + UP * 0.5)
        
        # Image 1 (Chó Doge Imperfect) - Cắt ảnh từ slide đưa vào
        doge1 = get_image_with_fallback("assets/video_03/scene3_4/doge_imperfect.png", 2.0, 2.0, "Doge\nImperfect").move_to(ORIGIN + UP * 0.5)
        
        # Box 3: MRF
        box2_rect = RoundedRectangle(width=2.2, height=1.5, corner_radius=0.2, color=WHITE)
        box2_text = Tex("MRF Model", font_size=32).set_color(WHITE).move_to(box2_rect.get_center())
        box2 = VGroup(box2_rect, box2_text).move_to(RIGHT * 2.5 + UP * 0.5)
        
        # Image 2 (Chó Doge Perfect) - Cắt ảnh từ slide đưa vào
        doge2 = get_image_with_fallback("assets/video_03/scene3_4/doge_perfect.png", 2.0, 2.0, "Doge\nPerfect").move_to(RIGHT * 5.5 + UP * 0.5)
        
        # Arrows
        a1 = Arrow(prompt.get_right(), box1.get_left(), buff=0.1, color=WHITE)
        a2 = Arrow(box1.get_right(), doge1.get_left(), buff=0.1, color=WHITE)
        a3 = Arrow(doge1.get_right(), box2.get_left(), buff=0.1, color=WHITE)
        a4 = Arrow(box2.get_right(), doge2.get_left(), buff=0.1, color=WHITE)
        
        # Text descriptions
        desc1_1 = Tex(r"$\bullet$ The heavy-lifting is done here.", font_size=24).scale(0.8).set_color(LIGHT_GREY).next_to(box1, DOWN, buff=1.0).align_to(box1, LEFT)
        desc1_2 = Tex(r"$\bullet$ Bulky, slow model.", font_size=24).scale(0.8).set_color(LIGHT_GREY).next_to(desc1_1, DOWN, buff=0.3).align_to(box1, LEFT)
        
        desc2_1 = Tex(r"$\bullet$ Fixes the incompatible tokens.", font_size=24).scale(0.8).set_color(GREEN).next_to(box2, DOWN, buff=1.0).align_to(box2, LEFT).shift(LEFT * 0.5)
        desc2_2 = Tex(r"$\bullet$ Light-weight and super fast.", font_size=24).scale(0.8).set_color(GREEN).next_to(desc2_1, DOWN, buff=0.3).align_to(desc2_1, LEFT)
        
        self.play(FadeIn(prompt), run_time=1.0)
        self.wait(2.0)
        self.play(GrowArrow(a1), FadeIn(box1), Write(desc1_1), Write(desc1_2), run_time=1.5)
        self.wait(8.0)
        self.play(GrowArrow(a2), FadeIn(doge1), run_time=1.0)
        self.wait(8.0)
        self.play(GrowArrow(a3), FadeIn(box2), Write(desc2_1), Write(desc2_2), run_time=1.5)
        self.wait(8.0)
        self.play(GrowArrow(a4), FadeIn(doge2), run_time=1.0)
        
        self.wait(13.69)

        # =======================================================
        # ⏱️ Khúc 1.4e: Speedup Table & Bar Chart (Từ 1.4c cũ)
        # =======================================================
        
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        self.add_sound("tts/outputs/video_03/scene3_4/5.wav")
        
        title4 = Text("Blazing Fast Inference Speed", font_size=40, color=BLUE).to_edge(UP, buff=0.2)
        self.play(Write(title4), run_time=1.0)
        self.wait(3.0)
        
        # Ép height nhỏ lại (2.8) để có nhiều chỗ hơn
        pdf_table = get_image_with_fallback(
            "assets/video_03/scene3_4/pdf_table_slide26.png", 
            6.0, 2.8, 
            "From Slide 26: Speed table"
        )
        pdf_table.next_to(title4, DOWN, buff=0.3) # Neo sát bên dưới Title
        self.play(FadeIn(pdf_table), run_time=1.5)
        self.wait(10.0)
        
        # Thu nhỏ size các thành phần của Bar Chart
        bar_title = Text("Total Generation Time (ms)", font_size=20, color=WHITE)
        
        muse_label = Text("Muse", font_size=20, color=LIGHT_GREY)
        muse_bar = Rectangle(width=5.0, height=0.3, fill_color=LIGHT_GREY, fill_opacity=0.8, stroke_width=0)
        muse_val = Text("442.05 ms", font_size=16, color=WHITE)
        
        muse_group = VGroup(muse_label, muse_bar, muse_val).arrange(RIGHT, buff=0.2)
        
        markov_label = Text("MarkovGen", font_size=20, color=TEAL)
        markov_bar = Rectangle(width=3.18, height=0.3, fill_color=TEAL, fill_opacity=0.8, stroke_width=0)
        markov_val = Text("281.03 ms", font_size=16, color=WHITE)
        
        # Căn lề trái cho 2 Label
        markov_label.align_to(muse_label, RIGHT)
        markov_bar.next_to(markov_label, RIGHT, buff=0.2)
        markov_val.next_to(markov_bar, RIGHT, buff=0.2)
        
        markov_group = VGroup(markov_label, markov_bar, markov_val)
        
        bars = VGroup(muse_group, markov_group).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        chart_group = VGroup(bar_title, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        chart_group.next_to(pdf_table, DOWN, buff=0.4)
        
        self.play(Write(bar_title), run_time=1.0)
        self.play(FadeIn(muse_label), GrowFromEdge(muse_bar, LEFT), Write(muse_val), run_time=1.5)
        self.wait(2.0)
        self.play(FadeIn(markov_label), GrowFromEdge(markov_bar, LEFT), Write(markov_val), run_time=1.5)
        self.wait(5.0)
        
        speedup_text = Text("1.5x OVERALL SPEEDUP!", font_size=32, color=YELLOW, weight=BOLD)
        speedup_text.next_to(chart_group, DOWN, buff=0.4)
        
        self.play(Write(speedup_text), run_time=1.0)
        self.play(Flash(speedup_text, color=YELLOW, line_length=0.5), Wiggle(speedup_text), run_time=1.5)
        
        self.wait(22.16)
