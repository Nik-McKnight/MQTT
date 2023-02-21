from time import sleep
from json import dumps
from kafka import KafkaProducer
import random

# Instantiate Kafka producer and connect to cluster
producer = KafkaProducer(bootstrap_servers=['54.214.206.185:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

# Produce random location data in same format as the MQTT publisher
for e in range(10):
    id = random.randrange(0,100000)
    latitude = random.randrange(0,180)
    longitude = random.randrange(0,360)
    temperature = random.randrange(0,263)
    altitude = random.randrange(0,30500)
    data = {'data' : "%d, %d, %d, %d, %d, " % (id, latitude, longitude, altitude, temperature)}
    producer.send('Location_Data', value=data)
    sleep(1)