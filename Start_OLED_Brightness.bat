@echo off
REM OLED Auto Brightness Launcher
REM Automatically finds Python and runs the program

cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\pythonw.exe" (
    echo Starting with virtual environment...
    start "" ".venv\Scripts\pythonw.exe" "OLED_Auto_Brightness.py"
) else (
    echo Starting with system Python...
    start "" pythonw.exe "OLED_Auto_Brightness.py"
)

REM Exit immediately
exit
