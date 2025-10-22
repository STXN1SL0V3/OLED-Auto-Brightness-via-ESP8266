# 🎉 Release v2.0.0 - Localization & Multi-Device Support

## 🔆 OLED Auto Brightness - Major Breaking Update

**⚠️ BREAKING CHANGES:** This version is not compatible with previous releases. Configuration file structure has changed, main file renamed, and new dependencies added.

A major rewrite featuring full interface localization, new modern theme, Digispark ATtiny85 USB sensor support, system tray functionality, and manual brightness control with global hotkeys.

---

## 🆕 What's New in v2.0.0

### ⚠️ Breaking Changes
- **File renamed:** `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`
- **Config structure changed:** New sections added, old `[Smoothing]` removed
- **New dependencies:** keyboard, mouse, pystray, pyusb required
- **Autostart path changed:** Registry entry needs updating if upgrading
- **Calibration storage:** Digispark calibration now in config.ini, not device memory

### 🌐 Full Localization
- **Bilingual interface:** Complete English and Russian translations
- **Language switcher:** Easy toggle between languages in main window
- **50+ translated strings:** All UI elements, dialogs, and messages
- **Persistent language setting:** Saved in config.ini

### 🎨 New Modern Theme
- **Dark color scheme:** Professional look with #1e1e1e background
- **Accent colors:** Cyan highlights (#4ec9b0) for better visibility
- **Consolas font:** Crisp, readable monospaced font throughout UI
- **Improved contrast:** Better readability in all lighting conditions

### 🔄 Digispark ATtiny85 Support
- **USB sensor alternative:** No WiFi required - direct USB connection
- **V-USB library:** Software USB implementation on ATtiny85
- **Comprehensive documentation:** Step-by-step flashing guide included
- **Automatic device detection:** Smart switching between ESP8266/Digispark
- **Device caching:** Optimized USB device search (no freezes)
- **VID/PID: 0x16c0:0x05df**

### 🖼️ System Tray Features
- **Minimize to tray:** Clean desktop while running in background
- **Global hotkey:** Ctrl+Shift+B to show/hide main window
- **Tray menu:** Quick access to show, settings, restart, and exit
- **Start minimized:** Optional boot-to-tray for silent startup
- **Custom icon:** Distinctive tray icon for easy identification

### 🖱️ Manual Brightness Control
- **Auto/Manual toggle:** Switch between automatic and manual modes
- **Brightness slider:** Precise manual brightness adjustment (0-100%)
- **Mouse wheel support:** Global mouse wheel control over tray icon
- **Persistent setting:** Manual brightness saved to config
- **Smooth transitions:** Same smooth dimming in manual mode

### ⚙️ Enhanced Settings
- **Settings dialog:** Dedicated window for all configuration options
- **Averaging period:** Adjustable 1-120 seconds for sensor smoothing
- **Device selection:** Easy switch between ESP8266 and Digispark
- **Calibration dialogs:** Dedicated calibration UI for each device type
- **Language preference:** Built into settings menu

### 🐛 Bug Fixes & Improvements
- **Config saving in EXE:** Fixed issue with compiled executable not saving settings
- **USB device search freezes:** Implemented device caching to prevent UI lockups
- **PIL import errors:** Added all required PIL hidden imports to build.spec
- **TCL/TK library errors:** Proper bundling of tkinter dependencies
- **Title centering:** Fixed window title alignment
- **Language button logic:** Corrected RU/EN button behavior

### 📚 Documentation Updates
- **Bilingual README:** Full documentation in English and Russian
- **ATtiny85 flashing guide:** Comprehensive instructions for Digispark
- **Updated CHANGELOG:** Detailed version history with all changes
- **Code comments:** Improved inline documentation
- **File naming:** Renamed to OLED_Auto_Brightness.py for clarity

---

## 📦 What's Included

### Main Application Files
- `OLED_Auto_Brightness.py` - Main Python application (renamed from simple_auto_brightness.py)
- `localization.py` - Translation system with EN/RU language support
- `config.ini` - Enhanced configuration file with new sections
- `icon.ico` - Application icon for window and tray

### Sensor Firmware
- `ESP8266_AutoBrightness.ino` - WiFi sensor firmware for ESP8266
- `Digispark_ATtiny85_VUSB/` - Complete ATtiny85 V-USB firmware and flashing tools

### Launch Scripts
- `Start_OLED_Brightness.vbs` - Silent startup (recommended for autostart)
- `Start_OLED_Brightness.bat` - Console startup for debugging

### Build & Dependencies
- `build.spec` - Enhanced PyInstaller config with TCL/TK, PIL, and libusb support
- `requirements.txt` - Updated dependencies including keyboard, mouse, pystray

### Documentation
- `README.md` - Complete English documentation
- `README_RU.md` - Russian documentation
- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md` - English flashing guide
- `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH_RU.md` - Russian flashing guide
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License

---

## 🛠️ Technical Details

### New Dependencies
```
keyboard>=0.13.5      # Global hotkey support
mouse>=0.7.1          # Mouse wheel control
pystray>=0.19.4       # System tray functionality
pyusb>=1.2.1          # USB device communication (Digispark)
libusb-package        # libusb-1.0.dll for Windows
```

### Enhanced Config Structure
```ini
[Brightness]
auto_enabled = True
manual_brightness = 100

[Averaging]
averaging_period = 10

[Mode]
device = digispark

[Interface]
language = en

[Startup]
start_minimized = False

[Calibration_esp8266]
min_light = 0
max_light = 33

[Calibration_digispark]
sensor_min = 10
sensor_max = 463
```

### Build Improvements
- **TCL/TK bundling:** Automatic detection and inclusion of tkinter libraries
- **PIL hidden imports:** All PIL modules properly included
- **libusb-1.0.dll:** Bundled for Digispark USB support
- **No external dependencies:** Fully standalone executable

---

## 🚀 Installation & Upgrade

### Fresh Installation
1. Download and extract release archive
2. Choose your sensor:
   - **ESP8266:** Flash `ESP8266_AutoBrightness.ino`, configure WiFi/IP
   - **Digispark:** Follow `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md`
3. Edit `config.ini` to match your device settings
4. Run `OLED_Auto_Brightness.exe` or `python OLED_Auto_Brightness.py`

### ⚠️ Upgrading from v1.0.1 - BREAKING CHANGES

**Important:** This is a major version bump with incompatible changes. Migration required.

1. **Backup your old config.ini and calibration data**

2. **Uninstall old version:**
   - Disable "Start with Windows" in old version
   - Close the program completely
   - Delete old autostart registry entry (or it will fail to start)

3. **Install v2.0.0:**
   - Extract to a new folder
   - Copy these values from old config to new:
     - `min_brightness`, `max_brightness` → `[Brightness]`
     - `esp_ip` → `[Connection]`
     - `min_light`, `max_light` → `[Calibration_esp8266]`

4. **Add new required config sections:**
   ```ini
   [Averaging]
   averaging_period = 10
   
   [Mode]
   device = esp8266
   
   [Interface]
   language = en
   
   [Brightness]
   auto_enabled = True
   manual_brightness = 100
   
   [Startup]
   start_minimized = False
   ```

5. **Update autostart:**
   - Run new version
   - Enable "Start with Windows" checkbox
   - Old registry entry will be replaced automatically

6. **Recalibrate sensor (recommended):**
   - ESP8266: Use web interface calibration
   - Digispark: Use in-app calibration dialog

---

## 🎯 Usage Highlights

### Quick Start
1. **ESP8266 mode:** Set `device = esp8266` in config.ini, configure `esp_ip`
2. **Digispark mode:** Set `device = digispark`, connect device via USB
3. Run program - it will auto-detect and connect to sensor
4. Use **Ctrl+Shift+B** to show/hide window anytime
5. Right-click tray icon for quick menu access

### Calibration
- **ESP8266:** Click "Open ESP8266 Calibration" → Web interface opens
- **Digispark:** Click "Settings" → "Calibrate Digispark" → Follow prompts

### Language Switching
- Click **RU** or **EN** button in main window
- Setting is saved immediately to config.ini
- Restart not required

---

## ⚠️ Known Limitations

- **Windows only** - Uses win32 API for overlay window
- **Mouse cursor not dimmed** - Windows API limitation
- **Overlay may flicker** - When fullscreen apps launch
- **Digispark first search** - May take 5 seconds on initial detection

---

## 🔄 Migration Notes

### File Renaming
- `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`
- All scripts and shortcuts need updating

### Removed Features
- `[Smoothing]` section removed (now uses averaging_period)
- Hardcoded config path replaced with dynamic detection

### New Required Files
- `localization.py` - Must be in same folder as main script
- `libusb-1.0.dll` - Required for Digispark support (auto-bundled in exe)

---

## 🙏 Credits

**Developer:** STXN1SL0V3

**Special Thanks:**
- V-USB Project (https://www.obdev.at/products/vusb/)
- Digistump Team (http://digistump.com/)
- Python Community

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🐛 Bug Reports

Found an issue? Please report it on GitHub:
https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266/issues

---

**Enjoy the new features! 🌟**
