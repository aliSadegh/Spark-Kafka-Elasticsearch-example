# OVERVIEW
You will be creating a pipeline to consume data from a kafka topic and aggregate the data to alert anomalies and also there should be a place to investigate raw data.

# Problem Statement
The input is the NGINX logs that provide request details to the website. We need to be notified if there is a problem in the website or we are under attack. Also there should be a feature to investigate through logs for finding some patterns.

A sample record is like:  
{'server': 's_v3', 'client_ip': '154.85.126.16', 'method': 'PUT', 'status': '201',
'request_time': '0.28', 'host': 'api_38.digikala.com', 'country': 'US', '@timestamp':
'1659509511.865323'}

# GOALS
1. Detects if a user requests more than 10 times in every 20 seconds (1 sec hopping).
2. Detects if a host returns 4XX more than 15 times in every 30 seconds (1 sec hopping).
3. Calculates successful requests for each country minutely and produces it to another topic.
4. Calculates average response time for each host minutely and produces it to another topic.
5. Publishes raw data to ElasticSearch.

نمونه لاگ شبیه سازی شده وب سرور:  
```
{'server': 's_v3', 'client_ip': '154.85.126.16', 'method': 'PUT', 'status': '201',  
'request_time': '0.28', 'host': 'api_38.digikala.com', 'country': 'US', '@timestamp':  
'1659509511.865323'}
```

# Pipeline
a architucture of this pipelines show as a picture below:  
![diagram-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/307d453b-cef1-400c-8617-c415cdf8b775)

## Data Ingestion

### Anomaly Detection and Data Aggrigation:

### Elasticsearch Integration:

## Challanges and Learnings

## Results and Impact

## Future Work

## Conclusion

## References