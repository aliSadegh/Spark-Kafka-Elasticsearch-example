FROM bitnami/spark:3.4
#COPY ./spark-sql-kafka-0-10_2.13-3.4.1.jar /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.13-3.4.1.jar
COPY ./hadoop-client-runtime-3.3.4.jar /opt/bitnami/spark/jars/hadoop-client-runtime-3.3.4.jar
COPY ./hadoop-client-runtime-3.3.4.pom /opt/bitnami/spark/jars/hadoop-client-runtime-3.3.4.pom
COPY ./src/* /src/
RUN ["pip3", "install", "kafka-python"]
CMD ["/bin/sh", "-c", \
"spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal1.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal2.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal3.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal4.py"]