import pika
import json
from datetime import datetime

# Fungsi untuk menulis pesan ke file
def tulis_ke_file(file_name, message):
    with open(file_name, 'w') as file:
        file.write(message)

# Koneksi RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='lionair.southeastasia.cloudapp.azure.com', port=5672, virtual_host='/', credentials=pika.PlainCredentials('guest', 'guest')))
channel = connection.channel()

# Deklarasi exchange dan queue
channel.exchange_declare(exchange='boarding_exchange', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='boarding_exchange', queue=queue_name)


# Fungsi untuk menangani pesan
def callback(ch, method, properties, body):
    pesan = json.loads(body)
    if 'boarding_time' in pesan:
        # Mengambil waktu boarding dari pesan
        waktu_boarding = pesan['boarding_time']

        formatted_message = (
                "Kepada Yth. Penumpang,\n\n"
                f"Kami informasikan bahwa jadwal boarding penerbangan XYZ123 tujuan Kota A mengalami perubahan. "
                f"Boarding akan dimulai pada {waktu_boarding}. Mohon maaf atas ketidaknyamanan ini dan terima kasih atas pengertiannya.\n\n"
                "Salam,\nLion Air Group"
            )
        
        tulis_ke_file('boarding.txt', formatted_message)
    if 'transit_location' in pesan:
        lokasi_transit = pesan['transit_location']
        # Memastikan lokasi transit adalah string sebelum menulis ke file
        if isinstance(lokasi_transit, str):

            formatted_message = (
                "Kepada Yth. Penumpang,\n\n"
                f"Kami informasikan bahwa lokasi transit untuk penerbangan XYZ123 tujuan Kota A telah mengalami perubahan. "
                f"Lokasi transit baru adalah {lokasi_transit}. Mohon diperhatikan informasi ini untuk kenyamanan perjalanan Anda.\n\n"
                f"Kami mohon maaf atas ketidaknyamanan yang terjadi dan terima kasih atas pengertiannya.\n\n"
                "Salam,\nLion Air Group"
            )

            tulis_ke_file('lokasi.txt', formatted_message)

    print("Pesan diterima:", pesan)

# Mengonsumsi pesan
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('\nMenunggu pesan...')
channel.start_consuming()
