# OLED Auto Brightness
# Copyright (C) 2025 STXN1SL0V3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Простое управление яркостью OLED от ESP8266 / Digispark ATtiny85
Автоматически подключается к датчику освещенности и регулирует яркость
"""

import tkinter as tk
from tkinter import ttk, messagebox
import win32con
import win32api
import win32gui
import requests
import threading
import time
import pystray
from PIL import Image, ImageDraw
import configparser
import os
import sys
import subprocess
import shutil
import tempfile
import atexit

# Импорт локализации
from localization import get_text, set_language, get_language, get_localization

def get_config_path():
    """Получить правильный путь к config.ini для скомпилированной программы"""
    if getattr(sys, 'frozen', False):
        # Если программа скомпилирована - сохраняем config рядом с exe
        return os.path.join(os.path.dirname(sys.executable), 'config.ini')
    else:
        # Если запущена как скрипт - в папке скрипта
        return os.path.join(os.path.dirname(__file__), 'config.ini')

def cleanup_pyinstaller_temp():
    """Очистка старых временных папок PyInstaller"""
    try:
        if not getattr(sys, 'frozen', False):
            return  # Работает только для скомпилированной программы
        
        temp_dir = tempfile.gettempdir()
        current_mei = getattr(sys, '_MEIPASS', None)
        
        # Ищем старые _MEI папки
        for item in os.listdir(temp_dir):
            if item.startswith('_MEI') and os.path.isdir(os.path.join(temp_dir, item)):
                mei_path = os.path.join(temp_dir, item)
                
                # Не удаляем текущую папку
                if current_mei and os.path.samefile(mei_path, current_mei):
                    continue
                
                # Пытаемся удалить старую папку
                try:
                    shutil.rmtree(mei_path, ignore_errors=True)
                    print(f"🗑️ Удалена старая временная папка: {item}")
                except Exception as e:
                    # Если не удалось - не критично, просто игнорируем
                    pass
    except Exception as e:
        print(f"⚠ Ошибка очистки временных файлов: {e}")

# Очищаем старые временные файлы при запуске
cleanup_pyinstaller_temp()

# Регистрируем очистку при выходе
atexit.register(cleanup_pyinstaller_temp)

# Добавляем libusb в PATH (для PyUSB)
if hasattr(sys, 'frozen'):
    # Если запущено как exe (PyInstaller) - DLL находится в корне временной папки
    libusb_path = sys._MEIPASS
else:
    # Если запущено как скрипт
    venv_path = os.path.dirname(sys.executable)
    libusb_path = os.path.join(venv_path, '..', 'Lib', 'site-packages', 'libusb_package')
    libusb_path = os.path.abspath(libusb_path)

if os.path.exists(libusb_path):
    os.environ['PATH'] = libusb_path + os.pathsep + os.environ.get('PATH', '')
    print(f"✓ libusb путь добавлен: {libusb_path}")
else:
    print(f"⚠ libusb_package не найден: {libusb_path}")

# Для горячих клавиш и глобальной прокрутки мыши
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# Для глобального перехвата прокрутки мыши
try:
    import mouse
    MOUSE_AVAILABLE = True
except ImportError:
    MOUSE_AVAILABLE = False

# Для Digispark
try:
    import usb.core
    import usb.util
    DIGISPARK_AVAILABLE = True
except ImportError:
    DIGISPARK_AVAILABLE = False

# Константы для Digispark
CUSTOM_RQ_ECHO = 0
CUSTOM_RQ_RESET = 1
CUSTOM_RQ_GET = 2
USB_VENDOR_ID = 0x16c0
USB_PRODUCT_ID = 0x05dc
MANUFACTURER_STRING = "TestDevice"
PRODUCT_STRING = "DigisparkTest"


class SimpleBrightnessControl:
    def __init__(self):
        # Загрузка конфигурации
        self.load_config()
        
        # Главное окно
        self.control_window = tk.Tk()
        self.control_window.title("OLED Auto Brightness")  # Убрали эмодзи солнца
        
        # Применяем тёмную тему для рамки окна (Windows 10/11)
        try:
            # Для Windows 10/11 - делаем тёмную рамку заголовка
            import ctypes
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            hwnd = ctypes.windll.user32.GetParent(self.control_window.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(1)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            pass  # Если не получилось - не критично
        
        # Временно устанавливаем размер для получения screen info
        self.control_window.geometry("450x500")
        self.control_window.update_idletasks()
        
        # Получаем размеры экрана
        screen_width = self.control_window.winfo_screenwidth()
        screen_height = self.control_window.winfo_screenheight()
        
        # ВАЖНО: вычитаем больше для учета панели задач (обычно 40-72px)
        window_width = 450
        window_height = 500
        x = screen_width - window_width - 10
        y = screen_height - window_height - 100  # 100px отступ снизу (учитывает панель задач)
        
        # Применяем финальную геометрию
        self.control_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.control_window.resizable(False, False)
        self.control_window.configure(bg='#2b2b2b')
        # НЕ используем topmost - перекрывает системный трей и другие важные окна
        # self.control_window.attributes('-topmost', True)
        
        # Установка иконки окна
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            try:
                self.control_window.iconbitmap(icon_path)
            except:
                pass
        
        # Настройки (загружаются из config.ini)
        self.overlay = None
        self.current_brightness = 100
        self.target_brightness = 100  # Целевая яркость
        self.connected = False
        self.running = True
        
        # Кэш USB устройства Digispark
        self.digispark_device = None
        self.digispark_last_check = 0  # Время последней проверки устройства
        
        # Системный трей
        self.tray_icon = None
        self.window_visible = True
        self.icon_path = icon_path  # Сохраняем путь для трея
        
        # Глобальная горячая клавиша для открытия окна (Ctrl+Shift+B)
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.add_hotkey('ctrl+shift+b', self.show_window_hotkey, suppress=False)
                print("✓ Горячая клавиша Ctrl+Shift+B для открытия окна настроена")
            except Exception as e:
                print(f"⚠ Ошибка настройки горячей клавиши: {e}")
        
        # Окно настроек
        self.settings_window = None  # Ссылка на открытое окно настроек
        
        # Усреднение значений
        self.brightness_history = []  # История значений яркости
        self.last_average_time = time.time()
        
        self.create_interface()
        
        # Привязываем событие потери фокуса - сворачиваем в трей
        self.control_window.bind("<FocusOut>", self.on_focus_out)
        
        # Запуск потока плавного изменения яркости
        self.smooth_thread = threading.Thread(target=self.smooth_brightness_loop, daemon=True)
        self.smooth_thread.start()
        
        # Запуск автоматического режима
        self.auto_thread = threading.Thread(target=self.auto_brightness_loop, daemon=True)
        self.auto_thread.start()
        
        # Запуск потока обновления overlay (для контекстных меню)
        self.overlay_update_thread = threading.Thread(target=self.overlay_update_loop, daemon=True)
        self.overlay_update_thread.start()
        
        # Подключение при запуске
        self.control_window.after(500, self.connect_to_esp)
        
        # Проверяем, нужно ли запускаться в трее
        if self.start_minimized:
            self.control_window.after(100, self.hide_window)
    
    def load_config(self):
        """Загрузка настроек из config.ini"""
        config = configparser.ConfigParser()
        config_path = get_config_path()
        
        # Значения по умолчанию
        self.min_brightness = 20
        self.max_brightness = 100
        self.averaging_period = 10  # Изменено с 60 на 10 секунд для более быстрой реакции
        self.esp_ip = "192.168.1.146"
        self.timeout = 5
        self.smooth_step = 2
        self.start_minimized = False  # Запуск в трее
        self.auto_brightness_enabled = True  # Автоматическая яркость
        self.hotkey_modifier = "ctrl"  # Клавиша-модификатор (ctrl, alt, shift)
        self.hotkey_key = "shift"  # Дополнительная клавиша
        self.manual_brightness = 100  # Ручная яркость
        
        if os.path.exists(config_path):
            try:
                config.read(config_path, encoding='utf-8')
                
                # Загрузка настроек яркости
                if 'Brightness' in config:
                    self.min_brightness = config.getint('Brightness', 'min_brightness', fallback=20)
                    self.max_brightness = config.getint('Brightness', 'max_brightness', fallback=100)
                    self.auto_brightness_enabled = config.getboolean('Brightness', 'auto_enabled', fallback=True)
                    self.manual_brightness = config.getint('Brightness', 'manual_brightness', fallback=100)
                
                # Загрузка настроек усреднения
                if 'Averaging' in config:
                    self.averaging_period = config.getint('Averaging', 'averaging_period', fallback=60)
                
                # Загрузка настроек подключения
                if 'Connection' in config:
                    self.esp_ip = config.get('Connection', 'esp_ip', fallback="192.168.1.146")
                    self.timeout = config.getint('Connection', 'timeout', fallback=5)
                
                # Загрузка настроек плавности
                if 'Smoothing' in config:
                    self.smooth_step = config.getint('Smoothing', 'smooth_step', fallback=2)
                
                # Загрузка настроек запуска
                if 'Startup' in config:
                    self.start_minimized = config.getboolean('Startup', 'start_minimized', fallback=False)
                
                # Загрузка горячих клавиш
                if 'Hotkeys' in config:
                    self.hotkey_modifier = config.get('Hotkeys', 'modifier', fallback='ctrl')
                    self.hotkey_key = config.get('Hotkeys', 'key', fallback='shift')
                
                # Загрузка языка интерфейса
                if 'Interface' in config:
                    language = config.get('Interface', 'language', fallback='ru')
                    set_language(language)
                else:
                    set_language('ru')  # Русский по умолчанию
                
                # Автоопределение режима при первом запуске (если не указан auto_enabled)
                if 'Brightness' not in config or not config.has_option('Brightness', 'auto_enabled'):
                    # Первый запуск - определяем наличие датчика
                    sensor_available = self.check_sensor_availability()
                    self.auto_brightness_enabled = sensor_available
                    print(f"✓ Первый запуск: {'автояркость включена' if sensor_available else 'ручной режим'} (датчик {'найден' if sensor_available else 'не найден'})")
                
                self.max_history_size = self.averaging_period
                
                print(f"✓ Конфигурация загружена:")
                print(f"  Яркость: {self.min_brightness}% - {self.max_brightness}%")
                print(f"  Усреднение: {self.averaging_period} сек")
                print(f"  ESP IP: {self.esp_ip}")
                print(f"  Горячие клавиши: {self.hotkey_modifier}+{self.hotkey_key}+MouseWheel")
                
            except Exception as e:
                print(f"⚠ Ошибка чтения config.ini: {e}")
                print("Используются значения по умолчанию")
                self.max_history_size = 60
        else:
            print("⚠ Файл config.ini не найден, используются значения по умолчанию")
            self.max_history_size = 60
    
    def save_calibration_if_changed(self, min_light, max_light):
        """Сохраняет калибровочные значения в config.ini, если они изменились"""
        # Проверяем, есть ли уже сохранённые значения
        config_path = get_config_path()
        config = configparser.ConfigParser()
        
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        
        # Добавляем секцию Calibration если её нет
        if 'Calibration' not in config:
            config['Calibration'] = {}
        
        # Получаем текущие сохранённые значения
        saved_min = config.getint('Calibration', 'min_light', fallback=-1)
        saved_max = config.getint('Calibration', 'max_light', fallback=-1)
        
        # Сохраняем только если значения изменились
        if saved_min != min_light or saved_max != max_light:
            config['Calibration']['min_light'] = str(min_light)
            config['Calibration']['max_light'] = str(max_light)
            
            with open(config_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            
            print(f"💾 Калибровка сохранена в config.ini: MIN={min_light}, MAX={max_light}")
    
    def create_interface(self):
        """Создание интерфейса"""
        
        # Цветовая схема Visual Studio Code Dark
        bg_main = '#1e1e1e'          # Основной фон VS Code
        bg_secondary = '#252526'      # Вторичный фон
        bg_input = '#3c3c3c'          # Фон для input/кнопок
        fg_primary = '#d4d4d4'        # Основной текст
        fg_accent = '#4ec9b0'         # Акцентный цвет (бирюзовый)
        fg_orange = '#ce9178'         # Оранжевый
        fg_green = '#6a9955'          # Зеленый
        
        self.control_window.configure(bg=bg_main)
        
        # Контейнер для заголовка и кнопки языка
        header_frame = tk.Frame(self.control_window, bg=bg_main)
        header_frame.pack(fill='x', pady=(12, 0))
        
        # Пустой фрейм слева для баланса
        tk.Frame(header_frame, bg=bg_main, width=50).pack(side='left')
        
        # Заголовок - акцентный цвет VS Code (по центру)
        tk.Label(
            header_frame,
            text="Auto OLED Brightness",
            font=("Consolas", 16, "bold"),  # Моноширинный шрифт VS Code
            bg=bg_main,
            fg=fg_accent
        ).pack(side='left', expand=True)
        
        # Кнопка переключения языка (верхний правый угол)
        # ИСПРАВЛЕНО: RU = русский, EN = английский
        self.lang_button = tk.Button(
            header_frame,
            text="RU" if get_language() == 'ru' else "EN",
            command=self.toggle_language,
            bg=bg_input,
            fg=fg_accent,
            relief='flat',
            padx=8,
            pady=4,
            font=("Consolas", 9, "bold"),
            cursor='hand2',
            width=3
        )
        self.lang_button.pack(side='right', padx=(0, 15))
        
        # Подпись автора
        tk.Label(
            self.control_window,
            text="by STXN1SL0V3",
            font=("Consolas", 8),
            bg=bg_main,
            fg=fg_green  # Зеленый для комментариев
        ).pack(pady=(2, 12))
        
        # Статус подключения
        self.connection_label = tk.Label(
            self.control_window,
            text=f"⚫ {get_text('connecting')}",
            font=("Consolas", 10),
            bg=bg_main,
            fg=fg_orange
        )
        self.connection_label.pack(pady=3)
        
        # Кнопка повторного поиска (скрыта по умолчанию)
        self.reconnect_button = tk.Button(
            self.control_window,
            text=f"🔍 {get_text('repeat_search')}",
            command=self.manual_reconnect,
            bg=bg_input,
            fg=fg_primary,
            relief='flat',
            padx=15,
            pady=5,
            font=("Consolas", 9),
            cursor='hand2'
        )
        # Не pack() - покажем только если не подключено
        
        # Текущая яркость
        self.brightness_label = tk.Label(
            self.control_window,
            text="100%",
            font=("Consolas", 36, "bold"),
            bg=bg_main,
            fg=fg_accent  # Акцентный бирюзовый
        )
        self.brightness_label.pack(pady=8)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(
            self.control_window,
            length=400,
            mode='determinate',
            maximum=100
        )
        self.progress['value'] = 100
        self.progress.pack(pady=6)
        
        # Текст для ручной регулировки
        self.manual_label = tk.Label(
            self.control_window,
            text=f"🎚️ {get_text('mode_manual')}:",
            bg=bg_main,
            fg=fg_primary,
            font=("Consolas", 9)
        )
        self.manual_label.pack(pady=(5, 0))
        
        # Ползунок ручной регулировки яркости
        self.manual_slider = tk.Scale(
            self.control_window,
            from_=1,
            to=100,
            orient='horizontal',
            length=400,
            command=self.on_manual_brightness_change,
            bg=bg_secondary,
            fg=fg_primary,
            troughcolor=bg_input,
            highlightthickness=0,
            font=("Consolas", 8),
            sliderlength=30,
            sliderrelief='flat'
        )
        self.manual_slider.set(self.manual_brightness)
        self.manual_slider.pack(pady=(0, 5))
        
        # Чекбокс автоматической яркости
        self.auto_brightness_var = tk.BooleanVar(value=self.auto_brightness_enabled)
        self.auto_check = tk.Checkbutton(
            self.control_window,
            text=f"🤖 {get_text('mode_auto')}",
            variable=self.auto_brightness_var,
            command=self.toggle_auto_brightness,
            bg=bg_main,
            fg=fg_accent,
            selectcolor=bg_input,
            activebackground=bg_main,
            activeforeground=fg_accent,
            font=("Consolas", 10, "bold")
        )
        self.auto_check.pack(pady=5)
        
        # Обновляем состояние ползунка
        self.update_slider_state()
        
        # Информация
        self.info_label = tk.Label(
            self.control_window,
            text=f"{get_text('sensor')}: --- | {get_text('averaging_for')} {self.averaging_period} {get_text('sec')}",
            font=("Consolas", 8),
            bg=bg_main,
            fg=fg_green  # Зеленый для информации
        )
        self.info_label.pack(pady=3)
        
        # Статус
        self.status_label = tk.Label(
            self.control_window,
            text=f"ESP8266: {self.esp_ip} | {get_text('brightness')}: {self.min_brightness}-{self.max_brightness}%",
            font=("Consolas", 8),
            bg=bg_main,
            fg=fg_green  # Зеленый для информации
        )
        self.status_label.pack(pady=3)
        
        # Кнопка настроек и калибровки
        self.settings_btn = tk.Button(
            self.control_window,
            text=f"⚙️ {get_text('settings')}",
            command=self.open_settings_window,
            bg=bg_input,
            fg=fg_primary,
            relief='flat',
            padx=15,
            pady=5,
            font=("Consolas", 9),
            cursor='hand2'
        )
        self.settings_btn.pack(pady=3)
        
        # Убрали чекбокс автозагрузки - теперь в настройках
        
        # Добавляем функционал перетаскивания основного окна за любую свободную область
        def start_move_main(event):
            # Проверяем, что клик не по ползунку или кнопке
            widget = event.widget
            if widget in (self.manual_slider, self.settings_btn):
                return
            self.control_window._drag_data = {"x": event.x, "y": event.y}
        
        def do_move_main(event):
            if hasattr(self.control_window, '_drag_data'):
                deltax = event.x - self.control_window._drag_data["x"]
                deltay = event.y - self.control_window._drag_data["y"]
                x = self.control_window.winfo_x() + deltax
                y = self.control_window.winfo_y() + deltay
                self.control_window.geometry(f"+{x}+{y}")
        
        def stop_move_main(event):
            if hasattr(self.control_window, '_drag_data'):
                del self.control_window._drag_data
        
        # Привязываем перетаскивание к основному окну
        self.control_window.bind("<Button-1>", start_move_main)
        self.control_window.bind("<B1-Motion>", do_move_main)
        self.control_window.bind("<ButtonRelease-1>", stop_move_main)
        
        # Отключаем перетаскивание для ползунка - разрешаем стандартное поведение
        def allow_slider_default(e):
            return  # Ничего не делаем, позволяем ползунку работать
        
        self.manual_slider.bind("<Button-1>", allow_slider_default, add='+')
        self.manual_slider.bind("<B1-Motion>", allow_slider_default, add='+')
        
        # Настраиваем ГЛОБАЛЬНЫЙ перехват прокрутки мыши (работает ВЕЗДЕ на экране)
        if MOUSE_AVAILABLE:
            try:
                # Регистрируем глобальный обработчик всех событий мыши
                mouse.hook(self.on_mouse_event_global)
                print("✓ Глобальная прокрутка мыши настроена (работает в любой зоне экрана)")
            except Exception as e:
                print(f"⚠ Ошибка настройки глобальной прокрутки: {e}")
                # Fallback на обычную прокрутку только в окне
                self.control_window.bind_all("<MouseWheel>", self.on_mouse_wheel)
        else:
            # Fallback: прокрутка только в окне программы
            self.control_window.bind_all("<MouseWheel>", self.on_mouse_wheel)
    
    def on_mouse_event_global(self, event):
        """Глобальный обработчик событий мыши (перехватывает ВСЕ события)"""
        # Фильтруем только события прокрутки
        if isinstance(event, mouse.WheelEvent):
            # Проверяем, что наше окно активно
            try:
                if not self.window_visible:
                    return  # Окно в трее, не обрабатываем
                
                # Проверяем, что окно видимо
                if self.control_window.state() != 'normal':
                    return
            except:
                return
            
            # Работает только если автояркость выключена
            if not self.auto_brightness_enabled:
                # event.delta > 0 - прокрутка вверх, < 0 - вниз
                change = 5 if event.delta > 0 else -5
                new_value = max(1, min(100, self.manual_brightness + change))  # Минимум 1
                # Используем after для безопасного обновления GUI из другого потока
                self.control_window.after(0, lambda: self.manual_slider.set(new_value))
                self.control_window.after(0, lambda: self.on_manual_brightness_change(new_value))
    
    def on_mouse_wheel(self, event):
        """Обработка прокрутки колеса мыши (fallback для tkinter)"""
        # Проверяем, что наше окно на первом плане (активно)
        try:
            if not self.window_visible:
                return  # Окно в трее, не обрабатываем
            
            # Проверяем, что окно существует и видимо
            if self.control_window.state() != 'normal':
                return
        except:
            return
        
        # Работает только если автояркость выключена
        if not self.auto_brightness_enabled:
            # Изменяем яркость колесом мыши
            delta = 5 if event.delta > 0 else -5
            new_value = max(1, min(100, self.manual_brightness + delta))  # Минимум 1
            self.manual_slider.set(new_value)
            self.on_manual_brightness_change(new_value)
    
    def on_manual_brightness_change(self, value):
        """Изменение ручной яркости через ползунок"""
        self.manual_brightness = int(float(value))
        # Применяем ВСЕГДА, независимо от режима автояркости
        # Ручная регулировка имеет наивысший приоритет
        self.target_brightness = self.manual_brightness
        self.current_brightness = self.manual_brightness  # Сразу устанавливаем без плавности
        self.apply_brightness(self.manual_brightness)
        
        # Сохраняем значение
        self.save_auto_brightness_setting()
    
    def toggle_auto_brightness(self):
        """Переключение режима автоматической яркости"""
        self.auto_brightness_enabled = self.auto_brightness_var.get()
        self.update_slider_state()
        
        # Сохраняем настройку
        self.save_auto_brightness_setting()
        
        if self.auto_brightness_enabled:
            print("🤖 Автояркость включена")
        else:
            print("🎚️ Ручная регулировка яркости")
            # Устанавливаем текущее значение ползунка
            self.target_brightness = self.manual_brightness
            self.apply_brightness(self.manual_brightness)
    
    def update_slider_state(self):
        """Обновление состояния ползунка (активен/неактивен)"""
        if self.auto_brightness_enabled:
            self.manual_slider.config(state='disabled')
        else:
            self.manual_slider.config(state='normal')
    
    def save_auto_brightness_setting(self):
        """Сохранение настройки автояркости в config.ini"""
        config = configparser.ConfigParser()
        config_path = get_config_path()
        
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        
        if 'Brightness' not in config:
            config['Brightness'] = {}
        
        config['Brightness']['auto_enabled'] = str(self.auto_brightness_enabled)
        config['Brightness']['manual_brightness'] = str(self.manual_brightness)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
    
    def toggle_language(self):
        """Переключение языка интерфейса"""
        current_lang = get_language()
        new_lang = 'en' if current_lang == 'ru' else 'ru'
        set_language(new_lang)
        
        # Сохраняем в конфиг
        config = configparser.ConfigParser()
        config_path = get_config_path()
        
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        
        if 'Interface' not in config:
            config['Interface'] = {}
        
        config['Interface']['language'] = new_lang
        
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        
        # Обновляем кнопку языка (ИСПРАВЛЕНО: RU = русский, EN = английский)
        self.lang_button.config(text='RU' if new_lang == 'ru' else 'EN')
        
        # Обновляем тексты интерфейса
        self.update_interface_texts()
    
    def update_interface_texts(self):
        """Обновление текстов интерфейса после смены языка"""
        # Обновляем кнопку повторного поиска
        self.reconnect_button.config(text=f"🔍 {get_text('repeat_search')}")
        
        # Обновляем чекбокс автояркости
        if hasattr(self, 'auto_check'):
            self.auto_check.config(text=f"🤖 {get_text('mode_auto')}")
        
        # Обновляем надпись ручной регулировки
        if hasattr(self, 'manual_label'):
            self.manual_label.config(text=f"🎚️ {get_text('mode_manual')}:")
        
        # Обновляем кнопку настроек
        if hasattr(self, 'settings_btn'):
            self.settings_btn.config(text=f"⚙️ {get_text('settings')}")
        
        # Обновляем статус подключения
        if self.connected:
            self.connection_label.config(text=f"🟢 {get_text('connected')}")
        else:
            self.connection_label.config(text=f"⚫ {get_text('connecting')}")
        
        # Обновляем строку статуса
        self.status_label.config(
            text=f"ESP8266: {self.esp_ip} | {get_text('brightness')}: {self.min_brightness}-{self.max_brightness}%"
        )
    
    def open_settings_window(self):
        """Открыть окно настроек с калибровкой"""
        # Проверяем, не открыто ли уже окно настроек
        if self.settings_window and self.settings_window.winfo_exists():
            # Если окно уже открыто, просто поднимаем его наверх
            self.settings_window.lift()
            self.settings_window.focus_force()
            return
        
        settings = tk.Toplevel(self.control_window)
        settings.title(get_text('settings_title'))
        settings.resizable(False, False)
        settings.configure(bg='#2b2b2b')
        
        # Применяем тёмную тему для рамки окна настроек (Windows 10/11)
        try:
            import ctypes
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            settings.update()  # Убеждаемся что окно создано
            hwnd = ctypes.windll.user32.GetParent(settings.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(1)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            pass  # Если не получилось - не критично
        
        # НЕ используем topmost - вызывает мерцание яркости!
        
        # Сохраняем ссылку на окно
        self.settings_window = settings
        
        # При закрытии окна сбрасываем ссылку
        def on_close():
            self.settings_window = None
            settings.destroy()
        
        settings.protocol("WM_DELETE_WINDOW", on_close)
        
        # Опускаем основное окно на задний план
        self.control_window.lower()
        
        # Добавляем функционал перетаскивания окна за любую свободную область
        def start_move(event):
            settings._drag_data = {"x": event.x, "y": event.y}
        
        def do_move(event):
            if hasattr(settings, '_drag_data'):
                deltax = event.x - settings._drag_data["x"]
                deltay = event.y - settings._drag_data["y"]
                x = settings.winfo_x() + deltax
                y = settings.winfo_y() + deltay
                settings.geometry(f"+{x}+{y}")
        
        def stop_move(event):
            if hasattr(settings, '_drag_data'):
                del settings._drag_data
        
        # Привязываем перетаскивание к самому окну настроек
        settings.bind("<Button-1>", start_move)
        settings.bind("<B1-Motion>", do_move)
        settings.bind("<ButtonRelease-1>", stop_move)
        
        # Загружаем конфигурацию
        config = configparser.ConfigParser()
        config_path = get_config_path()
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        
        # === ВЫБОР РЕЖИМА ===
        mode_frame = tk.LabelFrame(settings, text=get_text('mode_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        mode_frame.pack(fill='x', padx=15, pady=(10, 5))
        
        mode_var = tk.StringVar(value=config.get('Mode', 'device', fallback='esp8266'))
        
        # Функция для обновления видимости блока ESP8266
        def update_esp_visibility():
            if mode_var.get() == 'esp8266':
                esp_frame.pack(fill='x', padx=15, pady=5, before=startup_frame)
            else:
                esp_frame.pack_forget()
        
        tk.Radiobutton(
            mode_frame,
            text=get_text('mode_esp8266'),
            variable=mode_var,
            value='esp8266',
            command=update_esp_visibility,
            bg='#2b2b2b',
            fg='white',
            selectcolor='#404040',
            activebackground='#2b2b2b',
            activeforeground='white',
            font=("Segoe UI", 9)
        ).pack(anchor='w', padx=10, pady=5)
        
        digispark_text = get_text('mode_digispark') if DIGISPARK_AVAILABLE else get_text('mode_digispark_unavailable')
        
        tk.Radiobutton(
            mode_frame,
            text=digispark_text,
            variable=mode_var,
            value='digispark',
            command=update_esp_visibility,
            state='normal' if DIGISPARK_AVAILABLE else 'disabled',
            bg='#2b2b2b',
            fg='white' if DIGISPARK_AVAILABLE else '#666666',
            selectcolor='#404040',
            activebackground='#2b2b2b',
            activeforeground='white',
            font=("Segoe UI", 9)
        ).pack(anchor='w', padx=10, pady=5)
        
        # === КАЛИБРОВКА ===
        calib_frame = tk.LabelFrame(settings, text=get_text('calibration_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        calib_frame.pack(fill='x', padx=15, pady=5)
        
        # Получаем текущие значения калибровки
        current_mode = mode_var.get()
        section_name = f'Calibration_{current_mode}'
        
        sensor_min = config.getint(section_name, 'sensor_min', fallback=0)
        sensor_max = config.getint(section_name, 'sensor_max', fallback=1023)
        
        # Поля для отображения текущих значений
        tk.Label(calib_frame, text=f"{get_text('current_calibration')} ({current_mode}):", bg='#2b2b2b', fg='#888888', font=("Segoe UI", 9)).pack(pady=5)
        
        calib_info = tk.Label(
            calib_frame,
            text=f"{get_text('minimum')}: {sensor_min}  |  {get_text('maximum')}: {sensor_max}",
            bg='#2b2b2b',
            fg='#00ff88',
            font=("Segoe UI", 10, "bold")
        )
        calib_info.pack(pady=5)
        
        # Кнопки калибровки
        btn_frame = tk.Frame(calib_frame, bg='#2b2b2b')
        btn_frame.pack(pady=10)
        
        def start_calibration_min():
            """Калибровка минимума (темно)"""
            result = messagebox.askokcancel(
                get_text('calib_min_title'),
                get_text('calib_min_message'),
                parent=settings
            )
            
            if not result:
                return
            
            # Читаем значения
            values = []
            device_mode = mode_var.get()
            
            for i in range(5):
                if device_mode == 'esp8266':
                    value = self.read_esp_sensor()
                else:  # digispark
                    value = self.read_digispark_sensor()
                
                if value is not None:
                    values.append(value)
                    calib_info.config(text=f"{get_text('measurement')} {i+1}/5: {value}")
                    settings.update_idletasks()  # Обновляем UI без задержки
                    settings.update()
                time.sleep(1)
            
            if values:
                min_val = min(values)
                
                # Сохраняем в config
                section = f'Calibration_{device_mode}'
                if section not in config:
                    config[section] = {}
                config[section]['sensor_min'] = str(min_val)
                
                # Сохраняем max если его нет
                if 'sensor_max' not in config[section]:
                    config[section]['sensor_max'] = str(1023)
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    config.write(f)
                
                calib_info.config(text=f"✓ {get_text('minimum')}: {min_val}  |  {get_text('maximum')}: {config.getint(section, 'sensor_max')}")
                messagebox.showinfo(get_text('success'), f"{get_text('calib_min_success')}: {min_val}", parent=settings)
            else:
                messagebox.showerror(get_text('error'), get_text('sensor_read_error'), parent=settings)
        
        def start_calibration_max():
            """Калибровка максимума (светло)"""
            result = messagebox.askokcancel(
                get_text('calib_max_title'),
                get_text('calib_max_message'),
                parent=settings
            )
            
            if not result:
                return
            
            # Читаем значения
            values = []
            device_mode = mode_var.get()
            
            for i in range(5):
                if device_mode == 'esp8266':
                    value = self.read_esp_sensor()
                else:  # digispark
                    value = self.read_digispark_sensor()
                
                if value is not None:
                    values.append(value)
                    calib_info.config(text=f"{get_text('measurement')} {i+1}/5: {value}")
                    settings.update_idletasks()
                time.sleep(1)
            
            if values:
                max_val = max(values)
                
                # Сохраняем в config
                section = f'Calibration_{device_mode}'
                if section not in config:
                    config[section] = {}
                config[section]['sensor_max'] = str(max_val)
                
                # Сохраняем min если его нет
                if 'sensor_min' not in config[section]:
                    config[section]['sensor_min'] = str(0)
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    config.write(f)
                
                calib_info.config(text=f"✓ {get_text('minimum')}: {config.getint(section, 'sensor_min')}  |  {get_text('maximum')}: {max_val}")
                messagebox.showinfo(get_text('success'), f"{get_text('calib_max_success')}: {max_val}", parent=settings)
            else:
                messagebox.showerror(get_text('error'), get_text('sensor_read_error'), parent=settings)
        
        tk.Button(
            btn_frame,
            text=f"📉 {get_text('calibrate_min')}",
            command=start_calibration_min,
            bg='#404040',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            font=("Segoe UI", 9)
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text=f"📈 {get_text('calibrate_max')}",
            command=start_calibration_max,
            bg='#404040',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            font=("Segoe UI", 9)
        ).pack(side='left', padx=5)
        
        # === НАСТРОЙКИ ЯРКОСТИ ЭКРАНА ===
        brightness_frame = tk.LabelFrame(settings, text=get_text('brightness_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        brightness_frame.pack(fill='x', padx=15, pady=5)
        
        # Минимальная яркость
        min_brightness_container = tk.Frame(brightness_frame, bg='#2b2b2b')
        min_brightness_container.pack(fill='x', padx=10, pady=(10, 5))
        
        tk.Label(min_brightness_container, text=get_text('min_brightness'), bg='#2b2b2b', fg='white', font=("Segoe UI", 9)).pack(side='left', padx=(0, 10))
        
        min_brightness_var = tk.IntVar(value=self.min_brightness)
        min_brightness_entry = tk.Entry(min_brightness_container, textvariable=min_brightness_var, font=("Segoe UI", 10), width=5, justify='center', bg='#404040', fg='white', insertbackground='white')
        min_brightness_entry.pack(side='left')
        
        tk.Label(min_brightness_container, text="%", bg='#2b2b2b', fg='#00ff88', font=("Segoe UI", 10, "bold")).pack(side='left', padx=(2, 0))
        
        tk.Label(min_brightness_container, text="(1-99)", bg='#2b2b2b', fg='#666666', font=("Segoe UI", 8)).pack(side='left', padx=(10, 0))
        
        # Максимальная яркость
        max_brightness_container = tk.Frame(brightness_frame, bg='#2b2b2b')
        max_brightness_container.pack(fill='x', padx=10, pady=(5, 10))
        
        tk.Label(max_brightness_container, text=get_text('max_brightness'), bg='#2b2b2b', fg='white', font=("Segoe UI", 9)).pack(side='left', padx=(0, 10))
        
        max_brightness_var = tk.IntVar(value=self.max_brightness)
        max_brightness_entry = tk.Entry(max_brightness_container, textvariable=max_brightness_var, font=("Segoe UI", 10), width=5, justify='center', bg='#404040', fg='white', insertbackground='white')
        max_brightness_entry.pack(side='left')
        
        tk.Label(max_brightness_container, text="%", bg='#2b2b2b', fg='#00ff88', font=("Segoe UI", 10, "bold")).pack(side='left', padx=(2, 0))
        
        tk.Label(max_brightness_container, text="(2-100)", bg='#2b2b2b', fg='#666666', font=("Segoe UI", 8)).pack(side='left', padx=(10, 0))
        
        # === НАСТРОЙКИ УСРЕДНЕНИЯ ===
        averaging_frame = tk.LabelFrame(settings, text=get_text('averaging_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        averaging_frame.pack(fill='x', padx=15, pady=5)
        
        # Информация об усреднении
        tk.Label(
            averaging_frame,
            text=get_text('averaging_info'),
            bg='#2b2b2b',
            fg='#888888',
            font=("Segoe UI", 8),
            wraplength=400,
            justify='left'
        ).pack(padx=10, pady=(5, 10))
        
        # Период усреднения
        averaging_container = tk.Frame(averaging_frame, bg='#2b2b2b')
        averaging_container.pack(fill='x', padx=10, pady=(5, 10))
        
        tk.Label(averaging_container, text=get_text('averaging_period'), bg='#2b2b2b', fg='white', font=("Segoe UI", 9)).pack(side='left', padx=(0, 10))
        
        averaging_period_var = tk.IntVar(value=self.averaging_period)
        averaging_period_entry = tk.Entry(averaging_container, textvariable=averaging_period_var, font=("Segoe UI", 10), width=5, justify='center', bg='#404040', fg='white', insertbackground='white')
        averaging_period_entry.pack(side='left')
        
        tk.Label(averaging_container, text=get_text('sec'), bg='#2b2b2b', fg='#00ff88', font=("Segoe UI", 10, "bold")).pack(side='left', padx=(2, 0))
        
        tk.Label(averaging_container, text="(1-120)", bg='#2b2b2b', fg='#666666', font=("Segoe UI", 8)).pack(side='left', padx=(10, 0))
        
        # === НАСТРОЙКИ ESP8266 (создаём раньше, чтобы можно было ссылаться) ===
        esp_frame = tk.LabelFrame(settings, text=get_text('esp_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        
        tk.Label(esp_frame, text=get_text('esp_ip'), bg='#2b2b2b', fg='white', font=("Segoe UI", 9)).pack(anchor='w', padx=10, pady=5)
        esp_ip_entry = tk.Entry(esp_frame, font=("Segoe UI", 10), width=30)
        esp_ip_entry.insert(0, config.get('Connection', 'esp_ip', fallback='192.168.1.146'))
        esp_ip_entry.pack(padx=10, pady=5)
        
        tk.Button(
            esp_frame,
            text=get_text('esp_open_web'),
            command=lambda: __import__('webbrowser').open(f"http://{esp_ip_entry.get()}"),
            bg='#404040',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            font=("Segoe UI", 9)
        ).pack(pady=5)
        
        # === ПАРАМЕТРЫ ЗАПУСКА ===
        startup_frame = tk.LabelFrame(settings, text=get_text('startup_title'), bg='#2b2b2b', fg='white', font=("Segoe UI", 10, "bold"))
        startup_frame.pack(fill='x', padx=15, pady=5)
        
        # Чекбокс автозагрузки
        autostart_var = tk.BooleanVar(value=self.check_autostart())
        tk.Checkbutton(
            startup_frame,
            text=get_text('autostart'),
            variable=autostart_var,
            bg='#2b2b2b',
            fg='#cccccc',
            selectcolor='#404040',
            activebackground='#2b2b2b',
            activeforeground='white',
            font=("Segoe UI", 9)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Чекбокс запуска в трее
        start_minimized_var = tk.BooleanVar(value=config.getboolean('Startup', 'start_minimized', fallback=False))
        tk.Checkbutton(
            startup_frame,
            text=get_text('start_minimized'),
            variable=start_minimized_var,
            bg='#2b2b2b',
            fg='#cccccc',
            selectcolor='#404040',
            activebackground='#2b2b2b',
            activeforeground='white',
            font=("Segoe UI", 9)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Применяем начальную видимость ESP блока
        update_esp_visibility()
        
        # === КНОПКИ УПРАВЛЕНИЯ ===
        control_frame = tk.Frame(settings, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        # Центрируем кнопки с помощью внутреннего фрейма
        buttons_container = tk.Frame(control_frame, bg='#2b2b2b')
        buttons_container.pack(expand=True)
        
        def save_settings():
            """Сохранить все настройки"""
            # Валидируем яркость перед сохранением
            validate_brightness()
            
            # Сохраняем режим
            if 'Mode' not in config:
                config['Mode'] = {}
            config['Mode']['device'] = mode_var.get()
            
            # Сохраняем IP ESP8266
            if 'Connection' not in config:
                config['Connection'] = {}
            config['Connection']['esp_ip'] = esp_ip_entry.get()
            
            # Сохраняем настройки яркости экрана
            if 'Brightness' not in config:
                config['Brightness'] = {}
            config['Brightness']['min_brightness'] = str(min_brightness_var.get())
            config['Brightness']['max_brightness'] = str(max_brightness_var.get())
            
            # Сохраняем настройки усреднения
            if 'Averaging' not in config:
                config['Averaging'] = {}
            config['Averaging']['averaging_period'] = str(averaging_period_var.get())
            
            # Обновляем значения в памяти
            self.min_brightness = min_brightness_var.get()
            self.max_brightness = max_brightness_var.get()
            self.averaging_period = averaging_period_var.get()
            self.max_history_size = self.averaging_period  # Обновляем размер истории
            
            # Сохраняем параметры запуска
            if 'Startup' not in config:
                config['Startup'] = {}
            config['Startup']['start_minimized'] = str(start_minimized_var.get())
            
            with open(config_path, 'w', encoding='utf-8') as f:
                config.write(f)
            
            # Применяем автозагрузку
            self.apply_autostart(autostart_var.get())
            
            messagebox.showinfo(get_text('success'), get_text('settings_saved'), parent=settings)
            
            # Сбрасываем ссылку и закрываем окно
            self.settings_window = None
            settings.destroy()
        
        # Кнопка "Сохранить" - основной цвет иконки
        tk.Button(
            buttons_container,
            text=get_text('save_close'),
            command=save_settings,
            bg='#00ff88',  # Основной цвет иконки
            fg='#2b2b2b',  # Тёмный текст для контраста
            relief='flat',
            padx=40,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            cursor='hand2'
        ).pack(side='left', padx=8)
        
        # Кнопка "Отмена" - яркий голубой
        tk.Button(
            buttons_container,
            text=get_text('cancel'),
            command=settings.destroy,
            bg='#00ddff',  # Яркий голубой
            fg='#2b2b2b',  # Тёмный текст для контраста
            relief='flat',
            padx=40,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            cursor='hand2'
        ).pack(side='left', padx=8)
        
        # Валидация полей ввода яркости
        def validate_brightness():
            """Проверяет корректность введенных значений яркости"""
            try:
                min_val = min_brightness_var.get()
                max_val = max_brightness_var.get()
                
                # Ограничиваем диапазоны
                if min_val < 1:
                    min_brightness_var.set(1)
                elif min_val > 99:
                    min_brightness_var.set(99)
                
                if max_val < 2:
                    max_brightness_var.set(2)
                elif max_val > 100:
                    max_brightness_var.set(100)
                
                # Проверяем, чтобы минимум был меньше максимума
                min_val = min_brightness_var.get()
                max_val = max_brightness_var.get()
                
                if min_val >= max_val:
                    min_brightness_var.set(max_val - 1)
            except:
                # Если некорректное значение - восстанавливаем предыдущие
                min_brightness_var.set(self.min_brightness)
                max_brightness_var.set(self.max_brightness)
        
        min_brightness_entry.bind("<FocusOut>", lambda e: validate_brightness())
        max_brightness_entry.bind("<FocusOut>", lambda e: validate_brightness())
        
        # Привязываем обработчики перетаскивания ко всем Frame/LabelFrame
        # Это позволяет тянуть окно за любую свободную область
        for widget in [mode_frame, calib_frame, brightness_frame, esp_frame, startup_frame, control_frame, buttons_container]:
            widget.bind("<Button-1>", start_move)
            widget.bind("<B1-Motion>", do_move)
            widget.bind("<ButtonRelease-1>", stop_move)
        
        # Автоматически подстраиваем размер окна под содержимое
        settings.update_idletasks()
        width = 500
        height = settings.winfo_reqheight() + 20  # Добавляем небольшой отступ
        
        # Позиционируем окно в правом нижнем углу (+100px вверх от края)
        screen_width = settings.winfo_screenwidth()
        screen_height = settings.winfo_screenheight()
        x = screen_width - width - 10
        y = screen_height - height - 100  # 100px отступ снизу
        
        settings.geometry(f"{width}x{height}+{x}+{y}")
    
    def check_sensor_availability(self):
        """Проверка наличия датчика при первом запуске"""
        # Проверяем текущий режим устройства из конфига
        config = configparser.ConfigParser()
        config_path = get_config_path()
        
        selected_mode = 'esp8266'  # По умолчанию ESP8266
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
            selected_mode = config.get('Mode', 'device', fallback='esp8266')
        
        if selected_mode == 'esp8266':
            # Проверяем ESP8266
            try:
                response = requests.get(f"http://{self.esp_ip}/sensor", timeout=2)
                if response.status_code == 200:
                    return True
            except:
                pass
            return False
        else:
            # Проверяем Digispark
            if not DIGISPARK_AVAILABLE:
                return False
            
            try:
                devices = list(usb.core.find(find_all=True, idVendor=USB_VENDOR_ID, idProduct=USB_PRODUCT_ID))
                for d in devices:
                    try:
                        manufacturer = usb.util.get_string(d, d.iManufacturer) if d.iManufacturer else ""
                        product = usb.util.get_string(d, d.iProduct) if d.iProduct else ""
                        if manufacturer == MANUFACTURER_STRING and product == PRODUCT_STRING:
                            return True
                    except:
                        continue
            except:
                pass
            return False
    
    def read_esp_sensor(self):
        """Прочитать значение с ESP8266"""
        try:
            response = requests.get(f"http://{self.esp_ip}/sensor", timeout=2)
            if response.status_code == 200:
                return int(response.text)
        except:
            pass
        return None
    
    def read_digispark_sensor(self):
        """Прочитать значение с Digispark (с кэшированием устройства)"""
        if not DIGISPARK_AVAILABLE:
            return None
        
        try:
            # Проверяем кэшированное устройство (если есть)
            if self.digispark_device is not None:
                try:
                    # Пытаемся прочитать с кэшированного устройства
                    result = self.digispark_device.ctrl_transfer(
                        bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_IN,
                        bRequest=CUSTOM_RQ_GET,
                        wValue=0,
                        wIndex=0,
                        data_or_wLength=2
                    )
                    value = int.from_bytes(result, byteorder='little')
                    return value
                except:
                    # Устройство больше не доступно, сбрасываем кэш
                    self.digispark_device = None
            
            # Ищем устройство только раз в 5 секунд (чтобы не тормозить)
            current_time = time.time()
            if current_time - self.digispark_last_check < 5:
                return None  # Слишком рано для повторного поиска
            
            self.digispark_last_check = current_time
            
            # Поиск устройства (медленная операция)
            devices = list(usb.core.find(find_all=True, idVendor=USB_VENDOR_ID, idProduct=USB_PRODUCT_ID))
            dev = None
            
            for d in devices:
                try:
                    manufacturer = usb.util.get_string(d, d.iManufacturer) if d.iManufacturer else ""
                    product = usb.util.get_string(d, d.iProduct) if d.iProduct else ""
                    
                    if manufacturer == MANUFACTURER_STRING and product == PRODUCT_STRING:
                        dev = d
                        break
                except:
                    continue
            
            if not dev:
                return None
            
            # Сохраняем найденное устройство в кэш
            self.digispark_device = dev
            
            # Читаем значение
            result = dev.ctrl_transfer(
                bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_IN,
                bRequest=CUSTOM_RQ_GET,
                wValue=0,
                wIndex=0,
                data_or_wLength=2
            )
            
            value = int.from_bytes(result, byteorder='little')
            return value
        except Exception as e:
            print(f"Ошибка чтения Digispark: {e}")
            self.digispark_device = None  # Сбрасываем кэш при ошибке
            return None
    
    def check_autostart(self):
        """Проверяет, включена ли автозагрузка"""
        import winreg
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, "OLED_AutoBrightness")
                winreg.CloseKey(key)
                return True
            except WindowsError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def apply_autostart(self, enable):
        """Применить настройки автозагрузки с Windows"""
        import winreg
        import sys
        
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "OLED_AutoBrightness"
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_READ
            )
            
            if enable:
                # Включаем автозагрузку
                if getattr(sys, 'frozen', False):
                    # Если запущен из .exe
                    exe_path = sys.executable
                else:
                    # Если запущен из Python скрипта
                    script_path = os.path.abspath(__file__)
                    bat_path = os.path.join(os.path.dirname(script_path), 'Start_OLED_Brightness.bat')
                    
                    if os.path.exists(bat_path):
                        # Используем батник для запуска (он добавляет libusb в PATH)
                        exe_path = f'"{bat_path}"'
                    else:
                        venv_python = os.path.join(os.path.dirname(script_path), '.venv', 'Scripts', 'pythonw.exe')
                        if os.path.exists(venv_python):
                            exe_path = f'"{venv_python}" "{script_path}"'
                        else:
                            exe_path = f'pythonw.exe "{script_path}"'
                
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
                print(f"✓ Автозагрузка включена: {exe_path}")
            else:
                # Выключаем автозагрузку
                try:
                    winreg.DeleteValue(key, app_name)
                    print("✓ Автозагрузка выключена")
                except WindowsError:
                    pass
            
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"Ошибка изменения автозагрузки: {e}")
    
    def connect_to_esp(self):
        """Подключение к датчикам (ESP8266 или Digispark)"""
        # ОПТИМИЗАЦИЯ: Если уже подключены - не проверяем, просто планируем следующую проверку
        if self.connected:
            # Датчик уже работает, повторная проверка не нужна
            # Проверим снова только через минуту (или если соединение потеряется)
            self.control_window.after(60000, self.connect_to_esp)
            return
        
        # Ищем устройства только если НЕ подключены
        # Загружаем текущий режим из конфига
        config = configparser.ConfigParser()
        config_path = get_config_path()
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
        
        selected_mode = config.get('Mode', 'device', fallback='esp8266')
        
        esp_online = False
        digispark_online = False
        
        # Проверяем ESP8266
        try:
            response = requests.get(f"http://{self.esp_ip}/api/brightness", timeout=2)
            if response.status_code == 200:
                esp_online = True
        except:
            pass
        
        # Проверяем Digispark
        if DIGISPARK_AVAILABLE:
            print("🔍 Начинаю поиск Digispark...")
            # Сначала пробуем использовать кэшированное устройство
            if self.digispark_device is not None:
                print("  Проверяю кэшированное устройство...")
                try:
                    # Быстрая проверка: пытаемся прочитать
                    result = self.digispark_device.ctrl_transfer(
                        bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_IN,
                        bRequest=CUSTOM_RQ_GET,
                        wValue=0,
                        wIndex=0,
                        data_or_wLength=2
                    )
                    digispark_online = True
                    print("  ✓ Кэшированное устройство работает!")
                except Exception as e:
                    # Устройство больше недоступно
                    print(f"  ✗ Кэш не работает: {e}")
                    self.digispark_device = None
            
            # Если нет кэша или он не сработал, делаем полный поиск
            if not digispark_online:
                print("  Запускаю полный USB-поиск...")
                try:
                    devices = list(usb.core.find(find_all=True, idVendor=USB_VENDOR_ID, idProduct=USB_PRODUCT_ID))
                    print(f"  Найдено устройств с VID:PID {hex(USB_VENDOR_ID)}:{hex(USB_PRODUCT_ID)}: {len(devices)}")
                    for i, d in enumerate(devices):
                        try:
                            manufacturer = usb.util.get_string(d, d.iManufacturer) if d.iManufacturer else ""
                            product = usb.util.get_string(d, d.iProduct) if d.iProduct else ""
                            print(f"    Устройство {i+1}: Manufacturer='{manufacturer}', Product='{product}'")
                            
                            if manufacturer == MANUFACTURER_STRING and product == PRODUCT_STRING:
                                self.digispark_device = d  # Кэшируем найденное устройство
                                digispark_online = True
                                print(f"    ✓ Найден Digispark!")
                                break
                        except Exception as e:
                            print(f"    ✗ Ошибка чтения устройства {i+1}: {e}")
                            continue
                    if not digispark_online:
                        print("  ✗ Digispark не найден среди устройств")
                except Exception as e:
                    print(f"  ✗ Ошибка USB-поиска: {e}")
                    pass
        else:
            print("⚠ PyUSB недоступен, поиск Digispark пропущен")
        
        # Автоматически переключаем режим на найденное устройство
        if esp_online and selected_mode != 'esp8266':
            print(f"✓ ESP8266 найден, автоматически переключаюсь на него (было: {selected_mode})")
            selected_mode = 'esp8266'
            # Сохраняем в config
            config_path = get_config_path()
            config = configparser.ConfigParser()
            if os.path.exists(config_path):
                config.read(config_path, encoding='utf-8')
            if 'Mode' not in config:
                config['Mode'] = {}
            config['Mode']['device'] = 'esp8266'
            with open(config_path, 'w', encoding='utf-8') as f:
                config.write(f)
        
        if digispark_online and selected_mode != 'digispark':
            print(f"✓ Digispark найден, автоматически переключаюсь на него (было: {selected_mode})")
            selected_mode = 'digispark'
            # Сохраняем в config
            config_path = get_config_path()
            config = configparser.ConfigParser()
            if os.path.exists(config_path):
                config.read(config_path, encoding='utf-8')
            if 'Mode' not in config:
                config['Mode'] = {}
            config['Mode']['device'] = 'digispark'
            with open(config_path, 'w', encoding='utf-8') as f:
                config.write(f)
        
        # Определяем статус подключения (теперь всегда будет соответствие)
        if selected_mode == 'esp8266' and esp_online:
            self.connected = True
            self.connection_label.config(
                text=f"� Датчик (ESP8266) онлайн",
                fg='#00ff88'
            )
        elif selected_mode == 'digispark' and digispark_online:
            self.connected = True
            self.connection_label.config(
                text=f"� Датчик (Digispark) онлайн",
                fg='#00ff88'
            )
        else:
            # Ничего не найдено
            self.connected = False
            self.connection_label.config(
                text=f"🔴 Датчик не обнаружен",
                fg='#ff4444'
            )
            # Показываем кнопку повторного поиска
            self.reconnect_button.pack(pady=5)
            
            # Автоматически переходим в режим ручной регулировки
            if self.auto_brightness_enabled:
                self.auto_brightness_enabled = False
                self.auto_brightness_var.set(False)
                self.update_slider_state()
                print("⚠ Датчик не найден - автоматически переключено на ручную регулировку")
        
        # Если подключились - периодически проверяем соединение (раз в минуту)
        if self.connected:
            # Скрываем кнопку повторного поиска
            self.reconnect_button.pack_forget()
            print("✓ Датчик подключен - можно включить автоматическую регулировку")
            # Следующая проверка через минуту
            self.control_window.after(60000, self.connect_to_esp)
    
    def manual_reconnect(self):
        """Ручной повторный поиск датчика (вызывается кнопкой)"""
        # Обновляем статус
        self.connection_label.config(
            text="⚫ Поиск датчика...",
            fg='#ffaa00'
        )
        # Скрываем кнопку на время поиска
        self.reconnect_button.pack_forget()
        # Запускаем поиск через 100мс
        self.control_window.after(100, self.connect_to_esp)
    
    def smooth_brightness_loop(self):
        """Цикл плавного изменения яркости"""
        while self.running:
            # Плавно приближаем текущую яркость к целевой
            if abs(self.current_brightness - self.target_brightness) > 0.5:
                if self.current_brightness < self.target_brightness:
                    self.current_brightness += self.smooth_step
                    if self.current_brightness > self.target_brightness:
                        self.current_brightness = self.target_brightness
                else:
                    self.current_brightness -= self.smooth_step
                    if self.current_brightness < self.target_brightness:
                        self.current_brightness = self.target_brightness
                
                # Применяем яркость
                self.control_window.after(0, self.apply_brightness, int(self.current_brightness))
            
            time.sleep(0.1)  # Обновление 10 раз в секунду для плавности
    
    def overlay_update_loop(self):
        """Цикл обновления overlay - держит его поверх всех окон"""
        while self.running:
            if self.overlay:
                try:
                    # Поднимаем overlay каждые 50мс чтобы он был поверх контекстных меню мгновенно
                    self.overlay.lift()
                    self.overlay.attributes('-topmost', True)
                except:
                    pass
            time.sleep(0.05)  # 50 миллисекунд = почти мгновенное обновление
    
    def auto_brightness_loop(self):
        """Цикл получения данных от датчика и расчёт яркости"""
        # Загружаем режим
        config = configparser.ConfigParser()
        config_path = get_config_path()
        
        while self.running:
            if self.connected:
                try:
                    # Перечитываем режим на каждой итерации (может измениться в настройках)
                    if os.path.exists(config_path):
                        config.read(config_path, encoding='utf-8')
                    
                    selected_mode = config.get('Mode', 'device', fallback='esp8266')
                    
                    # === ЧТЕНИЕ ДАННЫХ В ЗАВИСИМОСТИ ОТ РЕЖИМА ===
                    if selected_mode == 'esp8266':
                        # ESP8266 режим
                        response = requests.get(f"http://{self.esp_ip}/api/brightness", timeout=5)
                        data = response.json()
                        
                        # ESP отдаёт сырые данные и калибровку
                        light_level = data['light_level']
                        min_light = data['min_light']
                        max_light = data['max_light']
                        
                        # Сохраняем калибровочные значения в config.ini (если изменились)
                        self.save_calibration_if_changed(min_light, max_light)
                        
                    else:  # digispark
                        # Digispark режим
                        light_level = self.read_digispark_sensor()
                        
                        if light_level is None:
                            raise Exception("Не удалось прочитать Digispark")
                        
                        # Загружаем калибровку из config
                        section = f'Calibration_{selected_mode}'
                        min_light = config.getint(section, 'sensor_min', fallback=0)
                        max_light = config.getint(section, 'sensor_max', fallback=1023)
                    
                    # ВАЖНО: Сначала ограничиваем значение датчика диапазоном калибровки
                    light_level_constrained = max(min_light, min(max_light, light_level))
                    
                    # Рассчитываем яркость на стороне Python
                    # map(value, fromLow, fromHigh, toLow, toHigh)
                    if max_light > min_light:
                        brightness = (light_level_constrained - min_light) * (self.max_brightness - self.min_brightness) / (max_light - min_light) + self.min_brightness
                    else:
                        brightness = self.min_brightness
                    
                    # Ограничиваем диапазон яркости
                    brightness = max(self.min_brightness, min(self.max_brightness, brightness))
                    brightness = int(brightness)
                    
                    # Добавляем значение в историю для усреднения
                    self.brightness_history.append(brightness)
                    
                    # Ограничиваем размер истории
                    if len(self.brightness_history) > self.max_history_size:
                        self.brightness_history.pop(0)
                    
                    # Пересчитываем среднюю яркость по периоду из конфига
                    current_time = time.time()
                    if current_time - self.last_average_time >= self.averaging_period:
                        # Вычисляем среднее значение (только если автояркость включена)
                        if self.brightness_history and self.auto_brightness_enabled:
                            avg_brightness = sum(self.brightness_history) / len(self.brightness_history)
                            self.target_brightness = int(avg_brightness)
                            self.last_average_time = current_time
                            
                            print(f"Усреднённая яркость за {self.averaging_period} сек: {self.target_brightness}% (из {len(self.brightness_history)} значений)")
                    else:
                        # До первого усреднения - используем текущее значение (если автояркость включена)
                        if len(self.brightness_history) <= 3 and self.auto_brightness_enabled:
                            # В первые 3 секунды сразу применяем значение
                            self.target_brightness = brightness
                            print(f"Начальная установка яркости: {brightness}% (датчик: {light_level})")
                    
                    # Обновляем интерфейс
                    self.control_window.after(0, self.update_interface, brightness, light_level)
                    
                except requests.exceptions.Timeout:
                    # Тайм-аут - просто пропускаем этот цикл (только для ESP)
                    if 'selected_mode' in locals() and selected_mode == 'esp8266':
                        print("Тайм-аут запроса к ESP8266, повторная попытка...")
                    time.sleep(2)
                    
                except requests.exceptions.ConnectionError:
                    # Потеря связи (только для ESP)
                    if 'selected_mode' in locals() and selected_mode == 'esp8266':
                        self.connected = False
                        self.digispark_device = None  # Сбрасываем кэш устройства
                        self.control_window.after(0, lambda: self.connection_label.config(
                            text="🔄 Переподключение к ESP8266...",
                            fg='#ffaa00'
                        ))
                        time.sleep(3)
                        # Попытка переподключения
                        self.control_window.after(0, self.connect_to_esp)
                    
                except Exception as e:
                    print(f"Ошибка получения данных: {e}")
                    # Сбрасываем соединение и устройство при любой ошибке
                    self.connected = False
                    self.digispark_device = None
                    self.control_window.after(0, lambda: self.connection_label.config(
                        text="🔄 Переподключение...",
                        fg='#ffaa00'
                    ))
                    self.control_window.after(0, self.connect_to_esp)
                    time.sleep(2)
            
            time.sleep(1)  # Получение данных каждую секунду
    
    def update_interface(self, brightness, light_level):
        """Обновление интерфейса (без изменения яркости экрана)"""
        # Показываем текущее значение с датчика (не усреднённое)
        self.brightness_label.config(text=f"{int(self.target_brightness)}%")
        self.progress['value'] = int(self.target_brightness)
        self.info_label.config(text=f"💡 {get_text('sensor')}: {light_level} | {get_text('target')}: {int(self.target_brightness)}% | {get_text('current_status')}: {int(self.current_brightness)}%")
    
    def update_brightness(self, brightness, light_level):
        """УСТАРЕВШАЯ: Обновление яркости и интерфейса"""
        # Эта функция больше не используется
        pass
    
    def apply_brightness(self, brightness_value):
        """Применение яркости через оверлей"""
        # Вычисляем затемнение
        darkness = 1.0 - (brightness_value / 100.0)
        
        if darkness > 0.01:
            if not self.overlay:
                self.create_overlay()
            
            self.overlay.attributes('-alpha', darkness)

            self.overlay.lift()
        else:
            if self.overlay:
                self.overlay.destroy()
                self.overlay = None
    
    def create_overlay(self):
        """Создание кликопрозрачного оверлея"""
        if self.overlay:
            self.overlay.destroy()
        
        self.overlay = tk.Toplevel()
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-alpha', 0.0)
        self.overlay.configure(bg='black')
        self.overlay.overrideredirect(True)
        self.overlay.update_idletasks()
        
        try:
            import win32gui
            hwnd = int(self.overlay.frame(), 16)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_ex_style = ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_ex_style)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                   new_ex_style | win32con.WS_EX_TOOLWINDOW)
        except Exception as e:
            print(f"Ошибка настройки оверлея: {e}")
    
    def create_tray_icon_image(self):
        """Создание иконки для трея"""
        # Пытаемся загрузить icon.ico, если не получается - создаём простую иконку
        if os.path.exists(self.icon_path):
            try:
                # Загружаем иконку из .ico файла
                image = Image.open(self.icon_path)
                # Берём максимальный размер из .ico
                if hasattr(image, 'size'):
                    return image
            except:
                pass
        
        # Если не получилось загрузить - создаём простую иконку
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='black')
        dc = ImageDraw.Draw(image)
        
        # Рисуем солнышко
        dc.ellipse([16, 16, 48, 48], fill='#00ff88', outline='#00ff88')
        
        return image
    
    def show_window(self, icon=None, item=None):
        """Показать окно из трея"""
        # Позиционируем окно в правом нижнем углу (+100px вверх от края)
        screen_width = self.control_window.winfo_screenwidth()
        screen_height = self.control_window.winfo_screenheight()
        window_width = 450
        window_height = 500
        x = screen_width - window_width - 10
        y = screen_height - window_height - 100  # 100px отступ снизу (учитывает панель задач)
        self.control_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Показываем окно
        self.control_window.deiconify()
        self.control_window.lift()
        self.control_window.focus_force()  # Принудительно даём фокус
        self.control_window.attributes('-topmost', True)  # Временно поверх всех
        self.control_window.after(100, lambda: self.control_window.attributes('-topmost', False))  # Через 100мс убираем topmost
        self.window_visible = True
    
    def show_window_hotkey(self):
        """Показать окно по горячей клавише (Ctrl+Shift+B)"""
        # Всегда пытаемся показать окно, независимо от состояния
        try:
            self.show_window(None, None)
        except Exception as e:
            print(f"⚠ Ошибка показа окна по горячей клавише: {e}")
    
    def on_focus_out(self, event):
        """Обработка потери фокуса окна - сворачиваем в трей"""
        # Проверяем, что событие именно от главного окна, а не от виджетов внутри
        if event.widget == self.control_window:
            # Небольшая задержка, чтобы не сворачивать при клике по элементам окна
            self.control_window.after(100, self.check_and_hide)
    
    def check_and_hide(self):
        """Проверяем и сворачиваем окно, если фокус действительно потерян"""
        # Проверяем, что фокус не в нашем окне
        try:
            focused = self.control_window.focus_get()
            if focused is None or focused.winfo_toplevel() != self.control_window:
                # Также проверяем, что окно настроек не открыто
                if not (self.settings_window and self.settings_window.winfo_exists()):
                    self.hide_window()
        except:
            pass  # Игнорируем ошибки (окно может быть уже закрыто)
    
    def hide_window(self):
        """Скрыть окно в трей"""
        self.control_window.withdraw()
        self.window_visible = False
        
        if self.tray_icon is None:
            # Создаём иконку трея
            icon_image = self.create_tray_icon_image()
            menu = pystray.Menu(
                pystray.MenuItem(get_text('tray_show'), self.show_window, default=True),
                pystray.MenuItem(get_text('tray_settings'), self.open_settings_window),
                pystray.MenuItem(get_text('tray_restart'), self.restart_app),
                pystray.MenuItem(get_text('tray_exit'), self.quit_app)
            )
            self.tray_icon = pystray.Icon("OLED Brightness", icon_image, "OLED Auto Brightness", menu)
            
            # Запускаем иконку трея в отдельном потоке
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def quit_app(self, icon=None, item=None):
        """Полное закрытие приложения"""
        self.running = False
        
        # Останавливаем иконку трея
        if self.tray_icon:
            self.tray_icon.stop()
        
        # Закрываем окна
        if self.overlay:
            try:
                self.overlay.destroy()
            except:
                pass
        
        try:
            self.control_window.destroy()
        except:
            pass
    
    def restart_app(self, icon=None, item=None):
        """Перезапуск приложения"""
        print("🔄 Перезапуск приложения...")
        
        # Останавливаем текущий процесс
        self.running = False
        
        # Останавливаем иконку трея
        if self.tray_icon:
            self.tray_icon.stop()
        
        # Закрываем окна
        if self.overlay:
            try:
                self.overlay.destroy()
            except:
                pass
        
        try:
            self.control_window.quit()
        except:
            pass
        
        # Принудительная очистка временных файлов перед перезапуском
        cleanup_pyinstaller_temp()
        
        # Небольшая задержка для завершения очистки
        time.sleep(0.5)
        
        # Запускаем новый процесс
        import subprocess
        python = sys.executable
        script = os.path.abspath(__file__)
        
        # Запускаем новый экземпляр с задержкой через батник
        if sys.platform == 'win32':
            if getattr(sys, 'frozen', False):
                # Для скомпилированной программы - добавляем задержку через cmd
                batch_command = f'timeout /t 1 /nobreak >nul & start "" "{python}"'
                subprocess.Popen(batch_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Для скрипта
                subprocess.Popen([python, script], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([python, script])
        
        # Завершаем текущий процесс
        sys.exit(0)
    
    def run(self):
        """Запуск приложения"""
        self.control_window.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.control_window.mainloop()
    
    def on_close(self):
        """Обработка закрытия (устарело, используется hide_window)"""
        self.hide_window()


def main():
    app = SimpleBrightnessControl()
    app.run()


if __name__ == "__main__":
    main()

