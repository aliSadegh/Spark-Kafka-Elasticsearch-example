FROM bitnami/kafka
COPY ./connect-plugins/confluentinc-kafka-connect-elasticsearch-14.0.8/ /opt/elastic-connector/plugin/
COPY ./connect-standalone.properties /opt/bitnami/kafka/config/
COPY ./elasticsearch-sink.properties /opt/elastic-connector/
CMD ["connect-standalone.sh",\
    "/opt/bitnami/kafka/config/connect-standalone.properties",\
    "/opt/elastic-connector/elasticsearch-sink.properties"]
