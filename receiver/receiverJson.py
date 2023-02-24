import paho.mqtt.client as paho
import time
import json

# IP address of the broker
brokerIp = "50.112.8.166"

# The topic to be subscribed to
topic = "Flight_Data"

# Fires when a message is received from the broker
def onMessage(client, userdata, msg):
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

# Fires when connection is lost unexpectedly.
def onDisconnect(client, userdata, rc):
    if rc != 0:
        raise Exception("Lost connection to broker.")

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
