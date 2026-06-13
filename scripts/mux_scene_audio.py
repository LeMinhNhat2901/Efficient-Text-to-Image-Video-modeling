from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import av


ROOT = Path(__file__).resolve().parents[1]


def media_duration(path: Path) -> float:
    with av.open(str(path)) as container:
        if container.duration is None:
            return 0.0
        return float(container.duration / 1_000_000)


def find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found

    env_root = Path(sys.executable).resolve().parents[1]
    candidate = env_root / "Library" / "bin" / "ffmpeg.exe"
    if candidate.exists():
        return str(candidate)

    raise FileNotFoundError("ffmpeg not found on PATH or in the active conda environment.")


def mux_with_pyav(video: Path, audio: Path, output: Path) -> None:
    audio_duration = media_duration(audio)
    with av.open(str(video)) as video_input, av.open(str(audio)) as audio_input:
        video_stream = video_input.streams.video[0]
        audio_stream = audio_input.streams.audio[0]
        rate = video_stream.average_rate or Fraction(15, 1)

        output_container = av.open(str(output), mode="w")
        out_video = output_container.add_stream("libx264", rate=rate)
        out_video.width = video_stream.codec_context.width
        out_video.height = video_stream.codec_context.height
        out_video.pix_fmt = "yuv420p"
        out_video.bit_rate = 4_000_000
        out_video.options = {"preset": "veryfast", "crf": "20"}

        out_audio = output_container.add_stream("aac", rate=audio_stream.codec_context.sample_rate or 44100)
        out_audio.bit_rate = 192_000

        for frame in video_input.decode(video_stream):
            if frame.time is not None and float(frame.time) > audio_duration:
                break
            frame = frame.reformat(out_video.width, out_video.height, format="yuv420p")
            for packet in out_video.encode(frame):
                output_container.mux(packet)

        for packet in out_video.encode():
            output_container.mux(packet)

        for frame in audio_input.decode(audio_stream):
            for packet in out_audio.encode(frame):
                output_container.mux(packet)

        for packet in out_audio.encode():
            output_container.mux(packet)

        output_container.close()


def default_video(scene: str, quality_dir: str) -> Path:
    scene_map = {
        "s00": ("s00_roadmap", "RoadmapOverview"),
        "s01": ("s01_forward_ou_wiener", "ForwardOUWiener"),
        "s02": ("s02_markov", "MarkovChainScene"),
        "s03": ("s03_reverse_chain", "ReverseMarkovChain"),
        "s04": ("s04_score_compass", "ScoreCompassScene"),
        "s05": ("s05_local_linear", "LocalLinearScoreScene"),
        "s06": ("s06_mse_conditional_mean", "MSEConditionalMeanScene"),
        "s07": ("s07_training_loop", "TrainingLoopScene"),
        "s08": ("s08_sde_drift_diffusion", "ContinuousTimeFlowScene"),
        "s09": ("s09_probability_flow_ode", "DriftDiffusionScene"),
        "s10": ("s10_fokker_planck_score", "FokkerPlanckScoreScene"),
        "s11": ("s11_reverse_distribution", "ReverseDistributionScene"),
        "s12": ("s12_runge_kutta_solver", "RungeKuttaSolverScene"),
        "s13": ("s13_finale_failure", "FinaleFailureScene"),
        "v02_s00": ("v02_s00_text_pixels_opening", "V02TextPixelsOpening"),
        "v02_s01": ("v02_s01_generative_backbones", "V02GenerativeBackbones"),
        "v02_s02": ("v02_s02_clip_coembedding", "V02ClipCoEmbedding"),
        "v02_s03": ("v02_s03_vqgan_visual_words", "V02VqganVisualWords"),
        "v02_s04": ("v02_s04_architecture_evolution", "V02ArchitectureEvolution"),
        "v02_s05": ("v02_s05_muse_markovgen", "V02MuseMarkovgen"),
        "v02_s06": ("v02_s06_diffusion_intuition", "V02DiffusionIntuition"),
        "v02_s07": ("v02_s07_diffusion_math", "V02DiffusionMath"),
        "v02_s08": ("v02_s08_guidance", "V02Guidance"),
        "v02_s09": ("v02_s09_latent_diffusion_crf", "V02LatentDiffusionCRF"),
        "v02_s10": ("v02_s10_sana_var", "V02SanaVar"),
        "v02_s11": ("v02_s11_discussion_finale", "V02DiscussionFinale"),
    }
    if scene not in scene_map:
        raise ValueError(f"No default path configured for scene {scene!r}. Pass --video explicitly.")
    folder, class_name = scene_map[scene]
    return ROOT / "media" / "videos" / folder / quality_dir / f"{class_name}.mp4"


def default_audio(scene: str) -> Path:
    audio_map = {
        "s00": ROOT / "tts" / "outputs" / "s00_roadmap.wav",
        "s01": ROOT / "tts" / "outputs" / "s01_forward_ou_wiener.wav",
        "s02": ROOT / "tts" / "outputs" / "s02_markov.wav",
        "s03": ROOT / "tts" / "outputs" / "s03_reverse_chain.wav",
        "s04": ROOT / "tts" / "outputs" / "s04_score_compass.wav",
        "s05": ROOT / "tts" / "outputs" / "s05_local_linear.wav",
        "s06": ROOT / "tts" / "outputs" / "s06_mse_conditional_mean.wav",
        "s07": ROOT / "tts" / "outputs" / "s07_training_loop.wav",
        "s08": ROOT / "tts" / "outputs" / "s08_sde_drift_diffusion.wav",
        "s09": ROOT / "tts" / "outputs" / "s09_probability_flow_ode.wav",
        "s10": ROOT / "tts" / "outputs" / "s10_fokker_planck_score.wav",
        "s11": ROOT / "tts" / "outputs" / "s11_reverse_distribution.wav",
        "s12": ROOT / "tts" / "outputs" / "s12_runge_kutta_solver.wav",
        "s13": ROOT / "tts" / "outputs" / "s13_finale_failure.wav",
        "v02_s00": ROOT / "tts" / "outputs" / "v02_s00_text_pixels_opening.wav",
        "v02_s01": ROOT / "tts" / "outputs" / "v02_s01_generative_backbones.wav",
        "v02_s02": ROOT / "tts" / "outputs" / "v02_s02_clip_coembedding.wav",
        "v02_s03": ROOT / "tts" / "outputs" / "v02_s03_vqgan_visual_words.wav",
        "v02_s04": ROOT / "tts" / "outputs" / "v02_s04_architecture_evolution.wav",
        "v02_s05": ROOT / "tts" / "outputs" / "v02_s05_muse_markovgen.wav",
        "v02_s06": ROOT / "tts" / "outputs" / "v02_s06_diffusion_intuition.wav",
        "v02_s07": ROOT / "tts" / "outputs" / "v02_s07_diffusion_math.wav",
        "v02_s08": ROOT / "tts" / "outputs" / "v02_s08_guidance.wav",
        "v02_s09": ROOT / "tts" / "outputs" / "v02_s09_latent_diffusion_crf.wav",
        "v02_s10": ROOT / "tts" / "outputs" / "v02_s10_sana_var.wav",
        "v02_s11": ROOT / "tts" / "outputs" / "v02_s11_discussion_finale.wav",
    }
    if scene not in audio_map:
        raise ValueError(f"No default audio configured for scene {scene!r}. Pass --audio explicitly.")
    return audio_map[scene]


def main() -> None:
    parser = argparse.ArgumentParser(description="Mux a rendered scene MP4 with its narration WAV.")
    parser.add_argument("--scene", default="s00", help="Scene key for default paths, e.g. s00 or s01.")
    parser.add_argument("--quality-dir", default="480p15", help="Rendered Manim quality folder, e.g. 480p15.")
    parser.add_argument("--video", type=Path, help="Rendered silent scene MP4.")
    parser.add_argument("--audio", type=Path, help="Narration WAV. Defaults to the scene audio when configured.")
    parser.add_argument("--output", type=Path, help="Output MP4 with audio.")
    parser.add_argument("--replace", action="store_true", help="Replace the input video with the muxed output.")
    parser.add_argument("--sidecar", action="store_true", help="Also write a *_with_audio.mp4 copy.")
    args = parser.parse_args()

    video = (args.video or default_video(args.scene, args.quality_dir)).resolve()
    audio = (args.audio or default_audio(args.scene)).resolve()
    if args.replace and args.output:
        raise ValueError("--replace and --output are mutually exclusive.")
    output = (args.output or video.with_name(f"{video.stem}_with_audio.mp4")).resolve()
    if args.replace:
        temp_dir = Path(tempfile.mkdtemp(prefix="scene_audio_mux_"))
        output = temp_dir / video.name

    if not video.exists():
        raise FileNotFoundError(video)
    if not audio.exists():
        raise FileNotFoundError(audio)

    output.parent.mkdir(parents=True, exist_ok=True)
    method = "pyav"
    try:
        ffmpeg = find_ffmpeg()
        command = [
            ffmpeg,
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ]
        subprocess.run(command, check=True)
        method = f"ffmpeg: {ffmpeg}"
    except (FileNotFoundError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ffmpeg failed, falling back to PyAV/libx264+aac: {exc}")
        mux_with_pyav(video, audio, output)

    print(f"video:  {video} | {media_duration(video):.2f}s")
    print(f"audio:  {audio} | {media_duration(audio):.2f}s")
    print(f"output: {output} | {media_duration(output):.2f}s")
    print(f"method: {method}")
    if args.replace:
        shutil.move(str(output), str(video))
        shutil.rmtree(output.parent, ignore_errors=True)
        print(f"replaced: {video} | {media_duration(video):.2f}s")
    if args.sidecar:
        sidecar = video.with_name(f"{video.stem}_with_audio{video.suffix}")
        shutil.copy2(video, sidecar)
        print(f"sidecar:  {sidecar} | {media_duration(sidecar):.2f}s")


if __name__ == "__main__":
    main()
