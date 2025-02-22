## Kite AI Automation

## 📌 Deskripsi

Kite AI Automation adalah skrip otomatisasi yang berinteraksi dengan AI untuk mendapatkan poin berdasarkan interaksi yang dilakukan menggunakan wallet address tertentu. Skrip ini mendukung eksekusi dalam dua bahasa pemrograman: JavaScript (Node.js) dan Python.

## 🛠 Fitur

Menggunakan API Kite AI untuk mengirimkan pertanyaan dan mendapatkan respons AI.

Membaca wallet address dari file data.txt.

Melacak jumlah interaksi harian dengan batasan maksimum.

Otomatis menunggu hingga reset waktu jika batas interaksi tercapai.

Menampilkan statistik pengguna berdasarkan wallet address.

Multi-threading support untuk eksekusi lebih cepat (Python & JavaScript).



---

## 🚀 Instalasi & Persiapan

1. Instalasi Node.js Script (bot.js)

Persyaratan

Node.js versi terbaru

Paket tambahan yang dibutuhkan:

```
npm install axios chalk progress winston readline
```

Menjalankan Script

```
node bot.js
```

---

2. Instalasi Python Script (bot.py)

Persyaratan

Python 3.12

Paket tambahan yang dibutuhkan:

```
pip install requests rich tqdm
```

Menjalankan Script

```
python bot.py
```

---

## 📄 Penggunaan

1. Tambahkan wallet address ke dalam file data.txt (satu per baris).


2. Jalankan script sesuai bahasa yang diinginkan (node bot.js atau python bot.py).


3. Masukkan jumlah thread yang ingin digunakan untuk pemrosesan multi-threading (1-10).


4. Script akan mulai berinteraksi dengan API dan mengumpulkan data.




---

## 📌 Perbedaan antara bot.js dan bot.py

Perbedaan antara bot.js (Node.js) dan bot.py (Python)

## 1. Logging:

bot.js: Menggunakan Winston untuk logging.

bot.py: Menggunakan RichHandler untuk logging dengan tampilan lebih rapi.



## 2. Multi-threading:

bot.js: Menggunakan async/await untuk eksekusi asinkron.

bot.py: Menggunakan ThreadPoolExecutor untuk eksekusi paralel.



## 3. Tampilan CLI:

bot.js: Menggunakan Chalk dan Progress untuk output berwarna dan progress bar.

bot.py: Menggunakan Rich dan TQDM untuk tampilan lebih interaktif.



## 4. API Requests:

bot.js: Menggunakan Axios untuk melakukan HTTP request.

bot.py: Menggunakan Requests untuk melakukan HTTP request.



## 5. Manajemen Input Data:

bot.js: Membaca data.txt menggunakan fs.promises.

bot.py: Membaca data.txt menggunakan fungsi open() dengan pengecekan os.path.exists().



## 6. Handling Waktu dan Delay:

bot.js: Menggunakan setTimeout() untuk jeda antara interaksi.

bot.py: Menggunakan time.sleep() untuk jeda antara interaksi.


---

## 🔧 Troubleshooting

Jika ada kesalahan pada koneksi API, pastikan koneksi internet stabil.

Jika data.txt tidak ditemukan, buat file data.txt secara manual dan tambahkan wallet address.

Jika script tidak berjalan, pastikan semua dependensi sudah terinstall dengan benar.



---


## 📜 Lisensi  

Script ini didistribusikan untuk keperluan pembelajaran dan pengujian. Penggunaan di luar tanggung jawab pengembang.  

Untuk update terbaru, bergabunglah di grup **Telegram**: [Klik di sini](https://t.me/sentineldiscus).


---

## 💡 Disclaimer
Penggunaan bot ini sepenuhnya tanggung jawab pengguna. Kami tidak bertanggung jawab atas penyalahgunaan skrip ini.
