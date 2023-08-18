# Overview
This is a simple pipeline example of using kafka and spark with elasticsearch for processing and storing log data.

# Problem Statement
The input is the NGINX logs that provide request details to the website. We need to be notified if there is a problem in the website or we are under attack. Also there should be a feature to investigate through logs for finding some patterns.

A sample record is like:  
```
{
    'server': 's_v3',
    'client_ip': '154.85.126.16',
    'method': 'PUT',
    'status': '201',
    'request_time': '0.28',
    'host': 'api_38.digikala.com',
    'country': 'US',
    '@timestamp': '1659509511.865323'
}
```

# Goalse
1. Detects if a user requests more than 10 times in every 20 seconds (1 sec hopping).
2. Detects if a host returns 4XX more than 15 times in every 30 seconds (1 sec hopping).
3. Calculates successful requests for each country minutely and produces it to another topic.
4. Calculates average response time for each host minutely and produces it to another topic.
5. Publishes raw data to ElasticSearch.

# Run
For deploy whole the solution run this command:
```
sudo docker-compose up docker-compose/ -d
```

# Test
For test your deployment, you can run the python file that exist in test directory  
For test data ingestion, run this command:  
```python3 test/kafka-consumer.py test-inter```  

For test goals 1 to 4, run this command:  
```python3 test/kafka-consumer.py goal[X]-topic```  
**insted of [X] write the number related to the goals**  

For test elasticsearch index run this commad:  
```curl http://localhost:9200/test-inter/_count```  
**run couple of times, the number of count field must be increase**  

# Pipeline
a architucture of this pipeline show as a picture below: 

![diagram-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/307d453b-cef1-400c-8617-c415cdf8b775)

As you can see, data ingest to kafka which is the buffering system that hold data, after data spark read data from kafka topic and proccess them, spark produce result data to kafka again for any action system can do on these data, also we connected kafka connect to kafka and elasticsearch for passing data from kafka topic to elasticsearch index.  

## Data Ingestion
For simulate data to generating Nginx log, we have a python code that generate random data.  
this python code exist in data_producer directory.  
after random data generated, they produced to a topic kafka like ```test-inter``` 

## Anomaly Detection and Data Aggrigation
The idea for solving goal 1 to 4 is same, we use spark as a proccessing engin for that.  
First we read data from kafka topics to Data Frames and do some aggrigation or filtring on that and finally we produce result to new Kafka topic for each goal.  

the python files that containes pyspark code for solving goal 1 to 4 are exists in ```docker-compose/spark-master/src```  

Before describing any codes, let's see the algorithm that we used to solve golas
### Tumbling time window
An important feature of stream processing tools is the ability to handle event time processing. Tumbling windows are non-overlapping fixed time intervals used to make aggregations using event-time columns. To put it more simply, they slice the timeline into equally sized slices so each event belongs to a single interval.  
For example, count, every 5 minutes, how many events were detected in the last 5 minutes.
![fix-window-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/7b602173-2de3-45a6-8a6a-c843cec8ad74)

### Sliding time window
Sliding time windows are a flexibilization of tumbling windows. Instead of creating non-overlapping intervals, they allow defining how often each interval will be created.  
For example, every 5 minutes, count how many events were detected in the last 30 minutes.  

![window-time1-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/7cf27475-8503-49f8-851f-8a40883a506b)

Now in goal 1 and 2 we used flexibale window algolithm for detect anomalies  
for goal 1 we count last 20 seconds receive logs for each ```client-ip``` every 1 second interval  
```
df = df\
    .groupby(
        F.window("@timestamp", "20 seconds", "1 seconds"),
        F.col("client_ip")
    )\
    .count()\
    .filter("count > 10")
```  

for goal 2 we count last 30 seconds recive logs for each ```host``` every 1 second interval  
```
df = df\
    .filter("status between 400 and 499")\
    .groupby(
        F.window("@timestamp", "30 seconds", "1 seconds"),
        F.col("host")
    )\
    .count()\
    .filter("count > 15")
```

for goal 3 and 4 it's easier, we used the fixed window algorithm.  
also in goal 3 we used a ```filter()``` function for select just successfull response.  
```
df = df\
    .filter("status between 200 and 299")\
    .groupby(
        F.window("@timestamp", "1 minutes"),
        F.col("country")
    )\
    .count()
```

finally for gola 4 we used same algorithm like goal 3 also for calculate average we used ```avg()``` function
```
df = df\
    .groupby(
        F.window("@timestamp", "1 minutes"),
        F.col("host")
    )\
    .avg("request_time")
```

## Elasticsearch Integration
The last goal is storing data in elasticsearch, for achive this goal we used Kafka connect that garantee ingest data from kafka to elastic.  
you can find this in ```kafka-connect``` directory  
```
name=elasticsearch-sink
connector.class=io.confluent.connect.elasticsearch.ElasticsearchSinkConnector
tasks.max=1
topics=test-inter
key.ignore=true
connection.url=http://elastic:9200
type.name=kafka-connect
schema.ignore=true
```

# Conclusion
This is a simple example of useing kafka and spark utilized with docker.  
There is a lots of things we can do for improve out sulotion and more efficient.

# References
Thanks to these links which inspire me to solve this challange
