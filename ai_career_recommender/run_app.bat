@echo off
title AI-Based Career Recommender
echo ===================================================
echo   AI-Based Skill & Career Recommendation System
echo ===================================================

cd /d "%~dp0backend"

REM Check if Python virtual environment exists in project or root
if exist "%~dp0venv\Scripts\python.exe" (
    echo [*] Using virtual environment at root venv...
    "%~dp0venv\Scripts\python.exe" run.py
) else if exist "%~dp0backend\venv\Scripts\python.exe" (
    echo [*] Using virtual environment at backend\venv...
    "%~dp0backend\venv\Scripts\python.exe" run.py
) else (
    echo [*] Using system Python...
    python run.py
)

pause
