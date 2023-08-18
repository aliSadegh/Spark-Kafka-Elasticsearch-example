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
To deploy the entire solution, navigate to docker-compose directory and execute the following command:  
```
sudo docker-compose up -d
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

![Architecture](/assets/diagram.png)

## Data Ingestion
To simulate real-world NGINX log data, we used a Python script that generated randomized log entries.  
You can find out in ```docker-compose/data_producer```

## Anomaly Detection and Data Aggrigation
Our approach to addressing goals 1 to 4 involved leveraging Spark for processing. Data from Kafka topics is fed into DataFrames, where aggregation and filtering are performed. Results are subsequently produced into new Kafka topics dedicated to each goal.   

The Python files that contain PySpark code for solving these goals exist in ```docker-compose/spark-master/src```  

Before describing any code, let's see the algorithm that we used to achieve our goals.  
### Tumbling time window
Tumbling windows are non-overlapping fixed time intervals that are vital for event time processing in stream processing tools. These windows are employed to make aggregations using event-time columns. Simply put, they divide the timeline into equally sized slices, ensuring each event belongs to a single interval. For instance, we can count the events detected in the last 5 minutes.  

![fix window example](/assets/fix-window.png)

### Sliding time window
Sliding time windows are a flexible version of tumbling windows. Unlike non-overlapping intervals, they enable us to define the frequency at which each interval is created. For example, we can count the events detected in the last 30 minutes every 5 minutes.    

![sliding window example](/assets/window-time.png)

For goals 1 and 2, we utilized the flexible window algorithm to detect anomalies.  
For goal 1, we counted the logs received for each ```client-ip``` in the last 20 seconds, with a 1-second interval.  
```
df = df\
    .groupby(
        F.window("@timestamp", "20 seconds", "1 seconds"),
        F.col("client_ip")
    )\
    .count()\
    .filter("count > 10")
```  

For goal 2, we counted the logs received for each ```host``` in the last 30 seconds, again with a 1-second interval.    
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

For goals 3 and 4, we used the fixed window algorithm. Additionally, for goal 3, we used the ```filter()``` function to select only successful responses. 
```
df = df\
    .filter("status between 200 and 299")\
    .groupby(
        F.window("@timestamp", "1 minutes"),
        F.col("country")
    )\
    .count()
```

Finally, for goal 4, we used the same algorithm as goal 3, and to calculate the average, we used the ```avg()``` function.
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
[A Fast Look at Spark Structured Streaming + Kafka](https://towardsdatascience.com/a-fast-look-at-spark-structured-streaming-kafka-f0ff64107325)  
[How to Link Kafka & ElasticSearch with a Kafka Connector in a Local Docker Container](https://medium.com/@jan_5421/how-to-add-an-elasticsearch-kafka-connector-to-a-local-docker-container-f495fe25ef72)
