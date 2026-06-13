from manim import *

class Scene3_3(Scene):
    def construct(self):
        # =======================================================
        # ⏱️ Khúc 1.3a: Từ Pixel Sư tử hóa thành Đồ thị
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_3/1.wav")
        
        title = Text("Markov Random Fields (MRFs)", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title), run_time=1.0)
        
        # Bức ảnh sư tử đặt bên PHẢI (giống hệt slide)
        lion_img = ImageMobject("assets/video_03/scene3_3/lion_motivation.jpg")
        lion_img.height = 5.0
        lion_img.move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(FadeIn(lion_img), run_time=1.5)
        
        # Tạo lưới 8x8 đè lên ảnh sư tử
        rows, cols = 8, 8
        cell_w = lion_img.width / cols
        cell_h = lion_img.height / rows
        
        grid_lines = VGroup()
        for i in range(1, cols):
            x = lion_img.get_left()[0] + i * cell_w
            grid_lines.add(Line(start=[x, lion_img.get_bottom()[1], 0], end=[x, lion_img.get_top()[1], 0], color=RED, stroke_width=1.5))
        for i in range(1, rows):
            y = lion_img.get_bottom()[1] + i * cell_h
            grid_lines.add(Line(start=[lion_img.get_left()[0], y, 0], end=[lion_img.get_right()[0], y, 0], color=RED, stroke_width=1.5))
            
        # Lưới viền ngoài cùng
        grid_lines.add(SurroundingRectangle(lion_img, color=RED, stroke_width=1.5, buff=0))
        self.play(Create(grid_lines), run_time=1.5)
        
        # Tạo các Node (vòng tròn) bên trong từng ô vuông của lưới
        nodes = VGroup()
        node_dict = {}
        for r in range(rows):
            for c in range(cols):
                # Tính tọa độ tâm của từng ô
                cx = lion_img.get_left()[0] + c * cell_w + cell_w / 2
                cy = lion_img.get_top()[1] - r * cell_h - cell_h / 2
                circle = Circle(radius=min(cell_w, cell_h) * 0.4, color=BLACK, stroke_width=1.5, fill_opacity=0.3, fill_color=WHITE)
                circle.move_to([cx, cy, 0])
                nodes.add(circle)
                node_dict[(r, c)] = circle
                
        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.02), run_time=2.0)
        
        # Text bên TRÁI (giảm font size và ép sát lề trái để không đè ảnh)
        t1 = MathTex(r"\text{• Define a discrete random variable } X_i \text{ at each cell } i.", font_size=24)
        t2 = MathTex(r"\text{• Connect the random variables to form a random field.}", font_size=24)
        t3 = MathTex(r"\text{• An assignment to the random field } X_1, X_2, \dots, X_N \\ \implies \text{an image.}", font_size=24)
        
        t_group = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.5)
        t_group.shift(UP * 0.5) # Nâng lên một chút cho cân đối
        
        self.play(Write(t1), run_time=1.0)
        self.wait(10.0)
        
        self.play(Write(t2), run_time=1.0)
        self.wait(8.0)
        
        # Color specific nodes (Green, Red, Purple) như trong Slide 14
        node_green = node_dict[(2, 3)]
        node_red = node_dict[(2, 4)]
        node_purple = node_dict[(3, 4)]
        
        self.play(
            node_green.animate.set_fill(GREEN, opacity=0.8),
            node_red.animate.set_fill(RED, opacity=0.8),
            node_purple.animate.set_fill(PURPLE, opacity=0.8),
            run_time=1.0
        )
        
        # Draw edges connecting them
        edge_gr = Line(node_green.get_center(), node_red.get_center(), color=BLACK, stroke_width=5)
        edge_rp = Line(node_red.get_center(), node_purple.get_center(), color=BLACK, stroke_width=5)
        self.play(Create(edge_gr), Create(edge_rp), run_time=1.0)
        self.wait(8.0)
        
        self.play(Write(t3), run_time=1.5)
        
        domain_eq = MathTex("X_1 \\in \\{l_1, l_2, \\dots, l_L\\}", font_size=24).next_to(t_group, DOWN, buff=0.8).align_to(t_group, LEFT)
        domain_eq_n = MathTex("X_N \\in \\{l_1, l_2, \\dots, l_L\\}", font_size=24).next_to(domain_eq, DOWN, buff=0.2).align_to(t_group, LEFT)
        
        self.play(Write(domain_eq), Write(domain_eq_n), run_time=1.5)
        self.wait(12.08)
        
        # =======================================================
        # ⏱️ Khúc 1.3b: Tối ưu hóa Năng lượng
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_3/2.wav")
        
        self.play(FadeOut(t_group), FadeOut(domain_eq), FadeOut(domain_eq_n), run_time=1.0)
        
        p1 = MathTex("P(X_1=x_1, \\dots, X_N=x_N) = P(\\mathbf{X} = \\mathbf{x})", font_size=32).to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        p2 = MathTex("P(\\mathbf{X} = \\mathbf{x}) = \\frac{1}{Z} \\exp(-E(\\mathbf{x}))", font_size=36).next_to(p1, DOWN, buff=0.6).align_to(p1, LEFT)
        
        self.play(Write(p1), run_time=1.5)
        self.wait(15.0)
        self.play(Write(p2), run_time=1.5)
        self.wait(15.0)
        
        max_min = MathTex("\\text{Maximize } P(\\mathbf{X} = \\mathbf{x}) \\implies \\text{Minimize } E(\\mathbf{X} = \\mathbf{x})", font_size=28)
        max_min.next_to(p2, DOWN, buff=0.8).align_to(p1, LEFT)
        
        def_E = Text("• We now need to define E(x) such that a\nphotorealistic image will have low E(x).", font_size=20)
        def_E.next_to(max_min, DOWN, buff=0.6).align_to(p1, LEFT)
        
        self.play(Write(max_min), run_time=1.5)
        self.play(Flash(max_min, line_length=0.4, color=YELLOW), run_time=1.0)
        self.wait(12.0)
        self.play(Write(def_E), run_time=1.5)
        
        self.wait(12.99)
        
        # =======================================================
        # ⏱️ Khúc 1.3c: Phân tích Unary Cost (Nút Đỏ)
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_3/3.wav")
        
        title2 = Text("Model Formulation", font_size=40, color=BLUE).to_edge(UP)
        self.play(
            ReplacementTransform(title, title2),
            FadeOut(p1), FadeOut(p2), FadeOut(max_min), FadeOut(def_E),
            run_time=1.5
        )
        
        energy_eq = MathTex("E(\\mathbf{x}) = ", "\\text{unary\\_cost}", " + ", "\\text{pairwise\\_cost}", font_size=32)
        energy_eq.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        self.play(Write(energy_eq), run_time=1.5)
        self.wait(4.0)
        
        # Unary
        unary_box = SurroundingRectangle(energy_eq[1], color=RED, buff=0.1)
        self.play(Create(unary_box), run_time=1.0)
        
        # Chớp sáng nút đỏ trên ảnh con sư tử
        self.play(Indicate(node_red, color=YELLOW, scale_factor=2.0), run_time=1.0)
        self.wait(8.0)
        
        unary_title = Text("Unary Cost", font_size=24, color=RED).next_to(energy_eq, DOWN, buff=0.8).align_to(energy_eq, LEFT)
        unary_math = MathTex("\\bullet\\ \\text{cost}(X_i = l) = -\\text{logit}_i(l)", font_size=28)
        unary_math.next_to(unary_title, DOWN, buff=0.3).align_to(unary_title, LEFT)
        
        unary_text = Text("• You pay a penalty if your label doesn't\nagree with the classifier.", font_size=20)
        unary_text.next_to(unary_math, DOWN, buff=0.3).align_to(unary_title, LEFT)
        
        self.play(Write(unary_title), run_time=0.5)
        self.play(Write(unary_math), run_time=1.0)
        self.wait(8.0)
        self.play(Write(unary_text), run_time=1.5)
        
        self.wait(11.99)
        
        # =======================================================
        # ⏱️ Khúc 1.3d: Phân tích Pairwise Cost (Nối Đỏ - Xanh)
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_3/4.wav")
        
        pairwise_box = SurroundingRectangle(energy_eq[3], color=BLUE, buff=0.1)
        self.play(ReplacementTransform(unary_box, pairwise_box), run_time=1.0)
        
        # Chớp sáng cạnh nối
        self.play(Indicate(edge_gr, color=YELLOW, scale_factor=2.0), Indicate(edge_rp, color=YELLOW, scale_factor=2.0), run_time=1.0)
        self.wait(8.0)
        
        pairwise_title = Text("Pairwise Cost", font_size=24, color=RED).next_to(unary_text, DOWN, buff=0.8).align_to(unary_title, LEFT)
        pairwise_math = MathTex("\\bullet\\ \\text{cost}(X_i = l', X_j = l'') = -c(l', l'')s(i,j)", font_size=28)
        pairwise_math.next_to(pairwise_title, DOWN, buff=0.3).align_to(unary_title, LEFT)
        
        pairwise_text = Text("• You pay a penalty if you assign \"incompatible\"\nlabels to two \"neighboring\" pixels.", font_size=20)
        pairwise_text.next_to(pairwise_math, DOWN, buff=0.3).align_to(unary_title, LEFT)
        
        self.play(Write(pairwise_title), run_time=0.5)
        self.play(Write(pairwise_math), run_time=1.0)
        self.wait(10.0)
        self.play(Write(pairwise_text), run_time=1.5)
        
        self.wait(25.63)
        
        # =======================================================
        # ⏱️ Khúc 1.3e: So sánh với Semantic Segmentation
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_3/5.wav")
        
        self.play(
            FadeOut(energy_eq), FadeOut(pairwise_box), 
            FadeOut(unary_title), FadeOut(unary_math), FadeOut(unary_text),
            FadeOut(pairwise_title), FadeOut(pairwise_math), FadeOut(pairwise_text),
            run_time=1.5
        )
        
        diff_title = Text("Difference Compared to Semantic Segmentation", font_size=36, color=BLUE).to_edge(UP)
        self.play(ReplacementTransform(title2, diff_title), run_time=1.0)
        
        # Tạo hiệu ứng fully connected: vẽ mũi tên cong với góc nhỏ để không bị lồi ra khỏi ảnh sư tử
        import random
        fc_edges = VGroup()
        node_list = list(nodes)
        for _ in range(30):
            n1 = random.choice(node_list)
            n2 = random.choice(node_list)
            if n1 != n2:
                # Góc cong nhỏ (0.2) giúp các đường đan xen gọn gàng bên trong ảnh
                edge = CurvedArrow(n1.get_center(), n2.get_center(), angle=0.2, color=YELLOW, stroke_width=1.5, stroke_opacity=0.6, tip_length=0.1)
                fc_edges.add(edge)
                
        # Bullets bên TRÁI ép lề
        b1 = Text("• The graph is truly fully-connected.", font_size=24, t2c={"fully-connected": RED})
        sub1 = Text("→ Every token influences every other token", font_size=18, color=LIGHT_GREY)
        
        b2 = Text("• Spatial relationships are not fixed.", font_size=24)
        sub2 = Text("→ Computed via Transformer Self-Attention", font_size=18, color=LIGHT_GREY)
        
        b3 = Text("• Label compatibilities are not fixed.", font_size=24)
        sub3 = Text("→ Dynamically driven by the Text Prompt", font_size=18, color=LIGHT_GREY)
        
        group1 = VGroup(b1, sub1).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        group2 = VGroup(b2, sub2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        group3 = VGroup(b3, sub3).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        bullets = VGroup(group1, group2, group3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets.to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        
        self.play(Write(b1), run_time=1.0)
        self.play(Write(sub1), run_time=1.0)
        
        # Hiện mũi tên fully connected
        self.play(LaggedStart(*[Create(e) for e in fc_edges], lag_ratio=0.05), run_time=2.0)
        self.wait(20.0)
        
        self.play(Write(b2), run_time=1.0)
        self.play(Write(sub2), run_time=1.0)
        self.wait(15.0)
        
        self.play(Write(b3), run_time=1.0)
        self.play(Write(sub3), run_time=1.0)
        
        self.wait(19.23)
