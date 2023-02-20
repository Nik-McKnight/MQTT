from time import sleep
from json import dumps
from kafka import KafkaProducer
import random

producer = KafkaProducer(bootstrap_servers=['54.214.206.185:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))



for e in range(1000):
    id = random.randrange(0,100000)
    latitude = random.randrange(0,180)
    longitude = random.randrange(0,360)
    temperature = random.randrange(0,263)
    altitude = random.randrange(0,30500)
    data = {'data' : "%d, %d, %d, %d, %d, " % (id, latitude, longitude, altitude, temperature)}
    producer.send('Location_Data', value=data)
    sleep(1)
