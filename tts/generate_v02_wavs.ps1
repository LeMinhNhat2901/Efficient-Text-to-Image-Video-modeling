# generate_v02_wavs.ps1
# Generates voiceover WAV files for Video 2 using the same TTS approach as Video 1.
# Run from the project root:   .\tts\generate_v02_wavs.ps1
#
# Requires: Python with edge-tts installed (`pip install edge-tts`)
# Or swap the COMMAND below for any TTS engine that accepts plain text.

param(
    [string]$Voice = "en-US-GuyNeural",
    [float]$Rate  = -5        # percent speed adjustment, e.g. -5 = slightly slower
)

$ScriptsDir = "$PSScriptRoot\scripts"
$OutputDir  = "$PSScriptRoot\outputs"

if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory $OutputDir | Out-Null }

$scenes = @(
    "v02_s00_text_pixels_opening",
    "v02_s01_generative_backbones",
    "v02_s02_clip_coembedding"
)

foreach ($scene in $scenes) {
    $textFile = "$ScriptsDir\$scene.txt"
    $wavFile  = "$OutputDir\$scene.wav"

    if (-not (Test-Path $textFile)) {
        Write-Warning "Script not found: $textFile"
        continue
    }

    Write-Host "Generating: $wavFile" -ForegroundColor Cyan
    $text = Get-Content $textFile -Raw

    # Write text to a temp file (edge-tts reads from file)
    $tmp = [System.IO.Path]::GetTempFileName() + ".txt"
    Set-Content $tmp $text -Encoding UTF8

    $rateStr = if ($Rate -ge 0) { "+${Rate}%" } else { "${Rate}%" }

    & python -m edge_tts `
        --voice $Voice `
        --rate  $rateStr `
        --file  $tmp `
        --write-media $wavFile

    Remove-Item $tmp -ErrorAction SilentlyContinue

    if (Test-Path $wavFile) {
        $sizeKB = [math]::Round((Get-Item $wavFile).Length / 1KB, 1)
        Write-Host "  -> OK  ($sizeKB KB)" -ForegroundColor Green
    } else {
        Write-Warning "  -> FAILED: $wavFile not created."
    }
}

Write-Host "`nDone. WAVs saved to: $OutputDir" -ForegroundColor Yellow
