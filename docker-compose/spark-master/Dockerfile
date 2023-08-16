FROM bitnami/spark:3.4
#COPY ./packages/* /opt/bitnami/spark/jars/
#COPY ./packages/* /opt/bitnami/spark/.ivy2/jars/
COPY ./src/* /src/
RUN ["pip3", "install", "kafka-python"]
CMD ["/bin/sh", "-c", \
"spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal1.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal2.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal3.py &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal4.py"]