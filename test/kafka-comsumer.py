import sys
from kafka import KafkaConsumer

topic_name = sys.argv[1]
consumer = KafkaConsumer(topic_name, bootstrap_servers='localhost:9094')
for msg in consumer:
    print(msg.value)