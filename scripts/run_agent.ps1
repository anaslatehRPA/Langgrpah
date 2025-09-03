Param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

Write-Host "Running Project Planning RAG Agent..."

# Forward any args to python main.py
if ($Args) {
    poetry run python main.py @Args
} else {
    poetry run python main.py
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Agent exited with code $LASTEXITCODE" -ForegroundColor Yellow
}
