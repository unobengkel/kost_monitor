# BAB 2: Pengembangan Proses Bisnis

## 2.1 Penjelasan Proses Bisnis Project

Proses bisnis dari sistem monitoring dan kontrol listrik kamar kost ini dimulai dari pemasangan perangkat keras (hardware) pada setiap kamar kost. Perangkat yang dipasang terdiri dari Wemos ESP8266, sensor arus, modul relay, dan LCD 16x2 I2C. Perangkat ini akan mengukur secara real-time besaran daya listrik yang digunakan di kamar tersebut.

Data hasil pengukuran akan dikirim secara periodik melalui koneksi WiFi ke server pusat menggunakan protokol HTTP (POST/GET). Server yang dibangun dengan Python dan database SQLite akan menerima, memproses, dan menyimpan data tersebut.

Pemilik kost dapat mengakses data melalui aplikasi web SPA (Single Page Application) yang responsif. Melalui web, pemilik dapat:
1. Memantau pemakaian listrik setiap kamar secara real-time
2. Melihat grafik historis pemakaian
3. Mengatur batas daya maksimal per kamar
4. Menyalakan atau mematikan listrik kamar dari jarak jauh
5. Melihat laporan dan mengekspor data

Jika suatu kamar melebihi batas daya yang telah ditentukan, sistem akan secara otomatis memadamkan listrik kamar tersebut melalui relay, dan pemilik kost akan mendapatkan notifikasi. Pengguna kost kemudian harus meminta kepada pemilik untuk menyalakan kembali listriknya melalui aplikasi web.

---

## 2.2 Penjelasan & Diagram Proses Bisnis

### 2.2.1 Alur Proses Bisnis Utama

Berikut adalah diagram alur proses bisnis utama sistem monitoring listrik kost:

```
                      +------------------------------------------+
                      |            PEMILIK KOST                   |
                      |  (Mengelola & Memantau Kamar Kost)       |
                      +--------------------+---------------------+
                                           |
                       +-------------------v-------------------+
                       |        APLIKASI WEB (SPA)             |
                       |  - Dashboard Monitoring               |
                       |  - Histori Pemakaian                  |
                       |  - Pengaturan Batas Daya              |
                       |  - Kontrol ON/OFF Kamar               |
                       |  - Export Data                        |
                       +-------------------^-------------------+
                                           |
                       +-------------------v-------------------+
                       |            SERVER PYTHON               |
                       |  - REST API HTTP POST/GET              |
                       |  - Database SQLite                     |
                       |  - Logika Batas Daya                   |
                       |  - Kalkulasi Rata-rata                 |
                       +-------------------^-------------------+
                                           |
               +---------------------------+---------------------------+
               |                           |                           |
    +----------v----------+    +----------v----------+    +----------v----------+
    | PERANGKAT KAMAR 1  |    | PERANGKAT KAMAR 2  |    | PERANGKAT KAMAR N  |
    | Wemos ESP8266      |    | Wemos ESP8266      |    | Wemos ESP8266      |
    | Sensor Arus        |    | Sensor Arus        |    | Sensor Arus        |
    | Relay ON/OFF       |    | Relay ON/OFF       |    | Relay ON/OFF       |
    | LCD 16x2 I2C       |    | LCD 16x2 I2C       |    | LCD 16x2 I2C       |
    +--------------------+    +--------------------+    +--------------------+
               |                           |                           |
    +----------v----------+    +----------v----------+    +----------v----------+
    | KAMAR KOST 1       |    | KAMAR KOST 2       |    | KAMAR KOST N       |
    | Beban Listrik      |    | Beban Listrik      |    | Beban Listrik      |
    +--------------------+    +--------------------+    +--------------------+
```

### 2.2.2 Alur Data dalam Proses Bisnis

```
                        FLOW DATA DALAM SISTEM
                         
    [Perangkat Kamar]                    [Server]                    [Web Browser]
         |                                  |                            |
         |  1. Baca sensor arus             |                            |
         |  2. Hitung daya (Watt)           |                            |
         |  3. Kirim data ke server         |                            |
         |  ---- HTTP POST -------->        |                            |
         |                                  |  4. Terima data           |
         |                                  |  5. Simpan ke SQLite      |
         |                                  |  6. Cek batas daya        |
         |                                  |                            |
         |  Jika melebihi batas:            |                            |
         |  <------- HTTP RESPONSE ----     |  7. Kirim perintah OFF    |
         |  8. Matikan relay               |                            |
         |  9. Tampilkan "PADAM" di LCD    |                            |
         |                                  |                            |
         |                                  |  10. Request data         |
         |                                  |  <---- HTTP GET --------- |
         |                                  |  11. Kirim data JSON      |
         |                                  |  ----- HTTP RESPONSE -->  |
         |                                  |                            |
```

---

## 2.3 Penjelasan & Diagram Use Case

### 2.3.1 Identifikasi Aktor

| Aktor | Deskripsi |
|-------|-----------|
| **Pemilik Kost** | Aktor utama yang memiliki akses penuh ke semua fitur aplikasi web |
| **Perangkat IoT** | Wemos ESP8266 yang secara otomatis mengirim dan menerima data dari server |
| **Sistem** | Server Python yang menjalankan logika bisnis secara otomatis |

### 2.3.2 Diagram Use Case

```
                         +-------------------------------------+
                         |     SISTEM MONITORING LISTRIK KOST  |
                         +-------------------------------------+
                                           |
     +-------------------+                 |                 +-------------------+
     |                   |                 |                 |                   |
     |   PEMILIK KOST    |                 |                 |   PERANGKAT IoT   |
     |   (Aktor Utama)   |                 |                 |   (Aktor Sistem)  |
     +--------+----------+                 |                 +--------+----------+
              |                            |                          |
              |                            |                          |
    +---------v---------+        +---------v---------+      +---------v---------+
    |                   |        |                   |      |                   |
    |  (UC-01) Login    |        |  (UC-08) Kirim    |      |  (UC-12) Kirim    |
    |  ke Sistem        |        |  Data Pemakaian   |      |  Data Sensor      |
    |                   |        |  ke Server        |      |  ke Server        |
    +-------------------+        +-------------------+      +-------------------+
              |                            |                          |
    +---------v---------+        +---------v---------+      +---------v---------+
    |                   |        |                   |      |                   |
    |  (UC-02) Lihat    |        |  (UC-09) Export   |      |  (UC-13) Terima   |
    |  Dashboard        |        |  Data PDF/Excel   |      |  Perintah Relay   |
    |                   |        |                   |      |                   |
    +-------------------+        +-------------------+      +-------------------+
              |                            |                          |
    +---------v---------+        +---------v---------+      +---------v---------+
    |                   |        |                   |      |                   |
    |  (UC-03) Pantau   |        |  (UC-10) Atur     |      |  (UC-14) Tampilkan|
    |  Kamar Spesifik   |        |  Batas Daya       |      |  Status di LCD    |
    |                   |        |  Maksimal         |      |                   |
    +-------------------+        +-------------------+      +-------------------+
              |                            |
    +---------v---------+        +---------v---------+
    |                   |        |                   |
    |  (UC-04) Kontrol  |        |  (UC-11) Tambah/  |
    |  ON/OFF Kamar     |        |  Hapus Kamar      |
    |                   |        |                   |
    +-------------------+        +-------------------+
              |
    +---------v---------+
    |                   |
    |  (UC-05) Lihat    |
    |  Histori Filter   |
    |  Tanggal & Kamar  |
    |                   |
    +-------------------+
              |
    +---------v---------+
    |                   |
    |  (UC-06) Lihat    |
    |  Grafik Per Jam   |
    |                   |
    +-------------------+
              |
    +---------v---------+
    |                   |
    |  (UC-07) Ganti    |
    |  Tema Tampilan    |
    |                   |
    +-------------------+

```

### 2.3.3 Spesifikasi Use Case

| Kode | Nama Use Case | Aktor | Deskripsi Singkat |
|------|--------------|-------|-------------------|
| UC-01 | Login ke Sistem | Pemilik Kost | Autentikasi pengguna untuk mengakses aplikasi |
| UC-02 | Lihat Dashboard | Pemilik Kost | Melihat halaman utama dashboard monitoring |
| UC-03 | Pantau Kamar Spesifik | Pemilik Kost | Memilih salah satu kamar untuk dipantau detail |
| UC-04 | Kontrol ON/OFF Kamar | Pemilik Kost | Menyalakan atau mematikan listrik kamar |
| UC-05 | Lihat Histori Filter | Pemilik Kost | Melihat data historis dengan filter tanggal & kamar |
| UC-06 | Lihat Grafik Per Jam | Pemilik Kost | Melihat grafik pemakaian listrik per jam |
| UC-07 | Ganti Tema Tampilan | Pemilik Kost | Mengubah tema tampilan aplikasi (gelap/terang) |
| UC-08 | Kirim Data Pemakaian | Perangkat IoT | Mengirim data daya listrik ke server secara periodik |
| UC-09 | Export Data PDF/Excel | Pemilik Kost | Mengexport data histori ke format PDF atau Excel |
| UC-10 | Atur Batas Daya Maksimal | Pemilik Kost | Mengatur batas daya maksimal per kamar |
| UC-11 | Tambah/Hapus Kamar | Pemilik Kost | Manajemen jumlah kamar yang dimonitoring |
| UC-12 | Kirim Data Sensor | Perangkat IoT | Mengirim data arus dan tegangan ke server |
| UC-13 | Terima Perintah Relay | Perangkat IoT | Menerima perintah ON/OFF dari server |
| UC-14 | Tampilkan Status di LCD | Perangkat IoT | Menampilkan status koneksi dan kondisi kamar di LCD |

---

## 2.4 Penjelasan & Alur Flowchart Project

### 2.4.1 Flowchart Sistem Utama

Berikut adalah flowchart yang menjelaskan alur kerja keseluruhan sistem:

```
                                START
                                  |
                                  v
                    +-----------------------------+
                    |  Inisialisasi Sistem        |
                    |  - Setup WiFi ESP8266       |
                    |  - Inisialisasi LCD         |
                    |  - Setup Sensor & Relay     |
                    +-----------------------------+
                                  |
                                  v
                    +-----------------------------+
                    |  Cek Koneksi WiFi           |
                    +-----------------------------+
                                  |
                    +-------------+-------------+
                    |                           |
                   YES                         NO
                    |                           |
                    v                           v
           +-----------------+     +-------------------------+
           | LCD: "WiFi OK"  |     | LCD: "WiFi Gagal"      |
           | Connect to      |     | LCD: "Coba Ulang..."   |
           | Server...       |     | Retry Koneksi          |
           +-----------------+     +-------------------------+
                    |                           |
                    v                           |
           +-----------------+                  |
           | Cek Koneksi     |                  |
           | ke Server       |                  |
           +-----------------+                  |
                    |                           |
          +---------+----------+                |
          |                    |                |
         YES                  NO               |
          |                    |                |
          v                    v                |
   +-------------+    +----------------+       |
   | LCD:        |    | LCD: "Server   |       |
   | "Server OK" |    | Gagal"         |       |
   +-------------+    +----------------+       |
          |                    |                |
          +--------------------+----------------+
                               |
                               v
                    +---------------------------+
                    | Loop Utama                |
                    | Setiap 1 detik:           |
                    +---------------------------+
                               |
                               v
                    +---------------------------+
                    | Baca Sensor Arus          |
                    | Hitung Daya (Watt)        |
                    +---------------------------+
                               |
                               v
                    +---------------------------+
                    | Cek Apakah Daya > Batas   |
                    +---------------------------+
                               |
                    +----------+----------+
                    |                     |
                   YES                   NO
                    |                     |
                    v                     v
           +-----------------+   +-----------------+
           | Relay OFF       |   | Relay ON        |
           | LCD: "PADAM"    |   | LCD: Daya Normal|
           | Kirim Status    |   | Kirim Data Daya |
           +-----------------+   +-----------------+
                    |                     |
                    +----------+----------+
                               |
                               v
                    +---------------------------+
                    | Kirim Data ke Server      |
                    | via HTTP POST             |
                    +---------------------------+
                               |
                               v
                    +---------------------------+
                    | Terima Response Server    |
                    | - Jika ada perintah relay |
                    |   Eksekusi ON/OFF        |
                    +---------------------------+
                               |
                               v
                    +---------------------------+
                    | Delay 1 detik             |
                    +---------------------------+
                               |
                               +-----------> (Kembali ke Loop)
```

### 2.4.2 Flowchart Aplikasi Web

```
                                START
                                  |
                                  v
                    +-----------------------------+
                    |  Pengguna Membuka Web       |
                    |  index.html                 |
                    +-----------------------------+
                                  |
                                  v
                    +-----------------------------+
                    |  Cek Status Login           |
                    +-----------------------------+
                                  |
                    +-------------+-------------+
                    |                           |
                 BELUM LOGIN                 SUDAH
                    |                           |
                    v                           v
         +---------------------+      +---------------------+
         | Tampilkan Halaman   |      | Tampilkan Sidebar   |
         | Login               |      | Dashboard           |
         +---------------------+      +---------------------+
                    |                           |
                    v                           |
         +---------------------+                |
         | Input Username &    |                |
         | Password            |                |
         +---------------------+                |
                    |                           |
                    v                           |
         +---------------------+                |
         | Kirim ke Server     |                |
         +---------------------+                |
                    |                           |
           +--------+----------+                |
           |                   |                |
         BERHASIL            GAGAL             |
           |                   |                |
           v                   v                |
   +-----------------+  +-----------------+     |
   | Redirect ke     |  | Tampilkan Error |     |
   | Dashboard       |  | Login Ulang     |     |
   +-----------------+  +-----------------+     |
           |                    |                |
           +--------------------+----------------+
                                |
                                v
                    +---------------------------+
                    | Sidebar Navigasi:         |
                    | [Dashboard] [Histori]     |
                    | [Pengaturan] [Logout]     |
                    +---------------------------+
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
         +-------------------+   +---------------------+
         | DASHBOARD:        |   | HISTORI:            |
         | - Pilih Kamar     |   | - Filter Kamar      |
         | - Widget Daya     |   | - Filter Tanggal    |
         | - Widget Rata-rata|   | - Tabel Data        |
         | - Grafik Per Jam  |   | - Tombol Cari       |
         | - Status Kamar    |   | - Tombol Hapus      |
         | - Tombol ON/OFF   |   | - Export PDF/Excel  |
         +-------------------+   +---------------------+
                       |                       |
                       +-----------+-----------+
                                   |
                                   v
                     +---------------------------+
                     | PENGATURAN:               |
                     | - Tema (Light/Dark)       |
                     | - Batas Daya Maksimal     |
                     | - Tambah/Hapus Kamar      |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     | Logout -> Kembali ke      |
                     | Halaman Login             |
                     +---------------------------+
```

### 2.4.3 Flowchart Proses Batas Daya Otomatis

```
                        MULAI
                          |
                          v
           +---------------------------+
           | Server Terima Data Daya   |
           | dari Perangkat kamar X    |
           +---------------------------+
                          |
                          v
           +---------------------------+
           | Bandingkan Daya dengan    |
           | Batas Maksimal Kamar X   |
           +---------------------------+
                          |
               +----------+----------+
               |                     |
            DAYA > BATAS         DAYA <= BATAS
               |                     |
               v                     v
    +---------------------+  +---------------------+
    | Set Status = PADAM  |  | Set Status = NORMAL |
    | Kirim Perintah OFF  |  | (Tidak ada aksi)    |
    | ke Perangkat via    |  |                     |
    | HTTP Response       |  |                     |
    +---------------------+  +---------------------+
               |                     |
               v                     v
    +---------------------+  +---------------------+
    | Catat ke Database:  |  | Simpan data daya    |
    | - Waktu Padam       |  | ke tabel historis   |
    | - Penyebab: Over    |  |                     |
    |   Limit             |  |                     |
    +---------------------+  +---------------------+
               |                     |
               +----------+----------+
                          |
                          v
           +---------------------------+
           | Update Dashboard Web      |
           | (Real-time via AJAX)      |
           +---------------------------+
                          |
                          v
           +---------------------------+
           | Jika status PADAM:        |
           | Tunggu perintah dari      |
           | Pemilik untuk ON kembali  |
           +---------------------------+
                          |
                          v
           +---------------------------+
           | Pemilik Klik Tombol ON    |
           | di Dashboard Web          |
           +---------------------------+
                          |
                          v
           +---------------------------+
           | Server Kirim Perintah ON  |
           | ke Perangkat Kamar X      |
           +---------------------------+
                          |
                          v
           +---------------------------+
           | Perangkat Nyalakan Relay  |
           | LCD: Daya Normal          |
           +---------------------------+
                          |
                          v
                         SELESAI
```

---

> **Lanjut ke Bab 3: Pengembangan Kerja Server**