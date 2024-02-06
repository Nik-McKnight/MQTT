
This project contains a basic MQTT publishing client, receiving client, and broker.

Instructions provided to run the project(s) in a Linux environment.

=======================================================================================================================

To start everything manually:

1. Install Mosquitto - http://www.steves-internet-guide.com/install-mosquitto-linux/

2. In publisher/publisher.c, uncomment line 24 and comment out line 25.

3. In receiver/receiver.py, uncomment line 69 and comment out line 70.

4. In the terminal, run "mosquitto -v" to start the broker.

5. In a second terminal, navigate to MQTT/publisher, run "apt-get -y update && apt-get install -y libmosquitto-dev", 
   "gcc publisher.c -o publisher -lmosquitto", and finally "./publisher" to start the publisher client.

6. In a third terminal, navigate to MQTT/receiver, run "pip install paho-mqtt", "pip install geopy",
   and finally "python3 receiver.py" to start the receiver client.

=======================================================================================================================

Github Repo - https://github.com/Nik-McKnight/MQTT
