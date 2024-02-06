
This project contains a basic MQTT publishing client, receiving client, and broker.

=======================================================================================================================

To start everything manually:

1. In publisher/publisher.c, uncomment line 24 and comment out line 25.

2. In receiver/receiver.py, uncomment line 69 and comment out line 70.

3. In the terminal, run "mosquitto -v" to start the broker.

4. In a second terminal, navigate to atugan/publisher, run "apt-get -y update && apt-get install -y libmosquitto-dev", 
   "gcc publisher.c -o publisher -lmosquitto", and finally "./publisher" to start the publisher client.

5. In a third terminal, navigate to atugan/receiver, run "pip install paho-mqtt", "pip install geopy",
   and finally "python3 receiver.py" to start the receiver client.

=======================================================================================================================

Github Repo - https://github.com/Nik-McKnight/MQTT
