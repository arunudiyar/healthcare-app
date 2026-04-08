import requests
import random
import time

API_URL = "https://fwdjxgz257.execute-api.ap-south-1.amazonaws.com/prod/ingest"

while True:

    payload = {
        "device_id": "device001",
        "heart_rate": random.randint(60,120),
        "bp": random.randint(90,140)
    }

    response = requests.post(API_URL, json=payload)

    print("Sent:", payload)
    print("Response:", response.status_code)

    time.sleep(2)
