import influxdb_client, os, random
from confluent_kafka import Consumer
from geopy.geocoders import Nominatim
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Set consumer configs
conf = {'bootstrap.servers': "54.214.206.185:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest',
        "enable.auto.commit": False}
consumer = Consumer(conf)
# print
# The topic(s) to be subscribed to
topics = ["Location_Data"]

# InfluxDB configs
token = os.environ.get("INFLUXDB_TOKEN")
org = "atugan-dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="test"

# Define the write api
write_api = write_client.write_api(write_options=SYNCHRONOUS)

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
        id = rawData[0][2:]

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

    try:
        # Create random airSPeed
        airSpeed = str(random.randrange(400,600)) + "mph";

        # Format data to be sent to Influx DB
        point = (
                Point("Flight_Data")
                .tag("id", id)
                .field("Latitude", convertedCoordinates[0])
                .field("Longitude", convertedCoordinates[1])
                .field("Altitude", "%dft / %dm" % (altitudeFt, altitudeM))
                .field("Temperature", "%d°F / %d°C" % (tempFahrenheit,tempCelsius))
                .field("Air Speed", airSpeed)
            )

        # Push data to Influx DB
        write_api.write(bucket=bucket, org=org, record=point)

        # Commit kafka topic offset only on a successful push. This prevents data loss.
        consumer.commit(asynchronous=False);
    
    # Handle an error with the push to Influx
    except influxdb_client.rest.ApiException:
        print("    Data was not pushed to Influx database. Check to make sure you have the right token.")

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
    

        

# Subscribe to topics
consumer.subscribe(topics)

while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        convertData(msg.value())
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down.")
        break

    except:
        print("Something went wrong.")

consumer.close()