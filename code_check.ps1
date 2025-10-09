# Venv activation
$venv = "$PSScriptRoot\venv\Scripts\Activate.ps1"
if (Test-Path $venv) {
    Write-Host "Activation virtualenv..."
    & $venv
} else {
    Write-Host "Not found virtualenv!"
    exit 1
}

# Mypy
Write-Host "`n===== Mypy ====="
python -m mypy "$PSScriptRoot\app"

# Black
Write-Host "`n===== Black ====="
python -m black "$PSScriptRoot\app"

# Flake8
Write-Host "`n===== Flake8 ====="
python -m flake8 "$PSScriptRoot\app"

Write-Host "`nAll done!"
