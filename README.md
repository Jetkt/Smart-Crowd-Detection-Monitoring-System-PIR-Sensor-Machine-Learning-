# 🚶‍♂️ Smart Crowd Detection & Monitoring System (PIR Sensor + Machine Learning)

Sistem pemantauan keramaian cerdas (Crowd Detection) terintegrasi yang menggunakan **Sensor PIR (Passive Infrared)** untuk mendeteksi pergerakan fisik. Data dari sensor dianalisis menggunakan **Machine Learning** untuk memprediksi tingkat keramaian suatu area. Hasil pemantauan disimpan ke dalam database, ditampilkan secara *real-time* melalui **Web Dashboard**, dan dilengkapi dengan sistem notifikasi peringatan via **Telegram Bot**.

---

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk mengotomatisasi pemantauan ruang publik atau ruangan tertutup. Berbeda dengan sensor gerak biasa yang hanya memberi sinyal *ON/OFF*, sistem ini dilatih menggunakan dataset pergerakan historis selama 30 hari untuk mengenali pola keramaian. Model kecerdasan buatan (*Deep Learning/Neural Network*) akan mengklasifikasikan data tersebut dan mendistribusikan hasilnya ke platform web dan Telegram agar mudah dipantau oleh pengelola gedung atau administrator.

---

## ⚙️ Fitur Utama

- **Deteksi Gerak Real-Time:** Membaca pergerakan manusia secara akurat menggunakan Sensor PIR.
- **Prediksi Keramaian (AI/ML):** Menggunakan model Machine Learning (`.h5`) yang telah dilatih dengan dataset khusus untuk memprediksi status keramaian.
- **Web Dashboard Interaktif:** Menampilkan status ruangan, grafik, dan log data historis yang mudah diakses via peramban (browser).
- **Notifikasi Telegram Bot:** Mengirimkan peringatan atau pembaruan status keramaian langsung ke aplikasi Telegram pengguna.
- **Database Logging:** Seluruh data pergerakan dan status keramaian terekam secara sistematis di dalam *database* untuk keperluan audit atau analisis lanjutan.

---

## 🛠️ Teknologi & Perangkat yang Digunakan

### **Hardware (Perangkat Keras):**
- Sensor PIR (Motion Sensor)
- Mikrokontroler NodeMCU ESP32
- Kabel Jumper & Breadboard

### **Software & Tech Stack:**
- **Bahasa Pemrograman:** Python, C++ (untuk mikrokontroler)
- **Machine Learning:** TensorFlow/Keras (Model `.h5`), Jupyter Notebook, Pandas (Data processing)
- **Backend & Web:** Flask (`app.py`), HTML/CSS (`templates/`)
- **Integrasi:** Telegram Bot API
- **Database:** SQLite 
- **Desain Rangkaian:** Fritzing (`sensorPIR.fzz`)

---

## 📁 Struktur Repositori

```text
├── MODEL.ipynb                 # Jupyter Notebook berisi script preprocessing & training AI
├── MOTION_SENSOR_30_days.xlsx  # Dataset mentah pergerakan selama 30 hari untuk training
├── app.py                      # Script utama Web Server (Flask) & koneksi Database
├── crowded.csv                 # Dataset keramaian yang sudah diproses
├── crowded_model.h5            # Model Machine Learning (Keras/TensorFlow) yang sudah dilatih
├── sensorPIR.fzz               # Skematik wiring hardware (Fritzing)
├── tele.py                     # Script Python untuk operasional Telegram Bot
├── templates/                  # Folder berisi file HTML untuk antarmuka Web Dashboard
└── sensor_keramaian/           # Modul tambahan / script pembantu untuk sensor
