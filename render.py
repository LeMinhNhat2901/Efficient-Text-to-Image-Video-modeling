from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


VIDEO1_SCENES = [
    ("scenes/video_01/s00_roadmap.py", "RoadmapOverview"),
    ("scenes/video_01/s01_forward_ou_wiener.py", "ForwardOUWiener"),
    ("scenes/video_01/s02_markov.py", "MarkovChainScene"),
    ("scenes/video_01/s03_reverse_chain.py", "ReverseMarkovChain"),
    ("scenes/video_01/s04_score_compass.py", "ScoreCompassScene"),
    ("scenes/video_01/s05_local_linear.py", "LocalLinearScoreScene"),
    ("scenes/video_01/s06_mse_conditional_mean.py", "MSEConditionalMeanScene"),
    ("scenes/video_01/s07_training_loop.py", "TrainingLoopScene"),
    ("scenes/video_01/s08_sde_drift_diffusion.py", "ContinuousTimeFlowScene"),
    ("scenes/video_01/s09_probability_flow_ode.py", "DriftDiffusionScene"),
    ("scenes/video_01/s10_fokker_planck_score.py", "FokkerPlanckScoreScene"),
    ("scenes/video_01/s11_reverse_distribution.py", "ReverseDistributionScene"),
    ("scenes/video_01/s12_runge_kutta_solver.py", "RungeKuttaSolverScene"),
    ("scenes/video_01/s13_finale_failure.py", "FinaleFailureScene"),
]

VIDEO2_SCENES = [
    ("scenes/video_02/s00_text_pixels_opening.py", "V02TextPixelsOpening"),
    ("scenes/video_02/s01_generative_backbones.py", "V02GenerativeBackbones"),
    ("scenes/video_02/s02_clip_coembedding.py", "V02ClipCoEmbedding"),
    ("scenes/video_02/s03_vqgan_visual_words.py", "V02VqganVisualWords"),
    ("scenes/video_02/s04_architecture_evolution.py", "V02ArchitectureEvolution"),
    ("scenes/video_02/s05_muse_markovgen.py", "V02MuseMarkovgen"),
    ("scenes/video_02/s06_diffusion_intuition.py", "V02DiffusionIntuition"),
    ("scenes/video_02/s07_diffusion_math.py", "V02DiffusionMath"),
    ("scenes/video_02/s08_guidance.py", "V02Guidance"),
    ("scenes/video_02/s09_latent_diffusion_crf.py", "V02LatentDiffusionCRF"),
    ("scenes/video_02/s10_sana_var.py", "V02SanaVar"),
    ("scenes/video_02/s11_discussion_finale.py", "V02DiscussionFinale"),
]

SCENE_GROUPS = {
    "1": VIDEO1_SCENES,
    "2": VIDEO2_SCENES,
    "all": VIDEO1_SCENES + VIDEO2_SCENES,
}

QUALITY_DIRS = {
    "-ql": "480p15",
    "-qm": "720p30",
    "-qh": "1080p60",
}

AUDIO_SCENES = {
    "RoadmapOverview": ("s00", Path("tts") / "outputs" / "video_01" / "s00_roadmap.wav"),
    "ForwardOUWiener": ("s01", Path("tts") / "outputs" / "video_01" / "s01_forward_ou_wiener.wav"),
    "MarkovChainScene": ("s02", Path("tts") / "outputs" / "video_01" / "s02_markov.wav"),
    "ReverseMarkovChain": ("s03", Path("tts") / "outputs" / "video_01" / "s03_reverse_chain.wav"),
    "ScoreCompassScene": ("s04", Path("tts") / "outputs" / "video_01" / "s04_score_compass.wav"),
    "LocalLinearScoreScene": ("s05", Path("tts") / "outputs" / "video_01" / "s05_local_linear.wav"),
    "MSEConditionalMeanScene": ("s06", Path("tts") / "outputs" / "video_01" / "s06_mse_conditional_mean.wav"),
    "TrainingLoopScene": ("s07", Path("tts") / "outputs" / "video_01" / "s07_training_loop.wav"),
    "ContinuousTimeFlowScene": ("s08", Path("tts") / "outputs" / "video_01" / "s08_sde_drift_diffusion.wav"),
    "DriftDiffusionScene": ("s09", Path("tts") / "outputs" / "video_01" / "s09_probability_flow_ode.wav"),
    "FokkerPlanckScoreScene": ("s10", Path("tts") / "outputs" / "video_01" / "s10_fokker_planck_score.wav"),
    "ReverseDistributionScene": ("s11", Path("tts") / "outputs" / "video_01" / "s11_reverse_distribution.wav"),
    "RungeKuttaSolverScene": ("s12", Path("tts") / "outputs" / "video_01" / "s12_runge_kutta_solver.wav"),
    "FinaleFailureScene": ("s13", Path("tts") / "outputs" / "video_01" / "s13_finale_failure.wav"),
    "V02TextPixelsOpening": ("v02_s00", Path("tts") / "outputs" / "video_02" / "s00_text_pixels_opening.wav"),
    "V02GenerativeBackbones": ("v02_s01", Path("tts") / "outputs" / "video_02" / "s01_generative_backbones.wav"),
    "V02ClipCoEmbedding": ("v02_s02", Path("tts") / "outputs" / "video_02" / "s02_clip_coembedding.wav"),
    "V02VqganVisualWords": ("v02_s03", Path("tts") / "outputs" / "video_02" / "s03_vqgan_visual_words.wav"),
    "V02ArchitectureEvolution": ("v02_s04", Path("tts") / "outputs" / "video_02" / "s04_architecture_evolution.wav"),
    "V02MuseMarkovgen": ("v02_s05", Path("tts") / "outputs" / "video_02" / "s05_muse_markovgen.wav"),
    "V02DiffusionIntuition": ("v02_s06", Path("tts") / "outputs" / "video_02" / "s06_diffusion_intuition.wav"),
    "V02DiffusionMath": ("v02_s07", Path("tts") / "outputs" / "video_02" / "s07_diffusion_math.wav"),
    "V02Guidance": ("v02_s08", Path("tts") / "outputs" / "video_02" / "s08_guidance.wav"),
    "V02LatentDiffusionCRF": ("v02_s09", Path("tts") / "outputs" / "video_02" / "s09_latent_diffusion_crf.wav"),
    "V02SanaVar": ("v02_s10", Path("tts") / "outputs" / "video_02" / "s10_sana_var.wav"),
    "V02DiscussionFinale": ("v02_s11", Path("tts") / "outputs" / "video_02" / "s11_discussion_finale.wav"),
}


def main() -> None:
    project_root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Render Manim scenes for the video series.")
    quality_group = parser.add_mutually_exclusive_group()
    quality_group.add_argument("-ql", dest="quality_flag", action="store_const", const="-ql", help="Low quality preview.")
    quality_group.add_argument("-qm", dest="quality_flag", action="store_const", const="-qm", help="Medium quality check.")
    quality_group.add_argument("-qh", dest="quality_flag", action="store_const", const="-qh", help="High quality final render.")
    quality_group.add_argument(
        "--quality",
        choices=["ql", "qm", "qh", "low", "medium", "high"],
        help="Quality name. Use ql/qm/qh or low/medium/high.",
    )
    parser.add_argument("--disable-caching", action="store_true", help="Pass Manim's --disable_caching flag.")
    parser.add_argument("--scene", help="Render one scene class by name.")
    parser.add_argument(
        "--video",
        choices=["1", "2", "all"],
        default="1",
        help="Render all scenes for a video. Ignored when --scene is supplied.",
    )
    args = parser.parse_args()
    quality_map = {
        None: "-ql",
        "ql": "-ql",
        "qm": "-qm",
        "qh": "-qh",
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh",
    }
    quality_flag = args.quality_flag or quality_map[args.quality]

    scene_pool = SCENE_GROUPS["all"] if args.scene else SCENE_GROUPS[args.video]
    selected = [item for item in scene_pool if args.scene in (None, item[1])]
    if not selected:
        names = ", ".join(name for _, name in SCENE_GROUPS["all"])
        raise SystemExit(f"Unknown scene. Available: {names}")

    for file_name, scene_name in selected:
        cmd = [sys.executable, "-m", "manim", quality_flag, file_name, scene_name]
        if args.disable_caching:
            cmd.insert(4, "--disable_caching")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True, cwd=project_root)

        audio_scene = AUDIO_SCENES.get(scene_name)
        if audio_scene is None:
            continue
        scene_key, audio_path = audio_scene
        if not (project_root / audio_path).exists():
            print(f"audio missing for {scene_name}: {audio_path}")
            continue
        mux_cmd = [
            sys.executable,
            "scripts/mux_scene_audio.py",
            "--scene",
            scene_key,
            "--quality-dir",
            QUALITY_DIRS[quality_flag],
            "--audio",
            str(audio_path),
            "--replace",
        ]
        print(" ".join(mux_cmd))
        subprocess.run(mux_cmd, check=True, cwd=project_root)


if __name__ == "__main__":
    main()
