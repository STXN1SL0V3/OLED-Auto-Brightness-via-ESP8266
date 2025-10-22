# Makefile для Digispark ATtiny85 Test Firmware
# На основе: https://github.com/xythobuz/AutoBrightness

MCU = attiny85
F_CPU = 16500000
TARGET = digispark_test

# Компилятор и утилиты
CC = avr-gcc
OBJCOPY = avr-objcopy
SIZE = avr-size
REMOVE = rm -f

# Пути к V-USB (НАСТРОЙТЕ ПОД СВОЮ СИСТЕМУ!)
VUSB_DIR = v-usb/usbdrv

# Исходные файлы
SRC = main.c $(VUSB_DIR)/usbdrv.c
ASRC = $(VUSB_DIR)/usbdrvasm.S

# Директории include
EXTRAINCDIRS = . $(VUSB_DIR)

# Флаги компиляции
CFLAGS = -g -Os
CFLAGS += -DF_CPU=$(F_CPU)UL
CFLAGS += -mmcu=$(MCU)
CFLAGS += -Wall -Wstrict-prototypes
CFLAGS += -funsigned-char
CFLAGS += -funsigned-bitfields
CFLAGS += -fpack-struct
CFLAGS += -fshort-enums
CFLAGS += $(patsubst %,-I%,$(EXTRAINCDIRS))
CFLAGS += -std=gnu99

# Флаги ассемблера
ASFLAGS = -DF_CPU=$(F_CPU)
ASFLAGS += $(patsubst %,-I%,$(EXTRAINCDIRS))
ASFLAGS += -x assembler-with-cpp
ASFLAGS += -Wa,-gstabs,--listing-cont-lines=100

# Флаги линковщика
LDFLAGS = -Wl,-Map=$(TARGET).map,--cref
LDFLAGS += -lm

# Правила сборки
all: $(TARGET).hex size

$(TARGET).elf: $(SRC) $(ASRC)
	$(CC) $(CFLAGS) $(ASFLAGS) -o $@ $^ $(LDFLAGS)

$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex -R .eeprom -R .fuse -R .lock -R .signature $< $@

size: $(TARGET).elf
	@echo
	@echo "=== Размер прошивки ==="
	$(SIZE) --mcu=$(MCU) --format=avr $<
	@echo

clean:
	$(REMOVE) $(TARGET).elf $(TARGET).hex $(TARGET).map

# Прошивка через micronucleus (для Digispark)
upload: $(TARGET).hex
	@echo "Подключите Digispark СЕЙЧАС..."
	micronucleus --run $(TARGET).hex

# Прошивка через avrdude (если у вас программатор)
program: $(TARGET).hex
	avrdude -p $(MCU) -c usbasp -U flash:w:$(TARGET).hex:i

.PHONY: all clean size upload program
