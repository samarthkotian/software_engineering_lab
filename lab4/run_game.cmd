@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" game.py
) else if exist "..\..\.venv\Scripts\python.exe" (
    "..\..\.venv\Scripts\python.exe" game.py
) else (
    py -3 game.py
)
if errorlevel 1 pause
