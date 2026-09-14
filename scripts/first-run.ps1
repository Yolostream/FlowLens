$ErrorActionPreference = "Stop"
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . pytest ruff
pytest
ruff check .
flowlens analyze examples/synthetic-solution --output flowlens-report
Write-Host "FlowLens setup and example analysis completed."
