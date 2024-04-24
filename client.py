import pika
import json
from datetime import datetime

# Fungsi untuk menulis pesan ke file
def tulis_ke_file(file_name, message):
    with open(file_name, 'a') as file:
        file.write(message + '\n')

# Koneksi RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='moaibad.southeastasia.cloudapp.azure.com', port=5672, virtual_host='/', credentials=pika.PlainCredentials('guest', 'guest')))
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
        # Mengambil tanggal dari waktu boarding
        tanggal_boarding = pesan['boarding_time'].split(' ')[0]
        tulis_ke_file('boarding.txt', tanggal_boarding)
    if 'transit_location' in pesan:
        lokasi_transit = pesan['transit_location']
        # Memastikan lokasi transit adalah string sebelum menulis ke file
        if isinstance(lokasi_transit, str):
            tulis_ke_file('lokasi.txt', lokasi_transit)

    print("Pesan diterima:", pesan)

# Mengonsumsi pesan
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Menunggu pesan...')
channel.start_consuming()
