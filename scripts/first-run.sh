#!/usr/bin/env sh
set -eu
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . pytest ruff
pytest
ruff check .
flowlens analyze examples/synthetic-solution --output flowlens-report
printf '%s\n' 'FlowLens setup and example analysis completed.'
