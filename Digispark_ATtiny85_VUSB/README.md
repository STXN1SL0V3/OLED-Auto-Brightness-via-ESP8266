# Digispark ATtiny85 V-USB Sensor Firmware# Digispark ATtiny85 V-USB Test Firmware



This folder contains the firmware source code for using Digispark ATtiny85 as a USB light sensor for OLED Auto Brightness application.Тестовая прошивка для Digispark ATtiny85, передающая двухзначные числа (0-99) через USB Control Transfer.



## ⚠️ Important: V-USB Library Required**На основе проекта:** https://github.com/xythobuz/AutoBrightness



This firmware requires the **V-USB library** which is licensed under **GPL v2/v3**. Due to license compatibility (this project is MIT), V-USB is **NOT included** in this repository.## Структура проекта



### Download V-USB```

Digispark_ATtiny85_VUSB/

**Official V-USB Project:**├── main.c          - Основной код firmware

- Website: https://www.obdev.at/products/vusb/├── usbconfig.h     - Конфигурация V-USB

- GitHub: https://github.com/obdev/v-usb├── Makefile        - Сборка проекта

└── README.md       - Эта инструкция

**How to obtain:**```

```bash

# Clone V-USB into this directory## Требования

git clone https://github.com/obdev/v-usb.git v-usb

```### Для компиляции firmware:



After downloading, your directory structure should be:1. **AVR GCC Toolchain**

```   ```bash

Digispark_ATtiny85_VUSB/   # Linux (Debian/Ubuntu)

├── v-usb/              # V-USB library (GPL, not included in repo)   sudo apt-get install gcc-avr avr-libc avrdude

│   └── usbdrv/         # USB driver files   

├── main.c              # Main firmware (MIT)   # macOS

├── usbconfig.h         # USB configuration (MIT)   brew tap osx-cross/avr

├── Makefile            # Build configuration (MIT)   brew install avr-gcc avr-libc avrdude

└── COMPILE_AND_FLASH.md # Instructions (MIT)   

```   # Windows

   # Скачать WinAVR: https://sourceforge.net/projects/winavr/

## 📋 What's Included (MIT License)   ```



- `main.c` - Main firmware implementation2. **V-USB Library**

- `usbconfig.h` - USB device configuration     ```bash

- `osccal.c/h` - Oscillator calibration   # Клонируем V-USB в директорию проекта

- `Makefile` - Build configuration   git clone https://github.com/obdev/v-usb.git

- `build.bat`, `upload.bat` - Windows scripts   ```

- `COMPILE_AND_FLASH.md` / `COMPILE_AND_FLASH_RU.md` - Full instructions

3. **Micronucleus** (для прошивки Digispark)

## 🚀 Quick Start   ```bash

   # Linux

1. **Download V-USB library** (required, GPL licensed)   sudo apt-get install micronucleus

2. **Follow flashing guide:**   

   - English: [COMPILE_AND_FLASH.md](COMPILE_AND_FLASH.md)   # или скачать с: https://github.com/micronucleus/micronucleus

   - Русский: [COMPILE_AND_FLASH_RU.md](COMPILE_AND_FLASH_RU.md)   ```



## 📄 License Information### Для Python скрипта:



**This Project:** MIT License  ```powershell

**V-USB Library:** GPL v2/v3 (separate download required)pip install pyusb libusb-package

```

⚠️ **License Compatibility:** Using GPL library typically requires GPL licensing for your project. For commercial use, consider purchasing V-USB commercial license: https://www.obdev.at/products/vusb/license.html

**Windows:** Установите драйвер через [Zadig](https://zadig.akeo.ie/)

---

## Сборка и прошивка

**Note:** V-USB is not included due to license compatibility. Download separately from official sources.

### 1. Подготовка

```bash
cd Digispark_ATtiny85_VUSB
```

Убедитесь, что V-USB находится в правильной директории:
```
v-usb/
  └── usbdrv/
      ├── usbdrv.c
      ├── usbdrvasm.S
      └── ...
```

### 2. Компиляция

```bash
make
```

Вы должны увидеть:
```
=== Размер прошивки ===
Program:    XXXX bytes
Data:       YYY bytes
```

### 3. Прошивка

```bash
make upload
```

Когда появится сообщение "Подключите Digispark СЕЙЧАС...", подключите устройство в USB порт.

Micronucleus автоматически:
- Найдет Digispark в режиме bootloader
- Прошьёт firmware
- Перезагрузит устройство

## Настройка для вашего проекта

### 1. Измените строки идентификации

В **`usbconfig.h`**:

```c
#define USB_CFG_VENDOR_NAME     'Y','o','u','r','N','a','m','e'
#define USB_CFG_VENDOR_NAME_LEN 8  // Длина строки

#define USB_CFG_DEVICE_NAME     'Y','o','u','r','D','e','v','i','c','e'
#define USB_CFG_DEVICE_NAME_LEN 11  // Длина строки
```

### 2. Обновите Python скрипт

В **`test_digispark_vusb.py`**:

```python
MANUFACTURER_STRING = "YourName"
PRODUCT_STRING = "YourDevice"
```

**ВАЖНО:** Строки должны совпадать в firmware и Python скрипте!

## Использование

### 1. Прошейте Digispark

```bash
cd Digispark_ATtiny85_VUSB
make upload
```

### 2. Установите драйвер (Windows)

1. Скачайте [Zadig](https://zadig.akeo.ie/)
2. Подключите Digispark
3. Выберите устройство "DigisparkTest"
4. Установите драйвер: **libusb-win32** или **WinUSB**

### 3. Запустите Python скрипт

```powershell
cd ..
python test_digispark_vusb.py
```

Вы должны увидеть:
```
Поиск устройства (VID: 0x16c0, PID: 0x05dc)...

Найдено устройство:
  Manufacturer: TestDevice
  Product: DigisparkTest
  ✓ Это наше устройство!

✓ Устройство найдено!
✓ Конфигурация установлена

Проверка связи через ECHO команду...
✓ ECHO test passed: [42, 23, 0, 0]

Начинаем чтение данных... (Ctrl+C для выхода)

Получено значение: 00 | Время: 14:23:45 | Успешно: 1
Получено значение: 01 | Время: 14:23:46 | Успешно: 2
Получено значение: 02 | Время: 14:23:47 | Успешно: 3
...
```

## Устранение проблем

### Компиляция

**Ошибка: `usbdrv.h: No such file or directory`**
- Проверьте путь к V-USB в Makefile
- Убедитесь, что V-USB клонирован правильно

**Ошибка: `region 'text' overflowed`**
- Firmware слишком большой для ATtiny85
- Уменьшите размер кода или используйте оптимизацию `-Os`

### Прошивка

**Ошибка: `micronucleus: command not found`**
- Установите micronucleus
- Или укажите полный путь в Makefile

**Ошибка: `Device not found`**
- Отключите и заново подключите Digispark
- Bootloader активен только 5 секунд после подключения
- Попробуйте другой USB порт

### Python скрипт

**Ошибка: `Device not found`**
1. Проверьте, что устройство определяется:
   ```powershell
   # Windows PowerShell
   Get-PnpDevice | Select-Object FriendlyName, Status
   ```

2. Проверьте строки идентификации в firmware и скрипте

3. Убедитесь, что драйвер установлен (Windows)

**Ошибка: `Access denied` (Windows)**
- Установите драйвер через Zadig
- Или запустите скрипт от администратора

**Ошибка: `usb.core.USBError: [Errno 110] Operation timed out`**
- Устройство занято другой программой
- Переподключите Digispark
- Проверьте, что firmware загружен корректно

## Модификация для реального проекта

### Для чтения датчика освещенности (как в оригинале):

1. Добавьте код датчика (I2C/ADC) в `main.c`
2. Замените `testValue` на реальное значение датчика
3. Измените строки USB на свои уникальные

### Пример для ADC:

```c
void adc_init(void) {
    ADMUX = (1 << REFS1);  // Internal 1.1V reference
    ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1);
}

uint16_t adc_read(void) {
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
    return ADC;
}

// В main():
uint16_t sensor_value = adc_read();
```

## Ссылки

- [Оригинальный проект](https://github.com/xythobuz/AutoBrightness)
- [V-USB Library](https://www.obdev.at/products/vusb/)
- [Digispark Wiki](http://digistump.com/wiki/digispark)
- [ATtiny85 Datasheet](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)
- [Micronucleus Bootloader](https://github.com/micronucleus/micronucleus)

## Лицензия

На основе кода из https://github.com/xythobuz/AutoBrightness (GPLv3)

Использует [V-USB](https://github.com/obdev/v-usb) (GPLv2/GPLv3)
