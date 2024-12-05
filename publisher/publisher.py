import time
import requests
from google.cloud import pubsub_v1

# Configuration
API_URL = 'http://your-api-server/calc_avg'
PROJECT_ID = 'your-google-cloud-project-id'
TOPIC_ID = 'your-pubsub-topic-id'
INTERVAL = 15 * 60  # 15 minutes in seconds

# Initialize Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def publish_message(data):
    message = str(data).encode('utf-8')
    future = publisher.publish(topic_path, message)
    future.result()  # Ensure the message is published

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