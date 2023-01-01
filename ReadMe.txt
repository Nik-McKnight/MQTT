
This project contains a basic MQTT publishing client, receiving client, and broker.

=======================================================================================================================

To start the project with Docker, simply run "docker compose up -d" in the terminal. 

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

You can also pull the following images and run them in the same container.

Publisher Docker - https://hub.docker.com/repository/docker/nikmcknight/atugan-publisher

Receiver Docker - https://hub.docker.com/repository/docker/nikmcknight/atugan-receiver

Broker Docker - https://hub.docker.com/repository/docker/nikmcknight/eclipse-mosquitto

=======================================================================================================================

Github Repo - https://github.com/Nik-McKnight/atugan
