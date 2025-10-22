@echo off
REM Upload script for Digispark ATtiny85 (Windows)
chcp 65001 > nul

echo ========================================
echo  Digispark ATtiny85 Upload Script
echo ========================================
echo.

REM Проверка наличия HEX файла
if not exist "build\digispark_test.hex" (
    echo [ERROR] HEX file not found!
    echo Please run build.bat first.
    echo.
    pause
    exit /b 1
)

REM Проверка наличия micronucleus
if not exist "micronucleus\micronucleus.exe" (
    echo [ERROR] micronucleus.exe not found!
    echo.
    echo Please download micronucleus for Windows:
    echo   https://github.com/micronucleus/micronucleus/releases
    echo.
    echo Download: micronucleus-cli-2.5-win.zip
    echo Extract to: micronucleus\ folder
    echo.
    pause
    exit /b 1
)

echo Ready to upload firmware to Digispark ATtiny85
echo.
echo IMPORTANT:
echo - Plug in the Digispark when you see "Plug in device now..."
echo - The bootloader is active for only 5 seconds after plugging in
echo - Make sure no other programs are using the device
echo.
pause

echo.
echo Starting upload...
echo.

REM Запускаем micronucleus
micronucleus\micronucleus.exe --run build\digispark_test.hex

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Upload failed!
    echo.
    echo Troubleshooting:
    echo - Make sure Digispark is connected during upload
    echo - Try unplugging and replugging the device
    echo - Use a different USB port
    echo - Check if another program is using the device
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Upload successful!
echo ========================================
echo.
echo The device should now be running the test firmware.
echo It will send values 0-99 every second via USB.
echo.
echo Next steps:
echo 1. Install USB driver using Zadig (if not already done)
echo 2. Run: python ..\test_digispark_vusb.py
echo.
pause
