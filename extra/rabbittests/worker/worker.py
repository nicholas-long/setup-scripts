import pika
import os
import random
from time import sleep

print("Starting worker")

rabbit = os.getenv('RABBIT')
queue = os.getenv('QUEUE')
print(f"Rabbit={rabbit}; queue={queue}", flush=True)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit, connection_attempts=50, retry_delay=1, heartbeat=0))
channel = connection.channel()

channel.queue_declare(queue=queue, durable=True, auto_delete=False)

for method_frame, properties, body in channel.consume(queue):
    print(f"Processing message: {body}", flush=True)
    sleep(1)
    if random.random() < 0.2:
        raise EOFError()
    print(f"Done: {body}", flush=True)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
