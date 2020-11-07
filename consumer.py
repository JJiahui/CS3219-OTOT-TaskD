from kafka import KafkaConsumer
import sys

topicName = sys.argv[1]
consumer = KafkaConsumer(topicName, bootstrap_servers=['localhost:9091','localhost:9092','localhost:9093'])
print("Reading messages from topic:", topicName)
for message in consumer:
    print(message)