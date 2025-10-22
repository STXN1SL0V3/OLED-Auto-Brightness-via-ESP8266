/*
 * ESP8266 AutoBrightness
 * Copyright (C) 2025 STXN1SL0V3
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>

// ===== НАСТРОЙКИ WiFi =====
// ВАЖНО: Укажите ваши данные WiFi
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ===== СТАТИЧЕСКИЙ IP АДРЕС =====
// Настройте под вашу сеть (опционально - можно использовать DHCP)
IPAddress local_IP(192, 168, 1, 146);      // IP адрес ESP8266
IPAddress gateway(192, 168, 1, 1);         // IP вашего роутера
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

// ===== НАСТРОЙКИ ДАТЧИКА =====
const int LIGHT_SENSOR_PIN = A0;  // Аналоговый пин для фоторезистора
const int READ_INTERVAL = 1000;   // Интервал чтения датчика (мс) - 1 Гц

// ===== АДРЕСА EEPROM ДЛЯ СОХРАНЕНИЯ КАЛИБРОВКИ =====
#define EEPROM_SIZE 16
#define EEPROM_MAGIC 0xAB  // Магическое число для проверки инициализации
#define ADDR_MAGIC 0
#define ADDR_MIN_LOW 1
#define ADDR_MIN_HIGH 2
#define ADDR_MAX_LOW 3
#define ADDR_MAX_HIGH 4

// ===== НАСТРОЙКИ КАЛИБРОВКИ ПО УМОЛЧАНИЮ =====
int minLightValue = 50;     // Минимальное значение датчика (темно)
int maxLightValue = 900;    // Максимальное значение датчика (светло)

// ===== ПЕРЕМЕННЫЕ =====
ESP8266WebServer server(80);
int currentLightLevel = 0;
unsigned long lastReadTime = 0;

// ===== ФУНКЦИИ =====

void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println("\n\n=================================");
  Serial.println("🔆 OLED Auto Brightness v2.0");
  Serial.println("=================================\n");
  
  // Инициализация EEPROM
  EEPROM.begin(EEPROM_SIZE);
  loadCalibrationFromEEPROM();
  
  // Настройка пина датчика
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  
  // Подключение к WiFi
  connectToWiFi();
  
  // Настройка веб-сервера
  setupWebServer();
  
  // Запуск сервера
  server.begin();
  Serial.println("✓ HTTP сервер запущен");
  Serial.print("✓ IP адрес: ");
  Serial.println(WiFi.localIP());
  Serial.println("\nДля доступа откройте: http://" + WiFi.localIP().toString());
  Serial.println("=================================\n");
}

void loop() {
  // ВАЖНО: handleClient() должен вызываться как можно чаще
  server.handleClient();
  yield();  // Даём ESP8266 время на обработку WiFi
  
  // Чтение датчика с интервалом
  if (millis() - lastReadTime >= READ_INTERVAL) {
    lastReadTime = millis();
    readLightSensor();
  }
}

void connectToWiFi() {
  Serial.print("Подключение к WiFi");
  WiFi.mode(WIFI_STA);
  
  // Настройка статического IP
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("\n✗ Ошибка настройки статического IP!");
  }
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi подключен!");
    Serial.print("✓ IP адрес: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ Не удалось подключиться к WiFi!");
    Serial.println("Перезагрузка через 5 секунд...");
    delay(5000);
    ESP.restart();
  }
}

// ===== ФУНКЦИИ ДЛЯ РАБОТЫ С EEPROM =====

void loadCalibrationFromEEPROM() {
  // Проверяем, инициализирована ли EEPROM
  byte magic = EEPROM.read(ADDR_MAGIC);
  
  if (magic == EEPROM_MAGIC) {
    // Загружаем сохранённые значения
    minLightValue = (EEPROM.read(ADDR_MIN_HIGH) << 8) | EEPROM.read(ADDR_MIN_LOW);
    maxLightValue = (EEPROM.read(ADDR_MAX_HIGH) << 8) | EEPROM.read(ADDR_MAX_LOW);
    
    Serial.println("✓ Калибровка загружена из памяти:");
    Serial.print("  MIN: ");
    Serial.println(minLightValue);
    Serial.print("  MAX: ");
    Serial.println(maxLightValue);
  } else {
    // Первый запуск - сохраняем значения по умолчанию
    Serial.println("⚠ Первый запуск - используются значения по умолчанию");
    saveCalibrationToEEPROM();
  }
}

void saveCalibrationToEEPROM() {
  // Сохраняем магическое число
  EEPROM.write(ADDR_MAGIC, EEPROM_MAGIC);
  
  // Сохраняем минимальное значение (2 байта)
  EEPROM.write(ADDR_MIN_LOW, minLightValue & 0xFF);
  EEPROM.write(ADDR_MIN_HIGH, (minLightValue >> 8) & 0xFF);
  
  // Сохраняем максимальное значение (2 байта)
  EEPROM.write(ADDR_MAX_LOW, maxLightValue & 0xFF);
  EEPROM.write(ADDR_MAX_HIGH, (maxLightValue >> 8) & 0xFF);
  
  // Записываем в EEPROM
  EEPROM.commit();
  
  Serial.println("💾 Калибровка сохранена в память:");
  Serial.print("  MIN: ");
  Serial.println(minLightValue);
  Serial.print("  MAX: ");
  Serial.println(maxLightValue);
}

void setupWebServer() {
  // Главная страница с информацией - с кешированием
  server.on("/", HTTP_GET, []() {
    server.sendHeader("Cache-Control", "max-age=3600");  // Кеш на 1 час
    String html = getWebPage();
    server.send(200, "text/html; charset=utf-8", html);
  });
  
  // API для получения сырого значения датчика (JSON) - без расчёта яркости
  server.on("/api/brightness", HTTP_GET, []() {
    // Отдаём только сырое значение датчика и калибровочные данные
    // Расчёт яркости делает Python
    String json = "{\"light_level\":";
    json += currentLightLevel;
    json += ",\"min_light\":";
    json += minLightValue;
    json += ",\"max_light\":";
    json += maxLightValue;
    json += "}";
    server.send(200, "application/json", json);
  });
  
  // API для калибровки минимума
  server.on("/api/calibrate/min", HTTP_GET, []() {
    minLightValue = analogRead(LIGHT_SENSOR_PIN);
    saveCalibrationToEEPROM();  // Сохраняем в EEPROM
    String response = "OK: Min = " + String(minLightValue) + " (сохранено)";
    server.send(200, "text/plain; charset=utf-8", response);
  });
  
  // API для калибровки максимума
  server.on("/api/calibrate/max", HTTP_GET, []() {
    maxLightValue = analogRead(LIGHT_SENSOR_PIN);
    saveCalibrationToEEPROM();  // Сохраняем в EEPROM
    String response = "OK: Max = " + String(maxLightValue) + " (сохранено)";
    server.send(200, "text/plain; charset=utf-8", response);
  });
  
  // API для сброса калибровки
  server.on("/api/calibrate/reset", HTTP_GET, []() {
    minLightValue = 50;
    maxLightValue = 900;
    saveCalibrationToEEPROM();
    server.send(200, "text/plain; charset=utf-8", "OK: Калибровка сброшена");
  });
}

void readLightSensor() {
  // Просто читаем датчик - весь расчёт делает Python
  currentLightLevel = analogRead(LIGHT_SENSOR_PIN);
  
  // Вывод в Serial для отладки (каждые 5 секунд)
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint >= 5000) {
    Serial.print("💡 Датчик: ");
    Serial.print(currentLightLevel);
    Serial.print(" (калибровка: ");
    Serial.print(minLightValue);
    Serial.print("-");
    Serial.print(maxLightValue);
    Serial.println(")");
    lastPrint = millis();
  }
}

String getWebPage() {
  // Генерируем минимальную HTML страницу порциями для экономии памяти
  String html = "";
  html.reserve(2048);  // Резервируем память заранее
  
  html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
  html += "<title>OLED Brightness</title>";
  html += "<style>body{font-family:Arial;background:#1a1a1a;color:#fff;padding:20px}";
  html += ".c{max-width:600px;margin:0 auto;background:#2b2b2b;padding:30px;border-radius:10px}";
  html += "h1{color:#0f8;text-align:center}.info{background:#333;padding:15px;border-radius:5px;margin:10px 0}";
  html += ".v{font-size:24px;color:#0f8;font-weight:bold}";
  html += "button{background:#0f8;color:#000;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;margin:5px}";
  html += ".bar{background:#444;height:30px;border-radius:5px;overflow:hidden}";
  html += ".bar>div{background:#0f8;height:100%;transition:width .3s}</style>";
  
  html += "<script>let a=1;function u(){if(!a)return;fetch('/api/brightness').then(r=>r.json()).then(d=>{";
  html += "document.getElementById('l').innerText=d.light_level;";
  html += "}).catch(e=>console.log(e))}";
  html += "function t(){a=!a;document.getElementById('t').innerText=a?'⏸':'▶';if(a)u()}";
  html += "setInterval(u,3000);u()</script></head><body><div class='c'>";
  html += "<h1>🔆 OLED Brightness</h1>";
  html += "<div style='text-align:center'><button id='t' onclick='t()' style='background:#fa0'>⏸</button></div>";
  
  html += "<div class='info'><h3>Датчик света:</h3><div class='v' id='l'>";
  html += currentLightLevel;
  html += "</div></div>";
  
  html += "<div class='info'><h3>Калибровка:</h3>";
  html += "<p>1. Закройте датчик → <button onclick=\"fetch('/api/calibrate/min').then(r=>r.text()).then(alert)\">MIN</button></p>";
  html += "<p>2. Фонарик на датчик → <button onclick=\"fetch('/api/calibrate/max').then(r=>r.text()).then(alert)\">MAX</button></p>";
  html += "<p><button onclick=\"if(confirm('Сброс?'))fetch('/api/calibrate/reset').then(r=>r.text()).then(alert)\" style='background:#f44'>Сброс</button></p></div>";
  
  html += "<div class='info'><p><b>IP:</b> ";
  html += WiFi.localIP().toString();
  html += "</p><p><b>Диапазон:</b> ";
  html += minLightValue;
  html += " - ";
  html += maxLightValue;
  html += "</p></div></div></body></html>";
  
  return html;
}
