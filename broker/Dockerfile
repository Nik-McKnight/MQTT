FROM eclipse-mosquitto:latest
COPY . /usr/src/broker
WORKDIR /usr/src/broker
CMD ["docker run -it -p 1883:1883 eclipse-mosquitto:latest mosquitto -c /mosquitto-no-auth.conf"]
