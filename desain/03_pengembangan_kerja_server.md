# BAB 3: Pengembangan Kerja Server

## 3.1 Penjelasan Server

Server adalah komponen inti dari sistem monitoring dan kontrol listrik kamar kost ini. Server berfungsi sebagai pusat data yang menerima, memproses, menyimpan, dan menyajikan data dari perangkat IoT (Wemos ESP8266) serta melayani permintaan dari aplikasi web.

### 3.1.1 Spesifikasi Teknis Server

| Komponen | Spesifikasi |
|----------|-------------|
| **Bahasa Pemrograman** | Python 3.x |
| **Framework Web** | Flask / FastAPI |
| **Database** | SQLite 3 |
| **Protokol Komunikasi** | HTTP (REST API) |
| **Format Data** | JSON |
| **Port Server** | 5000 (Flask default) |

### 3.1.2 Struktur REST API

Server menyediakan endpoint-endpoint REST API sebagai berikut:

#### A. Endpoint untuk Perangkat IoT

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| POST | `/api/device/data` | Menerima data sensor dari perangkat |
| GET | `/api/device/command/{id_kamar}` | Mengirim perintah ke perangkat (ON/OFF) |
| POST | `/api/device/register` | Mendaftarkan perangkat baru |

#### B. Endpoint untuk Aplikasi Web

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| POST | `/api/auth/login` | Login pengguna |
| POST | `/api/auth/logout` | Logout pengguna |
| GET | `/api/kamar` | Mendapatkan daftar semua kamar |
| GET | `/api/kamar/{id}` | Mendapatkan detail kamar tertentu |
| POST | `/api/kamar` | Menambah kamar baru |
| PUT | `/api/kamar/{id}` | Mengupdate data kamar |
| DELETE | `/api/kamar/{id}` | Menghapus kamar |
| GET | `/api/kamar/{id}/data` | Mendapatkan data real-time kamar |
| GET | `/api/kamar/{id}/histori` | Mendapatkan histori data kamar |
| PUT | `/api/kamar/{id}/control` | Mengontrol relay (ON/OFF) |
| PUT | `/api/kamar/{id}/batas` | Mengatur batas daya maksimal |
| GET | `/api/kamar/{id}/rata-rata` | Mendapatkan rata-rata pemakaian per hari |

#### C. Format Data JSON

**Contoh data yang dikirim perangkat ke server:**
```json
{
  "id_kamar": "KMR01",
  "tegangan": 220.5,
  "arus": 1.25,
  "daya": 275.6,
  "energy_kwh": 12.45,
  "status_relay": "ON",
  "timestamp": "2026-05-22 19:30:00"
}
```

**Contoh response server ke perangkat:**
```json
{
  "status": "success",
  "command": "OFF",
  "alasan": "OVER_LIMIT"
}
```

---

## 3.2 ERD Server (Entity Relationship Diagram)

### 3.2.1 Entitas dan Relasi

Berikut adalah Entity Relationship Diagram (ERD) untuk database server:

```
    +======================+          +==========================+
    ||      users         ||          ||       kamar            ||
    ||====================||          ||========================||
    || id_user     (PK)   ||          || id_kamar       (PK)    ||
    || username           ||          || nama_kamar             ||
    || password           ||          || daya_maksimal          ||
    || email              ||          || status_relay           ||
    || role               ||          || status_koneksi         ||
    || created_at         ||          || created_at             ||
    +======================+          || updated_at             ||
              |                       +==========================+
              |                                 |
              | 1                          1    |
              |                                 |
              |                                 |
              +-------(tidak relasi langsung)---+
                                    
                                    
    +========================+          +==========================+
    ||   data_realtime      ||          ||     data_histori       ||
    ||======================||          ||========================||
    || id_data      (PK)    ||          || id_histori     (PK)    ||
    || id_kamar     (FK)    ||----+----|| id_kamar      (FK)     ||
    || tegangan             ||    |    || tegangan                ||
    || arus                 ||    |    || arus                    ||
    || daya                 ||    |    || daya                    ||
    || energy_kwh           ||    |    || energy_kwh              ||
    || status_relay         ||    |    || status_relay            ||
    || timestamp            ||    |    || timestamp               ||
    +========================+    |    +==========================+
                                  |
                                  |
    +========================+    |
    ||   batas_daya_log     ||    |
    ||======================||    |
    || id_log        (PK)   ||    |
    || id_kamar      (FK)   ||----+
    || daya_saat           ||
    || daya_maksimal       ||
    || aksi                ||
    || timestamp            ||
    +========================+
```

### 3.2.2 Deskripsi Tabel

#### Tabel: `users`

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_user | INTEGER (PK) | Primary key, auto increment |
| username | VARCHAR(50) | Username untuk login |
| password | VARCHAR(255) | Password (hash) |
| email | VARCHAR(100) | Email pengguna |
| role | VARCHAR(20) | Role pengguna (admin) |
| created_at | DATETIME | Waktu pembuatan akun |

#### Tabel: `kamar`

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_kamar | INTEGER (PK) | Primary key, auto increment |
| nama_kamar | VARCHAR(50) | Nama kamar (misal: Kamar 1) |
| daya_maksimal | FLOAT | Batas daya maksimal dalam Watt |
| status_relay | VARCHAR(10) | Status relay (ON/OFF) |
| status_koneksi | VARCHAR(20) | Status koneksi perangkat |
| created_at | DATETIME | Waktu pembuatan data |
| updated_at | DATETIME | Waktu update terakhir |

#### Tabel: `data_realtime`

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_data | INTEGER (PK) | Primary key, auto increment |
| id_kamar | INTEGER (FK) | Foreign key ke tabel kamar |
| tegangan | FLOAT | Tegangan listrik (Volt) |
| arus | FLOAT | Arus listrik (Ampere) |
| daya | FLOAT | Daya listrik (Watt) |
| energy_kwh | FLOAT | Akumulasi energi (kWh) |
| status_relay | VARCHAR(10) | Status relay saat ini |
| timestamp | DATETIME | Waktu pencatatan data |

#### Tabel: `data_histori`

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_histori | INTEGER (PK) | Primary key, auto increment |
| id_kamar | INTEGER (FK) | Foreign key ke tabel kamar |
| tegangan | FLOAT | Tegangan listrik (Volt) |
| arus | FLOAT | Arus listrik (Ampere) |
| daya | FLOAT | Daya listrik (Watt) |
| energy_kwh | FLOAT | Akumulasi energi (kWh) |
| status_relay | VARCHAR(10) | Status relay saat itu |
| timestamp | DATETIME | Waktu pencatatan data |

#### Tabel: `batas_daya_log`

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_log | INTEGER (PK) | Primary key, auto increment |
| id_kamar | INTEGER (FK) | Foreign key ke tabel kamar |
| daya_saat | FLOAT | Daya saat terjadi pelanggaran |
| daya_maksimal | FLOAT | Batas daya yang ditetapkan |
| aksi | VARCHAR(50) | Aksi yang diambil (PADAM) |
| timestamp | DATETIME | Waktu kejadian |

### 3.2.3 Relasi Antar Tabel

```
Tabel users      --> Tidak memiliki relasi langsung dengan tabel lain
                       (digunakan untuk autentikasi)

Tabel kamar      --> 1 to Many --> data_realtime
                       (satu kamar memiliki banyak data real-time)
                  --> 1 to Many --> data_histori
                       (satu kamar memiliki banyak data histori)
                  --> 1 to Many --> batas_daya_log
                       (satu kamar memiliki banyak log batas daya)

Tabel data_realtime --> Data terbaru dari perangkat (hanya menyimpan
                         satu record terbaru per kamar atau riwayat singkat)

Tabel data_histori   --> Menyimpan data historis untuk analisis jangka panjang
                         (data dipindahkan dari real-time ke histori secara periodik)

Tabel batas_daya_log --> Mencatat setiap kejadian pelanggaran batas daya
```

---

## 3.3 DFD Level 0 (Data Flow Diagram)

### 3.3.1 Diagram Konteks (DFD Level 0)

```
                         +------------------------------------------+
                         |                                          |
                         |   SISTEM MONITORING & KONTROL LISTRIK    |
                         |           KAMAR KOST                     |
                         |                                          |
                         +--------------------+---------------------+
                                              |
              +-------------------------------v-------------------------------+
              |                                                                |
              |                    DATA FLOW DIAGRAM LEVEL 0                  |
              |                                                                |
              +----------------------------------------------------------------+
                                              |
     +-------------------------+              |              +-------------------------+
     |                         |              |              |                         |
     |    PEMILIK KOST         |              |              |    PERANGKAT IoT       |
     |    (Aktor Utama)        |              |              |    (ESP8266)           |
     |                         |              |              |                         |
     +-----------+-------------+              |              +------------+------------+
                 |                            |                           |
                 | (1) Request Login         |                           |
                 | (2) Response Token        |                           |
                 | (3) Request Data Kamar    |                           |
                 | (4) Response Data JSON    |                           |
                 | (5) Request Kontrol ON/OFF|                           |
                 | (6) Response Status       |                           |
                 | (7) Request Histori       |                           |
                 | (8) Response Histori JSON |                           |
                 | (9) Request Export        |                           |
                 | (10) File PDF/Excel       |                           |
                 |                           |                           |
                 |                           |    (A) Kirim Data Sensor |
                 |                           |    (B) Response Command  |
                 |                           |    (C) Register Device   |
                 |                           |    (D) Cek Koneksi       |
                 |                           |                           |
                 v                           v                           v
    +========================+     +===================+     +=====================+
    ||    APLIKASI WEB      ||     |                   |     |   PERANGKAT IoT    ||
    ||    (Browser)         ||     |   SERVER PYTHON   |     |   (ESP8266)        ||
    ||                      ||<--->|                   |<--->|                     ||
    ||   - HTML/CSS/JS      ||     |   - Flask/FastAPI |     |   - Wemos ESP8266   ||
    ||   - Tailwind CSS     ||     |   - SQLite DB     |     |   - Sensor Arus     ||
    ||   - Chart.js         ||     |   - REST API      |     |   - Relay Module    ||
    ||   - AJAX Fetch       ||     |   - Auth JWT      |     |   - LCD 16x2 I2C   ||
    +========================+     +-------------------+     +=====================+
```

### 3.3.2 Penjelasan Alur Data

| No | Alur Data | Dari | Ke | Keterangan |
|----|-----------|------|----|------------|
| 1 | Request Login | Pemilik Kost | Aplikasi Web | Input username & password |
| 2 | Response Token | Aplikasi Web | Pemilik Kost | Token autentikasi |
| 3 | Request Data | Aplikasi Web | Server | HTTP GET data kamar |
| 4 | Response Data | Server | Aplikasi Web | JSON data real-time |
| 5 | Request Kontrol | Aplikasi Web | Server | HTTP PUT ON/OFF |
| 6 | Response Status | Server | Aplikasi Web | JSON status update |
| 7 | Request Histori | Aplikasi Web | Server | HTTP GET dengan filter |
| 8 | Response Histori | Server | Aplikasi Web | JSON data historis |
| 9 | Request Export | Aplikasi Web | Server | PDF/Excel |
| 10 | File Export | Server | Aplikasi Web | Download file |
| A | Kirim Data Sensor | Perangkat IoT | Server | HTTP POST data daya |
| B | Response Command | Server | Perangkat IoT | Perintah relay ON/OFF |
| C | Register Device | Perangkat IoT | Server | Registrasi ID kamar |
| D | Cek Koneksi | Perangkat IoT | Server | Heartbeat/keep-alive |

---

## 3.4 Sequence Diagram Device di Project

### 3.4.1 Sequence Diagram: Kirim Data Sensor

```
Perangkat IoT                    Server Python                   Database SQLite
     |                               |                               |
     |  1. Baca Sensor Arus          |                               |
     |  2. Hitung Daya (Watt)        |                               |
     |  3. Baca Tegangan             |                               |
     |                               |                               |
     |  4. POST /api/device/data     |                               |
     |  ============================>|                               |
     |     JSON: {                   |                               |
     |       id_kamar: "KMR01",      |                               |
     |       tegangan: 220.5,        |                               |
     |       arus: 1.25,             |                               |
     |       daya: 275.6,            |                               |
     |       energy_kwh: 12.45,      |                               |
     |       status_relay: "ON"      |                               |
     |     }                         |                               |
     |                               |                               |
     |                               |  5. INSERT INTO data_realtime|
     |                               |  ============================>|
     |                               |                               |
     |                               |  6. INSERT INTO data_histori |
     |                               |  ============================>|
     |                               |                               |
     |                               |  7. SELECT daya_maksimal     |
     |                               |     FROM kamar WHERE id_kamar|
     |                               |  ============================>|
     |                               |                               |
     |                               |  8. RETURN daya_maksimal     |
     |                               |  <============================|
     |                               |                               |
     |                               |  9. Cek: daya > daya_maksimal|
     |                               |                               |
     |  10. Response HTTP            |                               |
     |  <============================|                               |
     |     JSON: {                   |                               |
     |       status: "success",      |                               |
     |       command: "OFF",         |                               |
     |       alasan: "OVER_LIMIT"    |                               |
     |     }                         |                               |
     |                               |                               |
     |  11. Jika command == "OFF":   |                               |
     |  12. Matikan Relay            |                               |
     |  13. LCD Tampilkan "PADAM"    |                               |
     |                               |                               |
```

### 3.4.2 Sequence Diagram: Kontrol ON/OFF dari Web

```
Pemilik Kost            Aplikasi Web              Server Python         Database SQLite           Perangkat IoT
     |                       |                         |                      |                       |
     |  1. Klik Tombol       |                         |                      |                       |
     |     ON/OFF            |                         |                      |                       |
     |  =====================>                         |                      |                       |
     |                       |                         |                      |                       |
     |                       |  2. PUT /api/kamar/     |                      |                       |
     |                       |     {id}/control        |                      |                       |
     |                       |  ========================>                      |                       |
     |                       |     JSON: {             |                      |                       |
     |                       |       command: "OFF"    |                      |                       |
     |                       |     }                   |                      |                       |
     |                       |                         |                      |                       |
     |                       |                         |  3. UPDATE kamar    |                       |
     |                       |                         |     SET status_relay|                       |
     |                       |                         |  =====================>                       |
     |                       |                         |                      |                       |
     |                       |                         |  4. Simpan ke       |                       |
     |                       |                         |     batas_daya_log  |                       |
     |                       |                         |     (jika OFF)      |                       |
     |                       |                         |  =====================>                       |
     |                       |                         |                      |                       |
     |                       |                         |  5. Simpan perintah |                       |
     |                       |                         |     ke tabel        |                       |
     |                       |                         |     perintah_relay  |                       |
     |                       |                         |  =====================>                       |
     |                       |                         |                      |                       |
     |                       |  6. Response Status     |                      |                       |
     |                       |  <========================                      |                       |
     |                       |     JSON: {             |                      |                       |
     |                       |       status: "success",|                      |                       |
     |                       |       relay: "OFF"      |                      |                       |
     |                       |     }                   |                      |                       |
     |                       |                         |                      |                       |
     |  7. Tampilkan         |                         |                      |                       |
     |     Status Baru       |                         |                      |                       |
     |  <=====================                         |                      |                       |
     |                       |                         |                      |                       |
     |                       |                         |  8. Perangkat IoT    |                       |
     |                       |                         |     melakukan polling|                       |
     |                       |                         |     GET /api/device/ |                       |
     |                       |                         |     command/{id}     |                       |
     |                       |                         |  <--------------------+                       |
     |                       |                         |                      |                       |
     |                       |                         |  9. Response: OFF    |                       |
     |                       |                         |  -------------------->                       |
     |                       |                         |                      |                       |
     |                       |                         |                      |  10. Matikan Relay    |
     |                       |                         |                      |  11. LCD: "PADAM"    |
```

### 3.4.3 Sequence Diagram: Registrasi Perangkat Baru

```
Perangkat IoT                    Server Python                   Database SQLite
     |                               |                               |
     |  1. POST /api/device/register |                               |
     |  ============================>|                               |
     |     JSON: {                   |                               |
     |       id_kamar: "KMR05",      |                               |
     |       mac_address: "AA:BB:.." |                               |
     |       nama: "Kamar 5"         |                               |
     |     }                         |                               |
     |                               |                               |
     |                               |  2. INSERT INTO kamar        |
     |                               |     (nama_kamar, daya_maks,  |
     |                               |      status_relay,           |
     |                               |      status_koneksi)         |
     |                               |  ============================>|
     |                               |                               |
     |                               |  3. Return id_kamar baru     |
     |                               |  <============================|
     |                               |                               |
     |  4. Response HTTP 201         |                               |
     |  <============================|                               |
     |     JSON: {                   |                               |
     |       status: "registered",   |                               |
     |       id_kamar: 5,            |                               |
     |       server_time: "..."      |                               |
     |     }                         |                               |
     |                               |                               |
```

---

## 3.5 Struktur Arsitektur (Clean Architecture) Server

### 3.5.1 Diagram Clean Architecture Server

```
    +-----------------------------------------------------------------------+
    |                        PRESENTATION LAYER                              |
    |  (Routing, HTTP Request/Response, Serialization)                       |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                      routes.py / api.py                          | |
    |  |  - /api/device/*   (Endpoint untuk perangkat IoT)               | |
    |  |  - /api/kamar/*    (Endpoint untuk aplikasi web)                | |
    |  |  - /api/auth/*     (Endpoint untuk autentikasi)                 | |
    |  +------------------------------------------------------------------+ |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                     serializers.py / schema.py                   | |
    |  |  - DeviceDataSchema (Validasi data dari perangkat)               | |
    |  |  - KamarSchema      (Validasi data kamar)                       | |
    |  |  - AuthSchema       (Validasi login)                           | |
    |  +------------------------------------------------------------------+ |
    +------------------------------------------------------------------------+
                                  |   berkomunikasi via
                                  v
    +------------------------------------------------------------------------+
    |                       APPLICATION / USE CASE LAYER                     |
    |  (Business Logic, Orchestration)                                       |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                    use_cases.py / service.py                    | |
    |  |                                                                 | |
    |  |  DeviceUseCase:                                                  | |
    |  |  - proses_data_sensor(data) -> Response                         | |
    |  |  - cek_batas_daya(id_kamar, daya) -> Boolean                    | |
    |  |  - kirim_perintah(id_kamar, command) -> Boolean                 | |
    |  |                                                                 | |
    |  |  KamarUseCase:                                                   | |
    |  |  - daftar_kamar() -> List[Kamar]                                | |
    |  |  - detail_kamar(id_kamar) -> Kamar                              | |
    |  |  - tambah_kamar(data) -> Kamar                                  | |
    |  |  - hapus_kamar(id_kamar) -> Boolean                             | |
    |  |  - kontrol_relay(id_kamar, command) -> Boolean                  | |
    |  |  - update_batas_daya(id_kamar, daya) -> Boolean                 | |
    |  |                                                                 | |
    |  |  AuthUseCase:                                                    | |
    |  |  - login(username, password) -> Token                            | |
    |  |  - verifikasi_token(token) -> Boolean                           | |
    |  |                                                                 | |
    |  |  HistoriUseCase:                                                 | |
    |  |  - get_histori(id_kamar, start_date, end_date) -> List[Data]    | |
    |  |  - rata_rata_harian(id_kamar) -> Float                          | |
    |  |  - export_pdf(id_kamar, start_date, end_date) -> File           | |
    |  |  - export_excel(id_kamar, start_date, end_date) -> File         | |
    |  +------------------------------------------------------------------+ |
    +------------------------------------------------------------------------+
                                  |   berkomunikasi via
                                  v
    +------------------------------------------------------------------------+
    |                       DOMAIN / ENTITY LAYER                            |
    |  (Enterprise Business Rules, Core Entities)                            |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                    models.py / domain.py                        | |
    |  |                                                                 | |
    |  |  @dataclass class Kamar:                                        | |
    |  |      id_kamar: int                                              | |
    |  |      nama_kamar: str                                            | |
    |  |      daya_maksimal: float                                       | |
    |  |      status_relay: str                                          | |
    |  |      status_koneksi: str                                        | |
    |  |                                                                 | |
    |  |  @dataclass class DataSensor:                                   | |
    |  |      id_kamar: int                                              | |
    |  |      tegangan: float                                            | |
    |  |      arus: float                                                | |
    |  |      daya: float                                                | |
    |  |      energy_kwh: float                                          | |
    |  |      status_relay: str                                          | |
    |  |      timestamp: datetime                                        | |
    |  |                                                                 | |
    |  |  @dataclass class User:                                         | |
    |  |      id_user: int                                               | |
    |  |      username: str                                              | |
    |  |      password_hash: str                                         | |
    |  |      email: str                                                 | |
    |  |      role: str                                                  | |
    |  |                                                                 | |
    |  |  enum StatusRelay: ON, OFF                                      | |
    |  |  enum StatusKoneksi: TERHUBUNG, TERPUTUS                        | |
    |  +------------------------------------------------------------------+ |
    +------------------------------------------------------------------------+
                                  |   berkomunikasi via
                                  v
    +------------------------------------------------------------------------+
    |                       INFRASTRUCTURE / REPOSITORY LAYER                |
    |  (Database, External Services, Framework implementations)             |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                    repository.py / database.py                  | |
    |  |                                                                 | |
    |  |  KamarRepository:                                               | |
    |  |  - get_all() -> List[KamarDict]                                 | |
    |  |  - get_by_id(id_kamar) -> KamarDict                             | |
    |  |  - create(data) -> int                                          | |
    |  |  - update(id_kamar, data) -> bool                               | |
    |  |  - delete(id_kamar) -> bool                                     | |
    |  |                                                                 | |
    |  |  DataSensorRepository:                                          | |
    |  |  - save_realtime(data) -> int                                   | |
    |  |  - save_histori(data) -> int                                    | |
    |  |  - get_histori(id_kamar, start, end) -> List[Dict]             | |
    |  |  - get_realtime(id_kamar) -> Dict                               | |
    |  |                                                                 | |
    |  |  UserRepository:                                                | |
    |  |  - get_by_username(username) -> UserDict                        | |
    |  |  - create(data) -> int                                          | |
    |  |                                                                 | |
    |  |  BatasDayaLogRepository:                                        | |
    |  |  - create(data) -> int                                          | |
    |  |  - get_by_kamar(id_kamar) -> List[Dict]                        | |
    |  +------------------------------------------------------------------+ |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                    database.py / db.py                          | |
    |  |                                                                 | |
    |  |  - init_db() -> void  (Membuat tabel-tabel)                    | |
    |  |  - get_connection() -> sqlite3.Connection                      | |
    |  |  - migrate() -> void  (Skema migrasi database)                 | |
    |  +------------------------------------------------------------------+ |
    |                                                                        |
    |  +------------------------------------------------------------------+ |
    |  |                    config.py / settings.py                      | |
    |  |                                                                 | |
    |  |  - SECRET_KEY: str                                              | |
    |  |  - DATABASE_PATH: str                                           | |
    |  |  - JWT_EXPIRATION: int (menit)                                  | |
    |  |  - MAX_ROOMS: int = 20                                          | |
    |  +------------------------------------------------------------------+ |
    +------------------------------------------------------------------------+
```

### 3.5.2 Penjelasan Struktur Clean Architecture

Clean Architecture digunakan untuk memisahkan kode server menjadi beberapa lapisan (layers) yang memiliki tanggung jawab berbeda. Berikut penjelasan setiap lapisan:

#### A. Presentation Layer (Layers Presentasi)
- **routes.py**: Berisi definisi endpoint REST API dan routing HTTP
- **serializers.py**: Mengubah data dari/ke format JSON, validasi input
- **Tujuan**: Menangani komunikasi HTTP dengan client (web & perangkat IoT)

#### B. Application / Use Case Layer (Layers Aplikasi)
- **use_cases.py**: Berisi logika bisnis aplikasi
- **service.py**: Orchestrasi alur kerja (workflow)
- **Tujuan**: Mengatur alur eksekusi bisnis tanpa bergantung pada framework atau database

#### C. Domain / Entity Layer (Layers Domain)
- **models.py**: Definisi entitas inti sistem
- **Tujuan**: Representasi data murni tanpa ketergantungan pada infrastruktur

#### D. Infrastructure / Repository Layer (Layers Infrastruktur)
- **repository.py**: Implementasi akses data (SQLite queries)
- **database.py**: Koneksi dan inisialisasi database
- **config.py**: Konfigurasi aplikasi
- **Tujuan**: Menangani detail teknis seperti database dan konfigurasi

### 3.5.3 Diagram Dependency Rule

```
    +---------------------------+
    |   Presentation Layer     |     (Bergantung ke Use Case Layer)
    +------------+--------------+
                 |  Memanggil
                 v
    +---------------------------+
    |   Application Layer      |     (Bergantung ke Domain Layer)
    +------------+--------------+
                 |  Menggunakan
                 v
    +---------------------------+
    |   Domain Layer           |     (Layer paling dalam, TIDAK bergantung)
    +------------+--------------+
                 |  Diimplementasikan oleh
                 v
    +---------------------------+
    | Infrastructure Layer     |     (Mengimplementasikan interface domain)
    +---------------------------+
```

**Aturan Dependency:**
- Layer luar bergantung pada layer dalam
- Layer dalam TIDAK boleh bergantung pada layer luar
- Domain Layer adalah yang paling inti, tidak bergantung pada apa pun
- Infrastructure Layer mengimplementasikan kontrak yang didefinisikan di Domain Layer

### 3.5.4 Struktur Folder Server

```
server/
    |
    +-- app/
    |   +-- __init__.py
    |   +-- config.py                # Konfigurasi aplikasi
    |   +--
    |   +-- domain/                   # Domain / Entity Layer
    |   |   +-- __init__.py
    |   |   +-- models.py           # Definisi entity (Kamar, DataSensor, User)
    |   |   +-- enums.py            # Enum (StatusRelay, StatusKoneksi)
    |   |
    |   +-- application/             # Application / Use Case Layer
    |   |   +-- __init__.py
    |   |   +-- device_service.py   # Logika untuk perangkat IoT
    |   |   +-- kamar_service.py    # Logika untuk manajemen kamar
    |   |   +-- auth_service.py     # Logika autentikasi
    |   |   +-- histori_service.py  # Logika histori dan laporan
    |   |
    |   +-- infrastructure/          # Infrastructure Layer
    |   |   +-- __init__.py
    |   |   +-- database.py         # Koneksi dan inisialisasi DB
    |   |   +-- repository.py       # Implementasi query database
    |   |   +-- auth.py             # Implementasi JWT token
    |   |
    |   +-- presentation/            # Presentation Layer
    |       +-- __init__.py
    |       +-- routes.py           # Definisi endpoint REST API
    |       +-- serializers.py      # Validasi dan serialisasi data
    |       +-- middlewares.py      # Middleware (auth, logging)
    |
    +-- main.py                     # Entry point aplikasi
    +-- requirements.txt            # Dependensi Python
    +-- data/
        +-- database.db             # File database SQLite
```

---

> **Lanjut ke Bab 4: Pengenalan Bagian Hardware**