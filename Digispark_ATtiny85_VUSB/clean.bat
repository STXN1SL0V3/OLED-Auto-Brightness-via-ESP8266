@echo off
REM Clean build artifacts (Windows)

echo Cleaning build artifacts...

if exist build (
    rmdir /s /q build
    echo Build folder removed.
)

if exist digispark_test.elf del digispark_test.elf
if exist digispark_test.hex del digispark_test.hex
if exist digispark_test.map del digispark_test.map

echo.
echo Cleanup complete!
echo.
pause
