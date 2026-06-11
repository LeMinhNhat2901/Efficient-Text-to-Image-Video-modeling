from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCENES = [
    ("scenes/s00_roadmap.py", "RoadmapOverview"),
    ("scenes/s01_forward_ou_wiener.py", "ForwardOUWiener"),
    ("scenes/s02_markov.py", "MarkovChainScene"),
    ("scenes/s03_reverse_chain.py", "ReverseMarkovChain"),
    ("scenes/s04_score_compass.py", "ScoreCompassScene"),
    ("scenes/s05_local_linear.py", "LocalLinearScoreScene"),
    ("scenes/s06_mse_conditional_mean.py", "MSEConditionalMeanScene"),
    ("scenes/s07_training_loop.py", "TrainingLoopScene"),
    ("scenes/s08_sde_drift_diffusion.py", "ContinuousTimeFlowScene"),
    ("scenes/s09_probability_flow_ode.py", "DriftDiffusionScene"),
    ("scenes/s10_fokker_planck_score.py", "FokkerPlanckScoreScene"),
    ("scenes/s11_reverse_distribution.py", "ReverseDistributionScene"),
    ("scenes/s12_runge_kutta_solver.py", "RungeKuttaSolverScene"),
    ("scenes/s13_finale_failure.py", "FinaleFailureScene"),
]

QUALITY_DIRS = {
    "-ql": "480p15",
    "-qm": "720p30",
    "-qh": "1080p60",
}

AUDIO_SCENES = {
    "RoadmapOverview": ("s00", Path("tts") / "outputs" / "s00_roadmap.wav"),
    "ForwardOUWiener": ("s01", Path("tts") / "outputs" / "s01_forward_ou_wiener.wav"),
    "MarkovChainScene": ("s02", Path("tts") / "outputs" / "s02_markov.wav"),
    "ReverseMarkovChain": ("s03", Path("tts") / "outputs" / "s03_reverse_chain.wav"),
    "ScoreCompassScene": ("s04", Path("tts") / "outputs" / "s04_score_compass.wav"),
    "LocalLinearScoreScene": ("s05", Path("tts") / "outputs" / "s05_local_linear.wav"),
    "MSEConditionalMeanScene": ("s06", Path("tts") / "outputs" / "s06_mse_conditional_mean.wav"),
    "TrainingLoopScene": ("s07", Path("tts") / "outputs" / "s07_training_loop.wav"),
    "ContinuousTimeFlowScene": ("s08", Path("tts") / "outputs" / "s08_sde_drift_diffusion.wav"),
    "DriftDiffusionScene": ("s09", Path("tts") / "outputs" / "s09_probability_flow_ode.wav"),
    "FokkerPlanckScoreScene": ("s10", Path("tts") / "outputs" / "s10_fokker_planck_score.wav"),
    "ReverseDistributionScene": ("s11", Path("tts") / "outputs" / "s11_reverse_distribution.wav"),
    "RungeKuttaSolverScene": ("s12", Path("tts") / "outputs" / "s12_runge_kutta_solver.wav"),
    "FinaleFailureScene": ("s13", Path("tts") / "outputs" / "s13_finale_failure.wav"),
}


def main() -> None:
    project_root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Render prototype diffusion Manim scenes.")
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

    selected = [item for item in SCENES if args.scene in (None, item[1])]
    if not selected:
        names = ", ".join(name for _, name in SCENES)
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
