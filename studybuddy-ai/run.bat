@echo off
REM ===== StudyBuddy AI - one-click run for Windows =====
REM Double-click this file, or run it in a terminal. It sets everything up for you.
cd /d "%~dp0"

echo Looking for Python...
where py >nul 2>nul && (set PY=py) || (set PY=python)

echo Creating the virtual environment (first time only)...
%PY% -m venv venv
if errorlevel 1 (
  echo Could not create a venv. Installing without one instead...
  %PY% -m pip install --user -r requirements.txt
  %PY% -m streamlit run app.py
  goto :eof
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
echo.
echo Starting StudyBuddy at http://localhost:8501 ...
python -m streamlit run app.py
pause
