/*
 * usbconfig.h - Конфигурация V-USB для Digispark ATtiny85
 * На основе: https://github.com/xythobuz/AutoBrightness
 */

#ifndef __usbconfig_h_included__
#define __usbconfig_h_included__

/* ---------------------------- Hardware Config ---------------------------- */

#define USB_CFG_IOPORTNAME      B
// Порт для USB (PORTB для Digispark)

#define USB_CFG_DMINUS_BIT      3
// D- подключен к PB3

#define USB_CFG_DPLUS_BIT       4
// D+ подключен к PB4 (и к INT0)

#define USB_CFG_CLOCK_KHZ       16500
// Частота ATtiny85 на Digispark (16.5 MHz)

/* --------------------------- Functional Range ---------------------------- */

#define USB_CFG_HAVE_INTRIN_ENDPOINT    0
// Не используем interrupt-in endpoint

#define USB_CFG_HAVE_INTRIN_ENDPOINT3   0
// Не используем endpoint 3

#define USB_CFG_IMPLEMENT_HALT          0
// Не нужна функция ENDPOINT_HALT

#define USB_CFG_SUPPRESS_INTR_CODE      0
// Компилируем код для interrupt endpoints

#define USB_CFG_INTR_POLL_INTERVAL      10
// Интервал опроса в миллисекундах

#define USB_CFG_IS_SELF_POWERED         0
// Питание от USB шины

#define USB_CFG_MAX_BUS_POWER           100
// Максимум 100 mA

#define USB_CFG_IMPLEMENT_FN_WRITE      0
// Не нужна usbFunctionWrite()

#define USB_CFG_IMPLEMENT_FN_READ       0
// Не нужна usbFunctionRead()

#define USB_CFG_IMPLEMENT_FN_WRITEOUT   0
// Не нужна usbFunctionWriteOut()

#define USB_CFG_HAVE_FLOWCONTROL        0
// Не нужен flow control

#define USB_CFG_DRIVER_FLASH_PAGE       0
// Для устройств < 64KB flash

#define USB_CFG_LONG_TRANSFERS          0
// Передачи < 254 байт

/* ------------------- USB Reset Hook with Oscillator Calibration ---------- */

#ifndef __ASSEMBLER__
#include <avr/interrupt.h>
extern void calibrateOscillator(void);
#endif

#define USB_RESET_HOOK(resetStarts)  if(!resetStarts){cli(); calibrateOscillator(); sei();}
// Калибровка осциллятора при USB reset

#define USB_CFG_CHECK_DATA_TOGGLING     0
// Не проверяем дубликаты пакетов

#define USB_CFG_HAVE_MEASURE_FRAME_LENGTH   1
// Включаем функцию калибровки осциллятора

#define USB_USE_FAST_CRC                0
// Используем компактную версию CRC

/* -------------------------- Device Description --------------------------- */

#define USB_CFG_VENDOR_ID       0xc0, 0x16
// Shared V-USB VID: 0x16c0

#define USB_CFG_DEVICE_ID       0xdc, 0x05
// Shared V-USB PID: 0x05dc

#define USB_CFG_DEVICE_VERSION  0x00, 0x01
// Версия 1.0

#define USB_CFG_VENDOR_NAME     'T','e','s','t','D','e','v','i','c','e'
#define USB_CFG_VENDOR_NAME_LEN 10
// Строка производителя (ИЗМЕНИТЕ НА СВОЮ!)

#define USB_CFG_DEVICE_NAME     'D','i','g','i','s','p','a','r','k','T','e','s','t'
#define USB_CFG_DEVICE_NAME_LEN 13
// Строка устройства (ИЗМЕНИТЕ НА СВОЮ!)

#define USB_CFG_DEVICE_CLASS        0xff    // Vendor specific
#define USB_CFG_DEVICE_SUBCLASS     0
#define USB_CFG_INTERFACE_CLASS     0
#define USB_CFG_INTERFACE_SUBCLASS  0
#define USB_CFG_INTERFACE_PROTOCOL  0

/* ------------------- Fine Control over USB Descriptors ------------------- */

#define USB_CFG_DESCR_PROPS_DEVICE                  0
#define USB_CFG_DESCR_PROPS_CONFIGURATION           0
#define USB_CFG_DESCR_PROPS_STRINGS                 0
#define USB_CFG_DESCR_PROPS_STRING_0                0
#define USB_CFG_DESCR_PROPS_STRING_VENDOR           0
#define USB_CFG_DESCR_PROPS_STRING_PRODUCT          0
#define USB_CFG_DESCR_PROPS_STRING_SERIAL_NUMBER    0
#define USB_CFG_DESCR_PROPS_HID                     0
#define USB_CFG_DESCR_PROPS_HID_REPORT              0
#define USB_CFG_DESCR_PROPS_UNKNOWN                 0

/* ----------------------- Optional MCU Description ------------------------ */

// Настройка прерываний для Digispark (из micronucleus bootloader)
#define USB_INTR_CFG            PCMSK
#define USB_INTR_CFG_SET        (1 << USB_CFG_DPLUS_BIT)
#define USB_INTR_CFG_CLR        0
#define USB_INTR_ENABLE         GIMSK
#define USB_INTR_ENABLE_BIT     PCIE
#define USB_INTR_PENDING        GIFR
#define USB_INTR_PENDING_BIT    PCIF
#define USB_INTR_VECTOR         PCINT0_vect

#define USB_CFG_CHECK_CRC       0
// Не проверяем CRC для экономии памяти

#define USB_COUNT_SOF           1
// Считаем SOF для калибровки осциллятора

#endif /* __usbconfig_h_included__ */
