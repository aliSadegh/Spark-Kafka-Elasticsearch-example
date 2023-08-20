import os
import random
import time
from json import dumps

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

P_BOOTSTRAP_SERVERS = os.getenv("P_BOOTSTRAP_SERVERS") .split(',')
TOPIC = os.getenv("TOPIC")

if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=P_BOOTSTRAP_SERVERS,
            value_serializer=lambda x:
            dumps(x).encode('utf-8'))
    while True:
        producer.send(TOPIC, value={"server": f"s_v{random.randint(0, 10)}",
            "client_ip": f"154.85.126.{random.randint(0, 255)}",
            "method": f"{random.choice(['POST', 'GET', 'PUT'])}",
            "status": f"{random.choice([200, 204, 201, 400, 403, 429, 500, 503])}",
            "request_time": f"{round(random.uniform(0.01, 1.01), 2)}",
            "host": f"api_{random.randint(0, 50)}.example.com",
            "country": f"{random.choice(['FR', 'US', 'IR', 'EN', 'GE'])}",
            "@timestamp": f"{time.time()}"})
        time.sleep(0.01)
