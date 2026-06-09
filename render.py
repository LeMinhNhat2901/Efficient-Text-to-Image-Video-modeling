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
]


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


if __name__ == "__main__":
    main()
