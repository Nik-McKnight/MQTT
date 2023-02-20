import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

mqtt_broker = "50.112.8.166"
mqtt_client = mqtt.Client("BridgeMQTT2Kafka")
mqtt_client.connect(mqtt_broker)

kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics["Location_Data"]
kafka_producer = kafka_topic.get_sync_producer()

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

    return convertedLat + ", " + convertedLon

# Fires when a message is received from the broker
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
        altitudeFt = int(rawData[3]) - 1410
        altitudeM = round(altitudeFt / 3.281)

        # Temperature is received from 0 to 263, representing the difference
        # between the highest and lowest recorded temperatures on Earth.
        tempFahrenheit = int(rawData[4]) - 129
        tempCelsius = round((tempFahrenheit - 32) * 5 / 9)

        # Print all the data
        #data =  "ID: %s, %s, %sft, %s°" % (id, convertedCoordinates, altitudeFt, tempFahrenheit)
        #data =  "ID: " + id + ", " + convertedCoordinates + ", " +  str(altitudeFt) + ", " + str(tempFahrenheit)
        data =  "ID: " + id + ", " + convertedCoordinates + ", " +  str(altitudeFt) + ", " + str(tempFahrenheit)

        print("Received MQTT message: ", data)
        kafka_producer.produce(data.encode('ascii'))
        print("KAFKA: Just published " + data + " to topic Location_Data")
    except:
        print("K2F input detected")
    # data = msg.payload.decode();
    # kafka_producer.produce(data.encode('ascii'))
    # print("KAFKA: Just published " + data + " to topic Location_Data")


mqtt_client.loop_start()
mqtt_client.subscribe("Location_Data")
mqtt_client.on_message = onMessage
time.sleep(300)
mqtt_client.loop_end()