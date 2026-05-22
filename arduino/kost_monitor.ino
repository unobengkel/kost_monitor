/*
 * ============================================================
 * SISTEM MONITORING & KONTROL LISTRIK KAMAR KOST
 * Berbasis Wemos D1 Mini (ESP8266)
 * 
 * Komponen:
 * - Wemos D1 Mini (ESP8266)
 * - LCD 16x2 I2C
 * - Sensor Arus ACS712 (30A)
 * - Modul Relay 1 Channel
 * 
 * Fitur:
 * - Monitoring daya listrik real-time
 * - Kontrol relay ON/OFF via server
 * - Proteksi overload otomatis
 * - Tampilan LCD status sistem
 * - Auto-reconnect WiFi & Server
 * ============================================================
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

// ============================================================
// KONFIGURASI PIN
// ============================================================
#define RELAY_PIN   D3    // GPIO0 - Relay Control (LOW aktif)
#define SENSOR_PIN  A0    // ADC   - ACS712 Output
#define LCD_SDA     D2    // GPIO4 - I2C Data
#define LCD_SCL     D1    // GPIO5 - I2C Clock

// ============================================================
// KONFIGURASI I2C LCD
// ============================================================
#define LCD_ADDRESS   0x27
#define LCD_COLUMNS   16
#define LCD_ROWS      2

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);

// ============================================================
// KONFIGURASI WiFi & SERVER
// ============================================================
const char* WIFI_SSID       = "WiFiKost";
const char* WIFI_PASSWORD   = "password123";
const char* SERVER_URL      = "http://192.168.1.100:5000";
const char* DEVICE_ID       = "kamar_01";

// ============================================================
// KONFIGURASI SENSOR ACS712 (30A)
// ============================================================
const float ACS712_SENSITIVITY = 0.066;   // 66 mV/A
const float ACS712_VREF        = 5.0;     // Tegangan referensi ADC
const float ADC_RESOLUTION     = 1024.0;  // Resolusi ADC ESP8266 (10-bit)
const float VOLTAGE_STANDARD   = 220.0;   // Tegangan standar PLN
const int   NUM_SAMPLES        = 100;     // Jumlah sampel untuk rata-rata

// ============================================================
// KONFIGURASI BATAS DAYA
// ============================================================
const float DAYA_MAX        = 900.0;   // Batas daya maksimal (Watt)
const int   OVERLOAD_COOLDOWN = 5000;  // Cooldown setelah overload (ms)

// ============================================================
// KONFIGURASI TIMING
// ============================================================
const unsigned long SEND_INTERVAL_MS = 5000;   // Kirim data setiap 5 detik
const unsigned long LCD_UPDATE_MS    = 1000;   // Update LCD setiap 1 detik
const unsigned long WIFI_RETRY_MS    = 10000;  // Retry WiFi setiap 10 detik
const unsigned long SERVER_TIMEOUT_MS = 3000;  // Timeout HTTP request

// ============================================================
// VARIABEL GLOBAL
// ============================================================
float currentValue    = 0.0;   // Arus terukur (Ampere)
float powerValue      = 0.0;   // Daya terukur (Watt)
float energyTotal     = 0.0;   // Total energi (kWh)
float powerMax        = 0.0;   // Daya maksimum yang tercatat
bool  relayState      = false; // Status relay: true=ON, false=OFF
bool  overloadState   = false; // Status overload: true=overload
bool  wifiConnected   = false; // Status WiFi
bool  serverConnected = false; // Status Server

unsigned long lastSendTime      = 0;
unsigned long lastLcdUpdate     = 0;
unsigned long lastWifiRetry     = 0;
unsigned long overloadStartTime = 0;
int           lcdDisplayMode    = 0;  // 0: status, 1: daya, 2: energi

// Kalibrasi offset sensor (di-set saat startup tanpa arus)
float sensorOffset = 0.0;

// ============================================================
// FUNCTION: BACA SENSOR ARUS (ACS712)
// ============================================================
float readCurrent() {
  long sum = 0;
  
  // Ambil sampel
  for (int i = 0; i < NUM_SAMPLES; i++) {
    sum += analogRead(SENSOR_PIN);
    delayMicroseconds(100);
  }
  
  // Rata-rata sampel
  float adcAverage = (float)sum / NUM_SAMPLES;
  
  // Konversi ADC ke tegangan (Volt)
  float voltage = (adcAverage / ADC_RESOLUTION) * ACS712_VREF;
  
  // Hitung arus: (tegangan - offset) / sensitivitas
  float current = (voltage - sensorOffset) / ACS712_SENSITIVITY;
  
  // Filter nilai negatif dan noise
  if (current < 0.1) {
    current = 0.0;
  }
  
  return current;
}

// ============================================================
// FUNCTION: KALIBRASI SENSOR
// ============================================================
void calibrateSensor() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Kalibrasi Sensor");
  lcd.setCursor(0, 1);
  lcd.print("Tunggu...");
  
  delay(2000);
  
  long sum = 0;
  for (int i = 0; i < 500; i++) {
    sum += analogRead(SENSOR_PIN);
    delayMicroseconds(100);
  }
  
  float adcAvg = (float)sum / 500.0;
  sensorOffset = (adcAvg / ADC_RESOLUTION) * ACS712_VREF;
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Offset: ");
  lcd.print(sensorOffset, 3);
  lcd.print("V");
  lcd.setCursor(0, 1);
  lcd.print("Siap!");
  delay(1000);
}

// ============================================================
// FUNCTION: INIT LCD
// ============================================================
void initLCD() {
  Wire.begin(LCD_SDA, LCD_SCL);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  // Tampilkan splash screen
  lcd.setCursor(0, 0);
  lcd.print(" Kost Monitor ");
  lcd.setCursor(0, 1);
  lcd.print(" Ver 1.0 ");
  delay(2000);
  lcd.clear();
}

// ============================================================
// FUNCTION: KONEKSI WiFi
// ============================================================
bool connectWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Connecting WiFi");
    lcd.setCursor(0, 1);
    lcd.print(WIFI_SSID);
    
    Serial.println();
    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
      delay(500);
      Serial.print(".");
      attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println();
      Serial.println("WiFi Connected!");
      Serial.print("IP Address: ");
      Serial.println(WiFi.localIP());
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("WiFi: Connected");
      lcd.setCursor(0, 1);
      lcd.print("IP: ");
      lcd.print(WiFi.localIP().toString().substring(0, 13));
      delay(1500);
      
      wifiConnected = true;
      return true;
    } else {
      Serial.println();
      Serial.println("WiFi Failed!");
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("WiFi: GAGAL!");
      lcd.setCursor(0, 1);
      lcd.print("Coba ulang...");
      delay(2000);
      
      wifiConnected = false;
      return false;
    }
  }
  
  wifiConnected = true;
  return true;
}

// ============================================================
// FUNCTION: KIRIM DATA KE SERVER
// ============================================================
bool sendDataToServer() {
  if (WiFi.status() != WL_CONNECTED) {
    serverConnected = false;
    return false;
  }
  
  HTTPClient http;
  WiFiClient client;
  
  String url = String(SERVER_URL) + "/api/device/data";
  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(SERVER_TIMEOUT_MS);
  
  // Buat JSON payload
  StaticJsonDocument<256> doc;
  doc["device_id"]   = DEVICE_ID;
  doc["arus"]        = currentValue;
  doc["daya"]        = powerValue;
  doc["tegangan"]    = VOLTAGE_STANDARD;
  doc["relay_state"] = relayState ? "ON" : "OFF";
  doc["overload"]    = overloadState;
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("Mengirim data ke server...");
  Serial.println(payload);
  
  int httpCode = http.POST(payload);
  
  if (httpCode > 0) {
    Serial.print("Response code: ");
    Serial.println(httpCode);
    
    if (httpCode == HTTP_CODE_OK) {
      String response = http.getString();
      Serial.println("Response: " + response);
      
      // Parse response JSON untuk perintah relay
      StaticJsonDocument<128> respDoc;
      DeserializationError error = deserializeJson(respDoc, response);
      
      if (!error) {
        if (respDoc.containsKey("command")) {
          String command = respDoc["command"].as<String>();
          if (command == "RELAY_ON") {
            relayOn(true);
          } else if (command == "RELAY_OFF") {
            relayOff(true);
          }
        }
        
        if (respDoc.containsKey("batas_daya")) {
          // Server bisa mengirim batas daya baru
          // float batasBaru = respDoc["batas_daya"].as<float>();
          // TODO: update batas daya jika diperlukan
        }
      }
      
      http.end();
      serverConnected = true;
      return true;
    } else if (httpCode == HTTP_CODE_SERVICE_UNAVAILABLE) {
      Serial.println("Server overload/error");
      serverConnected = false;
    } else {
      serverConnected = false;
    }
  } else {
    Serial.print("HTTP Error: ");
    Serial.println(http.errorToString(httpCode).c_str());
    serverConnected = false;
  }
  
  http.end();
  return false;
}

// ============================================================
// FUNCTION: AMBIL PERINTAH RELAY DARI SERVER
// ============================================================
bool getRelayCommand() {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }
  
  HTTPClient http;
  WiFiClient client;
  
  String url = String(SERVER_URL) + "/api/device/command/" + DEVICE_ID;
  http.begin(client, url);
  http.setTimeout(SERVER_TIMEOUT_MS);
  
  int httpCode = http.GET();
  
  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    Serial.println("Command response: " + response);
    
    StaticJsonDocument<128> doc;
    DeserializationError error = deserializeJson(doc, response);
    
    if (!error) {
      String command = doc["command"].as<String>();
      
      if (command == "RELAY_ON") {
        relayOn(true);
        return true;
      } else if (command == "RELAY_OFF") {
        relayOff(true);
        return true;
      }
    }
  }
  
  http.end();
  return false;
}

// ============================================================
// FUNCTION: KONTROL RELAY
// ============================================================
void relayOn(bool fromServer = false) {
  digitalWrite(RELAY_PIN, LOW);   // Relay aktif LOW
  relayState = true;
  Serial.println("Relay: ON");
  
  if (!fromServer) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Relay: ON");
    lcd.setCursor(0, 1);
    lcd.print("Listrik Nyala");
    delay(1000);
  }
}

void relayOff(bool fromServer = false) {
  digitalWrite(RELAY_PIN, HIGH);  // Relay mati HIGH
  relayState = false;
  Serial.println("Relay: OFF");
  
  if (!fromServer) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Relay: OFF");
    lcd.setCursor(0, 1);
    lcd.print("Listrik Padam");
    delay(1000);
  }
}

// ============================================================
// FUNCTION: CEK OVERLOAD
// ============================================================
void checkOverload() {
  if (powerValue > DAYA_MAX && relayState && !overloadState) {
    // Overload terdeteksi!
    overloadState = true;
    overloadStartTime = millis();
    
    Serial.println("!!! OVERLOAD DETECTED !!!");
    Serial.print("Daya: ");
    Serial.print(powerValue);
    Serial.print("W > Batas: ");
    Serial.print(DAYA_MAX);
    Serial.println("W");
    
    // Matikan relay
    relayOff(false);
    
    // Kirim status overload ke server
    sendDataToServer();
    
    // Tampilkan di LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("!!! OVERLOAD !!!");
    lcd.setCursor(0, 1);
    lcd.print(powerValue, 0);
    lcd.print("W > ");
    lcd.print(DAYA_MAX, 0);
    lcd.print("W");
    delay(3000);
    
    // Tampilkan peringatan padam
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("LISTRIK PADAM");
    lcd.setCursor(0, 1);
    lcd.print("Overload! ");
    lcd.print(powerValue, 0);
    lcd.print("W");
  }
  
  // Reset overload setelah cooldown jika relay mati
  if (overloadState && !relayState) {
    if (millis() - overloadStartTime > OVERLOAD_COOLDOWN) {
      overloadState = false;
      Serial.println("Overload reset, relay siap diaktifkan kembali");
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Siap Aktifkan");
      lcd.setCursor(0, 1);
      lcd.print("Tekan ON di Web");
      delay(2000);
    }
  }
}

// ============================================================
// FUNCTION: UPDATE LCD DISPLAY
// ============================================================
void updateLCD() {
  lcdDisplayMode = (lcdDisplayMode + 1) % 3;
  
  lcd.clear();
  
  switch (lcdDisplayMode) {
    case 0:  // Mode: Status Koneksi
      lcd.setCursor(0, 0);
      lcd.print(DEVICE_ID);
      lcd.print(" ");
      if (relayState) {
        lcd.print((char)0);
        lcd.print("ON ");
      } else if (overloadState) {
        lcd.print("PADAM");
      } else {
        lcd.print("OFF");
      }
      
      lcd.setCursor(0, 1);
      if (wifiConnected) {
        lcd.print("WiFi:OK ");
      } else {
        lcd.print("WiFi:FAIL ");
      }
      if (serverConnected) {
        lcd.print("Srv:OK");
      } else {
        lcd.print("Srv:FAIL");
      }
      break;
      
    case 1:  // Mode: Daya & Arus
      lcd.setCursor(0, 0);
      lcd.print("Daya: ");
      lcd.print(powerValue, 0);
      lcd.print(" W   ");
      
      lcd.setCursor(0, 1);
      lcd.print("Arus: ");
      lcd.print(currentValue, 2);
      lcd.print(" A   ");
      break;
      
    case 2:  // Mode: Energi & Relay
      lcd.setCursor(0, 0);
      lcd.print("Energi: ");
      lcd.print(energyTotal, 2);
      lcd.print("kWh");
      
      lcd.setCursor(0, 1);
      lcd.print("Relay: ");
      if (relayState) {
        lcd.print("AKTIF");
      } else {
        lcd.print("MATI ");
      }
      lcd.print(" Max:");
      lcd.print(powerMax, 0);
      lcd.print("W");
      break;
  }
}

// ============================================================
// FUNCTION: BUAT KARAKTER KHUSUS UNTUK LCD
// ============================================================
void createCustomChars() {
  // Karakter untuk indikator ON (lingkaran terisi)
  byte onChar[8] = {
    0b01110,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b01110
  };
  lcd.createChar(0, onChar);
}

// ============================================================
// ARDUINO SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("========================================");
  Serial.println("  SISTEM MONITORING LISTRIK KOST v1.0 ");
  Serial.println("========================================");
  Serial.println("Inisialisasi sistem...");
  
  // Inisialisasi pin
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);  // Relay mati (LOW aktif)
  
  // Inisialisasi LCD
  initLCD();
  createCustomChars();
  
  // Kalibrasi sensor
  calibrateSensor();
  
  // Koneksi WiFi
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Mulai Sistem...");
  delay(500);
  
  connectWiFi();
  
  // Cek koneksi server dengan mengirim data pertama
  if (WiFi.status() == WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Server: Connect");
    lcd.setCursor(0, 1);
    lcd.print("Mengirim data...");
    
    if (sendDataToServer()) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Server: OK");
      lcd.setCursor(0, 1);
      lcd.print("Siap Monitoring");
      delay(1500);
    } else {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Server: GAGAL");
      lcd.setCursor(0, 1);
      lcd.print("Mode Offline...");
      delay(2000);
    }
  }
  
  // Set waktu awal
  lastSendTime = millis();
  lastLcdUpdate = millis();
  lastWifiRetry = millis();
  
  Serial.println("Setup selesai. Memulai loop utama...");
  Serial.println("----------------------------------------");
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(DEVICE_ID);
  lcd.print(" Siap!");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring...");
  delay(1500);
}

// ============================================================
// ARDUINO MAIN LOOP
// ============================================================
void loop() {
  unsigned long now = millis();
  
  // ==========================================================
  // 1. CEK KONEKSI WiFi (retry setiap 10 detik jika gagal)
  // ==========================================================
  if (WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
    
    if (now - lastWifiRetry >= WIFI_RETRY_MS) {
      Serial.println("WiFi terputus, mencoba reconnect...");
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("WiFi Terputus!");
      lcd.setCursor(0, 1);
      lcd.print("Menghubungkan...");
      
      connectWiFi();
      lastWifiRetry = now;
    }
  } else {
    wifiConnected = true;
  }
  
  // ==========================================================
  // 2. BACA SENSOR ARUS (setiap iterasi loop)
  // ==========================================================
  currentValue = readCurrent();
  powerValue = currentValue * VOLTAGE_STANDARD;
  
  // Update daya maksimum
  if (powerValue > powerMax) {
    powerMax = powerValue;
  }
  
  // Update total energi (integrasi daya per detik)
  // Asumsi: loop berjalan ~1 detik, jadi tambah (daya * 1/3600) kWh
  static unsigned long lastEnergyCalc = 0;
  if (now - lastEnergyCalc >= 1000) {
    energyTotal += (powerValue / 1000.0) / 3600.0;  // kWh
    lastEnergyCalc = now;
  }
  
  // ==========================================================
  // 3. CEK KONDISI OVERLOAD
  // ==========================================================
  checkOverload();
  
  // ==========================================================
  // 4. KIRIM DATA KE SERVER (setiap 5 detik)
  // ==========================================================
  if (now - lastSendTime >= SEND_INTERVAL_MS) {
    if (WiFi.status() == WL_CONNECTED) {
      sendDataToServer();
    }
    lastSendTime = now;
  }
  
  // ==========================================================
  // 5. AMBIL PERINTAH RELAY DARI SERVER (setiap 10 detik)
  // ==========================================================
  static unsigned long lastCommandCheck = 0;
  if (now - lastCommandCheck >= 10000) {
    if (WiFi.status() == WL_CONNECTED) {
      getRelayCommand();
    }
    lastCommandCheck = now;
  }
  
  // ==========================================================
  // 6. UPDATE LCD (setiap 1 detik, ganti mode)
  // ==========================================================
  if (now - lastLcdUpdate >= LCD_UPDATE_MS) {
    // Jika overload, tampilkan peringatan terus
    if (overloadState && !relayState) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("!!! PADAM !!!");
      lcd.setCursor(0, 1);
      lcd.print("Overload ");
      lcd.print(powerValue, 0);
      lcd.print("W");
    } else {
      updateLCD();
    }
    
    lastLcdUpdate = now;
  }
  
  // ==========================================================
  // 7. DEBUG SERIAL (setiap 5 detik)
  // ==========================================================
  static unsigned long lastDebugPrint = 0;
  if (now - lastDebugPrint >= 5000) {
    Serial.println("----------------------------------------");
    Serial.print("Device: "); Serial.println(DEVICE_ID);
    Serial.print("Arus: "); Serial.print(currentValue, 3); Serial.println(" A");
    Serial.print("Daya: "); Serial.print(powerValue, 1); Serial.println(" W");
    Serial.print("Energi: "); Serial.print(energyTotal, 4); Serial.println(" kWh");
    Serial.print("Relay: "); Serial.println(relayState ? "ON" : "OFF");
    Serial.print("Overload: "); Serial.println(overloadState ? "YES" : "NO");
    Serial.print("WiFi: "); Serial.println(wifiConnected ? "OK" : "FAIL");
    Serial.print("Server: "); Serial.println(serverConnected ? "OK" : "FAIL");
    Serial.print("Daya Max: "); Serial.print(powerMax, 1); Serial.println(" W");
    Serial.println("----------------------------------------");
    
    lastDebugPrint = now;
  }
  
  // Delay untuk stabilitas
  delay(500);
}