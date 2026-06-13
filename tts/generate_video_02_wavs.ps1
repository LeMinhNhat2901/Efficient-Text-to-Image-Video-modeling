param(
    [string]$Scene = "all",
    [string]$Device = "cuda",
    [string]$Preset = "adam_slow",
    [int]$MaxChars = 180,
    [int]$PauseMs = 550,
    [double]$Tempo = 1.0,
    [double]$NormalizePeak = 0.90,
    [string]$VoicePrompt = ""
)

$ErrorActionPreference = "Stop"

$sceneFiles = [ordered]@{
    "v02_s00" = "tts/scripts/video_02/s00_text_pixels_opening.txt"
    "v02_s01" = "tts/scripts/video_02/s01_generative_backbones.txt"
    "v02_s02" = "tts/scripts/video_02/s02_clip_coembedding.txt"
    "v02_s03" = "tts/scripts/video_02/s03_vqgan_visual_words.txt"
    "v02_s04" = "tts/scripts/video_02/s04_architecture_evolution.txt"
    "v02_s05" = "tts/scripts/video_02/s05_muse_markovgen.txt"
    "v02_s06" = "tts/scripts/video_02/s06_diffusion_intuition.txt"
    "v02_s07" = "tts/scripts/video_02/s07_diffusion_math.txt"
    "v02_s08" = "tts/scripts/video_02/s08_guidance.txt"
    "v02_s09" = "tts/scripts/video_02/s09_latent_diffusion_crf.txt"
    "v02_s10" = "tts/scripts/video_02/s10_sana_var.txt"
    "v02_s11" = "tts/scripts/video_02/s11_discussion_finale.txt"
}

if ($Scene -eq "all") {
    $selected = $sceneFiles.GetEnumerator()
} elseif ($sceneFiles.Contains($Scene)) {
    $selected = @([pscustomobject]@{ Key = $Scene; Value = $sceneFiles[$Scene] })
} else {
    throw "Unknown scene '$Scene'. Use all or one of: $($sceneFiles.Keys -join ', ')"
}

foreach ($item in $selected) {
    if (-not (Test-Path $item.Value)) {
        Write-Warning "Script not found: $($item.Value)"
        continue
    }

    $argsList = @(
        "scripts/generate_chatterbox_tts.py",
        "--input", $item.Value,
        "--output-dir", "tts/outputs/video_02",
        "--device", $Device,
        "--preset", $Preset,
        "--max-chars", "$MaxChars",
        "--pause-ms", "$PauseMs",
        "--tempo", "$Tempo",
        "--normalize-peak", "$NormalizePeak",
        "--overwrite"
    )

    if ($VoicePrompt -ne "") {
        $argsList += @("--voice-prompt", $VoicePrompt)
    }

    Write-Host "Generating $($item.Key): $($item.Value)" -ForegroundColor Cyan
    python @argsList
}
