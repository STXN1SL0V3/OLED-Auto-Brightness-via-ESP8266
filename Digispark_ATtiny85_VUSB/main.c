/*
 * Digispark ATtiny85 Photoresistor Firmware
 * Читает значение фоторезистора и передает через USB Control Transfer
 * 
 * БЕЗОПАСНАЯ схема подключения:
 * +5V --- [Фоторезистор] --- P2 (физический pin 7) --- [47kΩ] --- GND
 * 
 * P2 = физический pin 7 = PB2 = ADC1 - ЕДИНСТВЕННЫЙ безопасный ADC пин!
 * 
 * На основе: https://github.com/xythobuz/AutoBrightness
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <util/delay.h>
#include <stdbool.h>

#include "usbdrv.h"
#include "osccal.h"

// Custom request commands
#define CUSTOM_RQ_ECHO  0  // для проверки связи
#define CUSTOM_RQ_RESET 1  // сброс в bootloader
#define CUSTOM_RQ_GET   2  // получить значение фоторезистора

static uint16_t sensorValue = 0;  // Значение АЦП (0-1023)
static uint16_t counter = 0;
static bool keep_feeding = true;

// Прототип функции
uint16_t readADC(uint8_t channel);

// Функция чтения АЦП с заданного канала
// channel: 0=ADC0, 1=ADC1, 2=ADC2, 3=ADC3
uint16_t readADC(uint8_t channel) {
    // Выбираем канал и опорное напряжение VCC
    ADMUX = (0 << REFS1) |   // VCC как опорное напряжение
            (0 << REFS0) |   // (REFS1:0 = 00)
            (0 << ADLAR) |   // Результат выравнен вправо (10 бит)
            (channel & 0x0F); // Выбираем канал (MUX[3:0])
    
    // Включаем АЦП, запускаем преобразование, делитель /128 (16.5MHz/128 = 129kHz)
    ADCSRA = (1 << ADEN) |   // Включить АЦП
             (1 << ADSC) |   // Начать преобразование
             (1 << ADPS2) |  // Prescaler 128
             (1 << ADPS1) |
             (1 << ADPS0);
    
    // Ждем завершения преобразования
    while (ADCSRA & (1 << ADSC));
    
    // Читаем результат (10 бит)
    uint16_t result = ADC;
    
    return result;
}

// USB callback для обработки control transfers
usbMsgLen_t usbFunctionSetup(uchar data[8]) {
    usbRequest_t *rq = (void *)data;
    static uchar dataBuffer[4];

    if (rq->bRequest == CUSTOM_RQ_ECHO) {
        // Echo test - возвращаем wValue и wIndex для проверки связи
        dataBuffer[0] = rq->wValue.bytes[0];
        dataBuffer[1] = rq->wValue.bytes[1];
        dataBuffer[2] = rq->wIndex.bytes[0];
        dataBuffer[3] = rq->wIndex.bytes[1];
        
        usbMsgPtr = dataBuffer;
        return 4;
        
    } else if (rq->bRequest == CUSTOM_RQ_RESET) {
        // Reset to bootloader (нужны правильные ключи)
        if ((rq->wValue.bytes[0] == 42) && (rq->wIndex.bytes[0] == 23)) {
            keep_feeding = false; // watchdog сбросит через 1 секунду
            wdt_reset();
            dataBuffer[0] = 42; // подтверждение
        } else {
            dataBuffer[0] = 0; // ошибка
        }
        usbMsgPtr = dataBuffer;
        return 1;
        
    } else if (rq->bRequest == CUSTOM_RQ_GET) {
        // Возвращаем текущее значение фоторезистора (0-1023)
        dataBuffer[0] = (sensorValue & 0x00FF) >> 0;  // младший байт
        dataBuffer[1] = (sensorValue & 0xFF00) >> 8;  // старший байт
        
        usbMsgPtr = dataBuffer;
        return 2;
    }

    return 0; // не обрабатываем другие запросы
}

int main(void) {
    wdt_enable(WDTO_1S);
    wdt_reset();

    // Настройка Status LED (PB1)
    DDRB |= (1 << DDB1);  // output
    PORTB |= (1 << PB1);  // включаем LED

    // Настройка АЦП: P2 (PB4) как вход (но PB4 используется для USB D+!)
    // Используем P2 = физический pin 3 = PB4 = ADC2, но это конфликт с USB!
    // РЕШЕНИЕ: Используем PB2 (физический pin 7) = ADC1
    DDRB &= ~(1 << DDB2);  // P2/PB2 как вход
    PORTB &= ~(1 << PB2);  // Отключаем подтяжку (используем внешний делитель)

    // Инициализация USB
    usbInit();
    
    // Форсируем re-enumeration
    usbDeviceDisconnect();
    
    wdt_reset();
    _delay_ms(255); // > 250ms для корректного отключения
    
    usbDeviceConnect();
    
    PORTB &= ~(1 << PB1); // выключаем status LED
    
    // Включаем прерывания
    sei();
    
    sensorValue = 0;
    counter = 0;

    // Главный цикл
    while (1) {
        if (keep_feeding) {
            wdt_reset();
        }
        
        usbPoll();
        
        // Читаем АЦП каждую ~1 секунду
        counter++;
        if (counter >= 10000) { // примерно 1 секунда
            counter = 0;
            
            // Читаем значение фоторезистора с ADC1 (P2/PB2)
            sensorValue = readADC(1);
            
            // LED выключен - не влияет на датчик
        }
        
        _delay_us(100);
    }
}
