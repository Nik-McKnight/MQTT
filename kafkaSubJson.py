from time import sleep
import json
from json import loads
from confluent_kafka import Consumer

# Set consumer configs
conf = {'bootstrap.servers': "54.214.206.185:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}
consumer = Consumer(conf)

# The topic(s) to be subscribed to
topics = ["Location_Data"]

def printData(rawData):
    # Convert encoded data to JSON.
    data = json.loads(rawData)
    
    # Print all the data
    print (f'''
    Topic: {msg.topic()}
    ID: {data["id"]}
    Latitude: {data["Latitude"]}
    Longitude: {data["Longitude"]}
    Altitude: {data["Altitude"]} above sea level
    Temperature: {data["Temperature"]}
    Airspeed: {data["Airspeed"]}
    \n
    {'-' * 100}
    ''')

# Subscribe to topics
consumer.subscribe(topics)

while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        printData(msg.value())
    except KeyboardInterrupt:
        break

consumer.close()