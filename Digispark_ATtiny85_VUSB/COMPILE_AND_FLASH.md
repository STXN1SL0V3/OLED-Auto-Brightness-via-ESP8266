# 🔧 Compiling and Flashing ATtiny85 (Digispark)

## 📋 Table of Contents
- [Requirements](#requirements)
- [Tool Installation](#tool-installation)
- [Firmware Compilation](#firmware-compilation)
- [Flashing ATtiny85](#flashing-attiny85)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🛠️ Requirements

### Hardware:
- **Digispark ATtiny85** (with pre-installed USB bootloader)
- USB cable (Micro-USB or USB-A, depending on model)
- Computer with Windows/Linux/macOS

### Software:
- **Arduino IDE** 1.8.x or 2.x
- **Digispark Board Support** for Arduino IDE
- **Micronucleus** (bootloader for flashing)

---

## 📦 Tool Installation

### 1. Installing Arduino IDE

**Windows:**
```powershell
# Download from official website
https://www.arduino.cc/en/software
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install arduino
```

**macOS:**
```bash
brew install --cask arduino
```

### 2. Installing Digispark Board Support

1. Open **Arduino IDE**
2. Go to **File → Preferences**
3. In **Additional Boards Manager URLs** field, add:
   ```
   http://digistump.com/package_digistump_index.json
   ```
4. Click **OK**
5. Open **Tools → Board → Boards Manager**
6. Search for **Digistump AVR Boards**
7. Click **Install**

### 3. Installing Drivers (Windows only)

1. Download Digispark driver:
   ```
   https://github.com/digistump/DigistumpArduino/releases
   ```
2. Run `DPinst64.exe` (for 64-bit Windows) or `DPinst.exe` (for 32-bit)
3. Follow installer instructions

---

## ⚙️ Firmware Compilation

### Project Structure:

```
Digispark_ATtiny85_VUSB/
├── Digispark_VUSB_Firmware.ino    # Main firmware
├── v-usb/                          # V-USB library
│   ├── usbdrv/                     # V-USB driver
│   └── README.md
└── COMPILE_AND_FLASH_EN.md         # This file
```

### Compilation Steps:

1. **Open Arduino IDE**

2. **Open firmware:**
   - File → Open
   - Select `Digispark_VUSB_Firmware.ino`

3. **Configure board settings:**
   - **Tools → Board** → Digistump AVR Boards → **Digispark (Default - 16.5MHz)**
   - **Tools → Programmer** → **Micronucleus**

4. **Verify compilation:**
   - Click **Verify** button (✓) or press `Ctrl+R`
   - Wait for "Done compiling" message

### Configuration Parameters (optional):

In `Digispark_VUSB_Firmware.ino` you can modify:

```cpp
// USB Device Info
#define USB_CFG_VENDOR_ID       0x16c0  // VID (don't change unless necessary)
#define USB_CFG_DEVICE_ID       0x05df  // PID (don't change unless necessary)
#define USB_CFG_VENDOR_NAME     'D','i','g','i','s','p','a','r','k'
#define USB_CFG_DEVICE_NAME     'O','L','E','D',' ','B','r','i','g','h','t'

// Data send interval (ms)
#define SEND_INTERVAL           100     // Default 100 ms
```

---

## 📲 Flashing ATtiny85

### ⚠️ IMPORTANT before flashing:

1. **DO NOT** connect Digispark to USB **BEFORE** starting the flash process
2. Make sure no other programs are using COM ports
3. Close all USB monitoring programs (e.g., USBDeview)

### Flashing Process:

1. **Start upload:**
   - In Arduino IDE, click **Upload** (→) or press `Ctrl+U`
   - You will see message:
     ```
     Running Micronucleus...
     Please plug in the device...
     ```

2. **Connect Digispark:**
   - **Within 60 seconds**, plug Digispark into USB port
   - Bootloader will automatically detect the device

3. **Wait for completion:**
   ```
   > Device is found!
   > Starting upload...
   > Writing: 100% complete
   > Starting the user app...
   > Micronucleus done. Thank you!
   ```

4. **Done!**
   - Disconnect and reconnect Digispark
   - Device is ready to use

### Alternative Method (command line):

**Windows:**
```powershell
# Navigate to micronucleus.exe folder
cd "C:\Users\<User>\AppData\Local\Arduino15\packages\digistump\tools\micronucleus\2.0a4"

# Run flash
.\micronucleus.exe --run "path\to\Digispark_VUSB_Firmware.ino.hex"
```

**Linux/macOS:**
```bash
# Install micronucleus (if not installed)
sudo apt install micronucleus  # Ubuntu/Debian
brew install micronucleus      # macOS

# Run flash
micronucleus --run /path/to/Digispark_VUSB_Firmware.ino.hex
```

---

## ✅ Testing

### 1. Check USB Connection:

**Windows:**
```powershell
# PowerShell - check USB devices
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*Digispark*"}
```

**Linux:**
```bash
# List USB devices
lsusb | grep "16c0:05df"
```

### 2. Check via Python Program:

Run main program `OLED_Auto_Brightness.py`:
```bash
python OLED_Auto_Brightness.py
```

In the program interface:
- Open **Settings** (⚙️)
- In **Device Selection** section, select **Digispark (V-USB)**
- Click **Save**

If everything works, you will see:
- ✅ Green connection indicator
- Current brightness value from sensor
- Automatic OLED brightness adjustment

### 3. Check Sensor Data:

Main window should display:
- **Sensor:** current light level (0-1023)
- **Target:** target brightness (40-100%)
- **Averaging:** averaged value over period

---

## 🔧 Troubleshooting

### ❌ Problem: "Device not found"

**Solution:**
1. Check USB cable (use data cable, not charge-only)
2. Try different USB port
3. Reinstall drivers (Windows):
   ```powershell
   # Run driver installer again
   DPinst64.exe
   ```
4. Check that Digispark is in bootloader mode:
   - Disconnect from USB
   - Press and hold RESET button (if available)
   - Connect to USB while holding RESET for 1-2 seconds

### ❌ Problem: "Access denied"

**Windows:**
- Run Arduino IDE **as Administrator**

**Linux:**
- Add udev rules:
  ```bash
  sudo nano /etc/udev/rules.d/49-micronucleus.rules
  ```
  Insert:
  ```
  SUBSYSTEMS=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE:="0666"
  ```
  Save and execute:
  ```bash
  sudo udevadm control --reload-rules
  sudo udevadm trigger
  ```

### ❌ Problem: Compilation fails

**Error:** `usbdrv.h: No such file or directory`

**Solution:**
1. Ensure `v-usb/usbdrv/` folder is in same directory as `.ino` file
2. Check include paths in code:
   ```cpp
   #include "v-usb/usbdrv/usbdrv.h"
   ```

### ❌ Problem: Device doesn't work after flashing

**Solution:**
1. Check that **Fuses** are configured correctly:
   - Low Fuse: `0xE1` (for 16.5 MHz PLL)
   - High Fuse: `0xDD`
   - Extended Fuse: `0xFE`

2. Re-flash device with "Burn Bootloader" option:
   - Tools → Burn Bootloader

3. Check power supply:
   - ATtiny85 requires stable 5V power
   - Use quality USB port (not a hub)

### ❌ Problem: Python program doesn't detect Digispark

**Solution:**
1. Check settings in `config.ini`:
   ```ini
   [Mode]
   device = digispark
   ```

2. Reinstall libusb driver:
   ```bash
   pip install --upgrade libusb-package
   ```

3. Verify device VID/PID:
   - Must match those specified in firmware
   - Default: `VID=0x16c0`, `PID=0x05df`

---

## 📚 Additional Resources

### Official Documentation:
- **Digispark Wiki:** http://digistump.com/wiki/
- **V-USB Project:** https://www.obdev.at/products/vusb/
- **ATtiny85 Datasheet:** https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf

### Forums and Communities:
- **Arduino Forum - Digispark:** https://forum.arduino.cc/
- **Digistump Forum:** http://digistump.com/board/

### Video Tutorials:
- YouTube: "How to program Digispark ATtiny85"
- YouTube: "V-USB tutorial for ATtiny85"

---

## 📝 Notes

### Important Points:

1. **Bootloader occupies ~2KB of memory**
   - ~6KB available for your program
   - Consider this when developing

2. **USB works via software (bit-banging)**
   - May be unstable under high loads
   - Recommended not to use delays > 10ms in loop()

3. **CPU Frequency: 16.5 MHz (internal PLL)**
   - Digispark uses internal RC oscillator + PLL
   - Accuracy ~±10% (sufficient for USB)

4. **First flash takes ~60 seconds**
   - Subsequent flashes ~5-10 seconds
   - This is normal for Micronucleus bootloader

---

## 🆘 Support

If you encounter problems:

1. **Check Issues on GitHub:**
   - https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266/issues

2. **Create new Issue:**
   - Describe the problem
   - Attach logs/screenshots
   - Specify Arduino IDE version and OS

3. **Contact:**
   - GitHub: [@STXN1SL0V3](https://github.com/STXN1SL0V3)

---

**Happy flashing! 🚀**
