from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf, to_json, struct
from pyspark.sql.types import ArrayType, StringType, StructType
from kafka import KafkaProducer
import spacy
import json

# Load the pre-trained spaCy NER model
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(text):
    doc = nlp(text)
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]
    return named_entities

# Define a user-defined function (UDF) to apply NER to each row of the DataFrame
extract_named_entities_udf = udf(extract_named_entities, ArrayType(StringType()))

def send_to_kafka(df, batch_id):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    records = df.toJSON().collect()
    for record in records:
        json_record = json.loads(record)
        producer.send('topic2', value=json.dumps(json_record).encode('utf-8'))



def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("NamedEntityRecognition") \
        .getOrCreate()

    # Define schema for the incoming Kafka messages
    schema = StructType().add("value", StringType())

    # Read data from Kafka topic
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "news_topic") \
        .load()

    # Convert binary data to string
    df = df.selectExpr("CAST(value AS STRING)")

    # Apply named entity recognition (NER) to each row
    df_with_entities = df.withColumn("named_entities", explode(extract_named_entities_udf(col("value"))))

    # Count the occurrences of each named entity
    df_counts = df_with_entities \
        .groupBy("named_entities") \
        .count() \
        .orderBy("count", ascending=False)

    # Convert DataFrame to JSON and send to Kafka topic2
    query = df_counts \
        .writeStream \
        .foreachBatch(send_to_kafka) \
        .outputMode("complete") \
        .start()

    # Wait for the stream to terminate
    query.awaitTermination()

if __name__ == "__main__":
    main()
