import sys
from kafka import KafkaProducer

bootstrap_servers = ['localhost:9091', 'localhost:9092', 'localhost:9093']
topicName = sys.argv[1]
msg = sys.argv[2]

producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

producer.send(topicName, msg.encode())
producer.flush()
