# 🔆 OLED Auto Brightness

Automatic OLED monitor brightness adjustment based on ESP8266 or Digispark ATtiny85 light sensor.

## 📋 Description

The program creates a transparent overlay window on top of the screen that dims the image based on room lighting. Brightness is determined via ESP8266 with a connected photoresistor or Digispark ATtiny85 with V-USB support.

### ✨ Features

- 🌓 Automatic brightness adjustment based on light sensor
- 🔄 Support for two sensor types: ESP8266 (WiFi) and Digispark ATtiny85 (USB)
- 🎯 Smooth transitions between brightness levels
- 📊 Reading averaging for stability
- 💾 Calibration saved in EEPROM (ESP8266) or device memory (Digispark)
- 🖥️ Click-through transparent overlay window
- 🎨 System tray icon
- ⌨️ Global hotkey (Ctrl+Shift+B)
- 🖱️ Manual brightness control with mouse wheel
- 🌐 Localization: English/Russian
- 🚀 Windows autostart
- ⚙️ Configuration via config.ini

## 📜 License

This project is licensed under the **GPL-3.0**. See the `LICENSE` file for more details.
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 🛠️ Required Hardware

### Option 1: ESP8266 (WiFi sensor)
- NodeMCU, Wemos D1 Mini, or similar
- Photoresistor (any type)
- 10 kΩ resistor

#### Wiring Diagram
```
3.3V ─── [Photoresistor] ─── A0 ─── [10kΩ] ─── GND
```

### Option 2: Digispark ATtiny85 (USB sensor)
- Digispark ATtiny85 board with V-USB support
- Photoresistor (any type)
- 10 kΩ resistor

#### Wiring Diagram
```
VCC (5V) ─── [Photoresistor] ─── P2 (ADC1) ─── [10kΩ] ─── GND
```

**See detailed flashing instructions in:**
- English: `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md`
- Russian: `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH_RU.md`

## 📦 Installation

### 1. Sensor Setup

#### For ESP8266:

1. Open `ESP8266_AutoBrightness.ino` in Arduino IDE
2. Install libraries (if needed):
   - ESP8266WiFi
   - ESP8266WebServer
   - EEPROM
3. **IMPORTANT:** Change WiFi settings:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";          // Your WiFi network name
   const char* password = "YOUR_WIFI_PASSWORD";  // WiFi password
   ```
4. Configure static IP (or use DHCP):
   ```cpp
   IPAddress local_IP(192, 168, 1, 146);   // Your IP address
   IPAddress gateway(192, 168, 1, 1);      // Router IP
   ```
5. Select board: `Tools → Board → ESP8266 Boards → NodeMCU 1.0`
6. Upload sketch to ESP8266

#### For Digispark ATtiny85

See comprehensive instructions in `Digispark_ATtiny85_VUSB/COMPILE_AND_FLASH.md`

### 2. Software Installation (Windows)

#### Option A: Pre-compiled EXE
1. Unpack the `dist` folder anywhere
2. Open `config.ini` and specify your device settings:
   - For ESP8266: set `esp_ip` under `[Connection]`
   - For Digispark: set `device = digispark` under `[Mode]`
3. Run `OLED_AutoBrightness.exe`

#### Option B: Run from Source

1. Install Python 3.12+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Edit `config.ini` (configure your sensor)
4. Run using one of these methods:
   - **Double-click:** `Start_OLED_Brightness.vbs` (silent mode)
   - **Or:** `Start_OLED_Brightness.bat` (with console)
   - **Or manually:**
     ```bash
     python OLED_Auto_Brightness.py
     ```

## ⚙️ Sensor Calibration

### ESP8266 Calibration:
1. Run the program
2. Click **"🛠️ Open ESP8266 Calibration"** button (opens web interface)
3. **Minimum calibration:**
   - Cover the photoresistor with your hand or turn off lights
   - Click **MIN** button
4. **Maximum calibration:**
   - Shine a flashlight on the photoresistor or turn on bright lights
   - Click **MAX** button
5. Calibration is automatically saved to EEPROM

### Digispark Calibration:
1. Run the program with `device = digispark` in config.ini
2. Click **"Settings"** button
3. Click **"Calibrate Digispark"** button
4. Follow on-screen instructions:
   - Cover sensor for minimum
   - Illuminate sensor for maximum
5. Calibration is saved to config.ini

## 🎛️ config.ini Settings

```ini
[Brightness]
auto_enabled = True    # Enable automatic brightness
manual_brightness = 100 # Manual brightness when auto is disabled (%)
min_brightness = 40    # Minimum screen brightness (%)
max_brightness = 100   # Maximum screen brightness (%)

[Averaging]
averaging_period = 10  # Averaging period in seconds (higher = smoother)

[Mode]
device = digispark     # Sensor type: 'esp8266' or 'digispark'

[Connection]
esp_ip = 192.168.1.146 # ESP8266 IP address (for WiFi mode)
timeout = 5            # Connection timeout

[Interface]
language = en          # Interface language: 'en' or 'ru'

[Startup]
start_minimized = False # Start minimized to system tray

[Calibration_esp8266]
# Filled automatically via web interface calibration
min_light = 0
max_light = 33

[Calibration_digispark]
# Filled automatically via calibration dialog
sensor_min = 10
sensor_max = 463
```

## 🎯 Usage

### Main Window
- **Displays:** current brightness, sensor value, connection status
- **Close button (❌):** minimizes program to system tray
- **Calibration button:** opens device-specific calibration interface
- **Autostart checkbox:** enable/disable Windows startup
- **Language switcher:** RU/EN interface language
- **Auto brightness toggle:** enable/disable automatic adjustment
- **Manual brightness slider:** control brightness when auto mode is off

### System Tray
- **Double-click:** restore main window
- **Global hotkey Ctrl+Shift+B:** show/hide window
- **Mouse wheel over tray icon:** adjust manual brightness globally
- **Right-click menu:**
  - "Show" - restore window
  - "Settings" - open settings dialog
  - "Restart" - restart the application
  - "Exit" - close program completely

### Windows Autostart
The main window has an **"Start with Windows"** checkbox.

- ✅ **Enabled:** program will automatically start when Windows boots
- ⬜ **Disabled:** manual start only

The program automatically adds/removes registry entry:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

**Note:** For manual autostart configuration, you can use the standard method:
1. Create a shortcut to `OLED_AutoBrightness.exe`
2. Move shortcut to: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

## 🔧 Compiling from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Compile
pyinstaller --clean build.spec

# Result in dist/ folder
```

**Important:** The build.spec includes:
- TCL/TK library bundling for tkinter
- PIL hidden imports for system tray icon
- libusb-1.0.dll for Digispark USB support

## 📊 Technical Details

### How It Works
1. Sensor reads photoresistor every second (1 Hz)
   - ESP8266: via WiFi HTTP API
   - Digispark: via USB using pyusb library
2. Python program receives data
3. Brightness calculated based on calibration values
4. Values averaged over N seconds (configurable)
5. Overlay window transparency smoothly adjusted

### ESP8266 API
- `GET /` - calibration web interface
- `GET /api/brightness` - get current data (JSON)
- `GET /api/calibrate/min` - set minimum
- `GET /api/calibrate/max` - set maximum
- `GET /api/calibrate/reset` - reset calibration

### API Response `/api/brightness`:
```json
{
  "light_level": 80,     // Current sensor value
  "min_light": 0,        // Calibration minimum
  "max_light": 33        // Calibration maximum
}
```

### Digispark USB Protocol
- Uses V-USB library for USB communication
- Device VID: 0x16c0, PID: 0x05df
- Control transfers for sensor data
- ADC reading from P2 (ADC1) pin
- Calibration stored in config.ini

## ⚠️ Known Limitations

- **Mouse cursor is not dimmed** - Windows API limitation
- **Windows only** - uses win32 API for overlay
- **Overlay may flicker** when opening fullscreen applications
- **Digispark device search** - may take 5 seconds on first launch

## 🆕 What's New in v2.0.0

### ⚠️ Breaking Changes
This is a major version with incompatible changes from v1.0.1:
- Main file renamed: `simple_auto_brightness.py` → `OLED_Auto_Brightness.py`
- Config structure changed: new sections added
- New dependencies required: keyboard, mouse, pystray, pyusb
- Autostart registry path changed (requires manual update when upgrading)

### New Features
- 🌐 **Full localization:** English/Russian interface
- 🎨 **New dark theme:** modern color scheme with Consolas font
- 🔄 **Digispark ATtiny85 support:** USB sensor alternative to ESP8266
- 🖼️ **System tray:** minimize to tray, global hotkey (Ctrl+Shift+B)
- 🖱️ **Manual brightness control:** slider + mouse wheel support
- ⚙️ **Enhanced settings:** averaging period, calibration dialogs
- 🐛 **Bug fixes:** USB device search freezes, config saving in exe
- 📚 **Documentation:** comprehensive guides for ATtiny85 flashing (EN/RU)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266/issues).
