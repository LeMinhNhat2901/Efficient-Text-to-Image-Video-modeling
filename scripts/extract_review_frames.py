from pathlib import Path

import av


SAMPLES = [
    ("s00_dimshift", Path("media/videos/s00_roadmap/480p15/RoadmapOverview.mp4"), 50.0),
    ("s01_variance", Path("media/videos/s01_forward_ou_wiener/480p15/ForwardOUWiener.mp4"), 25.0),
    ("s02_memory", Path("media/videos/s02_markov/480p15/MarkovChainScene.mp4"), 45.0),
    (
        "s03_puppy_reverse",
        Path("media/videos/s03_reverse_chain/480p15/ReverseMarkovChain.mp4"),
        15.0,
    ),
    ("s03_engine", Path("media/videos/s03_reverse_chain/480p15/ReverseMarkovChain.mp4"), 80.0),
]

CONTACT_SHEETS = [
    (
        "s00_contact",
        Path("media/videos/s00_roadmap/480p15/RoadmapOverview.mp4"),
        [18.0, 28.0, 38.0, 48.0, 58.0, 78.0],
    ),
    (
        "s01_contact",
        Path("media/videos/s01_forward_ou_wiener/480p15/ForwardOUWiener.mp4"),
        [8.0, 14.0, 20.0, 26.0, 36.0, 56.0],
    ),
    (
        "s02_contact",
        Path("media/videos/s02_markov/480p15/MarkovChainScene.mp4"),
        [12.0, 24.0, 34.0, 42.0, 54.0, 72.0],
    ),
    (
        "s03_contact",
        Path("media/videos/s03_reverse_chain/480p15/ReverseMarkovChain.mp4"),
        [12.0, 24.0, 42.0, 62.0, 82.0, 112.0],
    ),
]


def frame_at(path: Path, seconds: float):
    container = av.open(str(path))
    stream = container.streams.video[0]
    container.seek(int(seconds * 1_000_000), any_frame=False, backward=True)
    for packet in container.demux(stream):
        for frame in packet.decode():
            if float(frame.pts * frame.time_base) >= seconds:
                return frame

    container = av.open(str(path))
    return next(container.decode(video=0))


def main() -> None:
    out_dir = Path("tmp_review_frames")
    out_dir.mkdir(exist_ok=True)

    for name, path, seconds in SAMPLES:
        frame = frame_at(path, seconds)
        output = out_dir / f"{name}.png"
        frame.to_image().save(output)
        print(output)

    for name, path, seconds_list in CONTACT_SHEETS:
        images = [frame_at(path, seconds).to_image().resize((427, 240)) for seconds in seconds_list]
        sheet = images[0].copy().resize((854, 720))
        sheet.paste(images[0], (0, 0))
        sheet.paste(images[1], (427, 0))
        sheet.paste(images[2], (0, 240))
        sheet.paste(images[3], (427, 240))
        sheet.paste(images[4], (0, 480))
        sheet.paste(images[5], (427, 480))
        output = out_dir / f"{name}.png"
        sheet.save(output)
        print(output)


if __name__ == "__main__":
    main()
