# 🏠 Kost Monitor - Sistem Monitoring Listrik Kamar Kost

Sistem monitoring pemakaian listrik kamar kost berbasis **ESP8266/ESP32** dengan **server Flask** dan **web dashboard** real-time.

## 🎯 Fitur

- ✅ **Monitoring Real-Time** - Pantau daya, arus, dan energi setiap kamar
- ✅ **Kontrol Relay** - Nyalakan/matikan listrik kamar dari web
- ✅ **Proteksi Overload** - Relay mati otomatis jika daya melebihi batas
- ✅ **Riwayat Data** - Histori pemakaian listrik per kamar
- ✅ **Dark Mode** - Tema terang/gelap
- ✅ **Simulasi IoT** - Kirim data dummy untuk testing tanpa hardware
- ✅ **Multi-Perangkat** - Pantau banyak kamar sekaligus
- ✅ **Responsive** - Mobile & desktop friendly

## 📁 Struktur Proyek

```
kost_monitor/
├── arduino/
│   └── kost_monitor.ino        # Firmware ESP8266
├── server/
│   ├── app.py                  # Entry point server Flask
│   ├── requirements.txt        # Dependencies
│   └── app/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── entities.py     # Entity definitions
│       ├── application/
│       │   ├── __init__.py
│       │   └── services.py     # Business logic
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   └── repositories.py # Data storage (JSON)
│       └── presentation/
│           ├── __init__.py
│           └── routes.py       # REST API endpoints
├── web/
│   └── index.html              # Frontend SPA
├── document/
│   └── nama_project/           # Dokumentasi project
│       ├── 01_pengenalan_project.md
│       ├── 02_pengembangan_proses_bisnis.md
│       ├── 03_pengembangan_kerja_server.md
│       ├── 04_pengenalan_bagian_hardware.md
│       ├── 05_pengenalan_tampilan_antarmuka_aplikasi.md
│       └── 06_tutorial_penggunaan_project.md
└── README.md
```

## 🚀 Cara Menjalankan

### 1. Server Flask

```bash
# Install dependencies
cd server
pip install -r requirements.txt

# Jalankan server
python app.py
```

Server akan berjalan di `http://localhost:5000`.

### 2. Buka Web Dashboard

Buka browser dan akses: **http://localhost:5000**

### 3. Upload ke ESP8266 (Opsional)

Buka `arduino/kost_monitor.ino` di Arduino IDE, atur:
- `WIFI_SSID` dan `WIFI_PASS` dengan jaringan WiFi Anda
- `SERVER_URL` dengan alamat server (contoh: `http://192.168.1.10:5000`)

Upload ke board ESP8266/ESP32.

## 🔌 REST API Endpoints

| Method | Endpoint                        | Deskripsi                        |
|--------|---------------------------------|----------------------------------|
| GET    | `/api/health`                   | Health check server              |
| GET    | `/api/dashboard`                | Data dashboard real-time         |
| GET    | `/api/devices`                  | Daftar semua perangkat           |
| GET    | `/api/device/<id>`              | Detail perangkat spesifik        |
| POST   | `/api/device/data`              | Kirim data sensor (dari ESP)     |
| GET    | `/api/device/command/<id>`      | Ambil perintah relay (dari ESP)  |
| POST   | `/api/device/<id>/relay`        | Kontrol relay ON/OFF             |
| POST   | `/api/device/register`          | Daftarkan perangkat baru         |
| PUT    | `/api/device/<id>/batas-daya`   | Update batas daya                |
| GET    | `/api/device/<id>/history`      | Riwayat data sensor              |

## 🧪 Simulasi IoT (Tanpa Hardware)

1. Buka web dashboard
2. Klik **"Simulasi IoT"** di sidebar
3. Pilih perangkat, atur nilai arus/daya
4. Klik **"Kirim Data"**
5. Data akan muncul di dashboard real-time

## 🛠️ Tech Stack

- **Hardware:** ESP8266/ESP32, Sensor ACS712 (arus), Relay Module
- **Backend:** Python Flask (Clean Architecture)
- **Frontend:** HTML5, Tailwind CSS, Chart.js, Vanilla JS
- **Storage:** JSON file-based (data/devices.json, data/sensors.json)

## 📄 Lisensi

MIT License

---

Dibuat untuk kebutuhan monitoring listrik kamar kost secara real-time.