from manim import *


def staggered_fade_in(mobs, lag_ratio=0.08, shift=0.12 * DOWN, run_time=1.0):
    return LaggedStart(
        *[FadeIn(mob, shift=shift) for mob in mobs],
        lag_ratio=lag_ratio,
        run_time=run_time,
    )


def dim_all_except(mobs, keep, opacity=0.22):
    return AnimationGroup(
        *[mob.animate.set_opacity(1.0 if mob in keep else opacity) for mob in mobs],
        lag_ratio=0,
    )

