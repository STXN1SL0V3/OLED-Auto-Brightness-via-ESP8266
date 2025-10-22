# 📝 Changelog# 📝 Changelog# 📝 Changelog# 📝 Changelog# 📝 Changelog



All notable changes to this project will be documented in this file.



---All notable changes to this project will be documented in this file.



## [v2.0.0] - 2025-10-22



### ⚠️ BREAKING CHANGES---All notable changes to this project will be documented in this file.

- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

- **Config structure changed:** New sections added, `[Smoothing]` section removed.

- **New dependencies:** `keyboard`, `mouse`, `pystray`, `pyusb` are now required.

- **Autostart path changed:** Registry entry requires an update when upgrading from a previous version.## [v2.0.0] - 2025-10-22

- **Digispark calibration storage:** Calibration data is now stored in `config.ini` instead of the device's memory.



### 🌍 Localization

- **Full bilingual support:** The interface is now fully translated into Russian and English.### ⚠️ BREAKING CHANGES---All notable changes to this project will be documented in this file.Все значительные изменения в проекте документируются в этом файле.

  - Over 60 strings have been localized.

  - A language switcher button has been added to the main window.- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

  - The selected language is saved in `config.ini`.

  - All text updates dynamically when the language is switched.- **Config structure changed:** New sections added, `[Smoothing]` section removed

  - The localization system is handled by a separate `localization.py` module.

- **New dependencies:** keyboard, mouse, pystray, pyusb

### 🎨 New Theme

- **Dark color scheme:** A modern, minimalist dark theme has been implemented.- **Autostart path changed:** Registry entry requires update when upgrading## [v2.0.0] - 2025-10-22

  - Features a cyan accent color (`#4ec9b0`).

  - Uses the Consolas monospace font for clarity.- **Digispark calibration storage:** Now in config.ini instead of device memory

  - Consistent design across all windows and dialogs.

  - Background: `#1e1e1e`, Text: `#d4d4d4`.



### 🔌 Digispark ATtiny85 Support### 🌍 Localization

- **New USB sensor mode:** Added support for the Digispark ATtiny85 as a USB light sensor.

  - Utilizes the V-USB library for software-based USB communication.- **Full bilingual support:** Russian and English### ⚠️ BREAKING CHANGES------

  - Automatic detection of the connected device.

  - A setting to switch between ESP8266 and Digispark has been added.  - All interface elements translated (60+ strings)

  - Implemented USB device caching to prevent freezes during device search.

  - VID: `0x16c0`, PID: `0x05df`.  - Language switcher button in main window- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

  - Full documentation is available in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN).

  - Setting saved in config.ini

### ⚡ New Features

- **System tray integration:**  - Dynamic text update when switching languages- **Config structure changed:** New sections added, `[Smoothing]` section removed

  - The application now minimizes to the system tray on focus loss.

  - A global hotkey `Ctrl+Shift+B` has been added to show/hide the main window.  - Localization system in separate `localization.py` module

  - The tray icon includes a context menu with Show, Settings, Restart, and Exit options.

- **Manual brightness control:**- **New dependencies:** keyboard, mouse, pystray, pyusb

  - A slider for manual brightness adjustment (1-100%) has been added.

  - Global mouse wheel control over the tray icon allows for brightness changes from anywhere.### 🎨 New Theme

  - A toggle to switch between manual and automatic modes is now available.

- **Configurable averaging period:**- Dark color scheme interface- **Autostart path changed:** Registry entry requires update when upgrading## [v2.0.0] - 2025-10-22## [v2.0.0] - 2025-10-22

  - The sensor reading averaging period is now configurable from 1 to 120 seconds (default: 10s).

  - This can be adjusted via the Settings UI and is saved in `config.ini`.  - Modern minimalist design



### 🔧 Technical Improvements  - Cyan accent color (#4ec9b0)- **Digispark calibration storage:** Now in config.ini instead of device memory

- **Fixed application freezes:**

  - Optimized USB device search with caching.  - Consolas monospace font

  - Removed blocking calls when switching modes for a smoother UI.

- **Main file renamed:**  - Consistent design across all windows and dialogs

  - `simple_auto_brightness.py` is now `OLED_Auto_Brightness.py`.

  - All references in documentation and scripts have been updated.  - Background #1e1e1e, text #d4d4d4

- **Fixed compilation issues:**

  - Resolved an issue where settings were not saved correctly in the compiled `.exe`.### 🌍 Localization

  - The `get_config_path()` function now ensures correct paths in both script and compiled modes.

- **Improved PyInstaller compilation:**### 🔌 Digispark ATtiny85 Support

  - Added hidden imports for PIL/Pillow to prevent errors.

  - Fixed issues related to TCL/TK library packaging.- **New USB sensor mode**- **Full bilingual support:** Russian and English### ⚠️ BREAKING CHANGES### ⚠️ BREAKING CHANGES (Несовместимые изменения)



### 📦 New Files  - Digispark ATtiny85 support via V-USB

- `localization.py`: A new module for handling translations.

- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md`: Flashing instructions for the ATtiny85.  - Automatic connected device detection  - All interface elements translated (60+ strings)

- Updated `build.spec` for correct compilation.

  - Switch between ESP8266 and Digispark in settings

### 🐛 Bug Fixes

- Fixed window title centering.  - USB device caching (fixed search freezes)  - Language switcher button in main window- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`- **Переименован главный файл:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`

- Corrected the logic of the language button (RU/EN).

- Eliminated `_imaging` import issues in the compiled `.exe`.  - VID: 0x16c0, PID: 0x05df

- Resolved the `Can't find a usable init.tcl` error when running the `.exe`.

- Fixed an issue where settings were lost after an application restart.  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Setting saved in config.ini

- Eliminated freezes that occurred when searching for USB devices.



### 📚 Documentation

- Added a complete guide for the Digispark ATtiny85.### ⚡ New Features  - Dynamic text update when switching languages- **Config structure changed:** New sections added, `[Smoothing]` section removed- **Изменена структура config.ini:** Добавлены новые секции, удалена секция `[Smoothing]`

- Created English versions of all documentation.

- Updated `README.md` and all related instructions.- **System tray integration**



### 🔄 Updated Files  - Minimize on focus loss  - Localization system in separate `localization.py` module

- All batch and VBS scripts have been updated to use the new main filename.

- Synchronized files in the `Git_Export` directory.  - `Ctrl+Shift+B` hotkey to show window

- Added new requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`.

  - Tray context menu (Show/Settings/Restart/Exit)- **New dependencies:** keyboard, mouse, pystray, pyusb- **Новые зависимости:** keyboard, mouse, pystray, pyusb

---

  

## [v1.0.1] - 2025-10-19

- **Manual brightness control**### 🎨 New Theme

### ✨ Added

- **Windows Autostart:** A checkbox in the UI now allows for quick setup of autostart.  - Slider for manual adjustment (1-100%)

  - Automatically adds/removes the necessary Windows registry entry.

  - Works for both the compiled `.exe` and Python scripts.  - Global mouse wheel control (works anywhere on screen)- Dark color scheme interface- **Autostart path changed:** Registry entry requires update when upgrading- **Путь автозагрузки изменён:** Требуется обновление записи в реестре при обновлении

  - Includes automatic detection of the Python interpreter in a virtual environment.

  - Switch between manual and automatic modes

### 🔧 Improved

- **Optimized UI spacing:**    - Modern minimalist design

  - Reduced padding between elements for a more compact layout.

  - All elements are now visible in a 450x380 window without scrolling.- **Configurable averaging period**



### 📚 Documentation  - Range: 1-120 seconds (default 10 sec)  - Cyan accent color (#4ec9b0)- **Digispark calibration storage:** Now in config.ini instead of device memory- **Хранение калибровки Digispark:** Теперь в config.ini вместо памяти устройства

- Updated `README.md` with a description of the new autostart feature.

- Created `CHANGELOG.md` for tracking changes.  - Configure via Settings UI



---  - Saved in config.ini  - Consolas monospace font



## [v1.0.0] - 2025-10-18



### 🎉 First Stable Release### 🔧 Technical Improvements  - Consistent design across all windows and dialogs



#### ✨ Main Features- **Fixed application freezes**

- Automatic brightness adjustment via a transparent overlay window.

- Smooth, configurable transitions between brightness levels.  - Optimized USB device search (caching)  - Background #1e1e1e, text #d4d4d4

- Averaging of sensor readings (5-60+ seconds).

- System tray icon with a context menu.  - Removed blocking when switching modes

- Configuration via `config.ini` without needing to edit code.

- Click-through transparent overlay window.  - Smooth interface operation without freezes### 🌍 Localization### 🌍 Локализация



#### 📡 ESP8266 Firmware  

- WiFi connection with a configurable static IP.

- Web interface for sensor calibration.- **Main file renamed:**### 🔌 Digispark ATtiny85 Support

- Calibration storage in EEPROM.

- HTTP REST API for retrieving sensor data.  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`



#### 🛠️ Technical Implementation  - Updated all references in documentation and scripts- **New USB sensor mode**- **Full bilingual support:** Russian and English- **Полная поддержка двух языков:** Русский и Английский

- Overlay based on the win32 API (`WS_EX_LAYERED | WS_EX_TRANSPARENT`).

- Automatic reconnection on ESP8266 connection loss.  

- Custom icon support (`icon.ico`).

- **Fixed compilation issues:**  - Digispark ATtiny85 support via V-USB

#### 📦 Additional

- Launch scripts (`.vbs` for silent start, `.bat` with console).  - Resolved settings saving problem in .exe

- PyInstaller configuration for `.exe` compilation.

- Detailed documentation (`README.md`).  - `get_config_path()` function for correct paths  - Automatic connected device detection  - All interface elements translated (60+ strings)  - Все элементы интерфейса переведены (60+ строк)

- GPL v3 License.

- `requirements.txt` for easy dependency installation.  - Support for both script and compiled modes



---    - Switch between ESP8266 and Digispark in settings



## Versioning Format- **Improved PyInstaller compilation:**



This project uses [Semantic Versioning](https://semver.org/):  - Added hidden PIL/Pillow imports  - USB device caching (fixed search freezes)  - Language switcher button in main window  - Кнопка переключения языка в главном окне

- **MAJOR** (`X.0.0`) - Incompatible API changes.

- **MINOR** (`0.X.0`) - New functionality with backward compatibility.  - Fixed TCL/TK library errors

- **PATCH** (`0.0.X`) - Bug fixes and minor improvements.

  - Automatic packaging of required dependencies  - VID: 0x16c0, PID: 0x05df

---



## Symbol Legend

### 📦 New Files  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Setting saved in config.ini  - Настройка сохраняется в config.ini

- ✨ New features

- 🔧 Improvements- `localization.py` - localization module with translations

- 🐛 Bug fixes

- 📚 Documentation- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing instructions

- 🔒 Security

- ⚡ Performance- Updated `build.spec` for correct compilation

- 🎨 UI/UX changes

- ♻️ Refactoring- English documentation versions (README.md, COMPILE_AND_FLASH.md)### ⚡ New Features  - Dynamic text update when switching languages  - Динамическое обновление всех текстов при смене языка

- 🗑️ Removed



---

### 🐛 Bug Fixes- **System tray integration**

**Full changelog:** [GitHub Releases](../../releases)

- Fixed window title centering

- Fixed language button logic (RU = Russian, EN = English)  - Minimize on focus loss  - Localization system in separate `localization.py` module  - Система локализации в отдельном модуле `localization.py`

- Eliminated `_imaging` import issue in compiled .exe

- Eliminated `Can't find a usable init.tcl` error when running .exe  - `Ctrl+Shift+B` hotkey to show window

- Fixed settings loss after application restart

- Eliminated freezes when searching for USB devices  - Tray context menu (Show/Settings/Restart/Exit)



### 📚 Documentation  

- Added complete Digispark ATtiny85 guide

  - Step-by-step firmware compilation instructions- **Manual brightness control**### 🎨 New Theme### 🎨 Новая тема оформления

  - Flashing guide via Arduino IDE

  - Common problems and solutions  - Slider for manual adjustment (1-100%)

  - Device functionality testing

- Created English version of all documentation  - Global mouse wheel control (works anywhere on screen)- Dark color scheme interface- Тёмная цветовая схема интерфейса

- Updated README.md and all instructions

  - Switch between manual and automatic modes

### 🔄 Updated Files

- All batch and VBS scripts updated for new filename    - Modern minimalist design  - Современный минималистичный дизайн

- Synchronized files in Git_Export

- Added requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`- **Configurable averaging period**



---  - Range: 1-120 seconds (default 10 sec)  - Cyan accent color (#4ec9b0)  - Акцентный бирюзовый цвет (#4ec9b0)



## [v1.0.1] - 2025-10-19  - Configure via Settings UI



### ✨ Added  - Saved in config.ini  - Consolas monospace font  - Моноширинный шрифт Consolas

- **Windows Autostart** - checkbox in interface for quick setup

  - Automatic add/remove of Windows registry entry

  - Works for both compiled .exe and Python scripts

  - Automatic Python interpreter detection in virtual environment### 🔧 Technical Improvements  - Consistent design across all windows and dialogs  - Единообразный дизайн всех окон и диалогов



### 🔧 Improved- **Fixed application freezes**

- Optimized interface element spacing

  - Reduced padding while maintaining readability  - Optimized USB device search (caching)  - Background #1e1e1e, text #d4d4d4  - Фон #1e1e1e, текст #d4d4d4

  - All elements now visible without scrolling in 450x380 window

  - Compact design without loss of functionality  - Removed blocking when switching modes



### 📚 Documentation  - Smooth interface operation without freezes

- Updated README.md with autostart feature description

- Added checkbox information in "Usage" section  

- Updated release notes to v1.0.1

- Created CHANGELOG.md for change tracking- **Main file renamed:**### 🔌 Digispark ATtiny85 Support### 🔌 Поддержка Digispark ATtiny85



---  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`



## [v1.0.0] - 2025-10-18  - Updated all references in documentation and scripts- **New USB sensor mode**- **Новый режим работы с USB-датчиком**



### 🎉 First Stable Release  



#### ✨ Main Features- **Fixed compilation issues:**  - Digispark ATtiny85 support via V-USB  - Поддержка Digispark ATtiny85 через V-USB

- Automatic brightness adjustment via overlay window

- Smooth transitions between brightness levels (configurable)  - Resolved settings saving problem in .exe

- Sensor reading averaging (5-60+ seconds)

- System tray with icon and context menu  - `get_config_path()` function for correct paths  - Automatic connected device detection  - Автоматическое определение подключенного устройства

- Configuration via config.ini without code editing

- Click-through transparent overlay window  - Support for both script and compiled modes

- Instant context menu dimming (50ms update rate)

    - Switch between ESP8266 and Digispark in settings  - Переключение между ESP8266 и Digispark в настройках

#### 📡 ESP8266 Firmware

- WiFi connection with configurable static IP- **Improved PyInstaller compilation:**

- Web calibration interface

- Calibration storage in EEPROM  - Added hidden PIL/Pillow imports  - USB device caching (fixed search freezes)  - Кэширование USB устройств (исправлены зависания при поиске)

- HTTP REST API for data retrieval

- Optimized code (HTML ~1800 bytes)  - Fixed TCL/TK library errors

- 1 Hz sensor polling rate

  - Automatic packaging of required dependencies  - VID: 0x16c0, PID: 0x05df  - VID: 0x16c0, PID: 0x05df

#### 🛠️ Technical Implementation

- Overlay based on win32 API (WS_EX_LAYERED | WS_EX_TRANSPARENT)

- Smooth brightness change with configurable step

- Automatic reconnection on ESP8266 connection loss### 📦 New Files  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)  - Полная документация в `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)

- Calibration values saved in config.ini

- Custom icon support (icon.ico)- `localization.py` - localization module with translations



#### 📦 Additional- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing instructions

- Launch scripts (.vbs for silent start, .bat with console)

- PyInstaller configuration for .exe compilation- Updated `build.spec` for correct compilation

- Detailed documentation (README.md)

- GPL v3 License- English documentation versions (README.md, COMPILE_AND_FLASH.md)### ⚡ New Features### ⚡ Новые возможности

- requirements.txt for easy dependency installation



---

### 🐛 Bug Fixes- **System tray integration**- **Запуск в системном трее**

## Versioning Format

- Fixed window title centering

Project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - incompatible API changes- Fixed language button logic (RU = Russian, EN = English)  - Minimize on focus loss  - Сворачивание при потере фокуса

- **MINOR** (0.X.0) - new functionality with backward compatibility

- **PATCH** (0.0.X) - bug fixes and minor improvements- Eliminated `_imaging` import issue in compiled .exe



---- Eliminated `Can't find a usable init.tcl` error when running .exe  - `Ctrl+Shift+B` hotkey to show window  - Горячая клавиша `Ctrl+Shift+B` для вызова окна



## Symbol Legend- Fixed settings loss after application restart



- ✨ New features- Eliminated freezes when searching for USB devices  - Tray context menu (Show/Settings/Restart/Exit)  - Контекстное меню трея (Показать/Настройки/Перезапуск/Выход)

- 🔧 Improvements

- 🐛 Bug fixes

- 📚 Documentation

- 🔒 Security### 📚 Documentation    

- ⚡ Performance

- 🎨 UI/UX changes- Added complete Digispark ATtiny85 guide

- ♻️ Refactoring

- 🗑️ Removed  - Step-by-step firmware compilation instructions- **Manual brightness control**- **Ручная регулировка яркости**



---  - Flashing guide via Arduino IDE



**Full changelog:** [GitHub Releases](../../releases)  - Common problems and solutions  - Slider for manual adjustment (1-100%)  - Ползунок для ручной настройки (1-100%)


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

