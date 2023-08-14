from kafka import KafkaConsumer

consumer = KafkaConsumer('goal1-topic', bootstrap_servers='localhost:9094')
for msg in consumer:
    print(msg.value)
print('ok')
