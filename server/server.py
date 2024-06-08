import pika
import json

# Koneksi RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='lionair.southeastasia.cloudapp.azure.com', port=5672, virtual_host='/', credentials=pika.PlainCredentials('guest', 'guest')))
channel = connection.channel()

# Deklarasi exchange dan queue
channel.exchange_declare(exchange='boarding_exchange', exchange_type='fanout')

# Fungsi untuk menambahkan pesan ke file
def tulis_ke_file(file_name, message):
    with open(file_name, 'w') as file:
        file.write(message)

# Fungsi untuk mengirim pesan
def kirim_pesan(pesan):
    channel.basic_publish(exchange='boarding_exchange', routing_key='', body=json.dumps(pesan))

# Fungsi untuk memeriksa apakah waktu boarding telah berubah
def cek_perubahan_waktu_boarding(waktu_boarding):
    with open('boarding.txt', 'r') as file:
        last_boarding_time = file.read().strip()
    return waktu_boarding != last_boarding_time

# Fungsi untuk memeriksa apakah lokasi transit telah berubah
def cek_perubahan_lokasi_transit(lokasi_transit):
    with open('lokasi.txt', 'r') as file:
        last_transit_location = file.read().strip()
    return lokasi_transit != last_transit_location

# Mendapatkan input dari pengguna
def input_jadwal():
    waktu_boarding = input("Masukkan waktu boarding (format: YYYY-MM-DD HH:MM): ")
    lokasi_transit = input("Masukkan lokasi transit: ")
    return {
        "boarding_time": waktu_boarding,
        "transit_location": lokasi_transit,
        "message_type": "boarding_update",
        "content": "Jadwal boarding dan lokasi transit telah diupdate secara manual."
    }

# Loop untuk menerima input dan mengirim pesan
while True:
    inputan = input("\nApakah Anda ingin memperbarui jadwal? (y/n): ")
    if inputan.lower() == 'y':
        pesan = input_jadwal()
        if not cek_perubahan_waktu_boarding(pesan['boarding_time']) and not cek_perubahan_lokasi_transit(pesan['transit_location']):
            print("Tidak ada perubahan yang perlu dikirim.")
        if cek_perubahan_waktu_boarding(pesan['boarding_time']):
            tulis_ke_file('boarding.txt', pesan['boarding_time'])
            kirim_pesan({"boarding_time": pesan['boarding_time'], "message_type": "boarding_update"})
            print("Waktu boarding berhasil dikirim:", pesan['boarding_time'])
        if cek_perubahan_lokasi_transit(pesan['transit_location']):
            tulis_ke_file('lokasi.txt', pesan['transit_location'])
            kirim_pesan({"transit_location": pesan['transit_location'], "message_type": "transit_update"})
            print("Lokasi transit berhasil dikirim:", pesan['transit_location'])
    elif inputan.lower() == 'n':
        break
    else:
        print("Masukkan y untuk ya atau n untuk tidak.")

connection.close()