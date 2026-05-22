# BAB 4: Pengenalan Bagian Hardware

## 4.1 Pengenalan Komponen

Sistem monitoring dan kontrol listrik kamar kost ini menggunakan beberapa komponen perangkat keras yang bekerja sama untuk mengukur, memproses, dan mengontrol penggunaan listrik. Berikut adalah daftar komponen yang digunakan:

### 4.1.1 Daftar Komponen Utama

| No | Nama Komponen | Jumlah | Fungsi |
|----|---------------|--------|--------|
| 1 | Wemos D1 Mini (ESP8266) | 1 | Mikrokontroler utama, mengolah data dan komunikasi WiFi |
| 2 | LCD 16x2 I2C | 1 | Menampilkan status koneksi WiFi, server, dan daya |
| 3 | Sensor Arus ACS712 | 1 | Mengukur arus listrik AC yang digunakan |
| 4 | Modul Relay 1 Channel | 1 | Memutus/menyambung aliran listrik ke kamar |
| 5 | Power Supply 5V (Charger HP) | 1 | Sumber daya untuk perangkat |
| 6| Kabel Jumper | Secukupnya | Menghubungkan antar komponen |
| 7 | Adaptor AC ke DC 5V | 1 | Mengubah listrik AC 220V ke DC 5V |

### 4.1.2 Spesifikasi Detail Komponen

#### A. Wemos D1 Mini (ESP8266)

```
    +---------------------------------------------------------+
    |                   WEMOS D1 MINI                         |
    |                                                         |
    |   Spesifikasi:                                          |
    |   - Mikrokontroler: ESP8266EX                           |
    |   - Tegangan Operasi: 3.3V (dapat diberi 5V via USB)   |
    |   - WiFi: 802.11 b/g/n (2.4 GHz)                       |
    |   - GPIO: 11 pin                                       |
    |   - Analog Input: 1 pin (A0, 0-3.3V)                  |
    |   - Flash Memory: 4MB                                  |
    |   - Clock Speed: 80MHz / 160MHz                        |
    |   - USB Port: Micro USB                                |
    |                                                         |
    |   Pinout Digital:                                       |
    |   - D1 (GPIO5)  --> SCL (LCD I2C)                      |
    |   - D2 (GPIO4)  --> SDA (LCD I2C)                      |
    |   - D3 (GPIO0)  --> Relay Control                      |
    |   - A0          --> Sensor Arus ACS712                  |
    |                                                         |
    +---------------------------------------------------------+
```

#### B. LCD 16x2 I2C

```
    +---------------------------------------------------------+
    |                   LCD 16x2 I2C                          |
    |                                                         |
    |   Spesifikasi:                                          |
    |   - Display: 16 karakter x 2 baris                     |
    |   - Backlight: Biru/Hijau (dapat diatur via software)  |
    |   - Tegangan Operasi: 5V                               |
    |   - Alamat I2C: 0x27 (default, dapat diubah)           |
    |   - Komunikasi: I2C (hanya 2 kabel: SDA & SCL)        |
    |                                                         |
    |   Keunggulan:                                           |
    |   - Hanya butuh 4 kabel (VCC, GND, SDA, SCL)           |
    |   - Tidak perlu banyak pin GPIO                        |
    |   - Mudah diprogram dengan library LiquidCrystal_I2C   |
    |                                                         |
    +---------------------------------------------------------+
```

#### C. Sensor Arus ACS712 (30A)

```
    +---------------------------------------------------------+
    |                SENSOR ARUS ACS712 30A                   |
    |                                                         |
    |   Spesifikasi:                                          |
    |   - Chip: ACS712ELC-30A                                |
    |   - Rentang Arus: -30A s/d +30A                        |
    |   - Sensitivitas: 66 mV/A                              |
    |   - Tegangan Operasi: 5V                               |
    |   - Output: Analog (0-5V)                              |
    |   - Tipe: Non-invasif (mengapit kabel)                 |
    |                                                         |
    |   Pinout:                                               |
    |   - VCC (Merah)   --> 5V                               |
    |   - GND (Hitam)   --> GND                              |
    |   - OUT (Biru)    --> A0 (Wemos)                       |
    |                                                         |
    +---------------------------------------------------------+
```

#### D. Modul Relay 1 Channel

```
    +---------------------------------------------------------+
    |                MODUL RELAY 1 CHANNEL                    |
    |                                                         |
    |   Spesifikasi:                                          |
    |   - Tegangan Coil: 5V DC                               |
    |   - Kontak Relay: SPDT (Single Pole Double Throw)      |
    |   - Kapasitas Kontak: 250VAC / 10A                     |
    |   - Logika Kontrol: LOW aktif (active LOW)             |
    |   - Indikator LED: Menyala saat relay aktif            |
    |                                                         |
    |   Pinout:                                               |
    |   - VCC (Merah)   --> 5V                               |
    |   - GND (Hitam)   --> GND                              |
    |   - IN (Kuning)   --> D3 (GPIO0) Wemos                 |
    |                                                         |
    |   Terminal Output:                                      |
    |   - COM (Common)  --> Fase Listrik Masuk              |
    |   - NO (Normally Open)  --> Fase ke Beban Kamar       |
    |   - NC (Normally Closed) --> Tidak digunakan            |
    |                                                         |
    +---------------------------------------------------------+
```

#### E. Power Supply (Charger HP)

```
    +---------------------------------------------------------+
    |               POWER SUPPLY (CHARGER HP)                 |
    |                                                         |
    |   Spesifikasi:                                          |
    |   - Input: 100-240V AC 50/60Hz                        |
    |   - Output: 5V DC, >= 2A                               |
    |   - Konektor: Micro USB                                |
    |   - Proteksi: Short circuit, Over current              |
    |                                                         |
    |   Catatan Penting:                                      |
    |   - Gunakan charger dengan output minimal 2A            |
    |   - Charger berkualitas baik untuk stabilitas           |
    |   - Jangan gunakan charger KW (kualitas rendah)        |
    |                                                         |
    +---------------------------------------------------------+
```

---

## 4.2 Pengenalan Sumber Power

### 4.2.1 Diagram Aliran Daya

```
    LISTRIK PLN                          PERANGKAT SISTEM
    (AC 220V)                           (DC 5V / 3.3V)
        |                                     |
        |                                     |
   +----v----+                          +-----v-----+
   | Stop    |                          |  Charger  |
   | Kontak  +----> Adaptor/Charger --->|   HP      |
   | (AC)    |     AC 220V -> DC 5V     |  DC 5V    |
   +---------+                          +-----+-----+
                                               |
                                      +--------+--------+
                                      |                  |
                                +-----v-----+    +------v------+
                                |   Wemos   |    |   LCD 16x2  |
                                |  ESP8266  |    |   I2C (5V)  |
                                | (3.3V/5V) |    +-------------+
                                +-----+-----+
                                      |
                                +-----v-----+
                                |   Sensor   |
                                |  ACS712    |
                                |   (5V)     |
                                +-----------+
                                      |
                                +-----v-----+
                                |   Relay    |
                                |   Module   |
                                |   (5V)     |
                                +-----+-----+
                                      |
                                      v
                              +---------------+
                              | BEBAN KAMAR   |
                              | (Lampu, AC,   |
                              |  Kulkas, dll) |
                              +---------------+
```

### 4.2.2 Penjelasan Sistem Power

| No | Tingkat Daya | Tegangan | Digunakan Oleh |
|----|--------------|----------|----------------|
| 1 | Input Utama | 220V AC | Stop kontak dinding (PLN) |
| 2 | Power Supply | 5V DC | Seluruh komponen elektronik |
| 3 | Internal Wemos | 3.3V DC | Chip ESP8266 (dari regulator internal) |

**Alur Power:**
1. Listrik PLN (AC 220V) masuk ke stop kontak
2. Charger HP mengubah AC 220V menjadi DC 5V
3. DC 5V digunakan oleh:
   - Wemos D1 Mini (via port Micro USB)
   - LCD 16x2 I2C
   - Sensor ACS712
   - Modul Relay (coil)
4. Wemos memiliki regulator internal yang mengubah 5V ke 3.3V untuk chip ESP8266

### 4.2.3 Proteksi dan Keamanan

| Aspek | Keterangan |
|-------|------------|
| **Proteksi Arus Lebih** | Charger HP memiliki proteksi arus lebih internal |
| **Proteksi Hubung Singkat** | Charger akan mati otomatis jika terjadi short circuit |
| **Isolasi Listrik** | Charger HP memberikan isolasi galvanis antara AC 220V dan DC 5V |
| **Sekring** | Disarankan menambahkan sekring 1A pada jalur AC |
| **Pentanahan** | Pastikan stop kontak memiliki grounding yang baik |

---

## 4.3 Pengenalan Skema Rangkaian

### 4.3.1 Diagram Skema Rangkaian Keseluruhan

```
                    SKEMA RANGKAIAN MONITORING LISTRIK KOST
                    =======================================


                    +------------------------------------------+
                    |          WEMOS D1 MINI (ESP8266)          |
                    |                                          |
                    |   USB Port                               |
                    |      +                                   |
                    |      | (Power 5V)                        |
                    |      v                                   |
                    |  +--------+                              |
                    |  | 5V Vin |                              |
                    |  +--------+                              |
                    |      |                                   |
                    |   +--+--+                                |
                    |   |3.3V |  (Regulator Internal)          |
                    |   +--+--+                                |
                    |      |                                   |
                    |  +---+----------------------+             |
                    |  |                          |             |
                    |  |   GPIO PINS              |             |
                    |  |   +-------------------+  |             |
                    |  |   | D1 (GPIO5) = SCL  |  |             |
                    |  |   | D2 (GPIO4) = SDA  |  |             |
                    |  |   | D3 (GPIO0) = RELAY|  |             |
                    |  |   | A0 = ACS712 OUT   |  |             |
                    |  |   +-------------------+  |             |
                    |  |                          |             |
                    |  |   GND --------> Semua GND            |
                    |  +--------------------------+           |
                    +------------------------------------------+
                                      |
            +-------------------------+---------------------------+
            |                         |                           |
            |                         |                           |
    +-------v--------+      +--------v--------+        +---------v--------+
    | LCD 16x2 I2C   |      | SENSOR ACS712   |        | RELAY MODULE     |
    |                |      |                 |        |                  |
    |  Pin:          |      |  Pin:           |        |  Pin:            |
    |  VCC  --> 5V   |      |  VCC --> 5V     |        |  VCC --> 5V      |
    |  GND  --> GND  |      |  GND --> GND    |        |  GND --> GND     |
    |  SDA  --> D2   |      |  OUT --> A0     |        |  IN  --> D3      |
    |  SCL  --> D1   |      |                 |        |                  |
    +----------------+      +-----------------+        +--------+---------+
                                                                 |
                                                                 |
                                                    +------------+------------+
                                                    |                         |
                                              +-----v-----+           +-------v--------+
                                              |   COM     |           |   NO (Relay)   |
                                              | (Fase IN) |           | (Fase ke Kamar)|
                                              +-----------+           +----------------+
                                                    |                         |
                                                    |                         |
                                               +----+----+                   |
                                               |  Fase   |                   |
                                               |  PLN    |                   |
                                               |  (220V) |                   |
                                               +---------+                   |
                                                                             |
                                                                      +------v------+
                                                                      |   BEBAN     |
                                                                      |   KAMAR     |
                                                                      |  (Lampu,    |
                                                                      |   AC, dll)  |
                                                                      +-------------+

                    KETERANGAN WARNA KABEL:
                    =====================
                    Merah   = VCC (5V)
                    Hitam   = GND (0V)
                    Kuning  = Sinyal Data Digital
                    Biru    = Sinyal Analog
                    Coklat  = Fase Listrik AC 220V
                    Putih   = Netral Listrik AC 220V
```

### 4.3.2 Diagram Detail Koneksi Sensor ACS712 dengan Beban

```
                      +------------------------------------------------+
                      |         SENSOR ACS712 (Modul)                  |
                      |                                                |
                      |   +--------------------------------------+     |
                      |   |   +--------+      +--------+         |     |
                      |   |   |  IP+   |      |  IP-   |         |     |
                      |   |   +--------+      +--------+         |     |
                      |   |       |               |              |     |
                      +---+-------+---------------+--------------+-----+
                                  |               |
                                  |               |
                             +----+----+    +-----+------+
                             |  Fase   |    |   Fase ke  |
                             |  PLN    |    |   Relay    |
                             | (220V)  |    |   (Input)  |
                             +---------+    +------------+
```

**Catatan Penting Sensor ACS712:**
- Sensor ACS712 dipasang SERI pada kabel FASE listrik
- Arus yang mengalir melalui IP+ ke IP- akan dideteksi oleh sensor
- Output analog (OUT) menghasilkan tegangan yang proporsional dengan arus
- Tegangan output = 2.5V (saat arus 0A) +/- sensitivitas x arus

### 4.3.3 Diagram Detail Koneksi Relay

```
                    +--------------------------------------+
                    |         RELAY MODULE 1 CH            |
                    |                                      |
                    |   +-----+      +-----+               |
                    |   | JD  |      | VCC |               |
                    |   +-----+      +-----+               |
                    |     |             |                  |
                    |     +----+    +---+                  |
                    |          |    |                      |
                    |   +------v----v------+               |
                    |   |    Coil (5V)     |               |
                    |   +------------------+               |
                    |          |                           |
                    |   +------+------+                    |
                    |   |             |                    |
                    |   |   +---------v---------+         |
                    |   |   |   Kontak Relay    |         |
                    |   |   |                   |         |
                    |   |   |   COM ---- NO     |         |
                    |   |   |   (Input) (Output)|         |
                    |   |   +-------------------+         |
                    |   |             |                   |
                    +---+-------------+-------------------+
                        |             |
                        |             |
                    +---v----+   +----v----+
                    |  Fase  |   |  Fase   |
                    |  PLN   |   |  ke     |
                    |        |   |  Beban  |
                    +--------+   +---------+
```

---

## 4.4 Jalur Kabel Pin Power dan Data

### 4.4.1 Tabel Koneksi Pin (Wiring Diagram)

#### A. Koneksi Wemos ke LCD 16x2 I2C

| Pin Wemos | Pin LCD I2C | Fungsi | Warna Kabel |
|-----------|-------------|--------|-------------|
| 5V (Vin) | VCC | Power 5V untuk LCD | Merah |
| GND | GND | Ground | Hitam |
| D1 (GPIO5) | SCL | Clock I2C | Kuning |
| D2 (GPIO4) | SDA | Data I2C | Kuning |

#### B. Koneksi Wemos ke Sensor ACS712

| Pin Wemos | Pin ACS712 | Fungsi | Warna Kabel |
|-----------|------------|--------|-------------|
| 5V (Vin) | VCC | Power 5V untuk sensor | Merah |
| GND | GND | Ground | Hitam |
| A0 (ADC) | OUT | Output analog sensor | Biru |

#### C. Koneksi Wemos ke Modul Relay

| Pin Wemos | Pin Relay | Fungsi | Warna Kabel |
|-----------|-----------|--------|-------------|
| 5V (Vin) | VCC | Power 5V untuk relay | Merah |
| GND | GND | Ground | Hitam |
| D3 (GPIO0) | IN | Sinyal kontrol relay | Kuning |

#### D. Koneksi Relay ke Beban Listrik AC 220V

| Terminal Relay | Terhubung ke | Fungsi | Warna Kabel |
|----------------|--------------|--------|-------------|
| COM | Fase Listrik PLN (setelah sensor) | Input listrik AC | Coklat |
| NO | Beban Kamar (lampu/AC/dll) | Output ke kamar | Coklat |
| NC | Tidak terhubung | - | - |

### 4.4.2 Diagram Kabel Lengkap Sistem

```
                    DIAGRAM KABEL LENGKAP
                    =====================


    POWER SUPPLY (AC 220V -> DC 5V)
    ===============================
    +----------+     +----------+     +-----------+
    | Stop     |---->| Charger  |---->| USB Cable |
    | Kontak   |     | HP 5V 2A |     | ke Wemos  |
    | AC 220V  |     +----------+     +-----------+
    +----------+


    PEMBAGIAN POWER DC 5V
    ======================
    
    Wemos D1 Mini (USB Port)
          |  5V (Vin pin)
          +------+------+------+
          |      |      |      |
          v      v      v      v
        LCD    ACS712  Relay  (Fan, dll opsional)
        5V     5V      5V
    
    GROUND BERSAMA (Common Ground)
    ===============================
    Wemos GND
       +------+------+------+
       |      |      |      |
       v      v      v      v
     LCD    ACS712  Relay
     GND    GND     GND


    JALUR SINYAL DATA
    =================
    
    Wemos D1 (GPIO5) ---> LCD SCL (I2C Clock)
    Wemos D2 (GPIO4) ---> LCD SDA (I2C Data)
    Wemos A0 (ADC)   <--- ACS712 OUT (Analog)
    Wemos D3 (GPIO0) ---> Relay IN (Control)


    JALUR LISTRIK AC 220V
    ======================
    
    Fase PLN (220V)
       |
       v
    [ACS712 IP+] --- [ACS712 IP-]
       |
       v
    [Relay COM] --- [Relay NO]
       |
       v
    [Beban Kamar] (Lampu, AC, dll)
    
    Netral PLN --- Langsung ke Beban Kamar
```

### 4.4.3 Panduan Pemasangan Kabel

#### Langkah 1: Persiapan
1. Pastikan semua komponen dalam kondisi baik
2. Siapkan kabel jumper secukupnya
3. Siapkan obeng kecil untuk terminal relay

#### Langkah 2: Pemasangan Kabel DC (Low Voltage)
```
    Urutan Pemasangan:
    1. Hubungkan VCC LCD ke pin 5V Wemos
    2. Hubungkan GND LCD ke pin GND Wemos
    3. Hubungkan SDA LCD ke pin D2 Wemos
    4. Hubungkan SCL LCD ke pin D1 Wemos
    5. Hubungkan VCC ACS712 ke pin 5V Wemos
    6. Hubungkan GND ACS712 ke pin GND Wemos
    7. Hubungkan OUT ACS712 ke pin A0 Wemos
    8. Hubungkan VCC Relay ke pin 5V Wemos
    9. Hubungkan GND Relay ke pin GND Wemos
    10. Hubungkan IN Relay ke pin D3 Wemos
```

#### Langkah 3: Pemasangan Kabel AC (High Voltage - Hati-hati!)
```
    PERHATIAN: Listrik AC 220V BERBAHAYA!
    ======================================
    Matikan MCB utama sebelum memasang kabel AC!
    
    1. Pastikan tidak ada tegangan pada kabel yang akan dipasang
    2. Hubungkan Fase PLN ke Terminal IP+ ACS712
    3. Hubungkan Terminal IP- ACS712 ke COM Relay
    4. Hubungkan Terminal NO Relay ke Beban Kamar
    5. Hubungkan Netral PLN langsung ke Beban Kamar
    6. Pastikan semua sambungan kencang dan aman
    7. Isolasi sambungan dengan selotip listrik jika perlu
```

### 4.4.4 Tabel Konfigurasi Pin Software

Berikut adalah konfigurasi pin yang akan digunakan dalam pemrograman ESP8266:

```cpp
// KONFIGURASI PIN WEMOS D1 MINI
#define LCD_SDA   D2    // GPIO4 - I2C Data
#define LCD_SCL   D1    // GPIO5 - I2C Clock
#define RELAY_PIN D3    // GPIO0 - Relay Control
#define SENSOR_PIN A0   // ADC   - ACS712 Output

// KONFIGURASI I2C LCD
#define LCD_ADDRESS 0x27  // Alamat I2C LCD (default)
#define LCD_COLUMNS 16    // Jumlah kolom LCD
#define LCD_ROWS    2     // Jumlah baris LCD

// KONFIGURASI SENSOR
#define ACS712_SENSITIVITY 0.066  // 66 mV/A untuk ACS712 30A
#define ACS712_VREF        5.0    // Tegangan referensi ADC
#define VOLTAGE_STANDARD   220.0  // Tegangan standar PLN
```

---

> **Lanjut ke Bab 5: Pengenalan Tampilan Antarmuka Aplikasi**