param(
    [switch]$Web
)

# Change to the project directory relative to this script
Set-Location $PSScriptRoot

# Activate the virtual environment if it exists
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
}

# Run the application with Flet (desktop or web browser)
if ($Web) {
    Write-Host "Starting Choislet in Web Browser mode..." -ForegroundColor Cyan
    flet run --web src\main.py
} else {
    Write-Host "Starting Choislet Desktop mode..." -ForegroundColor Cyan
    flet run src\main.py
}
