# Скрипт для обновления существующего репозитория на GitHub
# Repository: https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📤 Обновление GitHub репозитория" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = "https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266.git"

# Проверка наличия Git
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "❌ Git не установлен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Скачайте Git с: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✅ Git найден" -ForegroundColor Green
Write-Host "📁 Репозиторий: STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266" -ForegroundColor Cyan
Write-Host ""

# Проверка, инициализирован ли Git
if (-not (Test-Path ".git")) {
    Write-Host "🔄 Git не инициализирован, инициализирую..." -ForegroundColor Yellow
    git init
    git branch -M main
    git remote add origin $repoUrl
    Write-Host "✅ Git инициализирован" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✅ Git уже инициализирован" -ForegroundColor Green
    Write-Host ""
    
    # Проверка remote
    $currentRemote = git remote get-url origin 2>$null
    if ($currentRemote -ne $repoUrl) {
        Write-Host "🔄 Обновляю remote URL..." -ForegroundColor Yellow
        git remote set-url origin $repoUrl
    }
}

# Показать статус
Write-Host "📊 Статус файлов:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Запрос подтверждения
$continue = Read-Host "Продолжить отправку изменений? (y/n)"
if ($continue -ne "y") {
    Write-Host "❌ Отменено" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 0
}

Write-Host ""
Write-Host "📝 Добавление всех файлов..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "💾 Создание коммита..." -ForegroundColor Cyan
$commitMessage = Read-Host "Введите сообщение коммита (Enter для использования по умолчанию)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "📝 Update v1.0.1 - Added autostart feature and updated documentation"
}

git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Нет изменений для коммита" -ForegroundColor Yellow
    Write-Host ""
    $forcePush = Read-Host "Попробовать отправить существующие коммиты? (y/n)"
    if ($forcePush -ne "y") {
        Read-Host "Нажмите Enter для выхода"
        exit 0
    }
}

Write-Host ""
Write-Host "🚀 Отправка на GitHub..." -ForegroundColor Cyan
Write-Host "⏳ Это может занять некоторое время..." -ForegroundColor Yellow
Write-Host ""

git push -u origin main 2>&1 | Out-String | Write-Host

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Изменения отправлены на GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Репозиторий: https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266" -ForegroundColor Cyan
    Write-Host ""
    
    $openBrowser = Read-Host "Открыть репозиторий в браузере? (y/n)"
    if ($openBrowser -eq "y") {
        Start-Process "https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266"
    }
} else {
    Write-Host ""
    Write-Host "❌ Ошибка при отправке на GitHub!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Возможные причины:" -ForegroundColor Yellow
    Write-Host "1. Нужна авторизация (Personal Access Token или SSH)" -ForegroundColor Yellow
    Write-Host "2. Есть конфликты с удалённой версией" -ForegroundColor Yellow
    Write-Host "3. Нет прав доступа к репозиторию" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Решение:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Вариант 1: Создайте Personal Access Token" -ForegroundColor White
    Write-Host "1. Откройте: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "2. Generate new token (classic)" -ForegroundColor Gray
    Write-Host "3. Выберите права: repo (все подпункты)" -ForegroundColor Gray
    Write-Host "4. При push используйте токен вместо пароля" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Вариант 2: Сначала получите изменения с GitHub" -ForegroundColor White
    Write-Host "  git pull origin main --rebase" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
    Write-Host ""
}

Read-Host "Нажмите Enter для выхода"
