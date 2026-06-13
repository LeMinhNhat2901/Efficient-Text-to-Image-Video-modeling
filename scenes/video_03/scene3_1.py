from manim import *
import wave
import os

def get_audio_duration(file_path):
    if not os.path.exists(file_path): return 5.0 # fallback
    with wave.open(file_path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

class Scene3_1(Scene):
    def construct(self):
        # Lưu ý: Các khoảng thời gian (wait) hiện tại đang để tạm là 2.0 giây.
        # Khi bạn gen audio (1.wav đến 3.wav) xong, tôi sẽ canh lại thời gian chuẩn sau.
        
        # =======================================================
        # ⏱️ Khúc 1: Mở đầu & Giới thiệu Speaker
        # =======================================================
        audio1 = "tts/outputs/video_03/scene3_1/1.wav"
        self.add_sound(audio1)
        dur1 = get_audio_duration(audio1)
        
        # Bắt đầu với màn hình nền đen
        # Góc trên cùng bên phải, dùng hiệu ứng FadeIn để hiện mờ ra ảnh cvpr_logo.png
        cvpr_logo = ImageMobject("assets/video_03/scene3_1/cvpr_logo.png")
        cvpr_logo.height = 1.5
        cvpr_logo.to_corner(UR)
            
            
        self.play(FadeIn(cvpr_logo), run_time=1.0)
        
        # Ở trung tâm màn hình, dùng module Text và hiệu ứng Write() để chữ tự động "đánh máy" ra tiêu đề chính
        title = Text("Efficient Text-to-Image Generation\nvia Structured Discrete Prediction", font_size=36, t2c={"Structured Discrete Prediction": BLUE})
        title.center()
        self.play(Write(title), run_time=1.5)
        
        # Ngay sau đó, dùng FadeIn(shift=UP) để đẩy dòng chữ màu vàng hoặc xanh dương từ dưới lên
        speaker = Text("Speaker: Sadeep Jayasumana", font_size=28, color=YELLOW)
        speaker.next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(speaker, shift=UP), run_time=1.0)
        
        self.wait(max(0, dur1 - 3.5))
        
        # =======================================================
        # ⏱️ Khúc 2: Phân loại các phương pháp tạo ảnh
        # =======================================================
        audio2 = "tts/outputs/video_03/scene3_1/2.wav"
        self.add_sound(audio2)
        dur2 = get_audio_duration(audio2)
        
        # Xóa toàn bộ các chữ ở Khúc 1
        self.play(FadeOut(title), FadeOut(speaker), FadeOut(cvpr_logo), run_time=1.0)
        
        # Hiện tiêu đề mới ở giữa phía trên
        methods_title = Text("Image Generation Methods", font_size=40)
        methods_title.to_edge(UP)
        self.play(Write(methods_title), run_time=1.0)
        
        # Tạo 2 cụm văn bản
        col_left = VGroup(
            Text("Diffusion models", color=BLUE, font_size=32),
            Text("- Stable Diffusion\n- Imagen\n- Dall-E 2", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)

        col_right = VGroup(
            Text("Transformer-based models", color=GREEN, font_size=32),
            Text("- Parti\n- Muse", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)

        # Gom 2 cột lại và đặt ở giữa (thu nhỏ lại để không bị tràn lề)
        columns = VGroup(col_left, col_right).arrange(RIGHT, buff=1.0).scale(0.85)
        
        # Rơi xuống lần lượt
        self.play(Write(col_left[0]), Write(col_right[0]), run_time=1.0)
        self.play(FadeIn(col_left[1], shift=DOWN*0.5), run_time=1.0)
        self.play(FadeIn(col_right[1], shift=DOWN*0.5), run_time=1.0)
        
        self.wait(max(0, dur2 - 5.0))
        
        # =======================================================
        # ⏱️ Khúc 3: Cú twist với bình chọn của Elon Musk
        # =======================================================
        audio3 = "tts/outputs/video_03/scene3_1/3.wav"
        self.add_sound(audio3)
        dur3 = get_audio_duration(audio3)
        
        # Ẩn 2 cột chữ đi để nhường toàn bộ không gian cho ảnh
        self.play(
            FadeOut(col_left),
            FadeOut(col_right),
            run_time=1.5
        )
        
        # Load ảnh Elon Musk bay ra ở giữa
        elon_img = ImageMobject("assets/video_03/scene3_1/elon_poll.png")
        elon_img.width = 7.0
            
        elon_img.move_to(DOWN * 1.0)
        self.play(GrowFromCenter(elon_img), run_time=1.5)
        
        # Highlight phần 77.4%
        highlight_box = Rectangle(width=6.6, height=0.45, color=YELLOW)
        highlight_box.move_to(elon_img.get_center() + UP * 0.05)
        
        self.play(Create(highlight_box), run_time=1.0)
        self.play(Indicate(highlight_box, color=YELLOW, scale_factor=1.1), run_time=1.5)
        
        self.wait(max(0, dur3 - 5.5))
