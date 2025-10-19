# 🚀 Инструкция по созданию релиза на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните поля:
   - **Repository name:** `AutoBrightOLED` (или другое имя)
   - **Description:** `🔆 Автоматическая регулировка яркости OLED-монитора через ESP8266 с датчиком света`
   - **Public** или **Private** (на ваш выбор)
   - ✅ Add README file (можно пропустить, у вас уже есть)
   - **License:** MIT License
3. Нажмите **Create repository**

## Шаг 2: Добавьте Topics (теги)

На странице репозитория нажмите ⚙️ рядом с **About** и добавьте теги:
```
oled
brightness-control
esp8266
python
arduino
iot
automation
overlay
screen-dimming
ambient-light-sensor
windows
home-automation
```

## Шаг 3: Загрузите код

### Вариант A: Через Git командную строку

```bash
cd Git_Export

# Инициализация репозитория
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "🎉 v1.0.1 - Initial release with autostart feature"

# Подключение к GitHub (замените YOUR_USERNAME на ваше имя)
git remote add origin https://github.com/YOUR_USERNAME/AutoBrightOLED.git

# Установка основной ветки
git branch -M main

# Загрузка кода
git push -u origin main
```

### Вариант B: Через GitHub Desktop

1. Откройте GitHub Desktop
2. File → Add Local Repository → выберите папку `Git_Export`
3. Создайте коммит: "🎉 v1.0.1 - Initial release with autostart feature"
4. Publish repository → выберите GitHub.com
5. Нажмите **Publish**

### Вариант C: Загрузка файлов через веб-интерфейс

1. Откройте ваш репозиторий на GitHub
2. Нажмите **Add file** → **Upload files**
3. Перетащите все файлы из папки `Git_Export`
4. Commit message: `🎉 v1.0.1 - Initial release with autostart feature`
5. Нажмите **Commit changes**

## Шаг 4: Создайте Release

1. Перейдите на страницу вашего репозитория
2. Справа найдите секцию **Releases** → **Create a new release**
3. Заполните поля:

   **Tag version:**
   ```
   v1.0.1
   ```

   **Release title:**
   ```
   🚀 v1.0.1 - Autostart Update
   ```

   **Description:** (скопируйте из `RELEASE_NOTES_v1.0.1.md`)
   ```markdown
   ## 🆕 Что нового в v1.0.1

   ### ✨ Новые функции
   - **🚀 Автозагрузка Windows** - простая галочка в интерфейсе
     - Автоматическое добавление в реестр Windows
     - Работает как для .exe, так и для Python скриптов
   
   ### 🔧 Улучшения интерфейса
   - Оптимизированы отступы для компактности
   - Все элементы видны без прокрутки
   
   ---
   
   📦 **Что включено:**
   - Исходный код Python программы
   - Прошивка ESP8266 (Arduino)
   - Полная документация
   - Скрипты запуска
   - Конфигурация для компиляции
   
   📚 Полная инструкция в [README.md](README.md)
   ```

4. **Прикрепите файлы (Assets):**
   - Если у вас есть скомпилированный `.exe`, создайте zip-архив:
     - `OLED_AutoBrightness_v1.0.1_Windows.zip` (содержит .exe, config.ini, icon.ico)
   - Или просто укажите, что релиз - source code

5. ✅ **This is a pre-release** - снимите галочку (это стабильная версия)
6. Нажмите **Publish release**

## Шаг 5: Обновите README.md на GitHub

GitHub автоматически отобразит ваш README.md на главной странице репозитория.

Проверьте, что отображается корректно:
- ✅ Эмодзи видны
- ✅ Блоки кода форматированы
- ✅ Ссылки работают
- ✅ Изображения загружены (если есть)

## Шаг 6: (Опционально) Добавьте скриншоты

1. Создайте папку `screenshots` в репозитории
2. Добавьте скриншоты:
   - `main_window.png` - главное окно программы
   - `calibration_web.png` - веб-интерфейс ESP8266
   - `tray_menu.png` - меню в системном трее
3. Вставьте в README.md:
   ```markdown
   ## 📸 Скриншоты
   
   ### Главное окно
   ![Main Window](screenshots/main_window.png)
   
   ### Веб-интерфейс калибровки
   ![Calibration](screenshots/calibration_web.png)
   ```

## Шаг 7: Поделитесь проектом

### Reddit
- r/esp8266
- r/arduino
- r/python
- r/homeautomation

### Twitter / X
```
🔆 Новый релиз: OLED Auto Brightness v1.0.1

Автоматическая регулировка яркости монитора через ESP8266
✨ Теперь с автозагрузкой Windows!

#ESP8266 #Python #IoT #OpenSource

https://github.com/YOUR_USERNAME/AutoBrightOLED
```

### LinkedIn / Facebook
Используйте текст из `PROJECT_DESCRIPTION.md` → раздел LinkedIn / Facebook

---

## ✅ Чеклист релиза

- [ ] Репозиторий создан на GitHub
- [ ] Topics (теги) добавлены
- [ ] Код загружен (все файлы из Git_Export)
- [ ] Release v1.0.1 создан
- [ ] README.md отображается корректно
- [ ] License (MIT) указан
- [ ] .gitignore настроен (исключает __pycache__, .venv и т.д.)
- [ ] (Опционально) Скриншоты добавлены
- [ ] (Опционально) GitHub Pages включен
- [ ] (Опционально) GitHub Discussions включен

---

## 🔄 Обновление релиза в будущем

Для создания нового релиза (например, v1.0.2):

1. Внесите изменения в код
2. Обновите `CHANGELOG.md`
3. Обновите `RELEASE_NOTES_vX.X.X.md`
4. Сделайте коммит:
   ```bash
   git add .
   git commit -m "🔧 v1.0.2 - Bug fixes and improvements"
   git push
   ```
5. Создайте новый Release на GitHub с тегом `v1.0.2`

---

**Удачи с вашим проектом! 🚀**
