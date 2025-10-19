# 🔄 Как обновлять репозиторий на GitHub

## 📍 Ваш репозиторий
**https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266**

---

## ⚡ Быстрое обновление (3 способа)

### Способ 1: Автоматический скрипт (РЕКОМЕНДУЕТСЯ)

1. Откройте папку `Git_Export`
2. **Двойной клик** на `UPDATE_GITHUB.ps1` (PowerShell)
   - или `UPDATE_GITHUB.bat` (CMD)
3. Следуйте инструкциям на экране

### Способ 2: Через командную строку

Откройте PowerShell в папке `Git_Export` и выполните:

```powershell
# Добавить все изменённые файлы
git add .

# Создать коммит с описанием
git commit -m "Описание изменений"

# Отправить на GitHub
git push origin main
```

### Способ 3: Одной командой

```powershell
git add . ; git commit -m "Update" ; git push origin main
```

---

## 📝 Примеры коммит-сообщений

```powershell
# Исправление бага
git commit -m "🐛 Fix brightness calculation error"

# Новая функция
git commit -m "✨ Add new calibration mode"

# Обновление документации
git commit -m "📚 Update README with new instructions"

# Улучшение производительности
git commit -m "⚡ Optimize overlay rendering"

# Обновление версии
git commit -m "🔖 Release v1.0.2"
```

---

## 🔍 Проверка статуса

Посмотреть какие файлы изменены:
```powershell
git status
```

Посмотреть историю коммитов:
```powershell
git log --oneline
```

---

## 🌿 Работа с ветками

### Создать новую ветку для разработки
```powershell
git checkout -b feature/new-feature
```

### Переключиться обратно на main
```powershell
git checkout main
```

### Слить ветку в main
```powershell
git checkout main
git merge feature/new-feature
git push origin main
```

---

## 📥 Получение изменений с GitHub

Если кто-то другой внёс изменения:
```powershell
git pull origin main
```

---

## 🏷️ Создание новой версии (Release)

### 1. Обновите файлы версии

Отредактируйте:
- `CHANGELOG.md` - добавьте новую версию
- `RELEASE_NOTES_vX.X.X.md` - создайте новый файл
- `README.md` - обновите если нужно

### 2. Создайте коммит
```powershell
git add .
git commit -m "🔖 Release v1.0.2"
git push origin main
```

### 3. Создайте Release на GitHub

1. Откройте: https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266/releases/new
2. Заполните:
   - **Tag:** `v1.0.2`
   - **Title:** `🚀 v1.0.2 - Краткое описание`
   - **Description:** Скопируйте из `RELEASE_NOTES_v1.0.2.md`
3. Нажмите **Publish release**

---

## ❌ Отмена изменений

### Отменить последний коммит (до push)
```powershell
git reset --soft HEAD~1
```

### Отменить все локальные изменения
```powershell
git reset --hard HEAD
```

### Отменить изменения конкретного файла
```powershell
git checkout -- filename.py
```

---

## 🔧 Решение проблем

### "Updates were rejected"
Нужно сначала получить изменения с GitHub:
```powershell
git pull origin main --rebase
git push origin main
```

### "Permission denied"
Нужна авторизация. Создайте Personal Access Token:
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. Выберите права: `repo` (все подпункты)
4. При push используйте токен вместо пароля

### "Merge conflict"
Есть конфликты в файлах:
```powershell
# Использовать вашу версию
git checkout --ours filename.py
git add filename.py

# Или использовать версию с GitHub
git checkout --theirs filename.py
git add filename.py

# Завершить merge
git commit -m "Resolve conflicts"
```

---

## 📊 Полезные команды

```powershell
# Посмотреть изменения в файлах
git diff

# Посмотреть изменения в конкретном файле
git diff filename.py

# Удалить неотслеживаемые файлы
git clean -fd

# Посмотреть remote URL
git remote -v

# Изменить remote URL
git remote set-url origin NEW_URL

# Посмотреть все ветки
git branch -a

# Удалить ветку
git branch -d branch-name
```

---

## 📱 Использование .gitignore

Файл `.gitignore` уже настроен. Он исключает:
- `__pycache__/` - кэш Python
- `.venv/` - виртуальное окружение
- `dist/`, `build/` - результаты компиляции
- `*.pyc`, `*.pyo` - скомпилированные файлы Python

Если нужно добавить новые исключения, отредактируйте `.gitignore`

---

## 🎓 Дополнительная информация

### Официальная документация Git
- https://git-scm.com/doc

### GitHub Docs
- https://docs.github.com/

### Интерактивное обучение Git
- https://learngitbranching.js.org/

---

## ✅ Чеклист обновления

Перед каждым push проверьте:

- [ ] Все файлы сохранены
- [ ] Код работает без ошибок
- [ ] Документация обновлена (если нужно)
- [ ] `CHANGELOG.md` дополнен (для версий)
- [ ] Коммит-сообщение понятное
- [ ] Нет чувствительных данных (пароли, токены)

---

**Репозиторий:** https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266  
**Последнее обновление:** 2025-10-19  
**Текущая версия:** v1.0.1
