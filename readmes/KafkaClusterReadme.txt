Run following commands from the command line from ~/

Start the Cluster: kafka_2.13-3.4.0/bin/kafka-server-start.sh kafka_2.13-3.4.0/config/kraft/server.properties

Create a new topic: kafka_2.13-3.4.0/bin/kafka-topics.sh --create --topic [TOPIC NAME] --bootstrap-server [LOCALHOST OR REMOTE CLUSTER IP]:9092

Enable MQTT to Kafka Bridge: python3 mqttBridge.py

Enable Kafka to MQTT Bridge: python3 kafkaToMqttBridge.py

NOTES:  MQTT to Kafka bridge starts up right away. The Kafka to MQTT bridge takes a bit longer and may require a restart of the MQTT subscriber.
        Running both bridges at the same time will cause the same messages to be bounced back and forth instantly.

TODO:   Fix the noted issues.