import os
import time
import requests
from google.cloud import pubsub_v1

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("GCP_PUBLISH_ID")
API_URL = os.getenv("API_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
INTERVAL = 10 #15 * 60  # 15 minutes in seconds

# Initialize Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
print(f"Publisher initialized for topic: {topic_path}")

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def publish_message(data):
    for item in data:
        message = str(item).encode('utf-8')
        try:
            future = publisher.publish(topic_path, message)
            print(f"Published message ID: {future.result()}")  # Ensure the message is published
        except Exception as e:
            print(f"An error occurred while publishing message: {e}")

def main():
    while True:
        try:
            data = fetch_data()
            publish_message(data)
            print(f"Published data: {data}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()