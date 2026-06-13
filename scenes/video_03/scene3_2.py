from manim import *

class Scene3_2(Scene):
    def construct(self):
        # Lưu ý: Các khoảng thời gian (wait) hiện tại đang để tạm là 2.0 giây.
        # Khi bạn gen audio (1.wav đến 4.wav) xong, tôi sẽ canh lại thời gian chuẩn sau.
        
        # =======================================================
        # ⏱️ Khúc 1.2a: Vấn đề của phương pháp cũ
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_2/1.wav")
        
        # Tiêu đề nhỏ ở góc trên
        title1 = Text("The Limitation of Independent Prediction", font_size=36, color=RED).to_edge(UP)
        self.play(Write(title1), run_time=1.0)
        
        # Ảnh tree_noisy.png
        try:
            tree_img = ImageMobject("assets/video_03/scene3_2/tree_noisy.png")
            tree_img.height = 4.0
        except:
            # Fallback nếu chưa có ảnh
            tree_img = Rectangle(width=6.0, height=4.0, color=WHITE, fill_opacity=0.2)
            tree_text = Text("[tree_noisy.png]", font_size=24).move_to(tree_img)
            tree_img = Group(tree_img, tree_text)
            
        tree_img.move_to(ORIGIN)
        self.play(FadeIn(tree_img), run_time=1.5)
        
        # Khung đỏ khoanh viền nhiễu
        # Tạm thời khoanh một vùng nhỏ ở giữa (giả sử là ranh giới bầu trời và cây)
        noisy_area = Rectangle(width=2.0, height=1.5, color=RED, stroke_width=4)
        noisy_area.move_to(tree_img.get_center() + UP * 0.5)
        
        self.play(Create(noisy_area), run_time=1.0)
        self.play(Indicate(noisy_area, color=RED, scale_factor=1.2), run_time=1.5)
        
        # Dòng chữ giải thích
        limitation_text = Text("Independent pixel classification → Noisy results", font_size=28)
        limitation_text.next_to(tree_img, DOWN, buff=0.5)
        self.play(Write(limitation_text), run_time=1.5)
        
        self.wait(19.70)
        
        # =======================================================
        # ⏱️ Khúc 1.2b: Hình ảnh Sư tử & Token hóa
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_2/2.wav")
        
        self.play(
            FadeOut(tree_img), FadeOut(noisy_area), FadeOut(limitation_text),
            run_time=1.5
        )
        
        title2 = Text("Motivation: The Combinatorial Explosion", font_size=40, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        
        lion_img = ImageMobject("assets/video_03/scene3_2/lion_motivation.jpg")
        lion_img.height = 4.5
        lion_img.move_to(RIGHT * 1.5) # Để chừa không gian bên trái cho Vocab size
        
        self.play(GrowFromCenter(lion_img), run_time=1.5)
        
        # Vẽ lưới lên con sư tử
        lines = VGroup()
        for i in range(1, 16):
            x = lion_img.get_left()[0] + i * (lion_img.width / 16)
            lines.add(Line(start=[x, lion_img.get_bottom()[1], 0], end=[x, lion_img.get_top()[1], 0], color=GRAY, stroke_width=1.5))
            y = lion_img.get_bottom()[1] + i * (lion_img.height / 16)
            lines.add(Line(start=[lion_img.get_left()[0], y, 0], end=[lion_img.get_right()[0], y, 0], color=GRAY, stroke_width=1.5))
            
        self.play(Create(lines), run_time=2.0)
        
        lion_group = Group(lion_img, lines)
        
        # Vocab size bên trái
        vocab_text = MathTex(r"\text{Vocab size} = 8192", color=YELLOW, font_size=36)
        vocab_text.to_edge(LEFT, buff=1.0)
        
        self.play(Write(vocab_text), run_time=1.0)
        self.play(Flash(vocab_text, line_length=0.3, color=YELLOW), run_time=1.0)
        
        self.wait(17.35)
        
        # =======================================================
        # ⏱️ Khúc 1.2c: Sự bùng nổ tổ hợp
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_2/3.wav")
        
        # Đẩy sư tử sang mép trái
        self.play(
            lion_group.animate.scale(0.6).to_edge(LEFT, buff=0.5),
            FadeOut(vocab_text),
            run_time=1.5
        )
        
        # Cài đặt biến các công thức toán học
        eq1 = MathTex("2 \\times 2 \\text{ patch} \\rightarrow \\mathcal{O}(10^{15})", font_size=36)
        eq2 = MathTex("3 \\times 3 \\text{ patch} \\rightarrow \\mathcal{O}(10^{35})", font_size=36)
        eq3 = MathTex("16 \\times 16 \\text{ patch} \\rightarrow \\mathcal{O}(10^{1002})", font_size=48)
        eq3.set_color(RED)
        
        eq_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        eq_group.next_to(lion_group, RIGHT, buff=1.5)
        
        # Anim mượt mà: Dòng trên rớt xuống dòng dưới
        self.play(Write(eq1), run_time=1.0)
        self.wait(1.0)
        
        self.play(ReplacementTransform(eq1.copy(), eq2), run_time=1.0)
        self.wait(1.0)
        
        self.play(ReplacementTransform(eq2.copy(), eq3), run_time=1.5)
        
        # Hiệu ứng Wiggle + Chớp sáng cho O(10^1002)
        bg_flash = FullScreenRectangle(color=WHITE, fill_opacity=0.2)
        self.play(
            FadeIn(bg_flash, run_time=0.1),
            Wiggle(eq3, scale_value=1.3, run_time=2.0)
        )
        self.play(FadeOut(bg_flash, run_time=0.5))
        
        self.wait(20.74)
        
        # =======================================================
        # ⏱️ Khúc 1.2d: Câu hỏi định hướng
        # =======================================================
        self.add_sound("tts/outputs/video_03/scene3_2/4.wav")
        
        # Ẩn hoàn toàn ảnh và toán học để màn hình trống, tránh bị đè chữ
        self.play(
            FadeOut(lion_group),
            FadeOut(eq_group),
            run_time=1.5
        )
        
        bullet1 = Text("• Only a small subset of token arrangements will be valid", font_size=32)
        bullet2 = Text("• Highly confident tokens should influence nearby tokens", font_size=32)
        bullets = VGroup(bullet1, bullet2).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        bullets.move_to(UP * 1.0)
        
        self.play(Write(bullet1), run_time=1.5)
        self.wait(6.5)
        self.play(Write(bullet2), run_time=1.5)
        self.wait(8.0)
        
        # Câu hỏi bự màu vàng
        question = Text("How to make it efficient & accurate?", font_size=48, color=YELLOW, weight=BOLD)
        q_box = SurroundingRectangle(question, color=YELLOW, fill_opacity=0.1, buff=0.4)
        q_group = VGroup(q_box, question).next_to(bullets, DOWN, buff=1.5)
        
        self.play(DrawBorderThenFill(q_box), Write(question), run_time=1.5)
        self.play(Flash(question, line_length=0.4, color=YELLOW), run_time=1.5)
        
        self.wait(3.46)
