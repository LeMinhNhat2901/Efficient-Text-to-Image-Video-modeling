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
    ROOT / "media" / "videos" / "v02_s00_text_pixels_opening" / "480p15" / "V02TextPixelsOpening.mp4",
    ROOT / "media" / "videos" / "v02_s01_generative_backbones" / "480p15" / "V02GenerativeBackbones.mp4",
    ROOT / "media" / "videos" / "v02_s02_clip_coembedding" / "480p15" / "V02ClipCoEmbedding.mp4",
    ROOT / "media" / "videos" / "v02_s03_vqgan_visual_words" / "480p15" / "V02VqganVisualWords.mp4",
    ROOT / "media" / "videos" / "v02_s04_architecture_evolution" / "480p15" / "V02ArchitectureEvolution.mp4",
    ROOT / "media" / "videos" / "v02_s05_muse_markovgen" / "480p15" / "V02MuseMarkovgen.mp4",
    ROOT / "media" / "videos" / "v02_s06_diffusion_intuition" / "480p15" / "V02DiffusionIntuition.mp4",
    ROOT / "media" / "videos" / "v02_s07_diffusion_math" / "480p15" / "V02DiffusionMath.mp4",
    ROOT / "media" / "videos" / "v02_s08_guidance" / "480p15" / "V02Guidance.mp4",
    ROOT / "media" / "videos" / "v02_s09_latent_diffusion_crf" / "480p15" / "V02LatentDiffusionCRF.mp4",
    ROOT / "media" / "videos" / "v02_s10_sana_var" / "480p15" / "V02SanaVar.mp4",
    ROOT / "media" / "videos" / "v02_s11_discussion_finale" / "480p15" / "V02DiscussionFinale.mp4",
]

OUT_DIR = ROOT / "media" / "videos" / "preview_480p15"
OUT_PATH = OUT_DIR / "TextPixelsPreview.mp4"
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
    with tempfile.TemporaryDirectory(prefix="textpixels_concat_") as tmp:
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
    if OUT_PATH.exists():
        OUT_PATH.unlink()

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

    _write_manifest(OUT_DIR / "textpixels_preview_manifest.txt")
    print(f"{OUT_PATH}\nmethod: {method}")


if __name__ == "__main__":
    main()
