import requests
import random
import time

API_URL = "https://fwdjxgz257.execute-api.ap-south-1.amazonaws.com/prod/ingest"

NUM_DEVICES = 100   # simulate 100 devices locally

device_ids = [f"device{i:05d}" for i in range(1, NUM_DEVICES + 1)]

while True:

    device_id = random.choice(device_ids)

    payload = {
        "device_id": device_id,
        "heart_rate": random.randint(60, 120),
        "bp": random.randint(90, 140)
    }

    response = requests.post(API_URL, json=payload)

    print("Sent:", payload)
    print("Response:", response.status_code)

    time.sleep(0.2)
