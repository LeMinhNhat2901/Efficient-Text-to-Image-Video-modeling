from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class MarkovChainScene(DiffusionScene):
    TARGET_DURATION = 121.46

    def construct(self):
        start = self.time
        self.add_background_texture("textures/dark_grid.jpg", "textures/dark_grid.png", opacity=0.03)
        title = self.scene_title(
            "The Markov Property",
            "Long stochastic paths become local transitions",
        )
        self.play(FadeIn(title, shift=0.18 * DOWN), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(title), run_time=0.8)

        self.forward_equation_intro()
        self.markov_chain_highlight()
        self.joint_distribution()
        self.hold_to_time(start, self.TARGET_DURATION)

    def forward_equation_intro(self):
        question = self.hook_question("The forward equation hides a local rule.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)

        eq = self.display_equation(
            r"X_t=\alpha_tX_{t-1}+\sqrt{\beta_t}\,G",
            width=7.2,
            size=40,
            accent=ACCENT_2,
        ).move_to([0, 0.98, 0])
        prev_box = self.soft_box(2.15, 0.72, color=ACCENT, fill_opacity=0.055, stroke_opacity=0.7)
        prev_label = self.eq(r"X_{t-1}", size=34, color=ACCENT).move_to(prev_box)
        now_box = self.soft_box(2.15, 0.72, color=ACCENT_2, fill_opacity=0.055, stroke_opacity=0.7)
        now_label = self.eq(r"X_t", size=34, color=ACCENT_2).move_to(now_box)
        local = VGroup(
            VGroup(prev_box, prev_label),
            Arrow(LEFT, RIGHT, color=MUTED, stroke_width=4),
            VGroup(now_box, now_label),
        ).arrange(RIGHT, buff=0.34).move_to([0, -0.25, 0])
        old_history = VGroup(
            self.eq(r"X_0", size=25, color=MUTED),
            self.eq(r"X_1", size=25, color=MUTED),
            self.eq(r"\cdots", size=25, color=MUTED),
            self.eq(r"X_{t-2}", size=25, color=MUTED),
        ).arrange(RIGHT, buff=0.36).next_to(local[0], LEFT, buff=0.62)
        no_direct = Cross(old_history, stroke_color=RED, stroke_width=4).set_opacity(0.8)
        caption = self.label("use the previous state, not the whole history", SMALL_SIZE, MUTED)
        caption.next_to(local, DOWN, buff=0.28)

        self.play(FadeIn(eq, shift=0.08 * UP), run_time=1.2)
        self.play(FadeIn(local), FadeIn(caption), run_time=1.1)
        self.wait(5.2)
        self.play(FadeIn(old_history), Create(no_direct), run_time=1.0)
        self.wait(6.8)

        maze = self.robot_maze().scale(0.9).move_to([0, -0.15, 0])
        speech = VGroup(
            self.label("Where am I now?", SMALL_SIZE, TEXT),
            self.label("Let me move from here.", SMALL_SIZE, ACCENT_2),
        ).arrange(DOWN, buff=0.12)
        bubble = self.soft_box(width=max(3.3, speech.width + 0.45), height=speech.height + 0.34, color=ACCENT_2, fill_opacity=0.06)
        speech.move_to(bubble)
        bubble_group = VGroup(bubble, speech).next_to(maze, RIGHT, buff=0.55).shift(0.18 * UP)
        self.play(FadeOut(VGroup(eq, local, old_history, no_direct, caption)), FadeIn(maze), run_time=1.2)
        self.wait(2.5)
        self.play(FadeIn(bubble_group, shift=0.08 * UP), run_time=0.8)
        self.wait(10.5)

        markov = self.takeaway("Markov property: current state summarizes what matters.", ACCENT_2, width=9.8)
        markov.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(markov, shift=0.08 * UP), run_time=0.8)
        self.wait(2.9)
        self.play(FadeOut(VGroup(question, maze, bubble_group, markov)), run_time=0.8)

    def coin_toss_intuition(self):
        question = self.hook_question("What does it mean for the next step to be random?")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)

        coin = VGroup(
            Circle(radius=0.7, stroke_width=5, color=ACCENT_2, fill_color=ACCENT_2, fill_opacity=0.12),
            self.label("H", 44, ACCENT_2, font=FONT_TITLE),
        )
        coin.move_to([0, 0.75, 0])
        ground = Line([-2.2, -1.1, 0], [2.2, -1.1, 0], color=DIM, stroke_width=2)
        self.play(FadeIn(coin, scale=0.85), Create(ground), run_time=0.8)
        self.play(coin.animate.shift(1.0 * UP), Rotate(coin, TAU), rate_func=there_and_back, run_time=1.8)
        self.play(coin.animate.move_to([0, -0.35, 0]), run_time=0.7)
        self.wait(4.5)

        steps = [0, 1, 0, 1, 2, 1, 2]
        labels = ["H", "T", "H", "H", "T", "H"]
        path_points = [np.array([-3.0 + i * 1.0, -0.35 + 0.35 * y, 0]) for i, y in enumerate(steps)]
        walk = VMobject(color=ACCENT_2, stroke_width=3)
        walk.set_points_as_corners(path_points)
        decision_labels = VGroup(
            *[
                self.label(label, 16, ACCENT_2 if label == "H" else MUTED).move_to(path_points[i + 1] + 0.28 * UP)
                for i, label in enumerate(labels)
            ]
        )
        path_note = self.label("coin decisions create a state path", SMALL_SIZE, TEXT).next_to(walk, DOWN, buff=0.28)
        self.play(coin.animate.scale(0.55).to_corner(UL, buff=0.55), Create(walk), FadeIn(decision_labels), FadeIn(path_note), run_time=2.0)
        self.wait(4.0)

        state_nodes = VGroup(*[self.chain_node(r"s_" + str(i), color=ACCENT_2) for i in range(4)])
        state_nodes.arrange(RIGHT, buff=0.46).move_to([0, -1.75, 0])
        state_arrows = VGroup(*[self.small_arrow(state_nodes[i], state_nodes[i + 1], ACCENT_2) for i in range(3)])
        transition_note = self.label("coin decisions become local state transitions", SMALL_SIZE, ACCENT_2)
        transition_note.next_to(state_nodes, DOWN, buff=0.22)
        self.play(
            path_note.animate.set_opacity(0.25),
            LaggedStart(*[FadeIn(node, shift=0.06 * UP) for node in state_nodes], lag_ratio=0.08),
            LaggedStart(*[GrowArrow(arrow) for arrow in state_arrows], lag_ratio=0.1),
            FadeIn(transition_note),
            run_time=1.8,
        )
        self.wait(4.0)

        past = VGroup(
            self.concept_card("past tosses", "heads, tails, heads...", MUTED, width=3.5),
            self.concept_card("current toss", "new random outcome", ACCENT_2, width=3.5),
        ).arrange(RIGHT, buff=0.8).move_to([0, 1.1, 0])
        independence = self.label("The current toss does not directly depend on the whole history.", BODY_SIZE, TEXT)
        independence.to_edge(DOWN, buff=0.62)
        self.play(
            FadeOut(VGroup(coin, walk, decision_labels, path_note, state_nodes, state_arrows, transition_note)),
            FadeIn(past),
            FadeIn(independence),
            run_time=1.2,
        )
        self.wait(9.0)
        self.play(FadeOut(VGroup(question, past, independence, ground)), run_time=1.0)

    def markov_chain_highlight(self):
        question = VGroup(
            self.label("For diffusion,", SECTION_SIZE, TEXT, font=FONT_TITLE),
            self.eq(r"X_t", size=SECTION_SIZE + 2),
            self.label("is computed from", SECTION_SIZE, TEXT, font=FONT_TITLE),
            self.eq(r"X_{t-1}", size=SECTION_SIZE + 2),
            self.label(".", SECTION_SIZE, TEXT, font=FONT_TITLE),
        ).arrange(RIGHT, buff=0.16)
        question.to_edge(UP, buff=0.42)
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)

        portrait = None
        portrait_path = self.first_asset("images/markov_portrait.jpg", "images/markov_portrait.png")
        if portrait_path is not None:
            image = self.framed_image(portrait_path, width=0.84, height=1.08, color=MUTED, fill_opacity=0.02)
            image.to_edge(LEFT, buff=0.48).shift(1.42 * DOWN)
            caption = VGroup(
                self.label("Andrey Markov", 13, MUTED),
                self.label("local dependence", 12, DIM),
            ).arrange(DOWN, buff=0.04).next_to(image, DOWN, buff=0.12)
            portrait = Group(image, caption)

        tex = [r"x_0", r"x_1", r"\cdots", r"x_{t-1}", r"x_t", r"x_{t+1}"]
        nodes = VGroup(*[self.chain_node(item) for item in tex]).arrange(RIGHT, buff=0.54).move_to([0, 0.9, 0])
        arrows = VGroup(*[self.small_arrow(nodes[i], nodes[i + 1], MUTED) for i in range(len(nodes) - 1)])
        intro = [
            FadeIn(nodes),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.08),
        ]
        if portrait is not None:
            intro.append(FadeIn(portrait, shift=0.06 * UP))
        self.play(*intro, run_time=1.8)
        self.wait(1.1)

        formula = self.display_equation(
            r"p(x_t\mid x_0,\ldots,x_{t-1})=p(x_t\mid x_{t-1})",
            width=8.3,
            size=34,
            accent=ACCENT_2,
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(formula, shift=0.12 * UP), run_time=1.0)
        self.wait(27.0)

        focus_arrow = arrows[3]
        focus_box = self.soft_box(width=2.35, height=1.05, color=ACCENT_2, fill_opacity=0.045, stroke_opacity=0.86)
        focus_box.move_to(VGroup(nodes[3], nodes[4]))
        particle = Dot(nodes[3].get_center(), radius=0.07, color=ACCENT_2)
        beam = Line(nodes[3].get_right(), nodes[4].get_left(), color=ACCENT_2, stroke_width=8).set_opacity(0.48)
        beam_glow = Line(nodes[3].get_right(), nodes[4].get_left(), color=TEXT, stroke_width=2.3)
        memory_wall = self.memory_wall().move_to(
            [
                (nodes[2].get_right()[0] + nodes[3].get_left()[0]) / 2,
                nodes[2].get_y() + 2.2,
                0,
            ]
        )
        past = VGroup(nodes[0], nodes[1], nodes[2], arrows[0], arrows[1], arrows[2])
        future = VGroup(nodes[5], arrows[4])
        note = self.label(
            "The previous state summarizes the past.",
            SMALL_SIZE,
            MUTED,
        )
        note.next_to(focus_box, DOWN, buff=0.28)
        self.play(
            past.animate.set_opacity(0.15),
            future.animate.set_opacity(0.18),
            focus_arrow.animate.set_color(ACCENT_2).set_stroke(width=6),
            FadeIn(particle),
            memory_wall.animate.shift(1.05 * DOWN),
            Create(beam),
            Create(beam_glow),
            Create(focus_box),
            FadeIn(note),
            run_time=1.8,
        )
        self.play(particle.animate.move_to(nodes[4].get_center()), run_time=1.2)
        self.wait(5.5)
        outro = Group(question, nodes, arrows, focus_box, formula, particle, beam, beam_glow, memory_wall, note)
        if portrait is not None:
            outro.add(portrait)
        self.play(FadeOut(outro), run_time=0.8)

    def joint_distribution(self):
        question = self.hook_question("This local rule simplifies the whole path.")
        self.play(FadeIn(question, shift=0.12 * DOWN), run_time=1.0)

        chain = VGroup(*[self.chain_node(tex) for tex in [r"x_0", r"x_1", r"x_2", r"\cdots", r"x_T"]]).arrange(RIGHT, buff=0.58)
        chain.move_to([0, 1.05, 0])
        arrows = VGroup(*[self.small_arrow(chain[i], chain[i + 1], GREEN) for i in range(4)])
        self.play(FadeIn(chain), LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.08), run_time=1.4)
        self.wait(4.0)

        blocks = VGroup()
        labels = [
            (r"p(x_0)", "start"),
            (r"p(x_1\mid x_0)", "step 1"),
            (r"p(x_2\mid x_1)", "step 2"),
            (r"\cdots", "more steps"),
            (r"p(x_T\mid x_{T-1})", "last step"),
        ]
        for i, (tex, cap) in enumerate(labels):
            box = self.soft_box(2.06, 0.86, color=GREEN, fill_opacity=0.045, stroke_opacity=0.62)
            eq = self.fit_to_box(self.eq(tex, size=25), 1.62, 0.33)
            caption = self.label(cap, 13, MUTED)
            content = VGroup(eq, caption).arrange(DOWN, buff=0.08).move_to(box)
            item = VGroup(box, content).move_to([-4.25 + 2.13 * i, -0.62, 0])
            blocks.add(item)

        self.play(LaggedStart(*[FadeIn(block, shift=0.1 * UP) for block in blocks], lag_ratio=0.1), run_time=1.8)
        self.wait(7.0)

        joint = self.display_equation(
            r"p(x_{0:T})=p(x_0)\prod_{t=1}^{T}p(x_t\mid x_{t-1})",
            width=7.3,
            size=34,
            accent=GREEN,
        ).to_edge(DOWN, buff=0.42)
        self.play(FadeIn(joint, shift=0.12 * UP), run_time=1.0)
        self.wait(12.0)

        take = self.takeaway("Tiny transitions replace one impossible leap.", GREEN)
        take.next_to(joint, UP, buff=0.18)
        self.play(FadeIn(take, shift=0.08 * UP), run_time=0.8)
        self.wait(9.0)
        self.play(FadeOut(VGroup(question, chain, arrows, blocks, joint, take)), run_time=0.8)

    def robot_maze(self) -> VGroup:
        grid = VGroup()
        for i in range(6):
            grid.add(Line([-2.1 + i * 0.7, -1.4, 0], [-2.1 + i * 0.7, 1.4, 0], color=DIM, stroke_width=1.0))
        for j in range(5):
            grid.add(Line([-2.1, -1.4 + j * 0.7, 0], [1.4, -1.4 + j * 0.7, 0], color=DIM, stroke_width=1.0))
        walls = VGroup(
            Line([-1.4, 0.0, 0], [0.7, 0.0, 0], color=MUTED, stroke_width=5),
            Line([-0.7, -1.4, 0], [-0.7, -0.35, 0], color=MUTED, stroke_width=5),
            Line([0.7, 0.7, 0], [1.4, 0.7, 0], color=MUTED, stroke_width=5),
        )
        fog = VGroup(*[
            Circle(radius=0.32 + 0.07 * i, color=MUTED, stroke_width=1.0, stroke_opacity=0.12).shift((i - 2) * 0.52 * RIGHT + 0.2 * np.sin(i) * UP)
            for i in range(5)
        ])
        robot = VGroup(
            RoundedRectangle(width=0.42, height=0.34, corner_radius=0.08, color=ACCENT_2, stroke_width=2.2, fill_color=ACCENT_2, fill_opacity=0.18),
            Dot(radius=0.035, color=TEXT).shift(0.08 * LEFT + 0.04 * UP),
            Dot(radius=0.035, color=TEXT).shift(0.08 * RIGHT + 0.04 * UP),
            Line([-0.1, -0.07, 0], [0.1, -0.07, 0], color=TEXT, stroke_width=1.5),
        ).move_to([-1.75, -1.05, 0])
        path = VMobject(color=ACCENT_2, stroke_width=3)
        path.set_points_as_corners([
            np.array([-1.75, -1.05, 0]),
            np.array([-1.05, -1.05, 0]),
            np.array([-1.05, -0.35, 0]),
            np.array([-0.35, -0.35, 0]),
        ])
        current_dot = Dot(robot.get_center(), radius=0.055, color=ACCENT_2)
        return VGroup(grid, fog, walls, path, current_dot, robot)

    def memory_wall(self) -> VGroup:
        wall = VGroup()
        colors = ["#6B4B3E", "#7B5545", "#5E4238"]
        for row in range(3):
            for col in range(4):
                brick = RoundedRectangle(
                    width=0.32,
                    height=0.16,
                    corner_radius=0.025,
                    stroke_width=0.5,
                    stroke_color=DIM,
                    fill_color=colors[(row + col) % len(colors)],
                    fill_opacity=0.82,
                )
                brick.move_to([(col - 1.5) * 0.34 + (0.17 if row % 2 else 0), (row - 1) * 0.18, 0])
                wall.add(brick)
        label = self.label("far past", 12, MUTED).next_to(wall, DOWN, buff=0.08)
        return VGroup(wall, label)
