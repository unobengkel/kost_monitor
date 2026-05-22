# BAB 1: Pengenalan Project

## 1.1 Pendahuluan

Kos-kosan merupakan salah satu tempat tinggal yang banyak diminati oleh pelajar, mahasiswa, dan pekerja di berbagai daerah. Dalam pengelolaan kost, salah satu aspek yang sering menjadi permasalahan adalah penggunaan listrik. Para pemilik kost sering menghadapi kesulitan dalam memantau dan mengendalikan pemakaian listrik setiap kamar. Penggunaan listrik yang tidak terkontrol dapat menyebabkan pembengkakan biaya bulanan, bahkan dapat menyebabkan pemadaman total akibat kelebihan beban daya.

Dengan perkembangan teknologi Internet of Things (IoT), kini tersedia solusi untuk memantau dan mengendalikan perangkat elektronik secara jarak jauh melalui internet. **Sistem Monitoring & Kontrol Listrik Kamar Kost Berbasis IoT** hadir sebagai solusi untuk membantu pemilik kost dalam mengelola pemakaian listrik setiap kamar secara efisien, transparan, dan real-time.

### 1.1.1 Latar Belakang

Permasalahan utama yang dihadapi pemilik kost adalah:
- Tidak adanya alat untuk mengukur pemakaian listrik per kamar secara spesifik
- Pengguna kost sering menggunakan perangkat listrik secara berlebihan tanpa batasan
- Sering terjadi pemadaman total akibat daya listrik mencapai batas maksimal
- Pemilik kost tidak memiliki data historis pemakaian listrik untuk evaluasi

Dengan sistem ini, pemilik kost dapat memantau pemakaian listrik setiap kamar dari jarak jauh melalui aplikasi web, memberikan batasan daya otomatis, serta mendapatkan laporan historis pemakaian.

### 1.1.2 Tujuan Project

Tujuan dari pembuatan project ini adalah:
1. Membangun alat monitoring daya listrik per kamar berbasis Wemos ESP8266
2. Mengembangkan server untuk menyimpan dan mengolah data pemakaian listrik
3. Membuat aplikasi web untuk visualisasi data dan kontrol perangkat
4. Memberikan fitur pembatasan daya otomatis pada setiap kamar
5. Menyediakan laporan historis pemakaian listrik untuk analisis

---

## 1.2 Fitur dari Project

### A. Fitur Hardware (Perangkat Keras)
| No | Fitur | Keterangan |
|----|-------|------------|
| 1 | Monitoring Daya | Mengukur tegangan, arus, dan daya listrik secara real-time |
| 2 | Tampilan LCD | Menampilkan status koneksi WiFi dan server pada LCD 16x2 I2C |
| 3 | Kontrol Relay | Memutus dan menyambung aliran listrik ke kamar |
| 4| Sensor Arus | Mendeteksi besaran arus listrik yang digunakan |
| 5 | Koneksi WiFi | Mengirim data ke server melalui HTTP POST/GET |
| 6 | Batas Daya Otomatis | Mematikan listrik otomatis jika melebihi batas yang ditentukan |

### B. Fitur Server
| No | Fitur | Keterangan |
|----|-------|------------|
| 1 | REST API | Endpoint HTTP untuk menerima dan mengirim data |
| 2 | Database SQLite | Menyimpan data pemakaian listrik, konfigurasi, dan histori |
| 3 | Autentikasi | Sistem login untuk keamanan akses |
| 4 | CRUD Kamar | Menambah, mengubah, menghapus data kamar |
| 5 | Kalkulasi Otomatis | Menghitung rata-rata pemakaian per hari |

### C. Fitur Aplikasi Web
| No | Fitur | Keterangan |
|----|-------|------------|
| 1 | Dashboard Real-time | Monitoring daya setiap kamar secara langsung |
| 2 | Grafik Histori | Chart pemakaian listrik per jam dalam bentuk grafik |
| 3 | Kontrol Kamar | Tombol ON/OFF untuk menyalakan/mematikan listrik kamar |
| 4 | Filter Data | Filter berdasarkan kamar, tanggal start-end |
| 5 | Export Data | Cetak/export data ke PDF dan Excel |
| 6 | Pengaturan | Pengaturan tema tampilan dan batas daya maksimal |
| 7 | Manajemen Kamar | Tambah/hapus kamar kost |
| 8 | Responsive Design | Tampilan optimal di HP, Tablet, dan PC |

---

## 1.3 Target Demografi Pemakai

### A. Pengguna Utama (Primary User)
| Kategori | Deskripsi |
|----------|-----------|
| **Pemilik Kost** | Individu atau badan yang memiliki dan mengelola usaha kost. Bertanggung jawab atas pemeliharaan dan pengelolaan fasilitas kost termasuk listrik. |
| **Jumlah Unit** | Kost dengan 5 kamar atau lebih, dengan kemungkinan penambahan kamar |
| **Lokasi** | Perkotaan, pinggiran kota, area kampus/perkantoran |

### B. Pengguna Sekunder (Secondary User)
| Kategori | Deskripsi |
|----------|-----------|
| **Pengurus Kost** | Karyawan yang ditunjuk untuk mengelola operasional kost sehari-hari |
| **Teknisi** | Orang yang bertanggung jawab dalam perawatan dan instalasi perangkat |

### C. Karakteristik Pengguna
- **Tingkat literasi teknologi**: Menengah - memiliki kemampuan dasar menggunakan aplikasi web dan smartphone
- **Kebutuhan utama**: Kemudahan, transparansi, dan kontrol penuh terhadap penggunaan listrik
- **Latar belakang**: Tidak memerlukan pengetahuan teknis mendalam tentang IoT atau listrik

---

## 1.4 Masalah dan Solusi oleh Project

### Tabel Masalah & Solusi

| No | Masalah | Solusi |
|----|---------|--------|
| 1 | Pengguna kost menggunakan listrik tanpa batasan | Sistem memberikan batasan daya maksimal per kamar yang bisa diatur melalui web |
| 2 | Tidak ada perhitungan biaya listrik per kamar | Data pemakaian kWh tercatat otomatis dan dapat diakses kapan saja |
| 3 | Pemadaman total akibat kelebihan beban daya | Setiap kamar memiliki proteksi mandiri; jika satu kamar kelebihan beban, hanya kamar tersebut yang padam |
| 4 | Pemilik tidak bisa memantau pemakaian secara real-time | Dashboard web menampilkan data konsumsi listrik secara langsung (real-time) |
| 5 | Tidak ada data historis untuk evaluasi | Sistem menyimpan histori pemakaian yang bisa difilter dan diexport |
| 6 | Sulit menagih biaya listrik per kamar | Data pemakaian tersedia per kamar per bulan untuk dasar penagihan |
| 7 | Pengguna kost kesulitan jika listrik padam di malam hari | Pemilik bisa menyalakan ulang listrik melalui web dari jarak jauh |

### Analisis Dampak Solusi

| Aspek | Sebelum Menggunakan Sistem | Setelah Menggunakan Sistem |
|-------|---------------------------|---------------------------|
| **Pengelolaan Listrik** | Manual, tidak terukur | Otomatis, terukur, real-time |
| **Biaya Listrik** | Ditanggung pemilik secara global | Bisa dihitung per kamar secara akurat |
| **Kontrol Daya** | Tidak ada batasan | Ada batasan otomatis dengan notifikasi |
| **Data & Laporan** | Tidak ada | Tersedia histori lengkap dengan grafik |
| **Efisiensi** | Boros, tidak terkontrol | Efisien, setiap kamar bertanggung jawab |
| **Kepuasan Pengguna** | Sering ada konflik listrik | Transparan dan adil untuk semua pihak |

---

> **Lanjut ke Bab 2: Pengembangan Proses Bisnis**