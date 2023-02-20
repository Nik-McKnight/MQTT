import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

mqtt_broker = "50.112.8.166"
mqtt_client = mqtt.Client("BridgeMQTT2Kafka")
mqtt_client.connect(mqtt_broker)

kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics["Location_Data"]
kafka_producer = kafka_topic.get_sync_producer()


# Fires when a message is received from the broker
def onMessage(client, userdata, msg):
    try:
        # Converts data string into an array
        # rawData = msg.payload.decode().split(", ")
        rawData = msg.payload.decode()

        print("Received MQTT message: ", rawData)
        kafka_producer.produce(rawData.encode('ascii'))
        print("KAFKA: Just published " + rawData + " to topic Location_Data")
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


