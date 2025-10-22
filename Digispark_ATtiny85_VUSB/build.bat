@echo off
REM Build script for Digispark ATtiny85 Test Firmware (Windows)
chcp 65001 > nul

echo ========================================
echo  Digispark ATtiny85 Build Script
echo ========================================
echo.

REM Проверка наличия avr-gcc
where avr-gcc >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] avr-gcc not found!
    echo Please install WinAVR from: https://sourceforge.net/projects/winavr/
    echo.
    pause
    exit /b 1
)

REM Проверка наличия V-USB
if not exist "v-usb\usbdrv\usbdrv.c" (
    echo [ERROR] V-USB library not found!
    echo.
    echo Please clone V-USB:
    echo   git clone https://github.com/obdev/v-usb.git
    echo.
    echo Or download from: https://github.com/obdev/v-usb/archive/refs/heads/master.zip
    echo.
    pause
    exit /b 1
)

echo [1/3] Cleaning previous build...
if exist build rmdir /s /q build
mkdir build

echo [2/3] Compiling firmware...
echo.

REM Компиляция
avr-gcc -g -Os -DF_CPU=16500000UL -mmcu=attiny85 -Wall -Wstrict-prototypes ^
    -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums ^
    -std=gnu99 -I. -Iv-usb\usbdrv ^
    -o build\digispark_test.elf ^
    main.c osccal.c v-usb\usbdrv\usbdrv.c ^
    -x assembler-with-cpp -Wa,-gstabs,--listing-cont-lines=100 ^
    v-usb\usbdrv\usbdrvasm.S ^
    -Wl,-Map=build\digispark_test.map,--cref -lm

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Compilation failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Creating HEX file...

REM Создание HEX
avr-objcopy -O ihex -R .eeprom -R .fuse -R .lock -R .signature ^
    build\digispark_test.elf build\digispark_test.hex

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] HEX creation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build successful!
echo ========================================
echo.

REM Показываем размер
avr-size --mcu=attiny85 --format=avr build\digispark_test.elf

echo.
echo Output files:
echo   - build\digispark_test.elf
echo   - build\digispark_test.hex
echo.
echo Next step: Run upload.bat to flash the firmware
echo.
pause
