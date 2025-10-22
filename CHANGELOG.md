# 📝 Changelog# 📝 Changelog



All notable changes to this project will be documented in this file.Все значительные изменения в проекте документируются в этом файле.



------



## [v2.0.0] - 2025-10-22## [v2.0.0] - 2025-10-22



### ⚠️ BREAKING CHANGES### ⚠️ BREAKING CHANGES (Несовместимые изменения)

- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`- **Переименован главный файл:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

- **Config structure changed:** New sections added, `[Smoothing]` section removed- **Изменена структура config.ini:** Добавлены новые секции, удалена секция `[Smoothing]`

- **New dependencies:** keyboard, mouse, pystray, pyusb- **Новые зависимости:** keyboard, mouse, pystray, pyusb

- **Autostart path changed:** Registry entry requires update when upgrading- **Путь автозагрузки изменён:** Требуется обновление записи в реестре при обновлении

- **Digispark calibration storage:** Now in config.ini instead of device memory- **Хранение калибровки Digispark:** Теперь в config.ini вместо памяти устройства



### 🌍 Localization### 🌍 Локализация

- **Full bilingual support:** Russian and English- **Полная поддержка двух языков:** Русский и Английский

  - All interface elements translated (60+ strings)  - Все элементы интерфейса переведены (60+ строк)

  - Language switcher button in main window  - Кнопка переключения языка в главном окне

  - Setting saved in config.ini  - Настройка сохраняется в config.ini

  - Dynamic text update when switching languages  - Динамическое обновление всех текстов при смене языка

  - Localization system in separate `localization.py` module  - Система локализации в отдельном модуле `localization.py`



### 🎨 New Theme### 🎨 Новая тема оформления

- Dark color scheme interface- Тёмная цветовая схема интерфейса

  - Modern minimalist design  - Современный минималистичный дизайн

  - Cyan accent color (#4ec9b0)  - Акцентный бирюзовый цвет (#4ec9b0)

  - Consolas monospace font  - Моноширинный шрифт Consolas

  - Consistent design across all windows and dialogs  - Единообразный дизайн всех окон и диалогов

  - Background #1e1e1e, text #d4d4d4  - Фон #1e1e1e, текст #d4d4d4



### 🔌 Digispark ATtiny85 Support### 🔌 Поддержка Digispark ATtiny85

- **New USB sensor mode**- **Новый режим работы с USB-датчиком**

  - Digispark ATtiny85 support via V-USB  - Поддержка Digispark ATtiny85 через V-USB

  - Automatic connected device detection  - Автоматическое определение подключенного устройства

  - Switch between ESP8266 and Digispark in settings  - Переключение между ESP8266 и Digispark в настройках

  - USB device caching (fixed search freezes)  - Кэширование USB устройств (исправлены зависания при поиске)

  - VID: 0x16c0, PID: 0x05df  - VID: 0x16c0, PID: 0x05df

  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Полная документация в `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)



### ⚡ New Features### ⚡ Новые возможности

- **System tray integration**- **Запуск в системном трее**

  - Minimize on focus loss  - Сворачивание при потере фокуса

  - `Ctrl+Shift+B` hotkey to show window  - Горячая клавиша `Ctrl+Shift+B` для вызова окна

  - Tray context menu (Show/Settings/Restart/Exit)  - Контекстное меню трея (Показать/Настройки/Перезапуск/Выход)

    

- **Manual brightness control**- **Ручная регулировка яркости**

  - Slider for manual adjustment (1-100%)  - Ползунок для ручной настройки (1-100%)

  - Global mouse wheel control (works anywhere on screen)  - Глобальная прокрутка мыши (работает в любом месте экрана)

  - Switch between manual and automatic modes  - Переключение между ручным и автоматическим режимом

    

- **Configurable averaging period**- **Настраиваемый период усреднения**

  - Range: 1-120 seconds (default 10 sec)  - Диапазон: 1-120 секунд (по умолчанию 10 сек)

  - Configure via Settings UI  - Настройка через Settings UI

  - Saved in config.ini  - Сохраняется в config.ini



### 🔧 Technical Improvements### 🔧 Технические улучшения

- **Fixed application freezes**- **Исправлены зависания программы**

  - Optimized USB device search (caching)  - Оптимизирован поиск USB-устройств (кэширование)

  - Removed blocking when switching modes  - Убрана блокировка при переключении режимов

  - Smooth interface operation without freezes  - Плавная работа интерфейса без фризов

    

- **Main file renamed:**- **Переименование главного файла:**

  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

  - Updated all references in documentation and scripts  - Обновлены все ссылки в документации и скриптах

    

- **Fixed compilation issues:**- **Исправлена работа компиляции:**

  - Resolved settings saving problem in .exe  - Решена проблема сохранения настроек в .exe

  - `get_config_path()` function for correct paths  - Функция `get_config_path()` для корректных путей

  - Support for both script and compiled modes  - Поддержка как скриптового режима, так и скомпилированного

    

- **Improved PyInstaller compilation:**- **Улучшена компиляция PyInstaller:**

  - Added hidden PIL/Pillow imports  - Добавлены скрытые импорты PIL/Pillow

  - Fixed TCL/TK library errors  - Исправлена ошибка TCL/TK библиотек

  - Automatic packaging of required dependencies  - Автоматическая упаковка необходимых зависимостей



### 📦 New Files### 📦 Новые файлы

- `localization.py` - localization module with translations- `localization.py` - модуль локализации с переводами

- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing instructions- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - инструкция по прошивке ATtiny85

- Updated `build.spec` for correct compilation- Обновлённые `build.spec` для корректной компиляции

- English documentation versions (README.md, COMPILE_AND_FLASH.md)- Английские версии документации (README_EN.md, COMPILE_AND_FLASH_EN.md)



### 🐛 Bug Fixes### 🐛 Исправленные ошибки

- Fixed window title centering- Исправлено центрирование заголовка окна

- Fixed language button logic (RU = Russian, EN = English)- Исправлена логика кнопки языка (RU = Русский, EN = English)

- Eliminated `_imaging` import issue in compiled .exe- Устранена проблема с импортом `_imaging` в скомпилированном .exe

- Eliminated `Can't find a usable init.tcl` error when running .exe- Устранена ошибка `Can't find a usable init.tcl` при запуске .exe

- Fixed settings loss after application restart- Исправлена потеря настроек после перезапуска программы

- Eliminated freezes when searching for USB devices- Устранены фризы при поиске USB-устройств



### 📚 Documentation### 📚 Документация

- Added complete Digispark ATtiny85 guide- Добавлена полная инструкция для Digispark ATtiny85

  - Step-by-step firmware compilation instructions  - Пошаговые инструкции по компиляции прошивки

  - Flashing guide via Arduino IDE  - Руководство по прошивке через Arduino IDE

  - Common problems and solutions  - Решение распространённых проблем

  - Device functionality testing  - Проверка работоспособности устройства

- Created English version of all documentation- Создана английская версия всей документации

- Updated README.md and all instructions- Обновлены README.md и все инструкции



### 🔄 Updated Files### 🔄 Обновлённые файлы

- All batch and VBS scripts updated for new filename- Все батники и VBS скрипты обновлены под новое имя файла

- Synchronized files in Git_Export- Синхронизированы файлы в Git_Export

- Added requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`- Добавлены requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`



------



## [v1.0.1] - 2025-10-19## [v1.0.1] - 2025-10-19



### ✨ Added### ✨ Добавлено

- **Windows Autostart** - checkbox in interface for quick setup- **Автозагрузка Windows** - чекбокс в интерфейсе для быстрой настройки

  - Automatic add/remove of Windows registry entry  - Автоматическое добавление/удаление записи в реестре Windows

  - Works for both compiled .exe and Python scripts  - Работает как для скомпилированного .exe, так и для Python скриптов

  - Automatic Python interpreter detection in virtual environment  - Автоматический поиск Python интерпретатора в виртуальном окружении



### 🔧 Improved### 🔧 Улучшено

- Optimized interface element spacing- Оптимизированы отступы между элементами интерфейса

  - Reduced padding while maintaining readability  - Уменьшены отступы с сохранением читаемости

  - All elements now visible without scrolling in 450x380 window  - Все элементы теперь видны без прокрутки в окне 450x380

  - Compact design without loss of functionality  - Компактный дизайн без потери функциональности



### 📚 Documentation### 📚 Документация

- Updated README.md with autostart feature description- Обновлён README.md с описанием функции автозагрузки

- Added checkbox information in "Usage" section- Добавлена информация о чекбоксе в разделе "Использование"

- Updated release notes to v1.0.1- Обновлены release notes на v1.0.1

- Created CHANGELOG.md for change tracking- Создан CHANGELOG.md для отслеживания изменений



------



## [v1.0.0] - 2025-10-18## [v1.0.0] - 2025-10-18



### 🎉 First Stable Release### 🎉 Первый стабильный релиз



#### ✨ Main Features#### ✨ Основные функции

- Automatic brightness adjustment via overlay window- Автоматическая регулировка яркости через overlay-окно

- Smooth transitions between brightness levels (configurable)- Плавные переходы между уровнями яркости (настраиваемые)

- Sensor reading averaging (5-60+ seconds)- Усреднение показаний датчика (5-60+ секунд)

- System tray with icon and context menu- Системный трей с иконкой и контекстным меню

- Configuration via config.ini without code editing- Настройка через config.ini без редактирования кода

- Click-through transparent overlay window- Прозрачное для кликов overlay-окно

- Instant context menu dimming (50ms update rate)- Мгновенное затенение контекстных меню (50мс обновление)



#### 📡 ESP8266 Firmware#### 📡 ESP8266 Firmware

- WiFi connection with configurable static IP- WiFi подключение с настраиваемым статическим IP

- Web calibration interface- Веб-интерфейс калибровки датчика

- Calibration storage in EEPROM- Сохранение калибровки в EEPROM

- HTTP REST API for data retrieval- HTTP REST API для получения данных

- Optimized code (HTML ~1800 bytes)- Оптимизированный код (HTML ~1800 байт)

- 1 Hz sensor polling rate- Частота опроса датчика 1 Гц



#### 🛠️ Technical Implementation#### 🛠️ Техническая реализация

- Overlay based on win32 API (WS_EX_LAYERED | WS_EX_TRANSPARENT)- Overlay на базе win32 API (WS_EX_LAYERED | WS_EX_TRANSPARENT)

- Smooth brightness change with configurable step- Плавное изменение яркости с настраиваемым шагом

- Automatic reconnection on ESP8266 connection loss- Автоматическое переподключение при потере связи с ESP8266

- Calibration values saved in config.ini- Сохранение калибровочных значений в config.ini

- Custom icon support (icon.ico)- Поддержка custom иконки (icon.ico)



#### 📦 Additional#### 📦 Дополнительно

- Launch scripts (.vbs for silent start, .bat with console)- Скрипты запуска (.vbs для невидимого старта, .bat с консолью)

- PyInstaller configuration for .exe compilation- Конфигурация PyInstaller для компиляции в .exe

- Detailed documentation (README.md)- Подробная документация (README.md)

- GPL v3 License- MIT лицензия

- requirements.txt for easy dependency installation- requirements.txt для простой установки зависимостей



------



## Versioning Format## Формат версионирования



Project uses [Semantic Versioning](https://semver.org/):Проект использует [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - incompatible API changes- **MAJOR** (X.0.0) - несовместимые изменения API

- **MINOR** (0.X.0) - new functionality with backward compatibility- **MINOR** (0.X.0) - новая функциональность с обратной совместимостью

- **PATCH** (0.0.X) - bug fixes and minor improvements- **PATCH** (0.0.X) - исправления и мелкие улучшения



------



## Symbol Legend## Легенда символов



- ✨ New features- ✨ Новые функции

- 🔧 Improvements- 🔧 Улучшения

- 🐛 Bug fixes- 🐛 Исправления багов

- 📚 Documentation- 📚 Документация

- 🔒 Security- 🔒 Безопасность

- ⚡ Performance- ⚡ Производительность

- 🎨 UI/UX changes- 🎨 UI/UX изменения

- ♻️ Refactoring- ♻️ Рефакторинг

- 🗑️ Removed- 🗑️ Удалённое



------



**Full changelog:** [GitHub Releases](../../releases)**Полный список изменений:** [GitHub Releases](../../releases)

