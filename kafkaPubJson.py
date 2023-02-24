from time import sleep
import json
from json import dumps
from kafka import KafkaProducer
import random

# Instantiate Kafka producer and connect to cluster
producer = KafkaProducer(bootstrap_servers=['54.214.206.185:9092'],
                         value_serializer=lambda x:
                         bytes(json.dumps(x, default=str).encode('utf-8')))

# Converts coordinates from raw numbers to strings
def convertCoordinates(lat,lon):
    if (0 > lat):
        convertedLat = str(-lat) + "S"
    else:
        convertedLat = str(lat) + "N"

    if (0 > lon):
        convertedLon = str(-lon) + "W"
    else:
        convertedLon = str(lon) + "E"

    return [convertedLat,convertedLon]

# Produce random location data in same format as the MQTT publisher
for i in range(10):
    latitude = random.randrange(-90,90)
    longitude = random.randrange(-180,180)
    convertedCoordinates = convertCoordinates(latitude,longitude)
    temperature = str(random.randrange(-40,120)) + "F"
    altitude = str(random.randrange(20000,40000)) + "ft"
    airspeed = str(random.randrange(400,600)) + "mph"

    data = {"id": str(i), 
            "Latitude": convertedCoordinates[0], 
            "Longitude": convertedCoordinates[1], 
            "Altitude": altitude, 
            "Temperature": temperature, 
            "Airspeed": airspeed
            }

    producer.send('Flight_Data', data)
    sleep(1)