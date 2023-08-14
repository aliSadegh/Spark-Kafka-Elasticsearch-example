#Calculates successful requests for each country minutely and produces it to another topic.

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, FloatType, TimestampType

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "test-inter"

SCHEMA = StructType([
    StructField("server", StringType()),
    StructField("client_ip", StringType()),
    StructField("method", StringType()),
    StructField("status", StringType()),
    StructField("request_time", StringType()),
    StructField("host", StringType()),
    StructField("country", StringType()),
    StructField("@timestamp", StringType())
    ])

spark = SparkSession.builder.appName("read_test_straeam").getOrCreate()

# Reduce logging
spark.sparkContext.setLogLevel("WARN")

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

df2 = df.select(
        # Convert the value to a string
        F.from_json(
            F.decode(F.col("value"), "utf-8"),
            SCHEMA
        ).alias("value")
    )\
    .select("value.*")

df2 = df2\
    .withColumn('@timestamp', F.from_unixtime('@timestamp').cast(TimestampType()))\
    .withColumn('status', df2["status"].cast(IntegerType()))\
    .withColumn('request_time', df2["request_time"].cast(FloatType()))

df2 = df2\
    .filter("status between 200 and 299")\
    .groupby(
        F.window("@timestamp", "1 minutes"),
        F.col("country")
    )\
    .count()
#    .withColumn("value", F.to_json( F.struct(F.col("*"))))\
#    .withColumn("value", F.encode(F.col("value"), "utf-8").cast("binary"))

df2 = df2\
    .writeStream\
    .option("truncate", "false")\
    .outputMode("update")\
    .format("console")\
    .start()\
    .awaitTermination()

#df2\
#    .writeStream\
#    .format("kafka")\
#    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)\
#    .option("topic", "goal1-topic")\
#    .option("checkpointLocation", "/tmp/checkpoint")\
#    .start()\
#    .awaitTermination()
