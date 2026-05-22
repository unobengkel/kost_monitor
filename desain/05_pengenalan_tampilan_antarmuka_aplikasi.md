# BAB 5: Pengenalan Tampilan Antarmuka Aplikasi

## 5.1 Pengenalan Aplikasi

Aplikasi web dari sistem monitoring dan kontrol listrik kamar kost ini adalah sebuah **Single Page Application (SPA)** yang dibangun menggunakan **HTML5** dan **Tailwind CSS** (framework CSS utility-first). Aplikasi ini berfungsi sebagai antarmuka bagi pemilik kost untuk memantau, mengontrol, dan menganalisis penggunaan listrik di setiap kamar kost secara real-time.

### 5.1.1 Spesifikasi Teknis Aplikasi

| Komponen | Spesifikasi |
|----------|-------------|
| **Arsitektur** | Single Page Application (SPA) |
| **HTML** | HTML5 |
| **CSS Framework** | Tailwind CSS (CDN) |
| **JavaScript** | Vanilla JS (ES6+) |
| **Chart** | Chart.js untuk grafik |
| **Komunikasi Server** | Fetch API (AJAX) |
| **Responsive** | Mendukung HP, Tablet, dan PC |
| **Tema** | Light & Dark mode |

### 5.1.2 Karakteristik Aplikasi

1. **SPA (Single Page Application)**: Semua halaman dimuat dalam satu file HTML. Navigasi antar halaman dilakukan tanpa reload halaman, menggunakan JavaScript untuk menampilkan/menyembunyikan konten.
2. **Responsive Design**: Layout menyesuaikan dengan ukuran layar perangkat (mobile-first).
3. **Real-time**: Data diperbarui secara otomatis menggunakan AJAX polling.
4. **Premium Look**: Desain modern dengan gradien, shadow, animasi halus.
5. **Dark & Light Theme**: Pengguna dapat memilih tema sesuai preferensi.

---

## 5.2 Fitur dari Aplikasi

### 5.2.1 Daftar Fitur Lengkap

| No | Fitur | Halaman | Deskripsi |
|----|-------|---------|-----------|
| 1 | Login Autentikasi | Login | Sistem login untuk mengamankan akses aplikasi |
| 2 | Dashboard Monitoring | Dashboard | Tampilan utama monitoring daya listrik semua kamar |
| 3 | Pemilihan Kamar | Dashboard | Dropdown/pilih kamar yang akan dipantau |
| 4 | Widget Daya Real-time | Dashboard | Menampilkan konsumsi daya listrik saat ini (Watt) |
| 5 | Widget Rata-rata | Dashboard | Menampilkan rata-rata pemakaian daya per hari (kWh) |
| 6 | Widget Status Kamar | Dashboard | Menampilkan status kamar (ON/OFF/PADAM) |
| 7 | Grafik Histori Harian | Dashboard | Grafik pemakaian listrik per jam (hari ini) |
| 8 | Tombol Kontrol | Dashboard | Tombol ON/OFF untuk menyalakan/mematikan listrik kamar |
| 9 | Filter Histori | Histori | Filter berdasarkan kamar dan rentang tanggal |
| 10 | Tabel Data Histori | Histori | Tabel detail data historis pemakaian listrik |
| 11 | Tombol Cari | Histori | Mencari data berdasarkan filter yang dipilih |
| 12 | Tombol Hapus | Histori | Menghapus data histori yang dipilih |
| 13 | Export PDF | Histori | Mengexport data histori ke file PDF |
| 14 | Export Excel | Histori | Mengexport data histori ke file Excel (CSV) |
| 15 | Pengaturan Tema | Pengaturan | Mengubah tema tampilan (Light/Dark) |
| 16 | Pengaturan Batas Daya | Pengaturan | Mengatur batas daya maksimal per kamar |
| 17 | Manajemen Kamar | Pengaturan | Menambah/menghapus kamar kost |
| 18 | Sidebar Navigasi | Semua Halaman | Menu navigasi untuk berpindah halaman |

---

## 5.3 Pengenalan Halaman dan Komponen di Aplikasi

### 5.3.1 Struktur Halaman Aplikasi

```
    +============================================================+
    ||                   APLIKASI WEB MONITORING                 ||
    ||                   LISTRIK KAMAR KOST                      ||
    +============================================================+
                                |
            +-------------------+-------------------+
            |                                       |
            v                                       v
    +===================+                 +===================+
    ||  HALAMAN LOGIN  ||                 ||  HALAMAN UTAMA  ||
    ||                 ||                 ||  (Setelah Login) ||
    ||  - Form Login   ||                 ||                  ||
    ||  - Logo App     ||                 ||  +----------+    ||
    ||  - Input User   ||                 ||  | SIDEBAR |    ||
    ||  - Input Pass   ||                 ||  +----------+    ||
    ||  - Tombol Login ||                 ||  | CONTENT  |    ||
    +===================+                 ||  | AREA     |    ||
                                          ||  +----------+    ||
                                          +===================+
                                                |
                    +---------------------------+---------------------------+
                    |                           |                           |
                    v                           v                           v
        +===================+       +===================+       +===================+
        ||   DASHBOARD     ||       ||    HISTORI      ||       ||   PENGATURAN     ||
        ||                 ||       ||                 ||       ||                  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||  | Pilih     | ||       ||  | Filter    |  ||       ||  | Pengaturan  |  ||
        ||  | Kamar     | ||       ||  | Kamar     |  ||       ||  | Tema        |  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||                 ||       ||                 ||       ||                  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||  | Widget    | ||       ||  | Tabel     |  ||       ||  | Pengaturan  |  ||
        ||  | Daya      | ||       ||  | Histori   |  ||       ||  | Batas Daya  |  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||                 ||       ||                 ||       ||                  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||  | Grafik    | ||       ||  | Tombol    |  ||       ||  | Manajemen   |  ||
        ||  | Chart     | ||       ||  | Export    |  ||       ||  | Kamar       |  ||
        ||  +-----------+ ||       ||  +-----------+  ||       ||  +------------+  ||
        ||                 ||       ||                 ||       ||                  ||
        ||  +-----------+ ||       +===================+       +===================+
        ||  | Tombol    | ||
        ||  | ON/OFF    | ||
        ||  +-----------+ ||
        +===================+
```

### 5.3.2 Komponen Sidebar

```
    +------------------------------------------+
    |  SIDEBAR NAVIGASI                        |
    |                                          |
    |  +-------------------------------------+ |
    |  | [LOGO APLIKASI]                     | |
    |  | Sistem Monitoring Listrik Kost      | |
    |  +-------------------------------------+ |
    |                                          |
    |  +-------------------------------------+ |
    |  | NAVIGASI MENU:                      | |
    |  |                                     | |
    |  |   [I] Dashboard     <-- Aktif       | |
    |  |   [I] Histori                       | |
    |  |   [I] Pengaturan                    | |
    |  |   [I] Simulasi IoT   <-- Hide/Show  | |
    |  |                                     | |
    |  +-------------------------------------+ |
    |                                          |
    |  +-------------------------------------+ |
    |  | INFO PENGGUNA:                      | |
    |  |   [Avatar] Nama Pengguna            | |
    |  |            role: Admin              | |
    |  +-------------------------------------+ |
    |                                          |
    |  +-------------------------------------+ |
    |  | [Tombol Logout]                     | |
    |  +-------------------------------------+ |
    +------------------------------------------+
```

### 5.3.3 Komponen Halaman Dashboard

```
    +============================================================+
    ||  HALAMAN DASHBOARD                                        ||
    ||  "Pantau dan kontrol pemakaian listrik kamar kost Anda"  ||
    +============================================================+
    
    +------------------------------------------------------------+
    |  SELECTOR KAMAR                                           |
    |  +---------------------+   +---------------------+        |
    |  | Pilih Kamar: [v]   |   | Status: ONLINE      |        |
    |  | Kamar 1 (default)  |   | Update: 10 detik    |        |
    |  +---------------------+   +---------------------+        |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  WIDGET DASHBOARD (4 Kolom Grid)                         |
    |                                                           |
    |  +----------+  +----------+  +----------+  +----------+  |
    |  | DAYA     |  | RATA2    |  | ENERGI   |  | STATUS   |  |
    |  | SEKARANG |  | PER HARI |  | BULAN INI|  | KAMAR    |  |
    |  |          |  |          |  |          |  |          |  |
    |  | 350 Watt |  | 2.4 kWh  |  | 72 kWh   |  | [ON]     |  |
    |  |          |  |          |  |          |  | AKTIF    |  |
    |  +----------+  +----------+  +----------+  +----------+  |
    |                                                           |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  GRAFIK HISTORI HARI INI (PER JAM)                       |
    |                                                           |
    |   Daya (Watt)                                             |
    |     500 |    *                                            |
    |     400 |  * * *   *                                     |
    |     300 | * * * * * * *  *                               |
    |     200 | * * * * * * * * * * * *                       |
    |     100 | * * * * * * * * * * * * *                     |
    |       0 +----------------------------------------       |
    |         00 01 02 03 04 05 06 07 08 09 10 11 12 ... 23  |
    |                     Jam ke-                              |
    |                                                           |
    |  [Chart.js - Line Chart]                                  |
    |                                                           |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  KONTROL KAMAR                                           |
    |                                                           |
    |  +---------------------+   +---------------------+        |
    |  | [ON]  Nyalakan      |   | [OFF] Matikan       |        |
    |  |      Listrik        |   |      Listrik        |        |
    |  +---------------------+   +---------------------+        |
    |                                                           |
    |  Status Saat Ini: RELAY ON - Listrik Menyala            |
    |                                                           |
    +------------------------------------------------------------+
```

### 5.3.4 Komponen Halaman Histori

```
    +============================================================+
    ||  HALAMAN HISTORI                                         ||
    ||  "Lihat dan export data historis pemakaian listrik"     ||
    +============================================================+
    
    +------------------------------------------------------------+
    |  FILTER HISTORI                                           |
    |                                                           |
    |  Pilih Kamar: [v Kamar 1   ]                             |
    |  Tanggal Mulai: [01/05/2026]                             |
    |  Tanggal Akhir: [22/05/2026]                              |
    |                                                           |
    |  [Cari Data]  [Hapus Data]  [Export PDF]  [Export Excel] |
    |                                                           |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  TABEL DATA HISTORI                                       |
    |                                                           |
    |  +----+----------+-------+------+-------+----------+---+ |
    |  | No | Waktu    | Teg   | Arus | Daya  | Energi   |S  | |
    |  +----+----------+-------+------+-------+----------+---+ |
    |  | 1  |22/05 08:0| 220V  | 1.2A | 264W  | 1.25 kWh |ON | |
    |  | 2  |22/05 09:0| 221V  | 1.5A | 331W  | 1.58 kWh |ON | |
    |  | 3  |22/05 10:0| 219V  | 2.1A | 460W  | 2.10 kWh |ON | |
    |  | 4  |22/05 11:0| 220V  | 0.8A | 176W  | 0.85 kWh |ON | |
    |  | 5  |22/05 12:0| 220V  | 1.8A | 396W  | 1.90 kWh |ON | |
    |  | ...| ...      | ...   | ...  | ...   | ...      |.. | |
    |  +----+----------+-------+------+-------+----------+---+ |
    |                                                           |
    |  Halaman: [1] 2 3 ... [10]  [Prev] [Next]               |
    |  Total Data: 240 record                                  |
    |                                                           |
    +------------------------------------------------------------+
```

### 5.3.5 Komponen Halaman Pengaturan

```
    +============================================================+
    ||  HALAMAN PENGATURAN                                      ||
    ||  "Atur konfigurasi sistem monitoring listrik kost"      ||
    +============================================================+
    
    +------------------------------------------------------------+
    |  PENGATURAN TEMA                                          |
    |                                                           |
    |  Tema Tampilan:                                           |
    |  +----------+  +----------+                               |
    |  | [TERANG] |  | [GELAP]  |                               |
    |  |  Light   |  |  Dark    |                               |
    |  |   Mode   |  |   Mode   |                               |
    |  +----------+  +----------+                               |
    |                                                           |
    |  Tema Saat Ini: Light Mode                               |
    |                                                           |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  PENGATURAN BATAS DAYA                                    |
    |                                                           |
    |  Pilih Kamar: [v Kamar 1   ]                             |
    |                                                           |
    |  Batas Daya Maksimal:                                     |
    |  [==========o===========] 900 Watt                       |
    |  0 Watt                   2000 Watt                      |
    |                                                           |
    |  [Simpan Pengaturan]                                     |
    |                                                           |
    +------------------------------------------------------------+
    
    +------------------------------------------------------------+
    |  MANAJEMEN KAMAR                                          |
    |                                                           |
    |  Daftar Kamar:                                            |
    |  +----+------------+----------+--------+--------+------+ |
    |  | No | Nama Kamar | Daya Max | Status | Device | Aksi | |
    |  +----+------------+----------+--------+--------+------+ |
    |  | 1  | Kamar 1    | 900 Watt | Aktif  | Online | Hps | |
    |  | 2  | Kamar 2    | 900 Watt | Aktif  | Online | Hps | |
    |  | 3  | Kamar 3    | 900 Watt | Aktif  | Offline| Hps | |
    |  | 4  | Kamar 4    | 900 Watt | Aktif  | Online | Hps | |
    |  | 5  | Kamar 5    | 900 Watt | Aktif  | Online | Hps | |
    |  +----+------------+----------+--------+--------+------+ |
    |                                                           |
    |  +-----------------------------------------------------+ |
    |  | Tambah Kamar Baru:                                   | |
    |  | Nama Kamar : [                    ]                  | |
    |  | Daya Maks  : [                    ] Watt            | |
    |  | [Tambah Kamar]                                      | |
    |  +-----------------------------------------------------+ |
    |                                                           |
    +------------------------------------------------------------+
```

### 5.3.6 Komponen Modal Simulasi IoT

```
    +============================================================+
    ||  MODAL SIMULASI IoT (Hide/Show dari Sidebar)            ||
    +============================================================+
    
    +------------------------------------------------------------+
    |  [X] Close                                                 |
    |                                                           |
    |  SIMULASI DATA PERANGKAT IOT                             |
    |  "Simulasikan data dari perangkat Wemos ESP8266"         |
    |                                                           |
    +------------------------------------------------------------+
    |  KONFIGURASI PERANGKAT:                                   |
    |  ID Kamar    : [Kamar 1             ]                    |
    |  Status Relay: [ON (Hijau)] [OFF (Merah)]                |
    +------------------------------------------------------------+
    |  DATA SENSOR:                                             |
    |  Tegangan (V) : [=========o=======] 220.5 V             |
    |  Arus (A)     : [=====o===========] 1.25 A              |
    |  Daya (W)     : (Otomatis dari V x A) 275.6 W           |
    |  Energi (kWh) : [===========o=====] 12.45 kWh           |
    +------------------------------------------------------------+
    |  INFO KONEKSI:                                            |
    |  WiFi    : [TERHUBUNG] SSID: WiFiKost                    |
    |  Server  : [TERHUBUNG] IP: 192.168.1.100:5000            |
    |  LCD     : Menampilkan "Kamar 1 - 275W - ON"            |
    +------------------------------------------------------------+
    |  TOMBOL AKSI:                                             |
    |  [Kirim Data ke Server]  [Simulasi Overload]             |
    |  [Reset Energi]         [Simulasi WiFi Putus]           |
    +------------------------------------------------------------+
    |  LOG AKTIVITAS:                                           |
    |  [22/05 20:15:03] Data terkirim - 275.6W - Relay ON     |
    |  [22/05 20:15:02] Data terkirim - 268.3W - Relay ON     |
    |  [22/05 20:15:01] Data terkirim - 272.1W - Relay ON     |
    |  [22/05 20:15:00] Kirim data sensor ke server           |
    +------------------------------------------------------------+
```

---

## 5.4 Penjelasan per Halaman Aplikasi

### 5.4.1 Halaman Login

**Fungsi:** Sebagai gerbang keamanan aplikasi. Hanya pengguna yang terdaftar yang dapat mengakses sistem.

**Komponen:**
- Logo dan nama aplikasi
- Form input username
- Form input password (type=password)
- Tombol "Masuk / Login"
- Link "Lupa Password" (jika ada)

**Alur:**
1. Pengguna membuka aplikasi → diarahkan ke halaman login
2. Mengisi username dan password
3. Klik tombol login
4. Sistem memverifikasi ke server
5. Jika berhasil → masuk ke Dashboard
6. Jika gagal → tampilkan pesan error

### 5.4.2 Halaman Dashboard

**Fungsi:** Halaman utama untuk memantau dan mengontrol listrik kamar kost secara real-time.

**Komponen Utama:**
- **Selector Kamar**: Dropdown untuk memilih kamar yang akan dipantau
- **Widget Daya Sekarang**: Menampilkan konsumsi daya saat ini (Watt)
- **Widget Rata-rata Per Hari**: Menampilkan rata-rata pemakaian per hari (kWh)
- **Widget Energi Bulan Ini**: Menampilkan total energi bulan ini (kWh)
- **Widget Status Kamar**: Menampilkan status relay (ON/OFF/PADAM) dengan indikator warna
- **Grafik Histori**: Line chart pemakaian listrik per jam untuk hari ini
- **Tombol Kontrol**: Tombol ON dan OFF untuk mengontrol relay kamar

**Fungsi Fitur:**
| Fitur | Cara Kerja |
|-------|------------|
| Pemilihan Kamar | Dropdown mengubah data semua widget sesuai kamar terpilih |
| Update Real-time | Data diperbarui setiap 10 detik via AJAX |
| Grafik Chart | Menggunakan Chart.js, update setiap jam |
| Tombol ON/OFF | Mengirim perintah ke server, server meneruskan ke perangkat IoT |

### 5.4.3 Halaman Histori

**Fungsi:** Menampilkan data historis pemakaian listrik yang dapat difilter dan diexport.

**Komponen Utama:**
- **Filter Pencarian**: Dropdown kamar, input tanggal mulai & akhir
- **Tabel Data**: Menampilkan data historis dalam bentuk tabel
- **Tombol Aksi**: Cari, Hapus, Export PDF, Export Excel
- **Pagination**: Navigasi halaman tabel

**Fungsi Fitur:**
| Fitur | Cara Kerja |
|-------|------------|
| Filter Kamar | Memfilter data berdasarkan kamar tertentu |
| Filter Tanggal | Rentang tanggal start dan end |
| Tombol Cari | Menjalankan pencarian berdasarkan filter |
| Tombol Hapus | Menghapus data (dengan konfirmasi) |
| Export PDF | Generate file PDF dari data yang difilter |
| Export Excel | Generate file CSV/Excel dari data yang difilter |

### 5.4.4 Halaman Pengaturan

**Fungsi:** Mengatur konfigurasi sistem.

**Komponen Utama:**
- **Pengaturan Tema**: Tombol toggle Light/Dark mode
- **Pengaturan Batas Daya**: Slider/input untuk mengatur batas daya maksimal per kamar
- **Manajemen Kamar**: Daftar kamar + form tambah kamar baru

---

## 5.5 Cara Penggunaan

### 5.5.1 Panduan Cepat

| Langkah | Aksi | Keterangan |
|---------|------|------------|
| 1 | Buka Aplikasi | Akses URL aplikasi web |
| 2 | Login | Masukkan username dan password |
| 3 | Pilih Dashboard | Lihat monitoring real-time |
| 4 | Pilih Kamar | Pilih kamar dari dropdown |
| 5 | Pantau Data | Lihat widget daya, rata-rata, grafik |
| 6 | Kontrol Kamar | Tekan ON/OFF untuk mengontrol listrik |
| 7 | Lihat Histori | Buka halaman histori untuk data lampau |
| 8 | Export Data | Gunakan tombol export PDF/Excel |
| 9 | Atur Pengaturan | Sesuaikan tema dan batas daya |
| 10 | Logout | Keluar dari aplikasi |

### 5.5.2 Skenario Penggunaan

**Skenario 1: Memantau Pemakaian Listrik Harian**
1. Login ke aplikasi
2. Halaman Dashboard terbuka secara default
3. Pilih kamar yang ingin dipantau dari dropdown
4. Lihat widget "Daya Sekarang" untuk konsumsi saat ini
5. Lihat grafik untuk melihat pola pemakaian per jam

**Skenario 2: Menyalakan Listrik Kamar yang Padam**
1. Login ke aplikasi
2. Di Dashboard, pilih kamar yang padam
3. Widget Status akan menampilkan "PADAM" (merah)
4. Klik tombol "ON" untuk menyalakan kembali
5. Tunggu konfirmasi, status berubah menjadi "ON" (hijau)

**Skenario 3: Melihat dan Export Data Bulanan**
1. Login ke aplikasi
2. Buka halaman Histori
3. Pilih kamar, atur tanggal awal bulan dan akhir bulan
4. Klik "Cari Data" untuk menampilkan data
5. Klik "Export Excel" untuk download file perhitungan

**Skenario 4: Mengatur Batas Daya Kamar Baru**
1. Login ke aplikasi
2. Buka halaman Pengaturan
3. Pada bagian "Manajemen Kamar", tambah kamar baru
4. Input nama kamar dan daya maksimal
5. Klik "Tambah Kamar"
6. Pada bagian "Batas Daya", pilih kamar dan atur slider
7. Klik "Simpan Pengaturan"

---

### 5.5.3 Tabel Navigasi

| Dari Sidebar | Tujuan | Icon |
|--------------|--------|------|
| Dashboard | Halaman monitoring utama | 📊 |
| Histori | Data historis pemakaian | 📋 |
| Pengaturan | Konfigurasi sistem | ⚙️ |
| Simulasi IoT | Modal simulasi perangkat (hide/show) | 📡 |
| Logout | Keluar dari aplikasi | 🚪 |

---

> **Lanjut ke Bab 6: Tutorial Penggunaan Project**