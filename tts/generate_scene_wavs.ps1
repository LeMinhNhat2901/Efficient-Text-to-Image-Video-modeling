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
    "s00" = "tts/scripts/s00_roadmap.txt"
    "s01" = "tts/scripts/s01_forward_ou_wiener.txt"
    "s02" = "tts/scripts/s02_markov.txt"
    "s03" = "tts/scripts/s03_reverse_chain.txt"
    "s04" = "tts/scripts/s04_score_compass.txt"
    "s05" = "tts/scripts/s05_local_linear.txt"
    "s06" = "tts/scripts/s06_mse_conditional_mean.txt"
    "s07" = "tts/scripts/s07_training_loop.txt"
    "s08" = "tts/scripts/s08_sde_drift_diffusion.txt"
    "s09" = "tts/scripts/s09_probability_flow_ode.txt"
    "s10" = "tts/scripts/s10_fokker_planck_score.txt"
    "s11" = "tts/scripts/s11_reverse_distribution.txt"
    "s12" = "tts/scripts/s12_runge_kutta_solver.txt"
    "s13" = "tts/scripts/s13_finale_failure.txt"
}

if ($Scene -eq "all") {
    $selected = $sceneFiles.GetEnumerator()
} elseif ($sceneFiles.Contains($Scene)) {
    $selected = @([pscustomobject]@{ Key = $Scene; Value = $sceneFiles[$Scene] })
} else {
    throw "Unknown scene '$Scene'. Use all or one of: $($sceneFiles.Keys -join ', ')"
}

foreach ($item in $selected) {
    $argsList = @(
        "scripts/generate_chatterbox_tts.py",
        "--input", $item.Value,
        "--output-dir", "tts/outputs",
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

    Write-Host "Generating $($item.Key): $($item.Value)"
    python @argsList
}
