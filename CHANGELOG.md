# 📝 Changelog

All notable changes to this project are documented in this file.

---

## [v2.0.0] - 2025-10-22

### ⚠️ BREAKING CHANGES
- **Main file renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`
- **Config.ini structure changed:** New sections added, `[Smoothing]` section removed
- **New dependencies:** keyboard, mouse, pystray, pyusb
- **Autostart path changed:** Registry entry requires update when upgrading
- **Digispark calibration storage:** Now in config.ini instead of device memory

### 🌍 Localization
- **Full bilingual support:** Russian and English
  - All interface elements translated (60+ strings)
  - Language switcher button in main window
  - Setting saved in config.ini
  - Dynamic text updates when language changes
  - Localization system in separate `localization.py` module

### 🎨 New Theme
- Dark color scheme interface
  - Modern minimalist design
  - Cyan accent color (#4ec9b0)
  - Consolas monospace font
  - Consistent design across all windows and dialogs
  - Background #1e1e1e, text #d4d4d4

### 🔌 Digispark ATtiny85 Support
- **New USB sensor mode**
  - Support for Digispark ATtiny85 via V-USB
  - Automatic detection of connected device
  - Switch between ESP8266 and Digispark in settings
  - USB device caching (fixed search freezes)
  - VID: 0x16c0, PID: 0x05df
  - Full documentation in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` (RU/EN)

### ⚡ New Features
- **System tray integration**
  - Minimize on focus loss
  - Global hotkey `Ctrl+Shift+B` to show/hide window
  - Tray context menu (Show/Settings/Restart/Exit)
  
- **Manual brightness control**
  - Slider for manual adjustment (1-100%)
  - Global mouse wheel scrolling (works anywhere on screen)
  - Toggle between manual and automatic mode
  
- **Configurable averaging period**
  - Range: 1-120 seconds (default 10 sec)
  - Adjustable via Settings UI
  - Saved in config.ini

### 🔧 Technical Improvements
- **Fixed application freezes**
  - Optimized USB device search (caching)
  - Removed blocking when switching modes
  - Smooth interface operation without freezes
  
- **Main file renamed:**
  - `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`
  - Updated all references in documentation and scripts
  
- **Fixed compilation issues:**
  - Resolved settings save problem in .exe
  - `get_config_path()` function for correct paths
  - Support for both script and compiled modes
  
- **Improved PyInstaller compilation:**
  - Added hidden imports for PIL/Pillow
  - Fixed TCL/TK library errors
  - Automatic packaging of required dependencies

### 📦 New Files
- `localization.py` - localization module with translations
- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - ATtiny85 flashing guide
- Updated `build.spec` for correct compilation
- English documentation versions (README_EN.md, COMPILE_AND_FLASH_EN.md)

### 🐛 Fixed Bugs
- Fixed window title centering
- Fixed language button logic (RU = Russian, EN = English)
- Eliminated `_imaging` import issue in compiled .exe
- Eliminated `Can't find a usable init.tcl` error when running .exe
- Fixed settings loss after program restart
- Eliminated freezes when searching for USB devices

### 📚 Documentation
- Added complete guide for Digispark ATtiny85
  - Step-by-step firmware compilation instructions
  - Flashing guide via Arduino IDE
  - Common troubleshooting solutions
  - Device functionality testing
- Created English version of all documentation
- Updated README.md and all instructions

### 🔄 Updated Files
- All batch and VBS scripts updated for new filename
- Synchronized files in Git_Export
- Added requirements: `keyboard>=0.13.5`, `mouse>=0.7.1`

---

## [v1.0.1] - 2025-10-19

### ✨ Added
- **Windows Autostart** - checkbox in interface for quick setup
  - Automatic add/remove Windows registry entry
  - Works for both compiled .exe and Python scripts
  - Automatic Python interpreter detection in virtual environment

### 🔧 Improved
- Optimized interface element spacing
  - Reduced padding while maintaining readability
  - All elements now visible without scrolling in 450x380 window
  - Compact design without loss of functionality

### 📚 Documentation
- Updated README.md with autostart feature description
- Added checkbox information in "Usage" section
- Updated release notes for v1.0.1
- Created CHANGELOG.md for tracking changes

---

## [v1.0.0] - 2025-10-18

### 🎉 First Stable Release

#### ✨ Main Features
- Automatic brightness adjustment via overlay window
- Smooth transitions between brightness levels (configurable)
- Sensor reading averaging (5-60+ seconds)
- System tray with icon and context menu
- Configuration via config.ini without code editing
- Click-through transparent overlay window
- Instant context menu dimming (50ms update)

#### 📡 ESP8266 Firmware
- WiFi connection with configurable static IP
- Web interface for sensor calibration
- Calibration storage in EEPROM
- HTTP REST API for data retrieval
- Optimized code (HTML ~1800 bytes)
- 1 Hz sensor polling frequency

#### 🛠️ Technical Implementation
- Overlay based on win32 API (WS_EX_LAYERED | WS_EX_TRANSPARENT)
- Smooth brightness changes with configurable step
- Automatic reconnection on ESP8266 connection loss
- Calibration values saved in config.ini
- Custom icon support (icon.ico)

#### 📦 Additional
- Launch scripts (.vbs for silent start, .bat with console)
- PyInstaller configuration for .exe compilation
- Detailed documentation (README.md)
- MIT License
- requirements.txt for easy dependency installation

---

## Versioning Format

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0) - incompatible API changes
- **MINOR** (0.X.0) - new functionality with backward compatibility
- **PATCH** (0.0.X) - bug fixes and minor improvements

---

## Symbol Legend

- ✨ New features
- 🔧 Improvements
- 🐛 Bug fixes
- 📚 Documentation
- 🔒 Security
- ⚡ Performance
- 🎨 UI/UX changes
- ♻️ Refactoring
- 🗑️ Removed

---

**Full changelog:** [GitHub Releases](../../releases)
