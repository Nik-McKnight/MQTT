FROM gcc:latest
COPY . /usr/src/publisher
WORKDIR /usr/src/publisher
RUN apt-get -y update && apt-get install -y libmosquitto-dev
RUN gcc publisher.c -o publisher -lmosquitto
CMD ["./publisher"]
