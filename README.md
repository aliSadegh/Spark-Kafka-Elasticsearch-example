# Overview
This is a simple example that we developed for processing NGINX log data, detecting anomalies, and performing data analytics using Kafka, Spark, and Elasticsearch.  

# Goals
Our objectives for this project were as follows:  
1. Detects if a user requests more than 10 times in every 20 seconds (1 sec hopping).
2. Detects if a host returns 4XX more than 15 times in every 30 seconds (1 sec hopping).
3. Calculates successful requests for each country minutely and produces it to another topic.
4. Calculates average response time for each host minutely and produces it to another topic.
5. Publishes raw data to ElasticSearch.

A sample record of log is like:  
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

# Execution
To deploy the entire solution, execute the following command:  
```
sudo docker-compose up docker-compose/ -d
```

# Testing
For testing, we provided Python script located in the test directory. This script allowed testing of data ingestion and anomaly detection goals.    

For testing data ingestion:  
```python3 test/kafka-consumer.py test-inter```  

For testing goals 1 to 4:  
```python3 test/kafka-consumer.py goal[X]-topic```  
**(Note: Replace [X] with the corresponding goal number)**  

To test the Elasticsearch index:  
```curl http://localhost:9200/test-inter/_count```  
**(Execute multiple times; the count field should increase)**  

# Pipeline
Our pipeline architecture comprised data ingestion from Kafka, Spark-based processing, and storage in Elasticsearch. This diagram illustrates the flow: 

![diagram-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/307d453b-cef1-400c-8617-c415cdf8b775)

## Data Ingestion
To simulate real-world NGINX log data, we used a Python script that generated randomized log entries.  
You can find out in ```docker-compose/data_producer```

## Anomaly Detection and Data Aggrigation
Our approach to addressing goals 1 to 4 involved leveraging Spark for processing. Data from Kafka topics is fed into DataFrames, where aggregation and filtering are performed. Results are subsequently produced into new Kafka topics dedicated to each goal.   

The Python files that containes pyspark code for solving these goals exists in ```docker-compose/spark-master/src```  

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
The pipeline integrated Kafka Connect to seamlessly transfer raw data from Kafka topics to Elasticsearch. This enabled us to store and query the data efficiently for analysis and visualization.   

# Conclusion
In conclusion, our NGINX log data processing and anomaly detection pipeline demonstrated the capabilities of Kafka, Spark, and Elasticsearch in creating an efficient and effective solution for website monitoring.

# References
We'd like to acknowledge the resources and inspiration from the following links that guided our solution:  

