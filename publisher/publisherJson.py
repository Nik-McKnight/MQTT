import paho.mqtt.client as paho
import time
import json
import random

# IP address of the broker
brokerIp = "50.112.8.166"

# The topic to be subscribed to
topic = "Flight_Data"

# Used to track spot in publish loop on unexpected disconnect
i = 0;

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

# Fires when connection is lost unexpectedly.
def onDisconnect(client, userdata, rc):
    if rc != 0:
        raise Exception("Lost connection to broker.")

while(True):
    try:
        # Create the client
        client = paho.Client("Location_Publisher")
        client.on_disconnect = onDisconnect
        # Connect the client to the broker
        # client.connect("localhost", 1883, 60)
        client.connect(brokerIp, 1883, 60)
        print("Connected to broker.")
    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down.")
        client.disconnect()
        break;
    
    except:
        print("Could not connect to broker. Trying again.")
        time.sleep(1)
        
    else:
        try:
            # Produce random flight data
            for j in range(i, 10):
                latitude = random.randrange(-90,90)
                longitude = random.randrange(-180,180)
                convertedCoordinates = convertCoordinates(latitude,longitude)
                temperature = str(random.randrange(-40,120)) + "F"
                altitude = str(random.randrange(20000,40000)) + "ft"
                airspeed = str(random.randrange(400,600)) + "mph"

                #Convert data to JSON
                data = {"id": str(i), 
                       "Latitude": convertedCoordinates[0], 
                        "Longitude": convertedCoordinates[1], 
                        "Altitude": altitude, 
                        "Temperature": temperature, 
                        "Airspeed": airspeed
                        }

				# Stringify JSON and publish
                client.publish(topic, json.dumps(data))
                i += 1
                print(data)
                time.sleep(1)
            client.disconnect()
            print("Disconnected from broker. Shutting down.")
            break;
        
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Shutting down.")
            client.disconnect()
            break;
        
        except Exception as e:
            print(e)
            client.disconnect()
