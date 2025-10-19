# Скрипт автоматической загрузки на GitHub
# Кодировка: UTF-8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Быстрая загрузка на GitHub" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверка наличия Git
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "❌ Git не установлен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Скачайте Git с: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✅ Git найден" -ForegroundColor Green
Write-Host ""

# Запрос URL репозитория
$repoUrl = Read-Host "Введите URL вашего GitHub репозитория (например, https://github.com/USERNAME/AutoBrightOLED.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ URL не указан!" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Проверка, не инициализирован ли уже Git
if (Test-Path ".git") {
    Write-Host "⚠️  Git уже инициализирован в этой папке" -ForegroundColor Yellow
    $continue = Read-Host "Продолжить? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
} else {
    Write-Host ""
    Write-Host "📦 Инициализация Git репозитория..." -ForegroundColor Cyan
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка инициализации Git" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

Write-Host ""
Write-Host "📝 Добавление всех файлов..." -ForegroundColor Cyan
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка добавления файлов" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host ""
Write-Host "💾 Создание коммита..." -ForegroundColor Cyan
git commit -m "🎉 v1.0.1 - Initial release with autostart feature"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Возможно, нет изменений для коммита" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌿 Установка основной ветки..." -ForegroundColor Cyan
git branch -M main

Write-Host ""
Write-Host "🔗 Подключение к GitHub..." -ForegroundColor Cyan
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' уже существует, обновляю..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

Write-Host ""
Write-Host "🚀 Загрузка на GitHub..." -ForegroundColor Cyan
Write-Host "⏳ Это может занять некоторое время..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Готово! Проект загружен на GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Откройте ваш репозиторий: $repoUrl" -ForegroundColor Cyan
    Write-Host ""
    
    # Попытка открыть в браузере
    $openBrowser = Read-Host "Открыть репозиторий в браузере? (y/n)"
    if ($openBrowser -eq "y") {
        $repoWebUrl = $repoUrl -replace "\.git$", ""
        Start-Process $repoWebUrl
    }
} else {
    Write-Host ""
    Write-Host "❌ Ошибка при загрузке на GitHub!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Возможные причины:" -ForegroundColor Yellow
    Write-Host "1. Репозиторий не создан на GitHub" -ForegroundColor Yellow
    Write-Host "2. Неверный URL репозитория" -ForegroundColor Yellow
    Write-Host "3. Нет прав доступа (нужна авторизация)" -ForegroundColor Yellow
    Write-Host "4. Репозиторий уже содержит файлы (используйте git pull сначала)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Для авторизации в GitHub используйте:" -ForegroundColor Cyan
    Write-Host "  git config --global user.name 'Ваше Имя'" -ForegroundColor White
    Write-Host "  git config --global user.email 'your@email.com'" -ForegroundColor White
    Write-Host ""
}

Read-Host "Нажмите Enter для выхода"
