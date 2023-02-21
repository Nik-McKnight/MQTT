
import paho.mqtt.client as mqtt
from confluent_kafka import Consumer

# IP of the remote VerneMQ broker
mqtt_broker = "50.112.8.166"

# create function for callback
def on_publish(client,userdata,result):
    print("data published \n")
    pass

# create client object
mqttPub= mqtt.Client()

# assign function to callback
mqttPub.on_publish = on_publish

# establish connection
mqttPub.connect(mqtt_broker,1883)

# Create the kafka consumer instance
kafkaSub=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'latest'})

print('Kafka Consumer has been initiated...')

# Subcribe to topic
kafkaSub.subscribe(['Location_Data'])

while True:
    try:
        #timeout
        msg=kafkaSub.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue

        data=msg.value().decode('utf-8')

        print(data)

        #publish to VerneMQ broker
        mqttPub.publish("Location_Data", data)

    except KeyboardInterrupt:
        break

kafkaSub.close()