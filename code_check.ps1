# Venv activation
$venv = "$PSScriptRoot\venv\Scripts\Activate.ps1"
if (Test-Path $venv) {
    Write-Host "Activating virtualenv..."
    & $venv
} else {
    Write-Host "Virtualenv not found!"
    exit 1
}

# Mypy
Write-Host "`n===== Mypy ====="
python -m mypy "$PSScriptRoot\app" --ignore-missing-imports

# Black
Write-Host "`n===== Black ====="
python -m black --line-length 120 "$PSScriptRoot\app"

# Flake8
Write-Host "`n===== Flake8 ====="
python -m flake8 "$PSScriptRoot\app" --max-line-length 120

Write-Host "`nAll done!"

