from pathlib import Path
import sys

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from base_scene import DiffusionScene
from config import *


class ReverseMarkovChain(DiffusionScene):
    def construct(self):
        title = self.scene_title("Act III: Reverse Markov chain", "Can we model the path from noise back to data?")
        self.play(FadeIn(title, shift=0.2 * DOWN), run_time=MED)

        self.reverse_question()
        self.bayes_inversion()
        self.inverse_gaussian_form()

    def reverse_question(self):
        forward_nodes = VGroup(*[self.chain_node(tex) for tex in [r"x_0", r"x_1", r"x_2", r"x_T"]]).arrange(RIGHT, buff=0.7)
        forward_nodes.move_to([0, 1.15, 0])
        forward_arrows = VGroup(*[self.small_arrow(forward_nodes[i], forward_nodes[i + 1], ACCENT) for i in range(3)])
        forward_label = self.label("Forward: designed corruption", SMALL_SIZE, ACCENT).next_to(forward_nodes, UP, buff=0.35)

        reverse_nodes = VGroup(*[self.chain_node(tex, color=GREEN) for tex in [r"x_T", r"x_{T-1}", r"x_{T-2}", r"x_0"]]).arrange(RIGHT, buff=0.7)
        reverse_nodes.move_to([0, -0.85, 0])
        reverse_arrows = VGroup(*[self.small_arrow(reverse_nodes[i], reverse_nodes[i + 1], GREEN) for i in range(3)])
        reverse_label = self.label("Reverse: learned denoising", SMALL_SIZE, GREEN).next_to(reverse_nodes, UP, buff=0.35)

        question = self.label("Does a Markov chain have a useful reverse chain?", BODY_SIZE, TEXT).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(forward_label), FadeIn(forward_nodes), LaggedStart(*[GrowArrow(a) for a in forward_arrows], lag_ratio=0.12), run_time=MED)
        self.play(FadeIn(reverse_label), FadeIn(reverse_nodes), LaggedStart(*[GrowArrow(a) for a in reverse_arrows], lag_ratio=0.12), run_time=MED)
        self.play(FadeIn(question, shift=0.12 * UP), run_time=MED)
        self.wait(0.45)
        self.play(FadeOut(VGroup(forward_nodes, forward_arrows, forward_label, reverse_nodes, reverse_arrows, reverse_label, question)), run_time=MED)

    def bayes_inversion(self):
        tag = self.top_left_tag("Bayes inversion", ACCENT_2)
        bayes = self.display_equation(
            r"p(x_{t-1}\mid x_t)=\frac{p(x_t\mid x_{t-1})p(x_{t-1})}{p(x_t)}",
            plain="p(x_{t-1} | x_t) = p(x_t | x_{t-1}) p(x_{t-1}) / p(x_t)",
            width=8.25,
            size=32,
            accent=ACCENT_2,
        ).move_to([0, 1.15, 0])

        left = self.soft_box(3.2, 1.15, color=ACCENT, fill_opacity=0.055).move_to([-3.0, -0.65, 0])
        right = self.soft_box(3.2, 1.15, color=RED, fill_opacity=0.045).move_to([3.0, -0.65, 0])
        known = VGroup(
            self.label("known transition", SMALL_SIZE, ACCENT),
            self.fit_to_box(self.eq(r"p(x_t\mid x_{t-1})", size=26, plain="p(x_t | x_{t-1})"), 2.35, 0.42),
        ).arrange(DOWN, buff=0.18).move_to(left)
        hard = VGroup(
            self.label("hard marginal", SMALL_SIZE, RED),
            self.fit_to_box(self.eq(r"p(x_t)", size=26, plain="p(x_t)"), 1.3, 0.42),
        ).arrange(DOWN, buff=0.18).move_to(right)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.38, color=MUTED, stroke_width=3)
        note = self.label("The formula is exact; using it directly is usually not practical.", SMALL_SIZE, MUTED).to_edge(DOWN, buff=0.58)

        self.play(FadeIn(tag), FadeIn(bayes, shift=0.12 * DOWN), run_time=MED)
        self.play(FadeIn(left), FadeIn(right), FadeIn(known), FadeIn(hard), GrowArrow(arrow), FadeIn(note), run_time=MED)
        self.wait(0.65)
        self.play(FadeOut(VGroup(tag, bayes, left, right, known, hard, arrow, note)), run_time=MED)

    def inverse_gaussian_form(self):
        tag = self.top_left_tag("Approximate inverse conditional", GREEN)
        xt = self.noisy_sample(0.72, scale=0.8, seed=80).move_to([-3.5, 0.5, 0])
        previous_cloud = self.gaussian_cloud(count=95, width=1.3, height=0.95, seed=81, color=GREEN).move_to([0.0, 0.5, 0])
        mean = Dot(previous_cloud.get_center() + 0.16 * RIGHT, radius=0.075, color=ACCENT_2)
        sample = self.noisy_sample(0.42, scale=0.8, seed=82).move_to([3.5, 0.5, 0])
        arrows = VGroup(
            Arrow(xt.get_right(), previous_cloud.get_left(), buff=0.28, color=GREEN, stroke_width=4),
            Arrow(previous_cloud.get_right(), sample.get_left(), buff=0.28, color=GREEN, stroke_width=4),
        )
        labels = VGroup(
            self.compact_eq(r"x_t", size=28, plain="x_t").next_to(xt, DOWN, buff=0.2),
            self.label("possible previous states", SMALL_SIZE, MUTED).next_to(previous_cloud, DOWN, buff=0.2),
            self.compact_eq(r"x_{t-1}", size=28, plain="x_{t-1}").next_to(sample, DOWN, buff=0.2),
        )
        eq = self.display_equation(
            r"p_\theta(x_{t-1}\mid x_t)=\mathcal{N}\left(\mu_\theta(x_t,t),\Sigma_\theta(x_t,t)\right)",
            plain="p_theta(x_{t-1} | x_t) = N(mu_theta(x_t,t), Sigma_theta(x_t,t))",
            width=8.6,
            size=30,
            accent=GREEN,
        ).to_edge(DOWN, buff=0.45)
        mean_label = self.label("learned mean", SMALL_SIZE, ACCENT_2).next_to(mean, UP, buff=0.18)

        self.play(FadeIn(tag), FadeIn(xt), FadeIn(labels[0]), run_time=FAST)
        self.play(GrowArrow(arrows[0]), FadeIn(previous_cloud), FadeIn(mean), FadeIn(mean_label), FadeIn(labels[1]), run_time=MED)
        self.play(GrowArrow(arrows[1]), FadeIn(sample), FadeIn(labels[2]), FadeIn(eq, shift=0.12 * UP), run_time=MED)
        caution = self.label("Gaussian here is a practical approximation, not a universal exact law.", SMALL_SIZE, MUTED)
        caution.next_to(eq, UP, buff=0.22)
        self.play(FadeIn(caution), run_time=FAST)
        self.wait(0.7)
