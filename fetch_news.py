from newsapi import NewsApiClient
from kafka import KafkaProducer
import json
import time
import os

# Retrieve the NewsAPI key from an environment variable
news_api_key = os.environ.get('NEWS_API_KEY')

# Check if the API key is provided
if not news_api_key:
    raise ValueError("NewsAPI key is missing. Please set the NEWS_API_KEY environment variable.")

# Start the NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Specify the topic to which news data will be written
kafka_topic = 'news_topic'

def fetch_and_send_news():
    while True:
        try:
            # Fetch news data from NewsAPI
            news = newsapi.get_top_headlines(language='en', country='us')

            # Send each news article to Kafka topic
            for article in news['articles']:
                producer.send(kafka_topic, value=article)

            print(f"{len(news['articles'])} articles published.")

            # Sleep for 60 seconds before fetching news again
            time.sleep(600)
        except Exception as e:
            print(f"Error fetching news: {e}")

if __name__ == "__main__":
    fetch_and_send_news()
