# 📝 Changelog# 📝 Changelog# 📝 Changelog



All notable changes to this project will be documented in this file.



---All notable changes to this project will be documented in this file.Все значительные изменения в проекте документируются в этом файле.



## [v2.0.0] - 2025-10-22



### ⚠️ BREAKING CHANGES------

- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

- **Config structure changed:** New sections added, `[Smoothing]` section removed

- **New dependencies:** keyboard, mouse, pystray, pyusb

- **Autostart path changed:** Registry entry requires update when upgrading## [v2.0.0] - 2025-10-22## [v2.0.0] - 2025-10-22

- **Digispark calibration storage:** Now in config.ini instead of device memory



### 🌍 Localization

- **Full bilingual support:** Russian and English### ⚠️ BREAKING CHANGES### ⚠️ BREAKING CHANGES (Несовместимые изменения)

  - All interface elements translated (60+ strings)

  - Language switcher button in main window- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`- **Переименован главный файл:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

  - Setting saved in config.ini

  - Dynamic text update when switching languages- **Config structure changed:** New sections added, `[Smoothing]` section removed- **Изменена структура config.ini:** Добавлены новые секции, удалена секция `[Smoothing]`

  - Localization system in separate `localization.py` module

- **New dependencies:** keyboard, mouse, pystray, pyusb- **Новые зависимости:** keyboard, mouse, pystray, pyusb

### 🎨 New Theme

- Dark color scheme interface- **Autostart path changed:** Registry entry requires update when upgrading- **Путь автозагрузки изменён:** Требуется обновление записи в реестре при обновлении

  - Modern minimalist design

  - Cyan accent color (#4ec9b0)- **Digispark calibration storage:** Now in config.ini instead of device memory- **Хранение калибровки Digispark:** Теперь в config.ini вместо памяти устройства

  - Consolas monospace font

  - Consistent design across all windows and dialogs

  - Background #1e1e1e, text #d4d4d4

### 🌍 Localization### 🌍 Локализация

### 🔌 Digispark ATtiny85 Support

- **New USB sensor mode**- **Full bilingual support:** Russian and English- **Полная поддержка двух языков:** Русский и Английский

  - Digispark ATtiny85 support via V-USB

  - Automatic connected device detection  - All interface elements translated (60+ strings)  - Все элементы интерфейса переведены (60+ строк)

  - Switch between ESP8266 and Digispark in settings

  - USB device caching (fixed search freezes)  - Language switcher button in main window  - Кнопка переключения языка в главном окне

  - VID: 0x16c0, PID: 0x05df

  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Setting saved in config.ini  - Настройка сохраняется в config.ini



### ⚡ New Features  - Dynamic text update when switching languages  - Динамическое обновление всех текстов при смене языка

- **System tray integration**

  - Minimize on focus loss  - Localization system in separate `localization.py` module  - Система локализации в отдельном модуле `localization.py`

  - `Ctrl+Shift+B` hotkey to show window

  - Tray context menu (Show/Settings/Restart/Exit)

  

- **Manual brightness control**### 🎨 New Theme### 🎨 Новая тема оформления

  - Slider for manual adjustment (1-100%)

  - Global mouse wheel control (works anywhere on screen)- Dark color scheme interface- Тёмная цветовая схема интерфейса

  - Switch between manual and automatic modes

    - Modern minimalist design  - Современный минималистичный дизайн

- **Configurable averaging period**

  - Range: 1-120 seconds (default 10 sec)  - Cyan accent color (#4ec9b0)  - Акцентный бирюзовый цвет (#4ec9b0)

  - Configure via Settings UI

  - Saved in config.ini  - Consolas monospace font  - Моноширинный шрифт Consolas



### 🔧 Technical Improvements  - Consistent design across all windows and dialogs  - Единообразный дизайн всех окон и диалогов

- **Fixed application freezes**

  - Optimized USB device search (caching)  - Background #1e1e1e, text #d4d4d4  - Фон #1e1e1e, текст #d4d4d4

  - Removed blocking when switching modes

  - Smooth interface operation without freezes

  

- **Main file renamed:**### 🔌 Digispark ATtiny85 Support### 🔌 Поддержка Digispark ATtiny85

  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

  - Updated all references in documentation and scripts- **New USB sensor mode**- **Новый режим работы с USB-датчиком**

  

- **Fixed compilation issues:**  - Digispark ATtiny85 support via V-USB  - Поддержка Digispark ATtiny85 через V-USB

  - Resolved settings saving problem in .exe

  - `get_config_path()` function for correct paths  - Automatic connected device detection  - Автоматическое определение подключенного устройства

  - Support for both script and compiled modes

    - Switch between ESP8266 and Digispark in settings  - Переключение между ESP8266 и Digispark в настройках

- **Improved PyInstaller compilation:**

  - Added hidden PIL/Pillow imports  - USB device caching (fixed search freezes)  - Кэширование USB устройств (исправлены зависания при поиске)

  - Fixed TCL/TK library errors

  - Automatic packaging of required dependencies  - VID: 0x16c0, PID: 0x05df  - VID: 0x16c0, PID: 0x05df



### 📦 New Files  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Полная документация в `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)

- `localization.py` - localization module with translations

- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing instructions

- Updated `build.spec` for correct compilation

- English documentation versions (README.md, COMPILE_AND_FLASH.md)### ⚡ New Features### ⚡ Новые возможности



### 🐛 Bug Fixes- **System tray integration**- **Запуск в системном трее**

- Fixed window title centering

- Fixed language button logic (RU = Russian, EN = English)  - Minimize on focus loss  - Сворачивание при потере фокуса

- Eliminated `_imaging` import issue in compiled .exe

- Eliminated `Can't find a usable init.tcl` error when running .exe  - `Ctrl+Shift+B` hotkey to show window  - Горячая клавиша `Ctrl+Shift+B` для вызова окна

- Fixed settings loss after application restart

- Eliminated freezes when searching for USB devices  - Tray context menu (Show/Settings/Restart/Exit)  - Контекстное меню трея (Показать/Настройки/Перезапуск/Выход)



### 📚 Documentation    

- Added complete Digispark ATtiny85 guide

  - Step-by-step firmware compilation instructions- **Manual brightness control**- **Ручная регулировка яркости**

  - Flashing guide via Arduino IDE

  - Common problems and solutions  - Slider for manual adjustment (1-100%)  - Ползунок для ручной настройки (1-100%)

  - Device functionality testing

- Created English version of all documentation  - Global mouse wheel control (works anywhere on screen)  - Глобальная прокрутка мыши (работает в любом месте экрана)

- Updated README.md and all instructions

  - Switch between manual and automatic modes  - Переключение между ручным и автоматическим режимом

### 🔄 Updated Files

- All batch and VBS scripts updated for new filename    

- Synchronized files in Git_Export

- Added requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`- **Configurable averaging period**- **Настраиваемый период усреднения**



---  - Range: 1-120 seconds (default 10 sec)  - Диапазон: 1-120 секунд (по умолчанию 10 сек)



## [v1.0.1] - 2025-10-19  - Configure via Settings UI  - Настройка через Settings UI



### ✨ Added  - Saved in config.ini  - Сохраняется в config.ini

- **Windows Autostart** - checkbox in interface for quick setup

  - Automatic add/remove of Windows registry entry

  - Works for both compiled .exe and Python scripts

  - Automatic Python interpreter detection in virtual environment### 🔧 Technical Improvements### 🔧 Технические улучшения



### 🔧 Improved- **Fixed application freezes**- **Исправлены зависания программы**

- Optimized interface element spacing

  - Reduced padding while maintaining readability  - Optimized USB device search (caching)  - Оптимизирован поиск USB-устройств (кэширование)

  - All elements now visible without scrolling in 450x380 window

  - Compact design without loss of functionality  - Removed blocking when switching modes  - Убрана блокировка при переключении режимов



### 📚 Documentation  - Smooth interface operation without freezes  - Плавная работа интерфейса без фризов

- Updated README.md with autostart feature description

- Added checkbox information in "Usage" section    

- Updated release notes to v1.0.1

- Created CHANGELOG.md for change tracking- **Main file renamed:**- **Переименование главного файла:**



---  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`



## [v1.0.0] - 2025-10-18  - Updated all references in documentation and scripts  - Обновлены все ссылки в документации и скриптах



### 🎉 First Stable Release    



#### ✨ Main Features- **Fixed compilation issues:**- **Исправлена работа компиляции:**

- Automatic brightness adjustment via overlay window

- Smooth transitions between brightness levels (configurable)  - Resolved settings saving problem in .exe  - Решена проблема сохранения настроек в .exe

- Sensor reading averaging (5-60+ seconds)

- System tray with icon and context menu  - `get_config_path()` function for correct paths  - Функция `get_config_path()` для корректных путей

- Configuration via config.ini without code editing

- Click-through transparent overlay window  - Support for both script and compiled modes  - Поддержка как скриптового режима, так и скомпилированного

- Instant context menu dimming (50ms update rate)

    

#### 📡 ESP8266 Firmware

- WiFi connection with configurable static IP- **Improved PyInstaller compilation:**- **Улучшена компиляция PyInstaller:**

- Web calibration interface

- Calibration storage in EEPROM  - Added hidden PIL/Pillow imports  - Добавлены скрытые импорты PIL/Pillow

- HTTP REST API for data retrieval

- Optimized code (HTML ~1800 bytes)  - Fixed TCL/TK library errors  - Исправлена ошибка TCL/TK библиотек

- 1 Hz sensor polling rate

  - Automatic packaging of required dependencies  - Автоматическая упаковка необходимых зависимостей

#### 🛠️ Technical Implementation

- Overlay based on win32 API (WS_EX_LAYERED | WS_EX_TRANSPARENT)

- Smooth brightness change with configurable step

- Automatic reconnection on ESP8266 connection loss### 📦 New Files### 📦 Новые файлы

- Calibration values saved in config.ini

- Custom icon support (icon.ico)- `localization.py` - localization module with translations- `localization.py` - модуль локализации с переводами



#### 📦 Additional- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing instructions- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - инструкция по прошивке ATtiny85

- Launch scripts (.vbs for silent start, .bat with console)

- PyInstaller configuration for .exe compilation- Updated `build.spec` for correct compilation- Обновлённые `build.spec` для корректной компиляции

- Detailed documentation (README.md)

- GPL v3 License- English documentation versions (README.md, COMPILE_AND_FLASH.md)- Английские версии документации (README_EN.md, COMPILE_AND_FLASH_EN.md)

- requirements.txt for easy dependency installation



---

### 🐛 Bug Fixes### 🐛 Исправленные ошибки

## Versioning Format

- Fixed window title centering- Исправлено центрирование заголовка окна

Project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - incompatible API changes- Fixed language button logic (RU = Russian, EN = English)- Исправлена логика кнопки языка (RU = Русский, EN = English)

- **MINOR** (0.X.0) - new functionality with backward compatibility

- **PATCH** (0.0.X) - bug fixes and minor improvements- Eliminated `_imaging` import issue in compiled .exe- Устранена проблема с импортом `_imaging` в скомпилированном .exe



---- Eliminated `Can't find a usable init.tcl` error when running .exe- Устранена ошибка `Can't find a usable init.tcl` при запуске .exe



## Symbol Legend- Fixed settings loss after application restart- Исправлена потеря настроек после перезапуска программы



- ✨ New features- Eliminated freezes when searching for USB devices- Устранены фризы при поиске USB-устройств

- 🔧 Improvements

- 🐛 Bug fixes

- 📚 Documentation

- 🔒 Security### 📚 Documentation### 📚 Документация

- ⚡ Performance

- 🎨 UI/UX changes- Added complete Digispark ATtiny85 guide- Добавлена полная инструкция для Digispark ATtiny85

- ♻️ Refactoring

- 🗑️ Removed  - Step-by-step firmware compilation instructions  - Пошаговые инструкции по компиляции прошивки



---  - Flashing guide via Arduino IDE  - Руководство по прошивке через Arduino IDE



**Full changelog:** [GitHub Releases](../../releases)  - Common problems and solutions  - Решение распространённых проблем


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

