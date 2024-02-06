
This project contains a basic MQTT publishing client, receiving client, and broker. 

The publisher is intended to be run in IoT devices (such as weather beacons) and publishes latitude, longitude, altitude, and temperature as a string. 

The receiver is intended to be run on a server and parses the received data. It provides more detailed location data, where possible.

Instructions provided to run the project in a Linux environment.

=======================================================================================================================

To start everything manually:

1. Install Mosquitto - http://www.steves-internet-guide.com/install-mosquitto-linux/

2. In the terminal, run "mosquitto -v" to start the broker.

3. In a second terminal, navigate to MQTT/publisher, run "apt-get -y update && apt-get install -y libmosquitto-dev", 
   "gcc publisher.c -o publisher -lmosquitto", and finally "./publisher" to start the publisher client.

4. In a third terminal, navigate to MQTT/receiver, run "pip install paho-mqtt", "pip install geopy",
   and finally "python3 receiver.py" to start the receiver client.

=======================================================================================================================

Github Repo - https://github.com/Nik-McKnight/MQTT
