# -*- coding: utf-8 -*-
"""
Файл локализации для Auto OLED Brightness
Поддерживаемые языки: русский (ru), английский (en)
"""

TRANSLATIONS = {
    'ru': {
        # Основное окно
        'mode_auto': 'Автоматическая яркость',
        'mode_manual': 'Ручная регулировка',
        'brightness': 'Яркость',
        'light_level': 'Уровень освещения',
        'sensor_value': 'Значение датчика',
        'settings': 'Настройки',
        'hide': 'Свернуть',
        'reconnect': 'Переподключить датчик',
        'searching_sensor': 'Поиск датчика...',
        'sensor_found': 'Датчик найден',
        'sensor_not_found': 'Датчик не найден',
        'connection_lost': 'Соединение потеряно',
        'repeat_search': 'Повторить поиск',
        
        # Настройки - Режим работы
        'settings_title': 'Настройки и калибровка',
        'mode_title': 'Режим работы',
        'mode_esp8266': 'ESP8266 (WiFi)',
        'mode_digispark': 'Digispark (USB)',
        'mode_digispark_unavailable': 'Digispark (USB) - недоступен (нет pyusb)',
        
        # Настройки - Калибровка
        'calibration_title': 'Калибровка датчика',
        'calibration_info': 'Настройте диапазон чувствительности датчика освещенности.',
        'sensor_min': 'Минимум (темно):',
        'sensor_max': 'Максимум (светло):',
        'current_value': 'Текущее значение',
        'set_min': 'Установить минимум',
        'set_max': 'Установить максимум',
        'calibration_saved': 'Калибровка сохранена',
        
        # Настройки - Яркость экрана
        'brightness_title': 'Яркость экрана (автоматический режим)',
        'min_brightness': 'Минимальная яркость:',
        'max_brightness': 'Максимальная яркость:',
        
        # Настройки - Усреднение
        'averaging_title': 'Усреднение показаний',
        'averaging_period': 'Период усреднения:',
        'averaging_info': 'Время усреднения показаний датчика. Чем меньше значение, тем быстрее реакция.',
        
        # Настройки - ESP8266
        'esp_title': 'Настройки ESP8266',
        'esp_ip': 'IP адрес:',
        'esp_open_web': '🌐 Открыть веб-интерфейс ESP8266',
        
        # Настройки - Запуск
        'startup_title': 'Параметры запуска',
        'autostart': 'Загружать вместе с Windows',
        'start_minimized': 'Запускать свернутым в трей',
        
        # Кнопки
        'save_close': '💾 Сохранить и закрыть',
        'cancel': '❌ Отмена',
        'success': 'Успех',
        'settings_saved': 'Настройки сохранены!\n\nИзменения яркости применены сразу.',
        
        # Трей
        'tray_show': 'Показать окно',
        'tray_settings': 'Настройки',
        'tray_restart': 'Перезапустить',
        'tray_exit': 'Выход',
        
        # Сообщения
        'device_not_found': 'Устройство не найдено',
        'connecting': 'Подключение...',
        'connected': 'Подключено',
        
        # Диалоги калибровки
        'calib_min_title': 'Калибровка минимума',
        'calib_min_message': 'Закройте датчик рукой или создайте полную темноту.\n\nПосле нажатия OK программа будет измерять значения 5 секунд.\n\nГотовы?',
        'calib_max_title': 'Калибровка максимума',
        'calib_max_message': 'Направьте датчик на яркий свет (лампа, окно).\n\nПосле нажатия OK программа будет измерять значения 5 секунд.\n\nГотовы?',
        'measurement': 'Измерение',
        'calib_min_success': 'Минимум откалиброван',
        'calib_max_success': 'Максимум откалиброван',
        'error': 'Ошибка',
        'sensor_read_error': 'Не удалось прочитать датчик!',
        'current_calibration': 'Текущая калибровка',
        'minimum': 'Минимум',
        'maximum': 'Максимум',
        
        # Кнопки калибровки
        'calibrate_min': 'Калибровать минимум (темно)',
        'calibrate_max': 'Калибровать максимум (светло)',
        
        # Строки статуса
        'sensor': 'Датчик',
        'averaging_for': 'Усреднение за',
        'sec': 'сек',
        'target': 'Целевая',
        'current_status': 'Текущая',
    },
    
    'en': {
        # Main window
        'mode_auto': 'Automatic Brightness',
        'mode_manual': 'Manual Control',
        'brightness': 'Brightness',
        'light_level': 'Light Level',
        'sensor_value': 'Sensor Value',
        'settings': 'Settings',
        'hide': 'Hide',
        'reconnect': 'Reconnect Sensor',
        'searching_sensor': 'Searching sensor...',
        'sensor_found': 'Sensor found',
        'sensor_not_found': 'Sensor not found',
        'connection_lost': 'Connection lost',
        'repeat_search': 'Repeat Search',
        
        # Settings - Mode
        'settings_title': 'Settings and Calibration',
        'mode_title': 'Operating Mode',
        'mode_esp8266': 'ESP8266 (WiFi)',
        'mode_digispark': 'Digispark (USB)',
        'mode_digispark_unavailable': 'Digispark (USB) - unavailable (no pyusb)',
        
        # Settings - Calibration
        'calibration_title': 'Sensor Calibration',
        'calibration_info': 'Adjust the light sensor sensitivity range.',
        'sensor_min': 'Minimum (dark):',
        'sensor_max': 'Maximum (bright):',
        'current_value': 'Current value',
        'set_min': 'Set Minimum',
        'set_max': 'Set Maximum',
        'calibration_saved': 'Calibration saved',
        
        # Settings - Screen Brightness
        'brightness_title': 'Screen Brightness (automatic mode)',
        'min_brightness': 'Minimum brightness:',
        'max_brightness': 'Maximum brightness:',
        
        # Settings - Averaging
        'averaging_title': 'Sensor Averaging',
        'averaging_period': 'Averaging period:',
        'averaging_info': 'Sensor data averaging time. Lower value = faster response.',
        
        # Settings - ESP8266
        'esp_title': 'ESP8266 Settings',
        'esp_ip': 'IP Address:',
        'esp_open_web': '🌐 Open ESP8266 Web Interface',
        
        # Settings - Startup
        'startup_title': 'Startup Options',
        'autostart': 'Start with Windows',
        'start_minimized': 'Start minimized to tray',
        
        # Buttons
        'save_close': '💾 Save and Close',
        'cancel': '❌ Cancel',
        'success': 'Success',
        'settings_saved': 'Settings saved!\n\nBrightness changes applied immediately.',
        
        # Tray
        'tray_show': 'Show Window',
        'tray_settings': 'Settings',
        'tray_restart': 'Restart',
        'tray_exit': 'Exit',
        
        # Messages
        'device_not_found': 'Device not found',
        'connecting': 'Connecting...',
        'connected': 'Connected',
        
        # Calibration dialogs
        'calib_min_title': 'Minimum Calibration',
        'calib_min_message': 'Cover the sensor with your hand or create complete darkness.\n\nAfter clicking OK, the program will measure values for 5 seconds.\n\nReady?',
        'calib_max_title': 'Maximum Calibration',
        'calib_max_message': 'Point the sensor at bright light (lamp, window).\n\nAfter clicking OK, the program will measure values for 5 seconds.\n\nReady?',
        'measurement': 'Measurement',
        'calib_min_success': 'Minimum calibrated',
        'calib_max_success': 'Maximum calibrated',
        'error': 'Error',
        'sensor_read_error': 'Failed to read sensor!',
        'current_calibration': 'Current calibration',
        'minimum': 'Minimum',
        'maximum': 'Maximum',
        
        # Calibration buttons
        'calibrate_min': 'Calibrate minimum (dark)',
        'calibrate_max': 'Calibrate maximum (bright)',
        
        # Status strings
        'sensor': 'Sensor',
        'averaging_for': 'Averaging for',
        'sec': 'sec',
        'target': 'Target',
        'current_status': 'Current',
    }
}


class Localization:
    """Класс для работы с локализацией"""
    
    def __init__(self, language='ru'):
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['ru'])
    
    def get(self, key, default=None):
        """Получить перевод по ключу"""
        return self.translations.get(key, default or key)
    
    def set_language(self, language):
        """Установить язык"""
        if language in TRANSLATIONS:
            self.language = language
            self.translations = TRANSLATIONS[language]
            return True
        return False
    
    def get_language(self):
        """Получить текущий язык"""
        return self.language
    
    def get_available_languages(self):
        """Получить список доступных языков"""
        return list(TRANSLATIONS.keys())


# Глобальный объект локализации (создается при импорте)
_localization = Localization()


def get_text(key, default=None):
    """Быстрый доступ к переводу"""
    return _localization.get(key, default)


def set_language(language):
    """Установить язык приложения"""
    return _localization.set_language(language)


def get_language():
    """Получить текущий язык"""
    return _localization.get_language()


def get_localization():
    """Получить объект локализации"""
    return _localization
