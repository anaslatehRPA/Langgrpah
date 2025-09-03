Param(
    [switch]$UseGoogleLLM
)

# Default: do not enable Google LLM
if ($UseGoogleLLM) {
    $env:USE_GOOGLE_LLM = "true"
} else {
    $env:USE_GOOGLE_LLM = "false"
}

Write-Host "Running scripts/run_priority_debug.py with USE_GOOGLE_LLM=$($env:USE_GOOGLE_LLM)"

poetry run python scripts/run_priority_debug.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Script exited with code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
