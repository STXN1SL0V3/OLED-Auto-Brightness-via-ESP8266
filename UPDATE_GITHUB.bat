@echo off
chcp 65001 >nul
echo ========================================
echo 📤 Обновление GitHub репозитория
echo ========================================
echo.
echo Репозиторий: STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266
echo.

REM Проверка Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git не установлен!
    echo Скачайте с: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Инициализация если нужно
if not exist ".git" (
    echo 🔄 Инициализация Git...
    git init
    git branch -M main
    git remote add origin https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266.git
    echo.
)

REM Добавление файлов
echo 📝 Добавление файлов...
git add .
echo.

REM Коммит
echo 💾 Создание коммита...
git commit -m "📝 Update v1.0.1 - Added autostart feature and updated documentation"
echo.

REM Push
echo 🚀 Отправка на GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ Изменения отправлены на GitHub!
    echo ========================================
    echo.
    echo 🔗 https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266
    echo.
) else (
    echo.
    echo ❌ Ошибка! Возможно нужна авторизация.
    echo.
    echo Создайте Personal Access Token:
    echo https://github.com/settings/tokens
    echo.
    echo Или попробуйте:
    echo   git pull origin main --rebase
    echo   git push origin main
    echo.
)

pause
