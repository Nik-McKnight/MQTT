
This project contains a basic MQTT publishing client, receiving client, and broker, a Kafka publisher, recceiver, and broker, and two bridges between the two.

=======================================================================================================================

You will need the private key file (KafkaCluster.pem) to log in to any of the following instances using SSH.

If you get an “unprotected key file” warning, run “chmod 400 KafkaCluster.pem” in whatever directory contains the key file.
Set-Up MQTT Broker and Clients

    Open one “MQTT_Broker” instance.

    Run "sudo service vernemq start" to start the MQTT broker.

    Run "sudo vernemq ping". It will respond with "pong" if the broker is running.

    Open two “MQTT_Client” instances.

    Run "python3 sub/subscriber.py" in one instance to start the MQTT subscriber.

    Run "./pub/mqttPublisher" in the other instance to start the MQTT publisher.

    The subscriber should now be receiving the data published by the publisher.

Set-Up Kafka Broker and Clients

    Open one “Kafka_Cluster” instance.

    Run "kafka_2.13-3.4.0/bin/kafka-server-start.sh kafka_2.13-3.4.0/config/kraft/server.properties" to start the Kafka server.

    Open two “Kafka_Client” instances.

    Run "python3 kafkaSub.py" in one instance to start the Kafka subscriber.

    Run "python3 kafkaPub.py" in the other instance to start the Kafka publisher.

    The subscriber should now be receiving the data published by the publisher.

Set-Up MQTT-Kafka Bridge

Note: There are two bridge programs, publishing from MQTT to Kafka and vice versa. Only one can be run at a time.

    Open another "Kafka_Cluster" instance.

    Run "python3 mqttBridge.py". If the MQTT broker, Kafka Cluster, MQTT Publisher, and Kafka Subscriber are all running, the Kafka Subscriber should be receiving data published by the MQTT Publisher.

    Stop the MQTT bridge with ctrl+c.

    Run "python3 kafkaToMqttBridge.py". If the MQTT broker, Kafka Cluster, MQTT Subscriber, and Kafka Publisher are all running, the MQTT Subscriber should be receiving data published by the Kafka Publisher.
