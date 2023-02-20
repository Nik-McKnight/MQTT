import paho.mqtt.client as mqtt
from pykafka import KafkaClient
# from confluent_kafka import Consumer
import time

mqtt_broker = "50.112.8.166"
mqtt_to_kafka = mqtt.Client("BridgeMQTT2Kafka")
# kafka_to_mqtt = mqtt.Client("BridgeKafka2MQTT")
mqtt_to_kafka.connect(mqtt_broker,1883)
# kafka_to_mqtt.connect(mqtt_broker, 1883)
kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics["Location_Data"]
kafka_producer = kafka_topic.get_sync_producer()
kafka_consumer = kafka_topic.get_simple_consumer()
# kafkaSub=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
# kafkaPub=Producer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})

def on_publish(client,userdata,result):  
    msg=kafka_consumer.poll(1.0) #timeout
    if msg is None:
        print("no message")
    if msg.error():
        print('Error: {}'.format(msg.error()))
    else:
        data=msg.value().decode('utf-8')
        print(data)
        #publish to VerneMQ broker
        mqtt_to_kafka.publish("Location_Data", data)           
        print("data published \n")

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

# assign function to callback

mqtt_to_kafka.loop_start()
mqtt_to_kafka.subscribe("Location_Data")
mqtt_to_kafka.on_message = onMessage
mqtt_to_kafka.on_publish = on_publish 
time.sleep(300)
mqtt_to_kafka.loop_end()


# while True:
#     msg=kafkaSub.poll(1.0) #timeout
#     if msg is None:
#         print("m2k")
#         mqtt_to_kafka.subscribe("Location_Data")
#         mqtt_to_kafka.on_message = onMessage
#     else:
#         if msg.error():
#             print('Error: {}'.format(msg.error()))
#             continue
#         data=msg.value().decode('utf-8')
#         print("k2m")
#         #publish to VerneMQ broker
#         mqtt_to_kafka.publish("Location_Data", data)
#         continue
# kafkaSub.close()

# kafka_client = KafkaClient(hosts="localhost:9092")
# kafka_topic = kafka_client.topics["Location_Data"]
# kafka_producer = kafka_topic.get_sync_producer()
# kafkaSub=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})

# def on_publish(client,userdata,result):             
#     print("data published \n")

# # Fires when a message is received from the broker
# def onMessage(client, userdata, msg):
#     try:
#         # Converts data string into an array
#         # rawData = msg.payload.decode().split(", ")
#         rawData = msg.payload.decode()

#         print("Received MQTT message: ", rawData)
#         kafka_producer.produce(rawData.encode('ascii'))
#         print("KAFKA: Just published " + rawData + " to topic Location_Data")
#     except:
#         print("K2F input detected")
#     # data = msg.payload.decode();
#     # kafka_producer.produce(data.encode('ascii'))
#     # print("KAFKA: Just published " + data + " to topic Location_Data")

# # assign function to callback
# kafka_to_mqtt.on_publish = on_publish 
# mqtt_to_kafka.on_message = onMessage

# kafkaSub.subscribe(['Location_Data'])
# mqtt_to_kafka.subscribe("Location_Data")


# while True:
#     msg=kafkaSub.poll(1.0) #timeout
#     if msg is None:
#         print("m2k")
#     else:
#         if msg.error():
#             print('Error: {}'.format(msg.error()))
#             continue
#         data=msg.value().decode('utf-8')
#         print("k2m")
#         #publish to VerneMQ broker
#         kafka_to_mqtt.publish("Location_Data", data)
#         continue
# kafkaSub.close()


# mqtt_to_kafka.loop_start()
# mqtt_to_kafka.subscribe("Location_Data")
# mqtt_to_kafka.on_message = onMessage
# time.sleep(300)
# mqtt_to_kafka.loop_end()