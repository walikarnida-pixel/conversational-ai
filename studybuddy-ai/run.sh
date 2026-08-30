#!/usr/bin/env bash
# ===== StudyBuddy AI - one-click run for macOS / Linux =====
set -e
cd "$(dirname "$0")"

PY=python3
command -v $PY >/dev/null 2>&1 || PY=python

echo "Creating the virtual environment (first time only)..."
if ! $PY -m venv venv 2>/dev/null; then
  echo "Could not create a venv; installing without one instead..."
  $PY -m pip install -r requirements.txt
  $PY -m streamlit run app.py
  exit 0
fi

source venv/bin/activate
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt
echo ""
echo "Starting StudyBuddy at http://localhost:8501 ..."
python -m streamlit run app.py
