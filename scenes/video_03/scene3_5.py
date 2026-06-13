from manim import *
import os

def get_image_with_fallback(path, fallback_width, fallback_height, fallback_text):
    if os.path.exists(path):
        img = ImageMobject(path)
        img.height = fallback_height # Force height to ensure uniformity
        return img
    else:
        rect = Rectangle(width=fallback_width, height=fallback_height, fill_color=DARK_GRAY, fill_opacity=0.8, color=WHITE)
        label = Text(f"[Image Missing]\n{fallback_text}\nPath: {path}", font_size=16, color=WHITE).move_to(rect.get_center())
        return Group(rect, label)

class Scene3_5(Scene):
    def safe_add_sound(self, file_path):
        if os.path.exists(file_path):
            self.add_sound(file_path)
        else:
            print(f"Warning: Audio file {file_path} not found. Skipping audio insertion.")

    def construct(self):
        # =======================================================
        # ⏱️ AUDIO 1: Corgi Bad
        # Script: "While we have established that MarkovGen is significantly faster, you might be wondering: does this speed come at the cost of generation quality? The answer is a resounding no. In fact, it's the exact opposite. Let's look at some qualitative results. When we observe standard accelerated generation methods like the Early Exit Muse, we often encounter glaring visual artifacts. Notice how the eye of this corgi in the first step is visibly distorted and unnatural."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/1.wav")
        
        title = Text("Qualitative Results: Step-by-step Quality", font_size=36, color=BLUE).to_edge(UP, buff=0.2)
        self.play(Write(title), run_time=1.0)
        self.wait(1.0)
        
        doge_muse = get_image_with_fallback("assets/video_03/scene3_5/doge_muse_row.png", 10.0, 2.5, "Doge\nEarly Exit Muse").move_to(UP * 1.5 + RIGHT * 0.5)
        doge_mrf = get_image_with_fallback("assets/video_03/scene3_5/doge_mrf_row.png", 10.0, 2.5, "Doge\nMarkovGen").move_to(DOWN * 1.5 + RIGHT * 0.5)
        
        label_muse = Text("Early Exit Muse", font_size=20, color=RED).rotate(PI/2).next_to(doge_muse, LEFT, buff=0.4)
        label_mrf = Text("MarkovGen", font_size=20, color=GREEN).rotate(PI/2).next_to(doge_mrf, LEFT, buff=0.4)
        
        self.play(FadeIn(doge_muse), Write(label_muse), run_time=1.5)
        
        w_doge = doge_muse.width
        center_step1 = doge_muse.get_left() + RIGHT * (w_doge / 8)
        center_step3 = doge_muse.get_left() + RIGHT * (w_doge * 5 / 8)
        
        face_bad = Circle(radius=w_doge/12, color=RED, stroke_width=4).move_to(center_step1 + UP * 0.2)
        wall_bad = Rectangle(width=w_doge/5, height=doge_muse.height/3, color=RED, stroke_width=4).move_to(center_step3 + UP * 0.8)
        
        self.play(Create(face_bad), Create(wall_bad), run_time=1.5)
        self.wait(24.9) # Wait for Audio 1
        
        # =======================================================
        # ⏱️ AUDIO 2: Corgi Good
        # Script: "Furthermore, if we examine the background, the wall textures are highly inconsistent across the generation steps. Now, let's compare this to MarkovGen. By employing our novel continuous-time Markov Chain framework and iterative message passing, MarkovGen perfectly preserves these crucial structural details. The eye is rendered sharply, and the background texture remains highly consistent."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/2.wav")
        
        self.play(FadeIn(doge_mrf), Write(label_mrf), run_time=1.0)
        
        center_step1_good = doge_mrf.get_left() + RIGHT * (w_doge / 8)
        center_step3_good = doge_mrf.get_left() + RIGHT * (w_doge * 5 / 8)
        
        face_good = Circle(radius=w_doge/12, color=GREEN, stroke_width=4).move_to(center_step1_good + UP * 0.2)
        wall_good = Rectangle(width=w_doge/5, height=doge_mrf.height/3, color=GREEN, stroke_width=4).move_to(center_step3_good + UP * 0.8)
        
        fix_arrow1 = Arrow(face_bad.get_bottom(), face_good.get_top(), buff=0.1, color=YELLOW)
        fix_arrow2 = Arrow(wall_bad.get_bottom(), wall_good.get_top(), buff=0.1, color=YELLOW)
        
        self.play(GrowArrow(fix_arrow1), Create(face_good), GrowArrow(fix_arrow2), Create(wall_good), run_time=1.5)
        self.wait(23.4) # Wait for Audio 2
        
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.5
        )
        
        # =======================================================
        # ⏱️ AUDIO 3: Robot/Rabbits Bad
        # Script: "This superior performance is not just an isolated case; it extends consistently across various complex scenes. When we look at broader evaluation sets, such as these detailed robotic figures or the intricate clothing on these rabbits, the limitations of previous methods become even more apparent. The Early Exit Muse model suffers from a severe loss of structural integrity, producing blurry and ill-defined outputs when forced to generate quickly."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/3.wav")
        
        robot_set = get_image_with_fallback("assets/video_03/scene3_5/robot_set.png", 10.0, 2.5, "Robot\nSet").move_to(UP * 1.5)
        rabbit_set = get_image_with_fallback("assets/video_03/scene3_5/rabbit_set.png", 10.0, 2.5, "Rabbit\nSet").move_to(DOWN * 1.5)
        
        self.play(FadeIn(robot_set), FadeIn(rabbit_set), run_time=1.5)
        
        w_robot = robot_set.width
        w_rabbit = rabbit_set.width
        
        box_mid_robot = Rectangle(width=w_robot/3.1, height=robot_set.height, color=RED, stroke_width=4).move_to(robot_set.get_center())
        box_mid_rabbit = Rectangle(width=w_rabbit/3.1, height=rabbit_set.height, color=RED, stroke_width=4).move_to(rabbit_set.get_center())
        
        # Fix text overlap: Put text_blur on top, not down, or center it between images
        text_blur = Text("Loss of structural integrity", font_size=20, color=RED, weight=BOLD).move_to(ORIGIN)
        self.play(Create(box_mid_robot), Create(box_mid_rabbit), Write(text_blur), run_time=1.0)
        self.wait(25.7) # Wait for Audio 3
        
        # FadeOut the RED text and RED boxes BEFORE showing GREEN
        self.play(FadeOut(text_blur), FadeOut(box_mid_robot), FadeOut(box_mid_rabbit), run_time=1.0)

        # =======================================================
        # ⏱️ AUDIO 4: Robot/Rabbits Good
        # Script: "In stark contrast, MarkovGen effortlessly maintains enhanced sharpness, high fidelity, and correct structural proportions. And here is the most impressive part: it achieves this stunning level of detail while still being 1.5 times faster than the full, uncompressed Muse model. We are getting the best of both worlds: unprecedented speed without compromising an ounce of visual quality."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/4.wav")

        center_right_robot = robot_set.get_right() + LEFT * (w_robot / 6)
        center_right_rabbit = rabbit_set.get_right() + LEFT * (w_rabbit / 6)
        
        box_right_robot = Rectangle(width=w_robot/3.1, height=robot_set.height, color=GREEN, stroke_width=4).move_to(center_right_robot)
        box_right_rabbit = Rectangle(width=w_rabbit/3.1, height=rabbit_set.height, color=GREEN, stroke_width=4).move_to(center_right_rabbit)
        
        text_sharp = Text("Enhanced sharpness & structure", font_size=20, color=GREEN, weight=BOLD).move_to(ORIGIN)
        
        self.play(Create(box_right_robot), Create(box_right_rabbit), Write(text_sharp), run_time=1.5)
        
        speedup_tag = Text("1.5x Faster vs Full Muse!", font_size=24, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.3)
        self.play(Write(speedup_tag), Flash(speedup_tag, color=YELLOW, line_length=0.3), run_time=1.0)
        self.wait(24.2) # Wait for Audio 4
        
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != title],
            run_time=1.5
        )
        
        # =======================================================
        # ⏱️ AUDIO 5: Porsche/Teddy
        # Script: "We observe the exact same pattern when dealing with highly structured geometric shapes or complex lighting scenarios. Take a look at this vintage Porsche and the illuminated Teddy Bear. While the baseline model struggles, creating wavy, broken brick walls and fuzzy ghosting artifacts around the bear's edges, MarkovGen easily corrects these issues, delivering crisp, flawless images that look completely natural."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/5.wav")
        
        porsche_muse = get_image_with_fallback("assets/video_03/scene3_5/porsche_muse.png", 3.5, 2.5, "Porsche\nMuse").move_to(LEFT * 3.0 + UP * 1.5)
        porsche_mrf = get_image_with_fallback("assets/video_03/scene3_5/porsche_mrf.png", 3.5, 2.5, "Porsche\nMarkovGen").move_to(LEFT * 3.0 + DOWN * 1.5)
        teddy_muse = get_image_with_fallback("assets/video_03/scene3_5/teddy_muse.png", 3.5, 2.5, "Teddy\nMuse").move_to(RIGHT * 3.0 + UP * 1.5)
        teddy_mrf = get_image_with_fallback("assets/video_03/scene3_5/teddy_mrf.png", 3.5, 2.5, "Teddy\nMarkovGen").move_to(RIGHT * 3.0 + DOWN * 1.5)
        
        self.play(FadeIn(porsche_muse), FadeIn(teddy_muse), run_time=1.5)
        
        wall_artifact = Rectangle(width=porsche_muse.width*0.8, height=porsche_muse.height*0.3, color=RED).move_to(porsche_muse.get_top() + DOWN * (porsche_muse.height*0.2))
        teddy_artifact = Circle(radius=teddy_muse.width*0.3, color=RED).move_to(teddy_muse.get_top() + DOWN * (teddy_muse.height*0.35))
        
        self.play(Create(wall_artifact), Create(teddy_artifact), run_time=1.0)
        
        self.play(FadeIn(porsche_mrf), FadeIn(teddy_mrf), run_time=1.0)
        
        wall_fixed = Rectangle(width=porsche_mrf.width*0.8, height=porsche_mrf.height*0.3, color=GREEN).move_to(porsche_mrf.get_top() + DOWN * (porsche_mrf.height*0.2))
        teddy_fixed = Circle(radius=teddy_mrf.width*0.3, color=GREEN).move_to(teddy_mrf.get_top() + DOWN * (teddy_mrf.height*0.35))
        
        arr_porsche = CurvedArrow(wall_artifact.get_bottom(), wall_fixed.get_top(), angle=TAU/4, color=YELLOW)
        arr_teddy = CurvedArrow(teddy_artifact.get_bottom(), teddy_fixed.get_top(), angle=-TAU/4, color=YELLOW)
        
        self.play(Create(arr_porsche), Create(arr_teddy), Create(wall_fixed), Create(teddy_fixed), run_time=1.5)
        self.wait(21.7) # Wait for Audio 5
        
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        
        # =======================================================
        # ⏱️ AUDIO 6: Bar Charts (Group 1 & 2)
        # Script: "Finally, let's examine the quantitative results. In a side-by-side comparison, human raters overwhelmingly prefer images generated by MarkovGen. When compared against the Early Exit Muse, MarkovGen wins a staggering 98.3 percent of the time. Even more impressively, when pitted against the much heavier Full Muse model, MarkovGen still dominates with an 85.6 percent preference rate."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/6.wav")
        
        title_quant = Text("Quantitative Results", font_size=40, color=BLUE).to_edge(UP, buff=0.2)
        self.play(Write(title_quant), run_time=1.0)
        
        # X-range covers 3 groups
        axes = Axes(
            x_range=[0, 16, 1],
            y_range=[0, 100, 20],
            x_length=12,
            y_length=4.5,
            axis_config={"color": WHITE, "include_numbers": False},
        ).move_to(DOWN * 0.5)
        
        y_label = Text("Percentage", font_size=16).next_to(axes.y_axis, UP).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.1)
        self.play(Create(axes), Write(y_label), run_time=1.5)
        
        # Hàm vẽ stacked bar chuẩn paper
        def create_stacked_bar(x_pos, percentage, label_text, color_dark="#2A0080", color_light="#8A9AFA"):
            total_h = axes.c2p(0, max(percentage, 1.0))[1] - axes.c2p(0, 0)[1]
            dark_h = total_h * 0.9 if percentage > 5 else total_h
            light_h = total_h - dark_h
            
            dark_bar = Rectangle(width=1.0, height=dark_h, fill_color=color_dark, fill_opacity=1, stroke_width=0)
            dark_bar.move_to(axes.c2p(x_pos, 0), aligned_edge=DOWN)
            
            light_bar = Rectangle(width=1.0, height=max(light_h, 0.01), fill_color=color_light, fill_opacity=1, stroke_width=0)
            light_bar.next_to(dark_bar, UP, buff=0)
            
            val_txt = Text(f"{percentage}%", font_size=18, weight=BOLD).next_to(light_bar, UP, buff=0.1)
            lbl_txt = Text(label_text, font_size=12).next_to(axes.c2p(x_pos, 0), DOWN, buff=0.2)
            
            return Group(dark_bar, light_bar, val_txt, lbl_txt)
        
        # Legend - moved to top right corner completely outside the chart
        leg_box = Rectangle(width=2.5, height=1.5, color=WHITE, stroke_width=1).to_corner(UR, buff=0.5)
        leg_title = Text("Preferred by\n# of raters", font_size=12).move_to(leg_box.get_top() + DOWN*0.4)
        leg_c1 = Square(side_length=0.2, fill_color="#8A9AFA", fill_opacity=1, stroke_width=0).next_to(leg_title, DOWN, buff=0.2).align_to(leg_title, LEFT)
        leg_t1 = Text("2/3", font_size=12).next_to(leg_c1, RIGHT, buff=0.2)
        leg_c2 = Square(side_length=0.2, fill_color="#2A0080", fill_opacity=1, stroke_width=0).next_to(leg_c1, DOWN, buff=0.2)
        leg_t2 = Text("3/3", font_size=12).next_to(leg_c2, RIGHT, buff=0.2)
        legend = Group(leg_box, leg_title, leg_c1, leg_t1, leg_c2, leg_t2)
        
        self.play(FadeIn(legend), run_time=1.0)
        
        # Group 1
        g1_b1 = create_stacked_bar(2.0, 98.3, "Markov-\nGen")
        g1_b2 = create_stacked_bar(3.5, 1.4, "Early\nExit\nMuse")
        self.play(GrowFromEdge(g1_b1[0], DOWN), GrowFromEdge(g1_b1[1], DOWN), Write(g1_b1[2]), Write(g1_b1[3]), run_time=1.0)
        self.play(GrowFromEdge(g1_b2[0], DOWN), GrowFromEdge(g1_b2[1], DOWN), Write(g1_b2[2]), Write(g1_b2[3]), run_time=0.5)
        
        # Group 2
        g2_b1 = create_stacked_bar(7.5, 85.6, "Markov-\nGen")
        g2_b2 = create_stacked_bar(9.0, 13.4, "Full\nMuse")
        self.play(GrowFromEdge(g2_b1[0], DOWN), GrowFromEdge(g2_b1[1], DOWN), Write(g2_b1[2]), Write(g2_b1[3]), run_time=1.0)
        self.play(Flash(g2_b1[2], color=YELLOW), Wiggle(g2_b1[2]), run_time=0.5)
        self.play(GrowFromEdge(g2_b2[0], DOWN), GrowFromEdge(g2_b2[1], DOWN), Write(g2_b2[2]), Write(g2_b2[3]), run_time=0.5)
        
        self.wait(23.8) # Wait for Audio 6
        
        # =======================================================
        # ⏱️ AUDIO 7: Bar Charts (Group 3)
        # Script: "The chart also reveals that Full Muse heavily beats Early Exit Muse at 92.5 percent, highlighting just how severe the quality drop is in standard early exiting. By contrast, MarkovGen achieves superior quality while retaining the speed benefits."
        # =======================================================
        self.safe_add_sound("tts/outputs/video_03/scene3_5/7.wav")
        
        # Group 3
        g3_b1 = create_stacked_bar(13.0, 92.5, "Full\nMuse")
        g3_b2 = create_stacked_bar(14.5, 6.9, "Early\nExit\nMuse")
        self.play(GrowFromEdge(g3_b1[0], DOWN), GrowFromEdge(g3_b1[1], DOWN), Write(g3_b1[2]), Write(g3_b1[3]), run_time=1.0)
        self.play(GrowFromEdge(g3_b2[0], DOWN), GrowFromEdge(g3_b2[1], DOWN), Write(g3_b2[2]), Write(g3_b2[3]), run_time=0.5)
        
        self.wait(16.9) # Wait for Audio 7
