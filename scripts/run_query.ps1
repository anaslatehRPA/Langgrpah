Param(
    [string]$Query = "คุณมีข้อมูล โปรเจคอะไรบ้าง"
)

Write-Host "Running agent one-shot query..."
poetry run python .\scripts\run_query.py --query "$Query"
