import influxdb_client, os, random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

# Instantiate mqtt client and connect to broker
mqtt_broker = "50.112.8.166"
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker)

# Instantiate kafka producer and connect to cluster
kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics["Location_Data"]
kafka_producer = kafka_topic.get_sync_producer()

# InfluxDB configs
token = os.environ.get("INFLUXDB_TOKEN")
org = "atugan-dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="test"

# Define the write api
write_api = write_client.write_api(write_options=SYNCHRONOUS)


# Fires when a message is received from the MQTT broker
def onMessage(client, userdata, msg):
    try:
        # Converts data string into an array
        rawData = msg.payload.decode()

        print("Received MQTT message: ", rawData)

        #Publish message to Kafka cluster
        kafka_producer.produce(rawData.encode('ascii'))
        print("KAFKA: Just published " + rawData + " to topic Location_Data")

    except:
        print("Something went wrong")


mqtt_client.loop_start()
mqtt_client.subscribe("Location_Data")
mqtt_client.on_message = onMessage
time.sleep(300)
mqtt_client.loop_end()

