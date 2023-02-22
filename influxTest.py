import influxdb_client, os, time, random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "atugan-dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="test"

# Define the write api
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# data = {
#   "point1": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 23,
#   },
#   "point2": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 30,
#   },
#   "point3": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 28,
#   },
#   "point4": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 32,
#   },
#   "point5": {
#     "location": "Klamath",
#     "species": "bees",
#     "count": 29,
#   },
#   "point6": {
#     "location": "Portland",
#     "species": "ants",
#     "count": 40,
#   },
#   }
data = {
  "point1": {
    "id": "1",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)
  },
  "point2": {
    "id": "2",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)  },
  "point3": {
    "id": "3",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)  },
  "point4": {
    "id": "4",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)  },
  "point5": {
    "id": "5",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)  },
  "point6": {
    "id": "6",
    "Latitude": random.randrange(-90, 90),
    "Longitude":random.randrange(-180, 180),
    "Altitude":random.randrange(10000, 40000),
    "Temperature" : random.randrange(-50,120),
    "Air Speed" : random.randrange(400,600)  },
  }
for j in range (5):
    Latitude = str(random.randrange(-90, 90)) + "°"
    Longitude = str(random.randrange(-180, 180)) + "°"
    Altitude = str(random.randrange(10000, 40000)) + "ft"
    Temperature = str(random.randrange(-50,120)) + "°F"
    AirSpeed = str(random.randrange(400,600)) + "mph"
    for i in range(10):
        point = (
            Point("Flight_Data")
            .tag("id", i)
            .field("Latitude", Latitude)
            .field("Longitude", Longitude)
            .field("Altitude", Altitude)
            .field("Temperature", Temperature)
            .field("Air Speed", AirSpeed)
        )
        write_api.write(bucket=bucket, org=org, record=point)
    time.sleep(1) # separate points by 1 second

# for key in data:
#   point = (
#     Point("Flight")
#     .tag("id", data[key]["id"])
#     .field("Latitude", data[key]["Latitude"])
#     .field("Longitude", data[key]["Longitude"])
#     .field("Altitude", data[key]["Longitude"])
#     .field("Temperature", data[key]["Longitude"])
#     .field("Air Speed", data[key]["Longitude"])

#   )
#   write_api.write(bucket=bucket, org=org, record=point)
#   time.sleep(1) # separate points by 1 second

# for key in data:
#   point = (
#     Point("census")
#     .tag("location", data[key]["location"])
#     .field(data[key]["species"], data[key]["count"])
#   )
#   write_api.write(bucket=bucket, org=org, record=point)
#   time.sleep(1) # separate points by 1 second

# data = {
#   "point1": {
#     # "id": 1,
#     "Latitude": random.randrange(-90, 90),
#     "Longitude":random.randrange(-180, 180),
#     "Altitude":random.randrange(10000, 40000),
#     # "Temperature" : random.randrange(-50,120),
#     # "Air Speed" : random.randrange(400,600)
#   },
#   "point2": {
#     # "id": 1,
#     "Latitude": random.randrange(-90, 90),
#     "Longitude":random.randrange(-180, 180),
#     "Altitude":random.randrange(10000, 40000),
#     # "Temperature" : random.randrange(-50,120),
#     # "Air Speed" : random.randrange(400,600)
#   },"point3": {
#     # "id": 1,
#     "Latitude": random.randrange(-90, 90),
#     "Longitude":random.randrange(-180, 180),
#     "Altitude":random.randrange(10000, 40000),
#     # "Temperature" : random.randrange(-50,120),
#     # "Air Speed" : random.randrange(400,600)
#   },"point4": {
#     # "id": 1,
#     "Latitude": random.randrange(-90, 90),
#     "Longitude":random.randrange(-180, 180),
#     "Altitude":random.randrange(10000, 40000),
#     # "Temperature" : random.randrange(-50,120),
#     # "Air Speed" : random.randrange(400,600)
#   },"point5": {
#     # "id": 1,
#     "Latitude": random.randrange(-90, 90),
#     "Longitude":random.randrange(-180, 180),
#     "Altitude":random.randrange(10000, 40000),
#     # "Temperature" : random.randrange(-50,120),
#     # "Air Speed" : random.randrange(400,600)
#   },
#   }

# for key in data:
#     # "obj" : {
#     #     "id": i,
#     #     "Latitude": random.randrange(-90, 90),
#     #     "Longitude":random.randrange(-180, 180),
#     #     "Altitude":random.randrange(10000, 40000),
#     #     "Temperature" : random.randrange(-50,120),
#     #     "Air Speed" : random.randrange(400,600)
#     # }
#     point = (
#         Point("Location_Data")
#         .tag("Latitude", data[key]["Latitude"])
#         .field(data[key]["Longitude"], data[key]["Altitude"])
#         # .field(data[key]["Latitude"], data[key]["Longitude"], 
#         # data[key]["Altitude"], data[key]["Temperature"], data[key]["Air Speed"])
#     )
#     write_api.write(bucket=bucket, org=org, record=point)
#     time.sleep(1) # separate points by 1 second



# print("Complete. Return to the InfluxDB UI.")

# from flightsql import FlightSQLClient

# query = """SELECT *
# FROM 'census'
# WHERE time >= now() - interval '24 hours'
# AND ('bees' IS NOT NULL OR 'ants' IS NOT NULL)"""

# # Define the query client
# query_client = FlightSQLClient(
#   host = "us-east-1-1.aws.cloud2.influxdata.com",
#   token = os.environ.get("INFLUXDB_TOKEN"),
#   metadata={"bucket-name": "test"})

# # Execute the query
# info = query_client.execute(query)
# reader = query_client.do_get(info.endpoints[0].ticket)

# # Convert to dataframe
# data = reader.read_all()
# df = data.to_pandas().sort_values(by="time")
# print(df)