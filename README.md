# Real-time Named Entity Recognition for News Articles

This project implements a workflow for performing Named Entity Recognition (NER) on news articles obtained from the NewsAPI. It processes the data using Apache Spark, streams it into Elasticsearch via Logstash, and visualizes the results using Kibana.

## System Overview

* `fetch_news.py`: Fetches news articles from the NewsAPI and sends them to a Kafka topic.
* `streaming_job.py`: Reads data from Kafka, performs NER using Spark, and sends the processed data to Elasticsearch via Logstash.
* Kibana is used to visualize the data stored in Elasticsearch.

## Prerequisites

* Python 3.x (tested with Python 3.11.1)
* Apache Kafka
* Apache Spark
* Elasticsearch, Kibana, and Logstash
* NewsAPI account and API key
* Java dependencies for the above tools

## Setup and Installation

1. Clone this repository to your local machine.

2. Install Python dependencies:
   
   pip install newsapi-python kafka-python spacy pyspark elasticsearch kibana
   python -m spacy download en_core_web_sm

3. Set up environment variable:
   Create an environment variable named `NEWS_API_KEY` and set it to your NewsAPI API key.
   
   export NEWS_API_KEY=your_api_key

4. Start Apache Kafka:
   
   <path_to_kafka>/bin/kafka-server-start.sh <path_to_kafka>/config/server.properties

5. Start Elasticsearch, Kibana, and Logstash:
   Note: Remove SSL in the communication between Elasticsearch and Kibana by setting `xpack.security.enabled: false` in the `elasticsearch.yml` file.

   <path_to_elasticsearch>/bin/elasticsearch
   <path_to_kibana>/bin/kibana
   bin/logstash -f /path/to/your/logstash.conf

6. Run the news fetching script:
   
   python fetch_news.py

7. Run the Spark streaming job:
   
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 streaming_job.py

8. Access Kibana at `http://localhost:5601` to create visualizations and dashboards.

## Note

These instructions are primarily for macOS/Linux. For Windows, use WSL or adjust the steps accordingly.
