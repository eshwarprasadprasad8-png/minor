# PowerShell Launcher for AI-Based Skill & Career Recommendation System
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  AI-Based Skill & Career Recommendation System" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

Set-Location $backendDir

$rootVenv = Join-Path $scriptDir "venv\Scripts\python.exe"
$backendVenv = Join-Path $backendDir "venv\Scripts\python.exe"

if (Test-Path $rootVenv) {
    Write-Host "[*] Using root virtual environment: $rootVenv" -ForegroundColor Green
    & $rootVenv run.py
} elseif (Test-Path $backendVenv) {
    Write-Host "[*] Using backend virtual environment: $backendVenv" -ForegroundColor Green
    & $backendVenv run.py
} else {
    Write-Host "[*] Using active/system Python..." -ForegroundColor Yellow
    python run.py
}
