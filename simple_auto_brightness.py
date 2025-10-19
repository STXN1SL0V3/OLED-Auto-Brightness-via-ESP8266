"""
Простое управление яркостью OLED от ESP8266
Автоматически подключается к http://192.168.1.146 и регулирует яркость
"""

import tkinter as tk
from tkinter import ttk
import win32con
import requests
import threading
import time
import pystray
from PIL import Image, ImageDraw
import configparser
import os


class SimpleBrightnessControl:
    def __init__(self):
        # Загрузка конфигурации
        self.load_config()
        
        # Главное окно
        self.control_window = tk.Tk()
        self.control_window.title("🔆 OLED Auto Brightness")
        self.control_window.geometry("450x350")
        self.control_window.resizable(False, False)
        self.control_window.configure(bg='#2b2b2b')
        self.control_window.attributes('-topmost', True)
        
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
        
        # Системный трей
        self.tray_icon = None
        self.window_visible = True
        self.icon_path = icon_path  # Сохраняем путь для трея
        
        # Усреднение значений
        self.brightness_history = []  # История значений яркости
        self.last_average_time = time.time()
        
        self.create_interface()
        
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
    
    def load_config(self):
        """Загрузка настроек из config.ini"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        
        # Значения по умолчанию
        self.min_brightness = 20
        self.max_brightness = 100
        self.averaging_period = 60
        self.esp_ip = "192.168.1.146"
        self.timeout = 5
        self.smooth_step = 2
        
        if os.path.exists(config_path):
            try:
                config.read(config_path, encoding='utf-8')
                
                # Загрузка настроек яркости
                if 'Brightness' in config:
                    self.min_brightness = config.getint('Brightness', 'min_brightness', fallback=20)
                    self.max_brightness = config.getint('Brightness', 'max_brightness', fallback=100)
                
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
                
                self.max_history_size = self.averaging_period
                
                print(f"✓ Конфигурация загружена:")
                print(f"  Яркость: {self.min_brightness}% - {self.max_brightness}%")
                print(f"  Усреднение: {self.averaging_period} сек")
                print(f"  ESP IP: {self.esp_ip}")
                
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
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
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
        
        # Заголовок
        tk.Label(
            self.control_window,
            text="🔆 Auto OLED Brightness",
            font=("Segoe UI", 18, "bold"),
            bg='#2b2b2b',
            fg='white'
        ).pack(pady=20)
        
        # Статус подключения
        self.connection_label = tk.Label(
            self.control_window,
            text="⚫ Подключение...",
            font=("Segoe UI", 10),
            bg='#2b2b2b',
            fg='#ffaa00'
        )
        self.connection_label.pack(pady=5)
        
        # Текущая яркость
        self.brightness_label = tk.Label(
            self.control_window,
            text="100%",
            font=("Segoe UI", 36, "bold"),
            bg='#2b2b2b',
            fg='#00ff88'
        )
        self.brightness_label.pack(pady=15)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(
            self.control_window,
            length=400,
            mode='determinate',
            maximum=100
        )
        self.progress['value'] = 100
        self.progress.pack(pady=10)
        
        # Информация
        self.info_label = tk.Label(
            self.control_window,
            text=f"Датчик: --- | Усреднение за {self.averaging_period} сек",
            font=("Segoe UI", 8),
            bg='#2b2b2b',
            fg='#888888'
        )
        self.info_label.pack(pady=5)
        
        # Статус
        self.status_label = tk.Label(
            self.control_window,
            text=f"ESP8266: {self.esp_ip} | Яркость: {self.min_brightness}-{self.max_brightness}%",
            font=("Segoe UI", 8),
            bg='#2b2b2b',
            fg='#666666'
        )
        self.status_label.pack(pady=5)
        
        # Кнопка калибровки
        calibrate_btn = tk.Button(
            self.control_window,
            text="🛠️ Открыть калибровку ESP8266",
            command=self.open_calibration,
            bg='#404040',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            font=("Segoe UI", 9)
        )
        calibrate_btn.pack(pady=5)
        
        # Подпись автора в правом нижнем углу
        author_label = tk.Label(
            self.control_window,
            text="STXN1SL0V3",
            font=("Segoe UI", 7),
            bg='#2b2b2b',
            fg='#444444'
        )
        author_label.place(relx=1.0, rely=1.0, anchor='se', x=-5, y=-5)
    
    def open_calibration(self):
        """Открыть веб-интерфейс калибровки в браузере"""
        import webbrowser
        webbrowser.open(f"http://{self.esp_ip}")
    
    def connect_to_esp(self):
        """Подключение к ESP8266"""
        try:
            response = requests.get(f"http://{self.esp_ip}/api/brightness", timeout=5)
            if response.status_code == 200:
                self.connected = True
                self.connection_label.config(
                    text=f"🟢 Подключено к ESP8266",
                    fg='#00ff88'
                )
            else:
                raise Exception("Неверный ответ")
        except Exception as e:
            self.connected = False
            self.connection_label.config(
                text=f"🔴 Нет связи с ESP8266",
                fg='#ff4444'
            )
            # Повторная попытка через 10 секунд (увеличено для стабильности)
            self.control_window.after(10000, self.connect_to_esp)
    
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
        """Цикл получения данных от ESP8266 и расчёт яркости"""
        while self.running:
            if self.connected:
                try:
                    response = requests.get(f"http://{self.esp_ip}/api/brightness", timeout=5)
                    data = response.json()
                    
                    # ESP отдаёт сырые данные и калибровку
                    light_level = data['light_level']
                    min_light = data['min_light']
                    max_light = data['max_light']
                    
                    # Сохраняем калибровочные значения в config.ini (если изменились)
                    self.save_calibration_if_changed(min_light, max_light)
                    
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
                        # Вычисляем среднее значение
                        if self.brightness_history:
                            avg_brightness = sum(self.brightness_history) / len(self.brightness_history)
                            self.target_brightness = int(avg_brightness)
                            self.last_average_time = current_time
                            
                            print(f"Усреднённая яркость за {self.averaging_period} сек: {self.target_brightness}% (из {len(self.brightness_history)} значений)")
                    else:
                        # До первого усреднения - используем текущее значение
                        if len(self.brightness_history) <= 3:
                            # В первые 3 секунды сразу применяем значение
                            self.target_brightness = brightness
                            print(f"Начальная установка яркости: {brightness}% (датчик: {light_level})")
                    
                    # Обновляем интерфейс
                    self.control_window.after(0, self.update_interface, brightness, light_level)
                    
                except requests.exceptions.Timeout:
                    # Тайм-аут - просто пропускаем этот цикл
                    print("Тайм-аут запроса, повторная попытка...")
                    time.sleep(2)
                    
                except requests.exceptions.ConnectionError:
                    # Потеряна связь
                    self.connected = False
                    self.control_window.after(0, lambda: self.connection_label.config(
                        text="� Переподключение к ESP8266...",
                        fg='#ffaa00'
                    ))
                    time.sleep(3)
                    # Попытка переподключения
                    self.control_window.after(0, self.connect_to_esp)
                    
                except Exception as e:
                    print(f"Ошибка получения данных: {e}")
                    time.sleep(2)
            
            time.sleep(1)  # Получение данных каждую секунду
    
    def update_interface(self, brightness, light_level):
        """Обновление интерфейса (без изменения яркости экрана)"""
        # Показываем текущее значение с датчика (не усреднённое)
        self.brightness_label.config(text=f"{int(self.target_brightness)}%")
        self.progress['value'] = int(self.target_brightness)
        self.info_label.config(text=f"💡 Датчик: {light_level} | Целевая: {int(self.target_brightness)}% | Текущая: {int(self.current_brightness)}%")
    
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
        self.control_window.deiconify()
        self.control_window.attributes('-topmost', True)
        self.window_visible = True
    
    def hide_window(self):
        """Скрыть окно в трей"""
        self.control_window.withdraw()
        self.window_visible = False
        
        if self.tray_icon is None:
            # Создаём иконку трея
            icon_image = self.create_tray_icon_image()
            menu = pystray.Menu(
                pystray.MenuItem("Показать", self.show_window, default=True),
                pystray.MenuItem("Выход", self.quit_app)
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
