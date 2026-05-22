# BAB 6: Tutorial Penggunaan Project

## 6.1 Persiapan Sebelum Menggunakan

### 6.1.1 Daftar Alat dan Bahan

Sebelum memulai proyek, pastikan Anda telah menyiapkan alat dan bahan berikut:

#### A. Perangkat Keras (Hardware)

| No | Nama Komponen | Jumlah | Keterangan |
|----|---------------|--------|------------|
| 1 | Wemos D1 Mini (ESP8266) | 1 | Mikrokontroler utama |
| 2 | LCD 16x2 I2C | 1 | Display informasi |
| 3 | Sensor Arus ACS712 (30A) | 1 | Sensor pengukur arus |
| 4 | Modul Relay 1 Channel | 1 | Kontrol ON/OFF listrik |
| 5 | Charger HP (5V, min 2A) | 1 | Power supply |
| 6 | Kabel USB Micro | 1 | Koneksi charger ke Wemos |
| 7 | Kabel Jumper (M-M) | 20 pcs | Kabel koneksi komponen |
| 8 | Kabel Listrik (NYA 1.5mm) | 2 meter | Kabel AC 220V |
| 9 | Stop Kontak | 1 | Sumber listrik AC |
| 10 | Project Box / Kotak Panel | 1 | Tempat komponen |

#### B. Perangkat Lunak (Software)

| No | Software | Fungsi | Link Download |
|----|----------|--------|---------------|
| 1 | Arduino IDE | Programming Wemos ESP8266 | arduino.cc |
| 2 | Python 3.x | Menjalankan server | python.org |
| 3 | Web Browser (Chrome/Edge) | Mengakses aplikasi web | - |
| 4 | Text Editor (VS Code) | Mengedit file | code.visualstudio.com |

#### C. Library yang Dibutuhkan

**Library Arduino IDE:**
```
1. ESP8266 Board Package  (via Board Manager)
2. LiquidCrystal_I2C      (via Library Manager)
3. ESP8266WiFi            (built-in)
4. ESP8266HTTPClient      (built-in)
5. ArduinoJson            (via Library Manager)
```

**Library Python:**
```
1. flask / fastapi
2. flask-cors
3. sqlite3 (built-in)
4. jwt / pyjwt
5. pandas (untuk export)
6. openpyxl (untuk export excel)
```

### 6.1.2 Persiapan Lingkungan

#### Langkah 1: Install Arduino IDE
1. Download Arduino IDE dari https://www.arduino.cc/en/software
2. Install sesuai sistem operasi (Windows/Mac/Linux)
3. Buka Arduino IDE

#### Langkah 2: Install Board ESP8266
1. Buka Arduino IDE
2. File > Preferences
3. Pada "Additional Boards Manager URLs", tambahkan:
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
4. Tools > Board > Boards Manager
5. Cari "ESP8266" dan install

#### Langkah 3: Install Library
1. Buka Arduino IDE
2. Sketch > Include Library > Manage Libraries
3. Cari dan install library berikut:
   - `LiquidCrystal_I2C` by Frank de Brabander
   - `ArduinoJson` by Benoit Blanchon

#### Langkah 4: Install Python
1. Download Python dari https://www.python.org/downloads/
2. Install Python (centang "Add Python to PATH")
3. Buka terminal/CMD dan verifikasi:
   ```
   python --version
   ```

#### Langkah 5: Install Library Python
```
pip install flask flask-cors pyjwt pandas openpyxl
```

### 6.1.3 Persiapan Server

Buat folder proyek server dengan struktur berikut:

```
C:\KostMonitor\server\
    +-- app/
    |   +-- __init__.py
    |   +-- config.py
    |   +-- domain/
    |   |   +-- __init__.py
    |   |   +-- models.py
    |   |   +-- enums.py
    |   +-- application/
    |   |   +-- __init__.py
    |   |   +-- device_service.py
    |   |   +-- kamar_service.py
    |   |   +-- auth_service.py
    |   |   +-- histori_service.py
    |   +-- infrastructure/
    |   |   +-- __init__.py
    |   |   +-- database.py
    |   |   +-- repository.py
    |   |   +-- auth.py
    |   +-- presentation/
    |       +-- __init__.py
    |       +-- routes.py
    |       +-- serializers.py
    |       +-- middlewares.py
    +-- main.py
    +-- requirements.txt
    +-- data/
        +-- (database.db akan dibuat otomatis)
```

---

## 6.2 Tutorial Menyalakan Project

### 6.2.1 Rangkaian Perangkat Keras

#### Langkah 1: Rakit Komponen

Ikuti diagram koneksi berikut:

```
WEMOS D1 MINI          LCD 16x2 I2C
+--------------+       +----------+
| 5V (Vin)     |------>| VCC      |
| GND          |------>| GND      |
| D1 (GPIO5)   |------>| SCL      |
| D2 (GPIO4)   |------>| SDA      |
+--------------+       +----------+

WEMOS D1 MINI          SENSOR ACS712
+--------------+       +----------+
| 5V (Vin)     |------>| VCC      |
| GND          |------>| GND      |
| A0 (ADC)     |<------| OUT      |
+--------------+       +----------+

WEMOS D1 MINI          RELAY MODULE
+--------------+       +----------+
| 5V (Vin)     |------>| VCC      |
| GND          |------>| GND      |
| D3 (GPIO0)   |------>| IN       |
+--------------+       +----------+

RELAY MODULE           BEBAN LISTRIK AC
+----------+           +----------+
| COM       |<---------| Fase PLN |
| NO        |--------->| Ke Kamar |
+----------+           +----------+

SENSOR ACS712          BEBAN LISTRIK AC
+----------+           +----------+
| IP+       |<---------| Fase PLN |
| IP-       |--------->| COM Relay|
+----------+           +----------+
```

#### Langkah 2: Hubungkan Power
1. Colokkan kabel USB Micro ke Wemos D1 Mini
2. Hubungkan charger HP ke stop kontak AC 220V
3. Hubungkan ujung USB charger ke kabel USB Micro Wemos
4. LED merah pada Wemos akan menyala menandakan ada daya

#### Langkah 3: Verifikasi Koneksi
Periksa LED indikator pada setiap komponen:
- **Wemos**: LED merah menyala (power)
- **LCD**: Backlight menyala (jika ada)
- **Relay**: LED indikator (menyala jika relay aktif)
- **ACS712**: Tidak ada LED, gunakan multimeter untuk cek output

### 6.2.2 Upload Program ke Wemos

#### Langkah 1: Buka Arduino IDE
1. Buka Arduino IDE
2. File > New untuk membuat sketch baru
3. Paste kode program ESP8266 (lihat 6.4.1)

#### Langkah 2: Konfigurasi Board
1. Tools > Board > ESP8266 Boards > "LOLIN(WEMOS) D1 R2 & mini"
2. Tools > Port > Pilih port COM Wemos (misal: COM3)
   - Cek port di Device Manager jika tidak muncul

#### Langkah 3: Sesuaikan Konfigurasi
Edit bagian konfigurasi pada kode:

```cpp
// ====== KONFIGURASI ======
const char* ssid = "NamaWiFiKost";       // Ganti dengan SSID WiFi
const char* password = "PasswordWiFi";    // Ganti dengan password WiFi
const char* serverUrl = "http://192.168.1.100:5000"; // IP server
const char* deviceId = "KMR01";          // ID perangkat
float dayaMaksimal = 900.0;              // Batas daya (Watt)
// =========================
```

#### Langkah 4: Upload Program
1. Klik tombol "Upload" (panah kanan) di Arduino IDE
2. Tunggu proses kompilasi dan upload selesai
3. Jika berhasil, akan muncul "Done uploading" di console
4. Wemos akan restart otomatis dan menjalankan program

### 6.2.3 Menjalankan Server

#### Langkah 1: Buka Terminal
Buka Command Prompt atau Terminal di folder server:

```bash
cd C:\KostMonitor\server
```

#### Langkah 2: Jalankan Server
```bash
python main.py
```

#### Langkah 3: Verifikasi Server
Buka browser dan akses:
```
http://localhost:5000/api/kamar
```

Jika berhasil, akan tampil response JSON data kamar.

### 6.2.4 Membuka Aplikasi Web

#### Langkah 1: Buka File HTML
1. Buka file `index.html` di browser (double-click)
2. Atau gunakan Live Server di VS Code

#### Langkah 2: Login
1. Masukkan username: `admin`
2. Masukkan password: `admin123`
3. Klik tombol "Masuk"

#### Langkah 3: Verifikasi
Setelah login, akan tampil halaman Dashboard dengan data monitoring.

---

## 6.3 Tutorial Membuka Program

### 6.3.1 Struktur File Program

```
C:\KostMonitor\
    |
    +-- document/                 # Folder dokumentasi
    |   +-- nama_project/
    |       +-- 01_pengenalan_project.md
    |       +-- 02_pengembangan_proses_bisnis.md
    |       +-- 03_pengembangan_kerja_server.md
    |       +-- 04_pengenalan_bagian_hardware.md
    |       +-- 05_pengenalan_tampilan_antarmuka_aplikasi.md
    |       +-- 06_tutorial_penggunaan_project.md
    |
    +-- server/                   # Folder server Python
    |   +-- app/
    |   |   +-- __init__.py
    |   |   +-- config.py
    |   |   +-- domain/
    |   |   |   +-- __init__.py
    |   |   |   +-- models.py
    |   |   |   +-- enums.py
    |   |   +-- application/
    |   |   |   +-- __init__.py
    |   |   |   +-- device_service.py
    |   |   |   +-- kamar_service.py
    |   |   |   +-- auth_service.py
    |   |   |   +-- histori_service.py
    |   |   +-- infrastructure/
    |   |   |   +-- __init__.py
    |   |   |   +-- database.py
    |   |   |   +-- repository.py
    |   |   |   +-- auth.py
    |   |   +-- presentation/
    |   |       +-- __init__.py
    |   |       +-- routes.py
    |   |       +-- serializers.py
    |   |       +-- middlewares.py
    |   +-- main.py
    |   +-- requirements.txt
    |   +-- data/
    |       +-- database.db
    |
    +-- esp8266/                  # Folder kode ESP8266
    |   +-- kost_monitor.ino
    |   +-- config.h
    |   +-- lcd_handler.h
    |   +-- sensor_handler.h
    |   +-- wifi_handler.h
    |   +-- server_handler.h
    |
    +-- web/                      # Folder aplikasi web
    |   +-- index.html
    |   +-- assets/
    |       +-- css/
    |       |   +-- style.css (opsional, jika tidak pakai CDN)
    |       +-- js/
    |           +-- app.js
    |           +-- dashboard.js
    |           +-- histori.js
    |           +-- settings.js
    |           +-- simulasi.js
    |
    +-- README.md
```

### 6.3.2 Cara Membuka Setiap Bagian

#### A. Membuka Dokumentasi
```
Buka folder document/nama_project/
Double-click file .md untuk melihat dokumentasi
Atau buka dengan VS Code untuk preview markdown
```

#### B. Membuka Kode Server
```
Buka folder server/ dengan VS Code
File utama: server/main.py
Jalankan: python server/main.py
```

#### C. Membuka Kode ESP8266
```
Buka file esp8266/kost_monitor.ino dengan Arduino IDE
Edit konfigurasi di file esp8266/config.h
Upload ke Wemos D1 Mini
```

#### D. Membuka Aplikasi Web
```
Buka folder web/
Double-click file index.html
Atau buka dengan VS Code dan gunakan Live Server
Atau deploy ke hosting web statis
```

### 6.3.3 Menjalankan Semua Sistem

Untuk menjalankan sistem secara lengkap, ikuti urutan berikut:

```
URUTAN MENJALANKAN SISTEM:
==========================

1. [HARDWARE] Rakit rangkaian sesuai diagram
2. [HARDWARE] Hubungkan power ke Wemos
3. [SOFTWARE] Upload program ke Wemos via Arduino IDE
4. [SERVER]   Jalankan server Python:
              cd C:\KostMonitor\server
              python main.py
5. [WEB]      Buka index.html di browser
6. [VERIFIKASI] Cek LCD pada perangkat: tampilkan "Server OK"
7. [VERIFIKASI] Cek Dashboard web: data muncul dalam 10 detik
```

---

## 6.4 Contoh Penggunaan

### 6.4.1 Contoh Kode Program ESP8266

Berikut adalah contoh kode lengkap untuk Wemos ESP8266:

#### File: `esp8266/kost_monitor.ino`

```cpp
/*
 * SISTEM MONITORING LISTRIK KAMAR KOST
 * Berbasis Wemos D1 Mini (ESP8266)
 * 
 * Fitur:
 * - Baca sensor arus ACS712
 * - Kirim data ke server via HTTP POST
 * - Terima perintah ON/OFF via HTTP GET
 * - Tampilkan status di LCD 16x2 I2C
 * - Matikan relay jika daya melebihi batas
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

#include "config.h"
#include "wifi_handler.h"
#include "lcd_handler.h"
#include "sensor_handler.h"
#include "server_handler.h"

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastSend = 0;
const unsigned long sendInterval = 5000; // Kirim data setiap 5 detik

float tegangan = VOLTAGE_STANDARD;
float arus = 0.0;
float daya = 0.0;
float energy_kwh = 0.0;
String statusRelay = "ON";

void setup() {
  Serial.begin(115200);
  Serial.println("\n=================================");
  Serial.println("SISTEM MONITORING LISTRIK KOST");
  Serial.println("=================================");
  
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Relay ON (active LOW)
  
  initLCD(lcd);
  tampilkanPesanLCD(lcd, "Memulai...", "System Booting", 2000);
  
  // Koneksi WiFi
  tampilkanPesanLCD(lcd, "WiFi", "Menghubungkan...", 0);
  initWiFi();
  
  if (WiFi.status() == WL_CONNECTED) {
    tampilkanPesanLCD(lcd, "WiFi OK", WiFi.localIP().toString(), 2000);
    
    tampilkanPesanLCD(lcd, "Server", "Menghubungkan...", 0);
    if (cekKoneksiServer()) {
      tampilkanPesanLCD(lcd, "Server OK", "Siap Monitor!", 2000);
    } else {
      tampilkanPesanLCD(lcd, "Server", "GAGAL!", 2000);
    }
  } else {
    tampilkanPesanLCD(lcd, "WiFi GAGAL", "Cek Koneksi!", 0);
  }
  
  Serial.println("System siap!");
  updateLCD(lcd, tegangan, arus, daya, statusRelay);
}

void loop() {
  // Baca sensor arus
  arus = bacaArus();
  daya = tegangan * arus;
  
  // Update LCD setiap loop
  updateLCD(lcd, tegangan, arus, daya, statusRelay);
  
  // Cek batas daya
  if (daya > DAYA_MAKSIMAL && statusRelay == "ON") {
    Serial.println("OVER LIMIT! Mematikan relay...");
    matikanRelay();
    statusRelay = "OFF";
    updateLCD(lcd, tegangan, arus, daya, statusRelay);
  }
  
  // Kirim data ke server setiap interval
  unsigned long now = millis();
  if (now - lastSend >= sendInterval) {
    lastSend = now;
    
    if (WiFi.status() == WL_CONNECTED) {
      String response = kirimDataKeServer(tegangan, arus, daya, energy_kwh, statusRelay);
      
      if (response.indexOf("OFF") > 0 && statusRelay == "ON") {
        Serial.println("Perintah OFF dari server!");
        matikanRelay();
        statusRelay = "OFF";
        updateLCD(lcd, tegangan, arus, daya, statusRelay);
      } else if (response.indexOf("ON") > 0 && statusRelay == "OFF") {
        Serial.println("Perintah ON dari server!");
        nyalakanRelay();
        statusRelay = "ON";
        updateLCD(lcd, tegangan, arus, daya, statusRelay);
      }
      
      // Akumulasi energi (kWh = (Watt * jam) / 1000)
      energy_kwh += (daya * (sendInterval / 3600000.0)) / 1000.0;
      
    } else {
      Serial.println("WiFi terputus! Mencoba reconnect...");
      tampilkanPesanLCD(lcd, "WiFi PUTUS", "Reconnect...", 1000);
      initWiFi();
    }
  }
  
  delay(500);
}

void matikanRelay() {
  digitalWrite(RELAY_PIN, HIGH); // Relay OFF (active LOW)
  Serial.println("Relay: OFF - Listrik Padam");
}

void nyalakanRelay() {
  digitalWrite(RELAY_PIN, LOW);  // Relay ON (active LOW)
  Serial.println("Relay: ON - Listrik Menyala");
}
```

#### File: `esp8266/config.h`

```cpp
#ifndef CONFIG_H
#define CONFIG_H

// ====== KONFIGURASI JARINGAN ======
const char* ssid = "NamaWiFiKost";        // Ganti dengan nama WiFi
const char* password = "PasswordWiFi123"; // Ganti dengan password WiFi

// ====== KONFIGURASI SERVER ======
const char* serverUrl = "http://192.168.1.100:5000";
const char* deviceId = "KMR01";

// ====== KONFIGURASI PIN ======
#define RELAY_PIN D3      // GPIO0 - Relay Control
#define SENSOR_PIN A0     // ADC   - Sensor ACS712

// ====== KONFIGURASI I2C LCD ======
#define LCD_ADDRESS 0x27  // Alamat I2C LCD
#define LCD_COLUMNS 16
#define LCD_ROWS    2

// ====== KONFIGURASI SENSOR ======
#define ACS712_SENSITIVITY 0.066  // 66 mV/A untuk ACS712 30A
#define ACS712_VREF        5.0    // Tegangan referensi ADC
#define ACS712_OFFSET      512    // Nilai ADC saat arus 0 (2.5V = 512)

// ====== KONFIGURASI DAYA ======
#define VOLTAGE_STANDARD   220.0  // Tegangan standar PLN
#define DAYA_MAKSIMAL      900.0  // Batas daya maksimal (Watt)

#endif
```

### 6.4.2 Contoh Kode Server (main.py)

```python
"""
SISTEM MONITORING LISTRIK KAMAR KOST
Server Python dengan Flask
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'data/database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Buat tabel-tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'admin',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kamar (
            id_kamar INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kamar TEXT NOT NULL,
            daya_maksimal REAL DEFAULT 900,
            status_relay TEXT DEFAULT 'ON',
            status_koneksi TEXT DEFAULT 'OFFLINE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_realtime (
            id_data INTEGER PRIMARY KEY AUTOINCREMENT,
            id_kamar INTEGER,
            tegangan REAL,
            arus REAL,
            daya REAL,
            energy_kwh REAL,
            status_relay TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_kamar) REFERENCES kamar(id_kamar)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_histori (
            id_histori INTEGER PRIMARY KEY AUTOINCREMENT,
            id_kamar INTEGER,
            tegangan REAL,
            arus REAL,
            daya REAL,
            energy_kwh REAL,
            status_relay TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_kamar) REFERENCES kamar(id_kamar)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batas_daya_log (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            id_kamar INTEGER,
            daya_saat REAL,
            daya_maksimal REAL,
            aksi TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_kamar) REFERENCES kamar(id_kamar)
        )
    ''')
    
    # Buat user default jika belum ada
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ('admin', 'admin123', 'admin@kost.com', 'admin')
        )
    
    # Buat data kamar default
    cursor.execute("SELECT * FROM kamar")
    if not cursor.fetchall():
        for i in range(1, 6):
            cursor.execute(
                "INSERT INTO kamar (nama_kamar, daya_maksimal) VALUES (?, ?)",
                (f'Kamar {i}', 900.0)
            )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# ========== ENDPOINT UNTUK PERANGKAT IoT ==========

@app.route('/api/device/data', methods=['POST'])
def terima_data_device():
    """Menerima data sensor dari perangkat ESP8266"""
    data = request.json
    
    id_kamar = data.get('id_kamar')
    tegangan = data.get('tegangan', 220.0)
    arus = data.get('arus', 0.0)
    daya = data.get('daya', 0.0)
    energy_kwh = data.get('energy_kwh', 0.0)
    status_relay = data.get('status_relay', 'ON')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Simpan ke realtime
    cursor.execute('''
        INSERT INTO data_realtime (id_kamar, tegangan, arus, daya, energy_kwh, status_relay)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_kamar, tegangan, arus, daya, energy_kwh, status_relay))
    
    # Simpan ke histori
    cursor.execute('''
        INSERT INTO data_histori (id_kamar, tegangan, arus, daya, energy_kwh, status_relay)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_kamar, tegangan, arus, daya, energy_kwh, status_relay))
    
    # Update status koneksi kamar
    cursor.execute('''
        UPDATE kamar SET status_koneksi = 'ONLINE', updated_at = CURRENT_TIMESTAMP
        WHERE id_kamar = ?
    ''', (id_kamar,))
    
    conn.commit()
    
    # Cek batas daya
    cursor.execute("SELECT daya_maksimal FROM kamar WHERE id_kamar = ?", (id_kamar,))
    kamar = cursor.fetchone()
    
    command = "NONE"
    alasan = ""
    
    if kamar and daya > kamar['daya_maksimal'] and status_relay == "ON":
        command = "OFF"
        alasan = "OVER_LIMIT"
        
        # Catat log pelanggaran
        cursor.execute('''
            INSERT INTO batas_daya_log (id_kamar, daya_saat, daya_maksimal, aksi)
            VALUES (?, ?, ?, ?)
        ''', (id_kamar, daya, kamar['daya_maksimal'], 'PADAM_OTOMATIS'))
        
        # Update status relay
        cursor.execute('''
            UPDATE kamar SET status_relay = 'OFF', updated_at = CURRENT_TIMESTAMP
            WHERE id_kamar = ?
        ''', (id_kamar,))
        
        conn.commit()
    
    conn.close()
    
    return jsonify({
        'status': 'success',
        'command': command,
        'alasan': alasan
    })

@app.route('/api/device/command/<int:id_kamar>', methods=['GET'])
def get_command(id_kamar):
    """Endpoint untuk perangkat mengambil perintah"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status_relay FROM kamar WHERE id_kamar = ?", (id_kamar,))
    kamar = cursor.fetchone()
    conn.close()
    
    if kamar:
        return jsonify({
            'command': kamar['status_relay'],
            'timestamp': datetime.now().isoformat()
        })
    
    return jsonify({'command': 'NONE'})

# ========== ENDPOINT UNTUK APLIKASI WEB ==========

@app.route('/api/kamar', methods=['GET'])
def get_kamar():
    """Mendapatkan daftar semua kamar"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kamar ORDER BY id_kamar")
    kamar = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(kamar)

@app.route('/api/kamar/<int:id_kamar>', methods=['GET'])
def detail_kamar(id_kamar):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kamar WHERE id_kamar = ?", (id_kamar,))
    kamar = cursor.fetchone()
    conn.close()
    
    if kamar:
        return jsonify(dict(kamar))
    return jsonify({'error': 'Kamar tidak ditemukan'}), 404

@app.route('/api/kamar/<int:id_kamar>/data', methods=['GET'])
def get_data_realtime(id_kamar):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM data_realtime 
        WHERE id_kamar = ? 
        ORDER BY id_data DESC LIMIT 1
    ''', (id_kamar,))
    data = cursor.fetchone()
    conn.close()
    
    if data:
        return jsonify(dict(data))
    return jsonify({'daya': 0, 'arus': 0, 'tegangan': 220})

@app.route('/api/kamar/<int:id_kamar>/histori', methods=['GET'])
def get_histori(id_kamar):
    start = request.args.get('start', '2026-01-01')
    end = request.args.get('end', '2026-12-31')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM data_histori 
        WHERE id_kamar = ? AND DATE(timestamp) BETWEEN ? AND ?
        ORDER BY timestamp DESC LIMIT 100
    ''', (id_kamar, start, end))
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/api/kamar/<int:id_kamar>/control', methods=['PUT'])
def kontrol_relay(id_kamar):
    data = request.json
    command = data.get('command', 'ON')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE kamar SET status_relay = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id_kamar = ?
    ''', (command, id_kamar))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'relay': command,
        'message': f'Relay {command} untuk kamar {id_kamar}'
    })

@app.route('/api/kamar/<int:id_kamar>/rata-rata', methods=['GET'])
def rata_rata_harian(id_kamar):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(daya) as rata_daya, 
               SUM(energy_kwh) as total_energi,
               DATE(timestamp) as tgl
        FROM data_histori 
        WHERE id_kamar = ? 
        GROUP BY DATE(timestamp)
        ORDER BY tgl DESC LIMIT 1
    ''', (id_kamar,))
    data = cursor.fetchone()
    conn.close()
    
    if data and data['rata_daya']:
        return jsonify({
            'rata_rata_daya': round(data['rata_daya'], 2),
            'total_energi_hari': round(data['total_energi'], 2),
            'tanggal': data['tgl']
        })
    return jsonify({'rata_rata_daya': 0, 'total_energi_hari': 0})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'status': 'success',
            'token': f'token_{username}_{datetime.now().timestamp()}',
            'user': {
                'id': user['id_user'],
                'username': user['username'],
                'role': user['role']
            }
        })
    
    return jsonify({'status': 'error', 'message': 'Login gagal'}), 401

if __name__ == '__main__':
    init_db()
    print("Server berjalan di http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 6.4.3 Contoh Skenario Lengkap

#### Skenario: Kamar 1 Melebihi Batas Daya

```
LANGKAH-LANGKAH:
=================

1. [FISIK] Kamar 1 menggunakan AC (800W) + Kulkas (150W) + Lampu (50W)
          Total daya = 1000W (melebihi batas 900W)

2. [ESP8266] Sensor ACS712 membaca arus tinggi:
          - Arus = 1000W / 220V = 4.55A
          - Daya dihitung = 1000W

3. [ESP8266] Cek daya > DAYA_MAKSIMAL (900W):
          - YA, daya melebihi batas!
          - Relay dipadamkan (OFF)
          - LCD menampilkan "PADAM - OVER LIMIT"

4. [ESP8266] Kirim data ke server:
          POST /api/device/data
          { id_kamar: "KMR01", daya: 1000, status_relay: "OFF" }

5. [SERVER] Terima data:
          - Simpan ke database
          - Catat log pelanggaran batas daya
          - Update status kamar menjadi "OFF"

6. [WEB] Dashboard menampilkan:
          - Kamar 1: Status "PADAM" (warna merah)
          - Daya terakhir: 1000W
          - Tombol ON tersedia untuk menyalakan kembali

7. [PEMILIK] Melihat notifikasi di Dashboard:
          - Kamar 1 padam karena overload
          - Pemilik menekan tombol ON

8. [SERVER] Menerima perintah ON:
          - Update status relay kamar menjadi "ON"

9. [ESP8266] Polling perintah:
          - GET /api/device/command/KMR01
          - Response: { command: "ON" }
          - Relay dinyalakan
          - LCD menampilkan "Kamar 1 - ON - 0W"

10. [SELESAI] Listrik Kamar 1 menyala kembali
```

### 6.4.4 Troubleshooting (Pemecahan Masalah)

| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| Wemos tidak menyala | Tidak ada power | Cek kabel USB dan charger |
| LCD tidak tampil | Kabel I2C terbalik | Periksa koneksi SDA/SCL |
| LCD tampil kotak-kotak | Alamat I2C salah | Scan alamat I2C dengan sketch |
| WiFi tidak konek | SSID/password salah | Cek konfigurasi di config.h |
| Data tidak terkirim | Server mati | Jalankan server python |
| Port COM tidak muncul | Driver CH340 belum installed | Install driver CH340 |
| Relay tidak aktif | Pin salah/koneksi longgar | Cek wiring relay |
| Sensor baca 0 terus | Sensor rusak/kabel putus | Cek dengan multimeter |

---

## Penutup

Dengan mengikuti tutorial di atas, Anda telah berhasil:

1. ✅ Merakit perangkat keras monitoring listrik
2. ✅ Mengupload program ke Wemos ESP8266
3. ✅ Menjalankan server Python
4. ✅ Membuka aplikasi web monitoring
5. ✅ Memahami contoh kode dan skenario penggunaan

Sistem Monitoring Listrik Kamar Kost ini siap digunakan untuk membantu pemilik kost dalam memantau dan mengontrol pemakaian listrik setiap kamar secara real-time.

---

**Selamat mencoba!**

*Dokumen ini disusun sebagai bagian dari dokumentasi proyek Sistem Monitoring & Kontrol Listrik Kamar Kost Berbasis IoT.*