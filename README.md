### Sistem Pemberitahuan Lion Air

---

#### Arsitektur

Arsitektur yang dirancang untuk implementasi sistem pemberitahuan Lion Air kepada penumpang melibatkan beberapa komponen kunci sebagai berikut:

1. **Publisher (Lion Air)**
   - Lion Air bertindak sebagai Publisher yang mengirimkan pesan-pesan terkait jadwal boarding dan lokasi transit ke RabbitMQ sebagai message broker.

2. **AMQP Broker (RabbitMQ)**
   - Merupakan message broker yang menerima pesan dari Publisher (Lion Air) dan menyampaikannya kepada Subscriber (Penumpang).

3. **Subscriber (Penumpang)**
   - Penumpang adalah sistem atau entitas dari penumpang yang berlangganan (Subscriber) untuk menerima pemberitahuan mengenai jadwal boarding dan lokasi transit.

---

#### Langkah-langkah Implementasi

Untuk mengimplementasikan sistem ini, ikuti langkah-langkah berikut:

1. **Clone Repository**
   - Clone repository ini ke komputer Anda dengan perintah `git clone https://github.com/Rekabriyan/Sistem-Terdistribusi.git`.

2. **Jalankan Server**
   - Buka terminal atau command prompt di server dan jalankan server dengan perintah `python server.py`.

3. **Jalankan Client**
   - Buka terminal atau command prompt di client dan jalankan client dengan perintah `python client.py`.

4. **Lakukan Perubahan Schedule**
   - Di sisi server, lakukan perubahan jadwal boarding atau lokasi transit sesuai kebutuhan.

5. **Pastikan Notifikasi Berhasil**
   - Pastikan bahwa server berhasil mengirimkan notifikasi perubahan kepada client.
   - Periksa terminal atau log client untuk melihat notifikasi yang diterima.

