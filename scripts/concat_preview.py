from __future__ import annotations

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

from config import BG

SCENES = [
    ROOT / "media" / "video_01" / "videos" / "s00_roadmap" / "480p15" / "RoadmapOverview.mp4",
    ROOT
    / "media"
    / "videos"
    / "s01_forward_ou_wiener"
    / "480p15"
    / "ForwardOUWiener.mp4",
    ROOT / "media" / "video_01" / "videos" / "s02_markov" / "480p15" / "MarkovChainScene.mp4",
    ROOT
    / "media"
    / "videos"
    / "s03_reverse_chain"
    / "480p15"
    / "ReverseMarkovChain.mp4",
    ROOT / "media" / "video_01" / "videos" / "s04_score_compass" / "480p15" / "ScoreCompassScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s05_local_linear" / "480p15" / "LocalLinearScoreScene.mp4",
    ROOT
    / "media"
    / "videos"
    / "s06_mse_conditional_mean"
    / "480p15"
    / "MSEConditionalMeanScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s07_training_loop" / "480p15" / "TrainingLoopScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s08_sde_drift_diffusion" / "480p15" / "ContinuousTimeFlowScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s09_probability_flow_ode" / "480p15" / "DriftDiffusionScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s10_fokker_planck_score" / "480p15" / "FokkerPlanckScoreScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s11_reverse_distribution" / "480p15" / "ReverseDistributionScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s12_runge_kutta_solver" / "480p15" / "RungeKuttaSolverScene.mp4",
    ROOT / "media" / "video_01" / "videos" / "s13_finale_failure" / "480p15" / "FinaleFailureScene.mp4",
]

OUT_DIR = ROOT / "media" / "video_01" / "videos" / "preview_480p15"
OUT_PATH = OUT_DIR / "DiffusionPrototypePreview.mp4"
FPS = 15
GAP_SECONDS = 0.25


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))


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


def _write_manifest(manifest: Path) -> None:
    manifest.write_text(
        "\n".join([f"Output: {OUT_PATH.name}", "", "Scene order:", *map(str, SCENES)]),
        encoding="utf-8",
    )


def _concat_with_ffmpeg(ffmpeg: str) -> None:
    width, height = _video_info(SCENES[0])
    with tempfile.TemporaryDirectory(prefix="diffusion_concat_") as tmp:
        tmp_dir = Path(tmp)
        gap = tmp_dir / "gap.mp4"
        concat_list = tmp_dir / "concat_list.txt"

        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"color=c=0x{BG.lstrip('#')}:s={width}x{height}:r={FPS}:d={GAP_SECONDS}",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                str(gap),
            ],
            check=True,
        )

        entries: list[str] = []
        for index, scene in enumerate(SCENES):
            entries.append(_manifest_line(scene))
            if index < len(SCENES) - 1:
                entries.append(_manifest_line(gap))
        concat_list.write_text("\n".join(entries), encoding="utf-8")

        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-an",
                "-r",
                str(FPS),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-movflags",
                "+faststart",
                str(OUT_PATH),
            ],
            check=True,
        )


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


def _concat_with_pyav() -> None:
    width, height = _video_info(SCENES[0])

    output = av.open(str(OUT_PATH), mode="w")
    stream = output.add_stream("libx264", rate=FPS)
    stream.width = width
    stream.height = height
    stream.pix_fmt = "yuv420p"
    stream.bit_rate = 4_000_000
    stream.time_base = Fraction(1, FPS)
    stream.options = {"preset": "veryfast", "crf": "20"}

    bg_rgb = np.array(_hex_to_rgb(BG), dtype=np.uint8)
    black = np.tile(bg_rgb, (height, width, 1))
    gap_frames = max(1, round(FPS * GAP_SECONDS))
    pts = 0

    for scene_index, input_path in enumerate(SCENES):
        with av.open(str(input_path)) as container:
            for frame in container.decode(video=0):
                frame = frame.reformat(width=width, height=height, format="yuv420p")
                _encode_frame(stream, output, frame, pts)
                pts += 1

        if scene_index < len(SCENES) - 1:
            for _ in range(gap_frames):
                frame = av.VideoFrame.from_ndarray(black, format="rgb24")
                frame = frame.reformat(format="yuv420p")
                _encode_frame(stream, output, frame, pts)
                pts += 1

    for packet in stream.encode():
        output.mux(packet)
    output.close()


def main() -> None:
    missing = [str(path) for path in SCENES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing rendered scene(s):\n" + "\n".join(missing))

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ffmpeg = _find_ffmpeg()
    if ffmpeg:
        try:
            _concat_with_ffmpeg(ffmpeg)
            method = f"ffmpeg: {ffmpeg}"
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"ffmpeg failed, falling back to PyAV/libx264: {exc}")
            _concat_with_pyav()
            method = "pyav: libx264"
    else:
        _concat_with_pyav()
        method = "pyav: libx264"

    _write_manifest(OUT_DIR / "preview_manifest.txt")
    print(f"{OUT_PATH}\nmethod: {method}")


if __name__ == "__main__":
    main()
