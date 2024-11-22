# subscriber/subscriber.py
import os
import json
import requests
import time
from google.cloud import pubsub_v1
#from dotenv import load_dotenv

# 환경 변수 로드
#load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("GCP_SUBSCRIPTION_ID")
API_URL = os.getenv("API_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def callback(message):
    print(f"Received message: {message.data}")
    try:
        data = json.loads(message.data.decode('utf-8'))
        # 필수 필드 검증
        required_fields = ['building_id', 'store_id', 'ewt_num', 'ewt_cur', 'timestamp']
        if not all(field in data for field in required_fields):
            print("Invalid message format")
            message.ack()
            return

        # API 서버로 데이터 전송
        # headers = {"X-API-Key": API_KEY}
        headers = {}
        for attempt in range(3):
            response = requests.post(API_URL, json=data, headers=headers)
            if response.status_code == 200:
                print("Data successfully inserted into DB")
                message.ack()
                break
            else:
                print(f"Failed to insert data into DB: {response.text}")
                time.sleep(5)  # 재시도 전 대기
        else:
            print("Max retries reached. Message will be nacked.")
            message.nack()

    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
    except Exception as e:
        print(f"Subscriber error: {e}")

if __name__ == "__main__":
    main()
