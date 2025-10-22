@echo off
REM Setup script for Digispark development on Windows 10
chcp 65001 > nul

echo ========================================
echo  Digispark ATtiny85 - Setup for Windows 10
echo ========================================
echo.

echo This script will help setup development environment.
echo.
echo What will be installed:
echo   1. Check WinAVR
echo   2. Download V-USB
echo   3. Download Micronucleus
echo   4. Install Python packages (pyusb)
echo.
pause

REM ======================================
REM 1. Check WinAVR
REM ======================================
echo.
echo [1/4] Checking WinAVR...

where avr-gcc >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] WinAVR not found!
    echo.
    echo Please install WinAVR manually:
    echo   1. Download: https://sourceforge.net/projects/winavr/files/WinAVR/20100110/
    echo   2. Install to: C:\WinAVR-20100110\
    echo   3. Add to PATH: C:\WinAVR-20100110\bin
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
) else (
    echo [OK] WinAVR found!
    avr-gcc --version | findstr /C:"avr-gcc"
)

REM ======================================
REM 2. V-USB Library
REM ======================================
echo.
echo [2/4] Checking V-USB library...

if exist "v-usb\usbdrv\usbdrv.c" (
    echo [OK] V-USB already installed!
) else (
    echo [!] V-USB not found. Cloning...
    
    where git >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Git not found!
        echo.
        echo Please download V-USB manually:
        echo   1. Open: https://github.com/obdev/v-usb/archive/refs/heads/master.zip
        echo   2. Extract to: v-usb\
        echo.
        pause
        exit /b 1
    )
    
    git clone https://github.com/obdev/v-usb.git
    
    if exist "v-usb\usbdrv\usbdrv.c" (
        echo [OK] V-USB installed successfully!
    ) else (
        echo [ERROR] Failed to install V-USB!
        pause
        exit /b 1
    )
)

REM ======================================
REM 3. Micronucleus
REM ======================================
echo.
echo [3/4] Checking Micronucleus...

if exist "micronucleus\micronucleus.exe" (
    echo [OK] Micronucleus already installed!
) else (
    echo [!] Micronucleus not found!
    echo.
    echo Please download Micronucleus manually:
    echo   1. Open: https://github.com/micronucleus/micronucleus/releases
    echo   2. Download: micronucleus-cli-2.5-win.zip
    echo   3. Extract micronucleus.exe to: micronucleus\
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

REM ======================================
REM 4. Python packages
REM ======================================
echo.
echo [4/4] Installing Python packages...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found!
    echo.
    echo Install Python from:
    echo   https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version

echo.
echo Installing pyusb and libusb...
python -m pip install pyusb libusb-package

if %errorlevel% neq 0 (
    echo [!] Failed to install Python packages!
    pause
    exit /b 1
)

echo [OK] Python packages installed!

REM ======================================
REM Done!
REM ======================================
echo.
echo ========================================
echo  Setup completed!
echo ========================================
echo.
echo All tools installed:
echo   [OK] WinAVR
echo   [OK] V-USB
echo   [OK] Micronucleus
echo   [OK] Python + PyUSB
echo.
echo Next steps:
echo   1. Run: build.bat      (compile firmware)
echo   2. Run: upload.bat     (flash Digispark)
echo   3. Install driver using Zadig
echo   4. Run: python ..\test_digispark_vusb.py
echo.
echo Documentation: README_WINDOWS.md
echo.
pause
