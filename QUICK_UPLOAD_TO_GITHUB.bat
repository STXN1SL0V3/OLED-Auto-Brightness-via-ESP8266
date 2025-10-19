@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 Быстрая загрузка на GitHub
echo ========================================
echo.

REM Проверка наличия Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git не установлен!
    echo.
    echo Скачайте Git с: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git найден
echo.

REM Запрос URL репозитория
set /p REPO_URL="Введите URL вашего GitHub репозитория (например, https://github.com/USERNAME/AutoBrightOLED.git): "

if "%REPO_URL%"=="" (
    echo ❌ URL не указан!
    pause
    exit /b 1
)

echo.
echo 📦 Инициализация Git репозитория...
git init

echo.
echo 📝 Добавление всех файлов...
git add .

echo.
echo 💾 Создание коммита...
git commit -m "🎉 v1.0.1 - Initial release with autostart feature"

echo.
echo 🌿 Установка основной ветки...
git branch -M main

echo.
echo 🔗 Подключение к GitHub...
git remote add origin %REPO_URL%

echo.
echo 🚀 Загрузка на GitHub...
git push -u origin main

echo.
echo ========================================
echo ✅ Готово! Проект загружен на GitHub!
echo ========================================
echo.
echo Откройте ваш репозиторий: %REPO_URL%
echo.
pause
