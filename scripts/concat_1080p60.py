"""concat_1080p60.py — concatenate high-quality 1080p60 rendered scenes.

Supports Video 1 (Diffusion Prototype) and Video 2 (Text-to-Pixels Journey).
Uses ffmpeg when available, falls back to PyAV/libx264 otherwise.

Usage examples:
    # Concat Video 1 only  (default)
    python scripts/concat_1080p60.py

    # Concat Video 2 only
    python scripts/concat_1080p60.py --video 2

    # Concat both videos into one file
    python scripts/concat_1080p60.py --video all

    # Seamless join (no gap between scenes)
    python scripts/concat_1080p60.py --no-gap

    # Custom output path
    python scripts/concat_1080p60.py --output out/MyVideo.mp4
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import av
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import BG  # noqa: E402  (must come after sys.path update)

# ──────────────────────────────────────────────────────────────────────────────
# Scene lists (scene_folder_name, rendered_filename)
# The final path is:  media/videos/<folder>/1080p60/<filename>.mp4
# ──────────────────────────────────────────────────────────────────────────────

VIDEO1_SCENES: list[tuple[str, str]] = [
    ("s00_roadmap",                "RoadmapOverview"),
    ("s01_forward_ou_wiener",      "ForwardOUWiener"),
    ("s02_markov",                 "MarkovChainScene"),
    ("s03_reverse_chain",          "ReverseMarkovChain"),
    ("s04_score_compass",          "ScoreCompassScene"),
    ("s05_local_linear",           "LocalLinearScoreScene"),
    ("s06_mse_conditional_mean",   "MSEConditionalMeanScene"),
    ("s07_training_loop",          "TrainingLoopScene"),
    ("s08_sde_drift_diffusion",    "ContinuousTimeFlowScene"),
    ("s09_probability_flow_ode",   "DriftDiffusionScene"),
    ("s10_fokker_planck_score",    "FokkerPlanckScoreScene"),
    ("s11_reverse_distribution",   "ReverseDistributionScene"),
    ("s12_runge_kutta_solver",     "RungeKuttaSolverScene"),
    ("s13_finale_failure",         "FinaleFailureScene"),
]

VIDEO2_SCENES: list[tuple[str, str]] = [
    ("v02_s00_text_pixels_opening",    "V02TextPixelsOpening"),
    ("v02_s01_generative_backbones",   "V02GenerativeBackbones"),
    ("v02_s02_clip_coembedding",       "V02ClipCoEmbedding"),
    ("v02_s03_vqgan_visual_words",     "V02VqganVisualWords"),
    ("v02_s04_architecture_evolution", "V02ArchitectureEvolution"),
    ("v02_s05_muse_markovgen",         "V02MuseMarkovgen"),
    ("v02_s06_diffusion_intuition",    "V02DiffusionIntuition"),
    ("v02_s07_diffusion_math",         "V02DiffusionMath"),
    ("v02_s08_guidance",               "V02Guidance"),
    ("v02_s09_latent_diffusion_crf",    "V02LatentDiffusionCRF"),
    ("v02_s10_sana_var",               "V02SanaVar"),
    ("v02_s11_discussion_finale",       "V02DiscussionFinale"),
]

QUALITY = "1080p60"
FPS = 60
GAP_SECONDS_DEFAULT = 0.5  # black gap between scenes (seconds)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _scene_path(folder: str, filename: str) -> Path:
    return ROOT / "media" / "videos" / folder / QUALITY / f"{filename}.mp4"


def _resolve_scenes(video: str) -> list[Path]:
    if video == "1":
        pairs = VIDEO1_SCENES
    elif video == "2":
        pairs = VIDEO2_SCENES
    else:  # "all"
        pairs = VIDEO1_SCENES + VIDEO2_SCENES
    return [_scene_path(folder, fname) for folder, fname in pairs]


def _default_output(video: str) -> Path:
    if video == "1":
        name = "Video1_DiffusionPrototype_1080p60.mp4"
    elif video == "2":
        name = "Video2_TextToPixels_1080p60.mp4"
    else:
        name = "FullVideo_1080p60.mp4"
    out_dir = ROOT / "media" / "videos" / "full_1080p60"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / name


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return tuple(int(text[i: i + 2], 16) for i in (0, 2, 4))


def _video_info(path: Path) -> tuple[int, int]:
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        return stream.codec_context.width, stream.codec_context.height


def _find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    env_root = Path(sys.executable).resolve().parents[1]
    candidate = env_root / "Library" / "bin" / "ffmpeg.exe"
    if candidate.exists():
        return str(candidate)
    return None


def _manifest_line(path: Path) -> str:
    value = path.resolve().as_posix().replace("'", r"'\''")
    return f"file '{value}'"


def _write_manifest(manifest_path: Path, out_path: Path, scenes: list[Path]) -> None:
    manifest_path.write_text(
        "\n".join([
            f"Output: {out_path.name}",
            f"Quality: {QUALITY}",
            f"Scenes ({len(scenes)}):",
            *[f"  {p}" for p in scenes],
        ]),
        encoding="utf-8",
    )
    print(f"Manifest written → {manifest_path}")


# ──────────────────────────────────────────────────────────────────────────────
# ffmpeg backend (preferred)
# ──────────────────────────────────────────────────────────────────────────────

def _concat_with_ffmpeg(
    ffmpeg: str,
    scenes: list[Path],
    out_path: Path,
    gap_seconds: float,
) -> None:
    width, height = _video_info(scenes[0])

    with tempfile.TemporaryDirectory(prefix="concat_1080p60_") as tmp:
        tmp_dir = Path(tmp)
        gap = tmp_dir / "gap.mp4"
        concat_list = tmp_dir / "concat_list.txt"

        if gap_seconds > 0:
            subprocess.run(
                [
                    ffmpeg, "-y",
                    "-f", "lavfi",
                    "-i", f"color=c=0x{BG.lstrip('#')}:s={width}x{height}:r={FPS}:d={gap_seconds}",
                    "-an",
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-preset", "veryfast",
                    "-crf", "18",
                    str(gap),
                ],
                check=True,
            )

        entries: list[str] = []
        for index, scene in enumerate(scenes):
            entries.append(_manifest_line(scene))
            if gap_seconds > 0 and index < len(scenes) - 1:
                entries.append(_manifest_line(gap))
        concat_list.write_text("\n".join(entries), encoding="utf-8")

        subprocess.run(
            [
                ffmpeg, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list),
                "-an",
                "-r", str(FPS),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "slow",      # higher quality for final 1080p60
                "-crf", "18",           # visually lossless for 1080p60
                "-movflags", "+faststart",
                str(out_path),
            ],
            check=True,
        )


# ──────────────────────────────────────────────────────────────────────────────
# PyAV fallback backend
# ──────────────────────────────────────────────────────────────────────────────

def _encode_frame(
    stream: av.video.stream.VideoStream,
    output: av.container.OutputContainer,
    frame: av.VideoFrame,
    pts: int,
) -> None:
    frame.pts = pts
    frame.time_base = Fraction(1, FPS)
    for packet in stream.encode(frame):
        output.mux(packet)


def _concat_with_pyav(
    scenes: list[Path],
    out_path: Path,
    gap_seconds: float,
) -> None:
    width, height = _video_info(scenes[0])

    output = av.open(str(out_path), mode="w")
    stream = output.add_stream("libx264", rate=FPS)
    stream.width = width
    stream.height = height
    stream.pix_fmt = "yuv420p"
    stream.bit_rate = 16_000_000   # ~16 Mbps for crisp 1080p60
    stream.time_base = Fraction(1, FPS)
    stream.options = {"preset": "slow", "crf": "18"}

    bg_rgb = np.array(_hex_to_rgb(BG), dtype=np.uint8)
    black = np.tile(bg_rgb, (height, width, 1))
    gap_frames = max(1, round(FPS * gap_seconds)) if gap_seconds > 0 else 0
    pts = 0

    for scene_index, input_path in enumerate(scenes):
        print(f"  [{scene_index + 1}/{len(scenes)}] Muxing {input_path.name} …")
        with av.open(str(input_path)) as container:
            for frame in container.decode(video=0):
                frame = frame.reformat(width=width, height=height, format="yuv420p")
                _encode_frame(stream, output, frame, pts)
                pts += 1

        if gap_frames > 0 and scene_index < len(scenes) - 1:
            for _ in range(gap_frames):
                frame = av.VideoFrame.from_ndarray(black, format="rgb24")
                frame = frame.reformat(format="yuv420p")
                _encode_frame(stream, output, frame, pts)
                pts += 1

    for packet in stream.encode():
        output.mux(packet)
    output.close()


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate 1080p60 rendered Manim scenes into one MP4.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--video",
        choices=["1", "2", "all"],
        default="1",
        help="Which video to concat: 1 (Video 1), 2 (Video 2), or all (both). Default: 1",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output MP4 path. If omitted, auto-selected under media/videos/full_1080p60/.",
    )
    parser.add_argument(
        "--gap",
        type=float,
        default=GAP_SECONDS_DEFAULT,
        metavar="SECONDS",
        help=f"Black gap between scenes in seconds. Default: {GAP_SECONDS_DEFAULT}",
    )
    parser.add_argument(
        "--no-gap",
        action="store_true",
        help="Disable the black gap between scenes (seamless join).",
    )
    args = parser.parse_args()

    gap_seconds = 0.0 if args.no_gap else args.gap
    scenes = _resolve_scenes(args.video)
    out_path = args.output or _default_output(args.video)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Validate that all files exist before starting
    missing = [str(p) for p in scenes if not p.exists()]
    if missing:
        print("ERROR — Missing rendered scene(s):")
        for m in missing:
            print(f"  {m}")
        raise SystemExit(1)

    print(f"Concatenating {len(scenes)} scene(s) → {out_path}")
    print(f"Gap between scenes: {gap_seconds}s  |  Quality: {QUALITY}  |  FPS: {FPS}")

    ffmpeg = _find_ffmpeg()
    if ffmpeg:
        try:
            _concat_with_ffmpeg(ffmpeg, scenes, out_path, gap_seconds)
            method = f"ffmpeg ({ffmpeg})"
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"ffmpeg failed → falling back to PyAV: {exc}")
            _concat_with_pyav(scenes, out_path, gap_seconds)
            method = "PyAV / libx264"
    else:
        _concat_with_pyav(scenes, out_path, gap_seconds)
        method = "PyAV / libx264"

    _write_manifest(out_path.with_suffix(".txt"), out_path, scenes)
    print(f"\nDone!\n  Output : {out_path}\n  Method : {method}")


if __name__ == "__main__":
    main()
