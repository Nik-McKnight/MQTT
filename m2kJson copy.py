import paho.mqtt.client as paho
from kafka import KafkaProducer
import json
import time

# IP address of the broker
brokerIp = "50.112.8.166"

# The topic to be subscribed to
topic = "Flight_Data"

# # Instantiate mqtt client and connect to broker
# mqtt_broker = "50.112.8.166"
# mqtt_client = mqtt.Client()
# mqtt_client.connect(mqtt_broker)

# Instantiate Kafka producer and connect to cluster
producer = KafkaProducer(bootstrap_servers=['54.214.206.185:9092'],
                         value_serializer=lambda x:
                         bytes(json.dumps(x, default=str).encode('utf-8')))


# Fires when a message is received from the MQTT broker
def onMessage(client, userdata, msg):
    try:
        # # Converts data string into an array
        # rawData = msg.payload.decode().split(", ")

        # id = rawData[0]

        # # latitude is received on a 0-180 scale, rather than -90 to 90
        # latitude = int(rawData[1]) - 90

        # # latitude is received on a 0-360 scale, rather than -180 to 180
        # longitude = int(rawData[2]) - 180

        # convertedCoordinates = convertCoordinates(latitude,longitude)

        # # altitude is received from 0' to 30500', representing the
        # # distance between the Dead Sea (-1410ft) and Everest (29000ft)
        # altitude = str(int(rawData[3]) - 1410) + "ft"

        # # Temperature is received from 0 to 263, representing the difference
        # # between the highest and lowest recorded temperatures on Earth.
        # temperature = str(int(rawData[4]) - 129) + "F"

        # airspeed = str(rawData[5]) + "mph"

        # print("Received MQTT message: ", rawData)

        # # Convert data to json
        # data = {"id": str(id), 
        #     "Latitude": convertedCoordinates[0], 
        #     "Longitude": convertedCoordinates[1], 
        #     "Altitude": altitude, 
        #     "Temperature": temperature, 
        #     "Airspeed": airspeed
        #     }

            # Convert encoded data back to JSON.
        data = json.loads(msg.payload.decode())
        # Print all the data
        print (f'''
        Topic: {topic}
        ID: {data["id"]}
        Latitude: {data["Latitude"]}
        Longitude: {data["Longitude"]}
        Altitude: {data["Altitude"]} above sea level
        Temperature: {data["Temperature"]}
        Airspeed: {data["Airspeed"]}
        \n
        {'-' * 100}
        ''')

        #Publish message to Kafka cluster
        producer.send('Location_Data', data)
        print("KAFKA: Just published json to topic Location_Data")

    except:
        print("Something went wrong")

# Fires when connection is lost unexpectedly.
def onDisconnect(client, userdata, rc):
    if rc != 0:
        raise Exception("Lost connection to broker.")

# mqtt_client.loop_start()
# mqtt_client.subscribe("Location_Data")
# mqtt_client.on_message = onMessage
# time.sleep(300)
# mqtt_client.loop_end()

while(True):
    try:
        # Create the client
        client = paho.Client("Location_Receiver")
        client.on_message = onMessage
        client.on_disconnect = onDisconnect
        # Connect the client to the broker
        # client.connect("localhost", 1883, 60)
        client.connect(brokerIp, 1883, 60)
        # Subscribe the client to the given topic
        client.subscribe(topic)
        print(f"\nNow subscribed to {topic}")
        print('-' * 104)
    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down.")
        client.disconnect()
        break;
    
    except:
        print("Could not connect to broker. Trying again.")
        time.sleep(1)

    else:
        try:
            # Keep running until the program is stopped manually
            client.loop_forever()
            
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Shutting down.")
            client.disconnect()
            break;
        
        except Exception as e:
            print(e)
            client.disconnect()
