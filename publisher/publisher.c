#include <stdio.h>
#include <stdlib.h>
#include <mosquitto.h>
#include <unistd.h>
#include <string.h>

int main()
{
	// return values
	int rv;

	struct mosquitto *mosq;

	// Initialize
	mosquitto_lib_init();

	// Loop until connected to the broker.
	while (true)
	{

		// Create new client instance
		mosq = mosquitto_new("Location_Publisher", true, NULL);

		// Try to connect to the broker.
		// rv = mosquitto_connect(mosq, "localhost", 1883, 60);
		rv = mosquitto_connect(mosq, "50.112.8.166", 1883, 60);

		// Connection fails
		if (rv != 0)
		{
			printf("Client could not connect to broker! Error code: %d. Trying again.\n", rv);
			sleep(1);
		}

		// Connection successful
		else
		{
			break;
		}
	}

	printf("We are now connected to the broker!\n");

	// Build 100 random locations with raw values representing latitude,
	// longitude, temperature, and altitude and publish them to the broker.
	// Values will be interpreted by the receiver.
	for (int i = 0; i < 100; i++)
	{
		// On a 0 to 180 scale instead of -90 to 90.
		int latitude = (rand() % 180) + 1;

		// On a 0 to 360 scale instead of -180 to 180.
		int longitude = (rand() % 360) + 1;

		// 263 = difference between highest and lowest recorded temperature
		int temperature = rand() % 263;

		// 30500 ~= difference between Dead Sea and Everest elevation
		int altitude = rand() % 30500;

		// Create a string with all of the raw values included.
		char str[32];
		sprintf(str, "%d, %d, %d, %d, %d, ", i, latitude, longitude, altitude, temperature);

		// Pad the string with trailing whitespace.
		char result[32];
		sprintf(result, "%-31s", str);

		// Publish the data
		mosquitto_publish(mosq, NULL, "Location_Data", 32, result, 0, false);
		sleep(2);
	}

	// Disconnect from broker
	mosquitto_disconnect(mosq);

	// Destroy client instance
	mosquitto_destroy(mosq);

	// Free up used resources
	mosquitto_lib_cleanup();
	return 0;
}
