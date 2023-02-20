from time import sleep
from confluent_kafka import Consumer
from geopy.geocoders import Nominatim


conf = {'bootstrap.servers': "54.214.206.185:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}


consumer = Consumer(conf)

# The topic(s) to be subscribed to
topics = ["Location_Data"]

# Geolocator instance
geolocator = Nominatim(user_agent="atuganReceiver")

# Returns a real-world location, if possible, based on the given coordinates.
# Mostly returns nothing since geolocator only returns anything for land coordinates.
def getLocation(lat, lon):
    locationData = geolocator.reverse(str(lat) + "," + str(lon), language='en')
    return locationData

# converts integer coordinates into directional coordinates
# e.g. "-45,90" to "45°S, 90°E"
def convertCoordinates(lat,lon):
    if (0 > lat):
        convertedLat = str(-lat) + "°S"
    else:
        convertedLat = str(lat) + "°N"

    if (0 > lon):
        convertedLon = str(-lon) + "°W"
    else:
        convertedLon = str(lon) + "°E"

    return [convertedLat,convertedLon]

def convertData(data):
    # Converts data string into an array
    rawData = str(data).split(", ")

    try:
        id = rawData[0].split(": \"")[1]
    except:
        id = rawData[0]

    # latitude is received on a 0-180 scale, rather than -90 to 90
    latitude = int(rawData[1]) - 90

    # latitude is received on a 0-360 scale, rather than -180 to 180
    longitude = int(rawData[2]) - 180

    convertedCoordinates = convertCoordinates(latitude,longitude)

    locationData = getLocation(latitude, longitude)

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
    Topic: {msg.topic()}
    ID: {id}
    Latitude: {convertedCoordinates[0]}
    Longitude: {convertedCoordinates[1]}
    Altitude: {altitudeFt}ft / {altitudeM}m above sea level
    Temperature: {tempFahrenheit}°F / {tempCelsius}°C
    Location Detail: {locationData if locationData else "Probably somewhere in the ocean."}
    \n
    {'-' * 100}
    ''')

consumer.subscribe(topics)
    
while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        convertData(msg.value())
    except KeyboardInterrupt:
        break

consumer.close()
# try:
#     while True:
#         msg = consumer.poll(timeout=1.0)
#         if msg is None: 
#             continue
#         if msg.error():
#             print('Error: {}'.format(msg.error()))
#             continue
#         convertData(msg.value())
#         sleep(300)
#         # # else:
#         # if (msg != None):
#         #     convertData(msg.value())
#         # else:
#         #     continue
# except:
#     print("Something went wrong")

# finally:
#     # Close down consumer to commit final offsets.
#     consumer.close()


