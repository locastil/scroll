@echo off
rem Starts Scroll (TikTok / Instagram Reels) with no console window.
cd /d "%~dp0"
start "" ".venv\Scripts\pythonw.exe" "scroll_app.py"
