$ErrorActionPreference = "Stop"

Write-Host "LegalEase setup" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found. Install Python 3.11+ and make sure 'python' is on PATH."
}

python --version
python -m venv .venv

Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Run: streamlit run app.py"
Write-Host "Optional API: uvicorn backend.main:app --reload --port 8000"
