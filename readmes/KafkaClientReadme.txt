Run following commands from the command line from ~/

Create a new topic: kafka_2.13-3.4.0/bin/kafka-topics.sh --create --topic [TOPIC NAME] --bootstrap-server [REMOTE CLUSTER IP]:9092
                    ex: kafka_2.13-3.4.0/bin/kafka-topics.sh --create --topic Location_Data --bootstrap-server 54.214.206.185:9092

Publish to a topic: python3 kafkaPub.py 
                    OR
                    kafka_2.13-3.4.0/bin/kafka-console-producer.sh --topic Location_Data --bootstrap-server 54.214.206.185:9092

Read from a topic:  python3 kafkaSub.py 
                    OR
                    kafka_2.13-3.4.0/bin/kafka-console-consumer.sh --topic Location_Data --from-beginning --bootstrap-server 54.214.206.185:9092

NOTES:  Will need two terminals to run both.