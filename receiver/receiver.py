import paho.mqtt.client as paho
import sys
import time
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="atuganReceiver")

# The topic to be subscribed to
topic = "Location_Data"

# Returns a location, if possible, based on the given coordinates.
# Mostly returns nothing since geolocator only returns something for land coordinates.
def getLocation(lat, lon):
    locationData = geolocator.reverse(str(lat) + "," + str(lon), language='en')
    return locationData

# converts integer coordinates into directional coordinates
# e.g. "-45,90" to "45°S, 90°E"
def convertCoordinates(lat,lon):
    # Defaults to North and East
    convertedLat = str(lat) + "°N"
    convertedLon = str(lon) + "°E"

    # Flips to South or West if the integer is negative
    if (0 > lat):
        convertedLat = str(-lat) + "°S"
    if (0 > lon):
        convertedLon = str(-lon) + "°W"

    return [convertedLat,convertedLon]

# Fires when a message is received from the broker
def onMessage(client, userdata, msg):
    # Converts data string into and array
    rawData = msg.payload.decode().split(", ")
    id = rawData[0]
    # latitude is received on a 0-180 scale, rather than -90 to 90
    rawLatitude = int(rawData[1]) - 90
    # latitude is received on a 0-360 scale, rather than -180 to 180
    rawLongitude = int(rawData[2]) - 180
    convertedCoordinates = convertCoordinates(rawLatitude,rawLongitude)
    locationData = getLocation(rawLatitude, rawLongitude)
    # altitude is received from 0' to 30500', representing the
    # distance between the Dead Sea (-1410ft) and Everest (29000ft)
    altitudeFt = int(rawData[3]) - 1410
    altitudeM = round(altitudeFt / 3.281)
    # Temperature is received from 0 to 263, representing the difference
    # between the highest and lowest recorded temperatures on Earth.
    tempFahrenheit = int(rawData[4]) - 129
    tempCelsius = round((tempFahrenheit - 32) * 5 / 9)
    # Print all the data
    print (f'''
    Topic: {topic}
    ID: {id}
    Latitude: {convertedCoordinates[0]}
    Longitude: {convertedCoordinates[1]}
    Altitude: {altitudeFt}ft / {altitudeM}m above sea level
    Temperature: {tempFahrenheit}°F / {tempCelsius}°C
    Location Detail: {locationData if locationData else "Probably somewhere in the ocean."}
    {'-' * 100}
    ''')

# Create the client
client = paho.Client("Location_Receiver")
client.on_message = onMessage

# Connect the client to the broker. Change the host name to connect to a different machine.
while(True):
    try:
        client.connect("localhost", 1883, 60)
        # client.connect("10.5.0.5", 1883, 60)
        break;
    except:
        print("Could not connect to broker. Trying again.")
        time.sleep(1)


# Subscribe the client to the given topic
client.subscribe(topic)
print(f"\nNow subscribed to {topic}")
print('-' * 104)

try:
    # Keep running until the program is stopped manually
    client.loop_forever()
except Exception as e:
    print(e)
    print("Disconnecting from broker.")
    client.disconnect()



