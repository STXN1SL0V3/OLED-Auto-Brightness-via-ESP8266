# 🔧 Компиляция и прошивка ATtiny85 (Digispark)

## 📋 Содержание
- [Требования](#требования)
- [Установка инструментов](#установка-инструментов)
- [Компиляция прошивки](#компиляция-прошивки)
- [Прошивка ATtiny85](#прошивка-attiny85)
- [Проверка работы](#проверка-работы)
- [Решение проблем](#решение-проблем)

---

## 🛠️ Требования

### Аппаратное обеспечение:
- **Digispark ATtiny85** (с предустановленным USB-загрузчиком)
- USB кабель (Micro-USB или USB-A, в зависимости от модели)
- Компьютер с Windows/Linux/macOS

### Программное обеспечение:
- **Arduino IDE** 1.8.x или 2.x
- **Digispark Board Support** для Arduino IDE
- **Micronucleus** (загрузчик для прошивки)

---

## 📦 Установка инструментов

### 1. Установка Arduino IDE

**Windows:**
```powershell
# Скачайте с официального сайта
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

### 2. Установка Digispark Board Support

1. Откройте **Arduino IDE**
2. Перейдите в **File → Preferences** (Файл → Настройки)
3. В поле **Additional Boards Manager URLs** добавьте:
   ```
   http://digistump.com/package_digistump_index.json
   ```
4. Нажмите **OK**
5. Откройте **Tools → Board → Boards Manager** (Инструменты → Плата → Менеджер плат)
6. Найдите **Digistump AVR Boards**
7. Нажмите **Install** (Установить)

### 3. Установка драйверов (только Windows)

1. Скачайте драйвер Digispark:
   ```
   https://github.com/digistump/DigistumpArduino/releases
   ```
2. Запустите `DPinst64.exe` (для 64-bit Windows) или `DPinst.exe` (для 32-bit)
3. Следуйте инструкциям установщика

---

## ⚙️ Компиляция прошивки

### Структура проекта:

```
Digispark_ATtiny85_VUSB/
├── Digispark_VUSB_Firmware.ino    # Основная прошивка
├── v-usb/                          # Библиотека V-USB
│   ├── usbdrv/                     # Драйвер V-USB
│   └── README.md
└── COMPILE_AND_FLASH.md            # Этот файл
```

### Шаги компиляции:

1. **Откройте Arduino IDE**

2. **Откройте прошивку:**
   - File → Open (Файл → Открыть)
   - Выберите `Digispark_VUSB_Firmware.ino`

3. **Настройте параметры платы:**
   - **Tools → Board** → Digistump AVR Boards → **Digispark (Default - 16.5MHz)**
   - **Tools → Programmer** → **Micronucleus**

4. **Проверьте компиляцию:**
   - Нажмите кнопку **Verify** (✓) или `Ctrl+R`
   - Дождитесь сообщения "Done compiling" (Компиляция завершена)

### Настройка параметров (опционально):

В файле `Digispark_VUSB_Firmware.ino` можете изменить:

```cpp
// USB Device Info
#define USB_CFG_VENDOR_ID       0x16c0  // VID (не меняйте без необходимости)
#define USB_CFG_DEVICE_ID       0x05df  // PID (не меняйте без необходимости)
#define USB_CFG_VENDOR_NAME     'D','i','g','i','s','p','a','r','k'
#define USB_CFG_DEVICE_NAME     'O','L','E','D',' ','B','r','i','g','h','t'

// Интервал отправки данных (мс)
#define SEND_INTERVAL           100     // По умолчанию 100 мс
```

---

## 📲 Прошивка ATtiny85

### ⚠️ ВАЖНО перед прошивкой:

1. **НЕ подключайте** Digispark к USB **ДО** начала прошивки
2. Убедитесь, что никакие другие программы не используют COM-порты
3. Закройте все программы мониторинга USB (например, USBDeview)

### Процесс прошивки:

1. **Запустите загрузку:**
   - В Arduino IDE нажмите **Upload** (→) или `Ctrl+U`
   - Вы увидите сообщение:
     ```
     Running Micronucleus...
     Please plug in the device...
     ```

2. **Подключите Digispark:**
   - **В течение 60 секунд** вставьте Digispark в USB-порт
   - Загрузчик автоматически обнаружит устройство

3. **Дождитесь завершения:**
   ```
   > Device is found!
   > Starting upload...
   > Writing: 100% complete
   > Starting the user app...
   > Micronucleus done. Thank you!
   ```

4. **Готово!**
   - Отключите и снова подключите Digispark
   - Устройство готово к работе

### Альтернативный метод (командная строка):

**Windows:**
```powershell
# Перейдите в папку с micronucleus.exe
cd "C:\Users\<User>\AppData\Local\Arduino15\packages\digistump\tools\micronucleus\2.0a4"

# Запустите прошивку
.\micronucleus.exe --run "путь\к\Digispark_VUSB_Firmware.ino.hex"
```

**Linux/macOS:**
```bash
# Установите micronucleus (если не установлен)
sudo apt install micronucleus  # Ubuntu/Debian
brew install micronucleus      # macOS

# Запустите прошивку
micronucleus --run /path/to/Digispark_VUSB_Firmware.ino.hex
```

---

## ✅ Проверка работы

### 1. Проверка USB-подключения:

**Windows:**
```powershell
# PowerShell - проверка USB устройств
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*Digispark*"}
```

**Linux:**
```bash
# Список USB устройств
lsusb | grep "16c0:05df"
```

### 2. Проверка через Python-программу:

Запустите основную программу `OLED_Auto_Brightness.py`:
```bash
python OLED_Auto_Brightness.py
```

В интерфейсе программы:
- Откройте **Settings** (⚙️ Настройки)
- В разделе **Device Selection** выберите **Digispark (V-USB)**
- Нажмите **Save**

Если всё работает, вы увидите:
- ✅ Зелёный индикатор подключения
- Текущее значение яркости с датчика
- Автоматическая регулировка яркости OLED

### 3. Проверка данных с датчика:

В главном окне программы должны отображаться:
- **Sensor:** текущее значение освещённости (0-1023)
- **Target:** целевая яркость (40-100%)
- **Averaging:** усреднённое значение за период

---

## 🔧 Решение проблем

### ❌ Проблема: "Device not found" (Устройство не найдено)

**Решение:**
1. Проверьте USB-кабель (используйте кабель с данными, не только для зарядки)
2. Попробуйте другой USB-порт
3. Переустановите драйверы (Windows):
   ```powershell
   # Запустите установщик драйверов повторно
   DPinst64.exe
   ```
4. Проверьте, что Digispark в режиме загрузчика:
   - Отключите от USB
   - Зажмите кнопку RESET (если есть)
   - Подключите к USB, удерживая RESET 1-2 секунды

### ❌ Проблема: "Access denied" (Доступ запрещён)

**Windows:**
- Запустите Arduino IDE **от имени администратора**

**Linux:**
- Добавьте правила udev:
  ```bash
  sudo nano /etc/udev/rules.d/49-micronucleus.rules
  ```
  Вставьте:
  ```
  SUBSYSTEMS=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE:="0666"
  ```
  Сохраните и выполните:
  ```bash
  sudo udevadm control --reload-rules
  sudo udevadm trigger
  ```

### ❌ Проблема: Компиляция не проходит

**Ошибка:** `usbdrv.h: No such file or directory`

**Решение:**
1. Убедитесь, что папка `v-usb/usbdrv/` находится в той же директории, что и `.ino` файл
2. Проверьте пути включения в коде:
   ```cpp
   #include "v-usb/usbdrv/usbdrv.h"
   ```

### ❌ Проблема: После прошивки устройство не работает

**Решение:**
1. Проверьте, что правильно настроены **Fuses** (предохранители):
   - Low Fuse: `0xE1` (для 16.5 MHz PLL)
   - High Fuse: `0xDD`
   - Extended Fuse: `0xFE`

2. Повторно прошейте устройство с опцией "Burn Bootloader":
   - Tools → Burn Bootloader (Инструменты → Записать загрузчик)

3. Проверьте питание:
   - ATtiny85 требует стабильное питание 5V
   - Используйте качественный USB-порт (не хаб)

### ❌ Проблема: Python-программа не видит Digispark

**Решение:**
1. Проверьте настройки в `config.ini`:
   ```ini
   [Mode]
   device = digispark
   ```

2. Переустановите драйвер libusb:
   ```bash
   pip install --upgrade libusb-package
   ```

3. Проверьте VID/PID устройства:
   - Должны совпадать с указанными в прошивке
   - По умолчанию: `VID=0x16c0`, `PID=0x05df`

---

## 📚 Дополнительные ресурсы

### Официальная документация:
- **Digispark Wiki:** http://digistump.com/wiki/
- **V-USB Project:** https://www.obdev.at/products/vusb/
- **ATtiny85 Datasheet:** https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf

### Форумы и сообщества:
- **Arduino Forum - Digispark:** https://forum.arduino.cc/
- **Digistump Forum:** http://digistump.com/board/

### Видео-инструкции:
- YouTube: "How to program Digispark ATtiny85"
- YouTube: "V-USB tutorial for ATtiny85"

---

## 📝 Примечания

### Важные моменты:

1. **Загрузчик занимает ~2KB памяти**
   - Доступно ~6KB для вашей программы
   - Учитывайте это при разработке

2. **USB работает программно (bit-banging)**
   - Может быть нестабильным при высоких нагрузках
   - Рекомендуется не использовать задержки > 10ms в loop()

3. **Частота CPU: 16.5 MHz (внутренний PLL)**
   - Digispark использует внутренний RC-генератор + PLL
   - Точность ~±10% (достаточно для USB)

4. **Первая прошивка занимает ~60 секунд**
   - Последующие прошивки ~5-10 секунд
   - Это нормально для загрузчика Micronucleus

---

## 🆘 Поддержка

Если у вас возникли проблемы:

1. **Проверьте Issues на GitHub:**
   - https://github.com/STXN1SL0V3/OLED-Auto-Brightness-via-ESP8266/issues

2. **Создайте новый Issue:**
   - Опишите проблему
   - Приложите логи/скриншоты
   - Укажите версию Arduino IDE и ОС

3. **Контакты:**
   - GitHub: [@STXN1SL0V3](https://github.com/STXN1SL0V3)

---

**Удачной прошивки! 🚀**
