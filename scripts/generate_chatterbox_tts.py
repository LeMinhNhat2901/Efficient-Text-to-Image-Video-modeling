from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("tts/scripts")
DEFAULT_OUTPUT_DIR = Path("tts/outputs")

PRESETS = {
    "normal": {
        "exaggeration": 0.55,
        "cfg_weight": 0.45,
        "temperature": 0.75,
    },
    "cinematic": {
        "exaggeration": 0.70,
        "cfg_weight": 0.35,
        "temperature": 0.80,
    },
    "formula": {
        "exaggeration": 0.45,
        "cfg_weight": 0.55,
        "temperature": 0.65,
    },
    "lecture_slow": {
        "exaggeration": 0.35,
        "cfg_weight": 0.30,
        "temperature": 0.60,
    },
    "adam_slow": {
        "exaggeration": 0.30,
        "cfg_weight": 0.25,
        "temperature": 0.55,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate scene narration WAV files with Chatterbox TTS."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="A .txt file or a directory of script files. Default: tts/scripts",
    )
    parser.add_argument(
        "--glob",
        default="s??_*.txt",
        help="File pattern used when --input is a directory. Default: s??_*.txt",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated WAV files. Default: tts/outputs",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Inference device. Default: auto",
    )
    parser.add_argument(
        "--voice-prompt",
        type=Path,
        default=None,
        help="Optional 10-30 second clean voice reference WAV/MP3.",
    )
    parser.add_argument(
        "--local-ckpt",
        type=Path,
        default=None,
        help="Optional local Chatterbox checkpoint directory. Avoids Hub download.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=650,
        help="Approximate max characters per generated chunk. Default: 650",
    )
    parser.add_argument(
        "--pause-ms",
        type=int,
        default=250,
        help="Silence inserted between chunks. Default: 250",
    )
    parser.add_argument(
        "--tempo",
        type=float,
        default=1.0,
        help="Post-process tempo. 0.90 slows audio down slightly; 1.0 disables.",
    )
    parser.add_argument(
        "--ffmpeg",
        default="ffmpeg",
        help="FFmpeg executable used for --tempo. Default: ffmpeg",
    )
    parser.add_argument("--exaggeration", type=float, default=0.5)
    parser.add_argument("--cfg-weight", type=float, default=0.5)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default=None,
        help="Style preset. Explicit --exaggeration/--cfg-weight/--temperature override it.",
    )
    parser.add_argument("--repetition-penalty", type=float, default=1.2)
    parser.add_argument("--min-p", type=float, default=0.05)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument(
        "--normalize-peak",
        type=float,
        default=0.0,
        help="Optional final peak normalization target, e.g. 0.95. Disabled by default.",
    )
    parser.add_argument(
        "--keep-chunks",
        action="store_true",
        help="Also save each generated chunk under tts/outputs/chunks.",
    )
    parser.add_argument(
        "--no-respect-paragraphs",
        action="store_true",
        help="Allow short paragraphs to be merged into the same TTS chunk.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing WAV files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned files/chunks without loading Chatterbox.",
    )
    return parser.parse_args()


def apply_preset(args: argparse.Namespace) -> argparse.Namespace:
    if args.preset is None:
        return args

    defaults = {
        "exaggeration": 0.5,
        "cfg_weight": 0.5,
        "temperature": 0.8,
    }
    for key, value in PRESETS[args.preset].items():
        if getattr(args, key) == defaults[key]:
            setattr(args, key, value)
    return args


def choose_device(requested: str) -> str:
    import torch

    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested, but torch.cuda.is_available() is False.")
    return requested


def discover_inputs(input_path: Path, pattern: str) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if input_path.is_dir():
        return sorted(p for p in input_path.glob(pattern) if p.is_file())
    raise FileNotFoundError(f"Input path does not exist: {input_path}")


def compact_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_long_piece(piece: str, max_chars: int) -> list[str]:
    if len(piece) <= max_chars:
        return [piece]

    parts = re.split(r"(?<=[,;:])\s+", piece)
    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current} {part}".strip()
        if current and len(candidate) > max_chars:
            chunks.append(current)
            current = part
        else:
            current = candidate
    if current:
        chunks.append(current)

    result: list[str] = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            result.append(chunk)
            continue

        words = chunk.split()
        current_words: list[str] = []
        current_len = 0
        for word in words:
            next_len = current_len + len(word) + (1 if current_words else 0)
            if current_words and next_len > max_chars:
                result.append(" ".join(current_words))
                current_words = [word]
                current_len = len(word)
            else:
                current_words.append(word)
                current_len = next_len
        if current_words:
            result.append(" ".join(current_words))
    return result


def split_text(text: str, max_chars: int, respect_paragraphs: bool = True) -> list[str]:
    if max_chars < 120:
        raise ValueError("--max-chars should be at least 120.")

    text = compact_text(text)
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            candidate = f"{current} {sentence}".strip()
            if current and len(candidate) > max_chars:
                chunks.extend(split_long_piece(current, max_chars))
                current = sentence
            else:
                current = candidate

        if respect_paragraphs and current:
            chunks.extend(split_long_piece(current, max_chars))
            current = ""

    if current:
        chunks.extend(split_long_piece(current, max_chars))

    return chunks


def ensure_2d(wav: Any) -> Any:
    if wav.ndim == 1:
        return wav.unsqueeze(0)
    if wav.ndim == 2:
        return wav
    raise ValueError(f"Expected 1D or 2D waveform, got shape {tuple(wav.shape)}")


def peak_normalize(wav: Any, target: float) -> Any:
    if target <= 0:
        return wav
    peak = wav.abs().max()
    if peak <= 0:
        return wav
    return wav * min(target / float(peak), 1.0)


def patch_broken_perth_watermarker() -> None:
    import perth

    if getattr(perth, "PerthImplicitWatermarker", None) is not None:
        return

    class NoOpWatermarker:
        def apply_watermark(self, wav: Any, sample_rate: int) -> Any:
            return wav

    perth.PerthImplicitWatermarker = NoOpWatermarker
    print("warning: Perth watermark backend is unavailable; saving unwatermarked audio.")


def load_model(device: str, local_ckpt: Path | None) -> Any:
    patch_broken_perth_watermarker()

    from chatterbox.tts import ChatterboxTTS

    if local_ckpt is not None:
        if not local_ckpt.exists():
            raise FileNotFoundError(f"Local checkpoint directory does not exist: {local_ckpt}")
        return ChatterboxTTS.from_local(local_ckpt, device=device)
    return ChatterboxTTS.from_pretrained(device=device)


def atempo_filter(tempo: float) -> str:
    if tempo <= 0:
        raise ValueError("--tempo must be greater than 0.")
    factors: list[float] = []
    remaining = tempo
    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5
    while remaining > 2.0:
        factors.append(2.0)
        remaining /= 2.0
    factors.append(remaining)
    return ",".join(f"atempo={factor:.6g}" for factor in factors)


def apply_tempo(ffmpeg: str, source: Path, target: Path, tempo: float) -> None:
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(source),
        "-filter:a",
        atempo_filter(tempo),
        str(target),
    ]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        print("warning: FFmpeg was not found; falling back to librosa time-stretch.")
        apply_tempo_librosa(source, target, tempo)
    except subprocess.CalledProcessError as exc:
        print(
            f"warning: FFmpeg tempo processing failed with exit code {exc.returncode}; "
            "falling back to librosa time-stretch."
        )
        apply_tempo_librosa(source, target, tempo)


def apply_tempo_librosa(source: Path, target: Path, tempo: float) -> None:
    import librosa
    import soundfile as sf

    audio, sample_rate = sf.read(str(source), always_2d=True)
    channels = []
    for channel_index in range(audio.shape[1]):
        channels.append(librosa.effects.time_stretch(audio[:, channel_index], rate=tempo))

    min_len = min(len(channel) for channel in channels)
    stretched = [channel[:min_len] for channel in channels]
    output = list(zip(*stretched))
    sf.write(str(target), output, sample_rate)


def generate_file(
    model: Any,
    script_path: Path,
    out_path: Path,
    args: argparse.Namespace,
) -> None:
    import torch
    import torchaudio as ta

    text = script_path.read_text(encoding="utf-8-sig").strip()
    chunks = split_text(text, args.max_chars, respect_paragraphs=not args.no_respect_paragraphs)
    if not chunks:
        print(f"skip empty file: {script_path}")
        return

    if out_path.exists() and not args.overwrite:
        print(f"skip existing file: {out_path}")
        return

    print(f"generate {script_path} -> {out_path} ({len(chunks)} chunk(s))")

    voice_prompt = str(args.voice_prompt) if args.voice_prompt else None
    wavs: list[torch.Tensor] = []
    chunk_dir = args.output_dir / "chunks"
    if args.keep_chunks:
        chunk_dir.mkdir(parents=True, exist_ok=True)

    for index, chunk in enumerate(chunks, start=1):
        print(f"  chunk {index:02d}/{len(chunks)}: {len(chunk)} chars")
        wav = model.generate(
            chunk,
            repetition_penalty=args.repetition_penalty,
            min_p=args.min_p,
            top_p=args.top_p,
            audio_prompt_path=voice_prompt,
            exaggeration=args.exaggeration,
            cfg_weight=args.cfg_weight,
            temperature=args.temperature,
        )
        wav = ensure_2d(wav.cpu())
        wavs.append(wav)

        if args.keep_chunks:
            chunk_path = chunk_dir / f"{script_path.stem}_{index:03d}.wav"
            ta.save(str(chunk_path), wav, model.sr)

        if args.pause_ms > 0 and index != len(chunks):
            silence_samples = int(model.sr * args.pause_ms / 1000)
            wavs.append(torch.zeros((wav.shape[0], silence_samples), dtype=wav.dtype))

    final_wav = torch.cat(wavs, dim=1)
    final_wav = peak_normalize(final_wav, args.normalize_peak)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    save_path = out_path
    temp_path = None
    if args.tempo != 1.0:
        temp_path = out_path.with_name(f"{out_path.stem}.raw{out_path.suffix}")
        save_path = temp_path

    ta.save(str(save_path), final_wav, model.sr)
    seconds = final_wav.shape[1] / model.sr

    if args.tempo != 1.0 and temp_path is not None:
        apply_tempo(args.ffmpeg, temp_path, out_path, args.tempo)
        temp_path.unlink(missing_ok=True)
        seconds = seconds / args.tempo

    print(f"saved {out_path} ({seconds:.1f}s, {model.sr} Hz)")


def main() -> int:
    args = apply_preset(parse_args())

    if args.tempo < 0.88:
        print(
            "warning: --tempo below 0.88 can make speech sound distorted. "
            "Prefer smaller --max-chars and larger --pause-ms first."
        )

    if args.voice_prompt is not None and not args.voice_prompt.exists():
        raise FileNotFoundError(f"Voice prompt does not exist: {args.voice_prompt}")

    input_files = discover_inputs(args.input, args.glob)
    if not input_files:
        print(f"No input files found in {args.input} with pattern {args.glob}")
        return 1

    planned = []
    for script_path in input_files:
        text = script_path.read_text(encoding="utf-8-sig")
        chunks = split_text(text, args.max_chars, respect_paragraphs=not args.no_respect_paragraphs)
        planned.append((script_path, args.output_dir / f"{script_path.stem}.wav", len(chunks)))

    if args.dry_run:
        for script_path, out_path, chunk_count in planned:
            print(f"{script_path} -> {out_path} ({chunk_count} chunk(s))")
        return 0

    device = choose_device(args.device)
    print(f"using device: {device}")
    model = load_model(device, args.local_ckpt)

    for script_path, out_path, _chunk_count in planned:
        generate_file(model, script_path, out_path, args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
