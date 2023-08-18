# Overview
You will be creating a pipeline to consume data from a kafka topic and aggregate the data to alert anomalies and also there should be a place to investigate raw data.

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

# test
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

## Data Ingestion
For simulate data to generating Nginx log, we have a python code that generate random data.  
this python code exist in data_producer directory.  
after random data generated, they produced to a topic kafka like ```test-inter``` 

## Anomaly Detection and Data Aggrigation:
Before describing any codes, let's see the algorithm that we used in goal 1 and 2  
### Sliding time window — Flexibilization on the time intervals
Sliding time windows are a flexibilization of tumbling windows. Instead of creating non-overlapping intervals, they allow defining how often each interval will be created.  
For example, every 5 minutes, count how many events were detected in the last 30 minutes.  
<<<<<<< HEAD
=======
![window-time1-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/7cf27475-8503-49f8-851f-8a40883a506b)
>>>>>>> 6c7fbab7c13a7eb050508a6807204f60eb5cd108

<<<<<<< HEAD

Now in goal 1 and 2 we used this algolithm for detect anomalies  
for goal 1 we must a window for 20 seconds in 1 second interval
```
df = df\
    .groupby(
        F.window("@timestamp", "20 seconds", "1 seconds"),
        F.col("client_ip")
    )\
    .count()\
    .filter("count > 10")
```  

for goal 1 we cound record every 1 second for last 30 seconds  
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


=======

>>>>>>> 6c7fbab7c13a7eb050508a6807204f60eb5cd108
## Elasticsearch Integration:

# Challanges and Learnings

# Future Work

# Conclusion

# References
