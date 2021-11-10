from flask import Flask, render_template, request
import pika
import os

rabbit = os.getenv('RABBIT')
queue = os.getenv('QUEUE')
print(f"Rabbit={rabbit}; queue={queue}", flush=True)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit, connection_attempts=50, retry_delay=1, heartbeat=0))
channel = connection.channel()

channel.queue_declare(queue=queue, durable=True, auto_delete=False)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/add', methods=["POST"])
def add():
    count = int(request.form['count'])
    messages = [f"Message {c}" for c in range(0, count)]
    for m in messages:
        channel.basic_publish(exchange='', routing_key=queue, body=m)
    return 'added\n'