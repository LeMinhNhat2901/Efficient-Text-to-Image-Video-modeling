from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import av
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SCENES = [
    ROOT / "media" / "videos" / "s00_roadmap" / "480p15" / "RoadmapOverview.mp4",
    ROOT
    / "media"
    / "videos"
    / "s01_forward_ou_wiener"
    / "480p15"
    / "ForwardOUWiener.mp4",
    ROOT / "media" / "videos" / "s02_markov" / "480p15" / "MarkovChainScene.mp4",
    ROOT
    / "media"
    / "videos"
    / "s03_reverse_chain"
    / "480p15"
    / "ReverseMarkovChain.mp4",
]

OUT_DIR = ROOT / "media" / "videos" / "preview_480p15"
OUT_PATH = OUT_DIR / "DiffusionPrototypePreview.mp4"
FPS = 15
GAP_SECONDS = 0.25


def _video_info(path: Path) -> tuple[int, int]:
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        return stream.codec_context.width, stream.codec_context.height


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


def main() -> None:
    missing = [str(path) for path in SCENES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing rendered scene(s):\n" + "\n".join(missing))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    width, height = _video_info(SCENES[0])

    output = av.open(str(OUT_PATH), mode="w")
    stream = output.add_stream("mpeg4", rate=FPS)
    stream.width = width
    stream.height = height
    stream.pix_fmt = "yuv420p"
    stream.bit_rate = 3_000_000
    stream.time_base = Fraction(1, FPS)

    black = np.zeros((height, width, 3), dtype=np.uint8)
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

    manifest = OUT_DIR / "preview_manifest.txt"
    manifest.write_text(
        "\n".join([f"Output: {OUT_PATH.name}", "", "Scene order:", *map(str, SCENES)]),
        encoding="utf-8",
    )
    print(OUT_PATH)


if __name__ == "__main__":
    main()
