import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json
from json import dumps
import time

# Instantiate mqtt client and connect to broker
mqtt_broker = "50.112.8.166"
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker)

# # Instantiate kafka producer and connect to cluster
# kafka_client = KafkaClient(hosts="localhost:9092")
# kafka_topic = kafka_client.topics["Location_Data"]
# kafka_producer = kafka_topic.get_sync_producer()
# Instantiate Kafka producer and connect to cluster
producer = KafkaProducer(bootstrap_servers=['54.214.206.185:9092'],
                         value_serializer=lambda x:
                         bytes(json.dumps(x, default=str).encode('utf-8')))


# converts integer coordinates into directional coordinates
# e.g. "-45,90" to "45°S, 90°E"
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

# Fires when a message is received from the MQTT broker
def onMessage(client, userdata, msg):
    try:
        # Converts data string into an array
        rawData = msg.payload.decode().split(", ")

        id = rawData[0]

        # latitude is received on a 0-180 scale, rather than -90 to 90
        latitude = int(rawData[1]) - 90

        # latitude is received on a 0-360 scale, rather than -180 to 180
        longitude = int(rawData[2]) - 180

        convertedCoordinates = convertCoordinates(latitude,longitude)

        # altitude is received from 0' to 30500', representing the
        # distance between the Dead Sea (-1410ft) and Everest (29000ft)
        altitude = str(int(rawData[3]) - 1410) + "ft"

        # Temperature is received from 0 to 263, representing the difference
        # between the highest and lowest recorded temperatures on Earth.
        temperature = str(int(rawData[4]) - 129) + "F"

        airspeed = str(rawData[5]) + "mph"

        print("Received MQTT message: ", rawData)

        # Convert data to json
        data = {"id": str(id), 
            "Latitude": convertedCoordinates[0], 
            "Longitude": convertedCoordinates[1], 
            "Altitude": altitude, 
            "Temperature": temperature, 
            "Airspeed": airspeed
            }

        #Publish message to Kafka cluster
        producer.send('Location_Data', data)
        print("KAFKA: Just published json to topic Location_Data")

    except:
        print("Something went wrong")


mqtt_client.loop_start()
mqtt_client.subscribe("Location_Data")
mqtt_client.on_message = onMessage
time.sleep(300)
mqtt_client.loop_end()

