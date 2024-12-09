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

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    print(f"fetched data: {response.json()}")
    return response.json()

def publish_message(data):
    message = str(data).encode('utf-8')
    future = publisher.publish(topic_path, message)
    future.result()  # Ensure the message is published

def main():
    while True:
        try:
            print(f"enter try block")
            data = fetch_data()
            publish_message(data)
            print(f"Published data: {data}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()