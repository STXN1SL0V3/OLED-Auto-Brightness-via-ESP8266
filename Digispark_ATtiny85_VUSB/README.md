# Digispark ATtiny85 V-USB Sensor Firmware

This folder contains the firmware source code for using Digispark ATtiny85 as a USB light sensor for OLED Auto Brightness application.

## ⚠️ Important: V-USB Library Required

This firmware requires the **V-USB library** which is licensed under **GPL v2/v3**. Due to license compatibility (this project is GPL v3), V-USB is **NOT included** in this repository.

### Download V-USB

**Official V-USB Project:**
- Website: <https://www.obdev.at/products/vusb/>
- GitHub: <https://github.com/obdev/v-usb>

**How to obtain:**
```bash
# Clone V-USB into this directory
git clone https://github.com/obdev/v-usb.git v-usb
```

After downloading, your directory structure should be:
```
Digispark_ATtiny85_VUSB/
├── v-usb/              # V-USB library (GPL, not included in repo)
│   └── usbdrv/         # USB driver files
├── main.c              # Main firmware (GPL v3)
├── usbconfig.h         # USB configuration (GPL v3)
├── Makefile            # Build configuration (GPL v3)
└── COMPILE_AND_FLASH.md # Instructions
```

## 📋 What's Included (GPL v3 License)

- `main.c` - Main firmware implementation
- `usbconfig.h` - USB device configuration
- `osccal.c/h` - Oscillator calibration
- `Makefile` - Build configuration
- `build.bat`, `upload.bat` - Windows scripts
- `COMPILE_AND_FLASH.md` / `COMPILE_AND_FLASH_RU.md` - Full instructions

## 🚀 Quick Start

1. **Download V-USB library** (required, GPL licensed)
2. **Follow flashing guide:**
   - English: [COMPILE_AND_FLASH.md](COMPILE_AND_FLASH.md)
   - Russian: [COMPILE_AND_FLASH_RU.md](COMPILE_AND_FLASH_RU.md)

## 📄 License Information

**This Project:** GPL v3 License  
**V-USB Library:** GPL v2/v3 (separate download required)

---

**Note:** V-USB is not included due to repository size and license clarity. Download separately from official sources.
