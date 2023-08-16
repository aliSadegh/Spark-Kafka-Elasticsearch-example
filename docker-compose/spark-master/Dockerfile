FROM bitnami/spark:3.4
COPY ./src/* /src/
RUN ["pip3", "install", "kafka-python"]
CMD ["/bin/sh", "-c", "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal1.py > /dev/null &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal2.py > /dev/null &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal3.py > /dev/null &\
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /src/goal4.py > /dev/null"]