# check_code.ps1

# Aktywuj virtualenv
$venv = "$PSScriptRoot\venv\Scripts\Activate.ps1"
if (Test-Path $venv) {
    Write-Host "Activation virtualenv..."
    & $venv
} else {
    Write-Host "Not found virtualenv!"
    exit 1
}

# Flake8 - linting
Write-Host "`n===== Flake8 ====="
python -m flake8 "$PSScriptRoot\app"

# Mypy - typy statyczne
Write-Host "`n===== Mypy ====="
python -m mypy "$PSScriptRoot\app"

# Black - formatowanie
Write-Host "`n===== Black ====="
python -m black "$PSScriptRoot\app"

Write-Host "`n✅ All done!"
