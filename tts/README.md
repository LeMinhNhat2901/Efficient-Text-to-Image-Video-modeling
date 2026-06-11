# Chatterbox TTS

This folder keeps narration text and generated voice files separate from the
Manim render environment.

Use the dedicated conda environment:

```powershell
conda activate chatterbox
```

Check the install:

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
python -c "from chatterbox.tts import ChatterboxTTS; print('chatterbox ok')"
```

Put narration text files in:

```text
tts/scripts/
```

Generate all text files:

```powershell
python scripts/generate_chatterbox_tts.py --input tts/scripts --output-dir tts/outputs --device cuda
```

When `--input` is a directory, the default glob is `s??_*.txt`, so `voice.txt`
and `scene_00_test.txt` are not generated accidentally.

Generate the first scene with the cinematic preset:

```powershell
python scripts/generate_chatterbox_tts.py --input tts/scripts/s00_roadmap.txt --output-dir tts/outputs --device cuda --preset cinematic --overwrite
```

Generate a slower first-scene read and stretch it with FFmpeg:

```powershell
python scripts/generate_chatterbox_tts.py --input tts/scripts/s00_roadmap.txt --output-dir tts/outputs --device cuda --preset adam_slow --max-chars 180 --pause-ms 550 --tempo 1.0 --normalize-peak 0.90 --overwrite
```

If it still feels too fast, use only a light stretch:

```powershell
python scripts/generate_chatterbox_tts.py --input tts/scripts/s00_roadmap.txt --output-dir tts/outputs --device cuda --preset adam_slow --max-chars 160 --pause-ms 700 --tempo 1.0 --normalize-peak 0.90 --overwrite
```

Use a voice reference:

```powershell
python scripts/generate_chatterbox_tts.py --input tts/scripts --output-dir tts/outputs --device cuda --voice-prompt tts/reference/voice_reference.wav
```

Available presets:

```text
normal     exaggeration=0.55 cfg_weight=0.45 temperature=0.75
cinematic  exaggeration=0.70 cfg_weight=0.35 temperature=0.80
formula    exaggeration=0.45 cfg_weight=0.55 temperature=0.65
lecture_slow exaggeration=0.35 cfg_weight=0.30 temperature=0.60
adam_slow exaggeration=0.30 cfg_weight=0.25 temperature=0.55
```

`--tempo` uses FFmpeg after generation. Values below 1.0 make the audio longer:

```text
--tempo 0.95  makes audio about 1.05x longer
--tempo 0.90  makes audio about 1.11x longer
```

Avoid `--tempo 0.75` or lower for narration unless you accept audible artifacts.
For cleaner speech, prefer more line breaks in the text, `--max-chars 160-220`,
and `--pause-ms 500-800`.

Blank lines are treated as hard pause points by default. Use
`--no-respect-paragraphs` only when you want the script to merge short lines
into longer chunks.

## Full Script Split

The full narration source lives at:

```text
tts/scripts/voice.txt
```

Split it into per-scene files:

```powershell
python scripts/split_voice_scenes.py
```

By default this keeps the hand-tuned `tts/scripts/s00_roadmap.txt`. To rebuild
scene 00 from `voice.txt` too:

```powershell
python scripts/split_voice_scenes.py --overwrite-s00
```

Generate one scene:

```powershell
.\tts\generate_scene_wavs.ps1 -Scene s01
```

Generate all scenes:

```powershell
.\tts\generate_scene_wavs.ps1 -Scene all
```

Preview chunking without loading the model:

```powershell
python scripts/generate_chatterbox_tts.py --dry-run
```

First model download:

Chatterbox loads model files from Hugging Face repo `ResembleAI/chatterbox` the
first time `from_pretrained()` runs. To download them explicitly before a long
generation session:

```powershell
python -c "from huggingface_hub import snapshot_download; snapshot_download('ResembleAI/chatterbox')"
```

If you use a manually downloaded checkpoint folder, pass it with:

```powershell
python scripts/generate_chatterbox_tts.py --local-ckpt path\to\chatterbox --device cuda
```

Generated audio and reference recordings are ignored by git.

## Troubleshooting

If Chatterbox raises this on Windows:

```text
TypeError: 'NoneType' object is not callable
```

from `perth.PerthImplicitWatermarker()`, the generation script patches in a
no-op watermarker and continues. The voice generation itself still works; only
the optional Perth watermark step is skipped.
