# subscriber/subscriber.py
import os
import json
import requests
from google.cloud import pubsub_v1

# 환경 변수 로드
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("GCP_SUBSCRIPTION_ID")
API_URL = os.getenv("API_URL")

def callback(message):
    print(f"Received message: {message.data}")
    try:
        data = json.loads(message.data.decode('utf-8'))
        # 필수 필드 검증
        required_fields = ['cafeteria_id', 'wait_count', 'estimated_wait_time', 'timestamp']
        if not all(field in data for field in required_fields):
            print("Invalid message format")
            message.ack()
            return

        # API 서버로 데이터 전송
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print("Data successfully inserted into DB")
        else:
            print(f"Failed to insert data into DB: {response.text}")
            # 재시도 필요 시 nack 처리
            # message.nack()
            # return

    except Exception as e:
        print(f"Error processing message: {e}")
        # 재시도 필요 시 nack 처리
        # message.nack()
        # return

    # 메시지 승인
    message.ack()

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
