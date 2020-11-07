# CS3219 OTOT Assignment Task D
An Apache Kafka cluster with 3 brokers, using Docker.


## Setup
Prerequisites 
* Docker & Docker Compose
* Python 3

Verify prerequisites:
```
$ docker -v   
$ docker-compose -v   
$ python -V
```

Install Python's Kafka library
```
$ python -m pip install kafka
$ python -m pip install kafka-python # also install this for Python 3.7+
```

Build & start containers locally  
```
$ docker-compose up -d
```
(-d for detached mode, run containers in the background)  
Ports used: (If necessary, the port numbers can be changed in `docker-compose.yml`)  
* 2181: Zookeeper
* 9091, 9092, 9093: the 3 brokers 
* 9000: Kafdrop, a monitoring interface for Kafka

Verify that the containers are running
```
$ docker-compose ps
      Name                     Command               State                     Ports                   
-------------------------------------------------------------------------------------------------------
kafka_kafdrop_1     /kafdrop.sh                      Up      0.0.0.0:9000->9000/tcp                    
kafka_kafka1_1      /etc/confluent/docker/run        Up      0.0.0.0:9091->9091/tcp, 9092/tcp          
kafka_kafka2_1      /etc/confluent/docker/run        Up      0.0.0.0:9092->9092/tcp                    
kafka_kafka3_1      /etc/confluent/docker/run        Up      9092/tcp, 0.0.0.0:9093->9093/tcp          
kafka_zookeeper_1   /docker-entrypoint.sh zkSe ...   Up      0.0.0.0:2181->2181/tcp, 2888/tcp, 3888/tcp
```

Create a topic "weather-updates", with replication factor 3
```
$ docker exec -it kafka_kafka1_1 kafka-topics --zookeeper zookeeper:2181 --create --topic weather-updates --partitions 1 --replication-factor 3

Created topic weather-updates.
```



Visit Kafdrop in a browser at `localhost:9000`  
![alt text](./images/Kafdrop_overall.jpg?raw=true)


## Publish and receive messages
Start the consumer, which will read messages from the topic weather-updates.
```
$ python consumer.py weather-updates
```
In another terminal, publish messages to the topic.
```
$ python producer_publish_msg.py weather-updates "it has started raining"
```
The message sent can be seen in the terminal running the consumer.
```
ConsumerRecord(topic='weather-updates', partition=0, offset=0, timestamp=1604742497967, timestamp_type=0, key=None, value=b'it has started raining', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=22, serialized_header_size=-1)
```

## Verify that another broker takes over after controller broker fails
From the interface in Kafdrop (visit `localhost:9000` in a browser), we can see which broker is the controller.  
![alt text](./images/brokers_before.jpg?raw=true)
In this case, kafka3 is the controller, so we stop it.
```
$ docker-compose stop kafka3
```
Verify that it has stopped
```
$ docker-compose ps
```
With the consumer running in a terminal, publish another message
```
$ python producer_publish_msg.py weather-updates "the rain has stopped"
```
In the terminal running the consumer, the published message can be seen
```
ConsumerRecord(topic='weather-updates', partition=0, offset=2, timestamp=1604744585846, timestamp_type=0, key=None, value=b'the rain has stopped', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=20, serialized_header_size=-1)
```
We can also verify in Kafdrop that another broker (kafka2 in this case) has become the controller

![alt text](./images/brokers_after.jpg?raw=true)

### References
https://medium.com/better-programming/a-simple-apache-kafka-cluster-with-docker-kafdrop-and-python-cf45ab99e2b9







