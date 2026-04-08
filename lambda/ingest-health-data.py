import json
import boto3
import base64
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('health_data')

def lambda_handler(event, context):

    for record in event['Records']:

        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)

        table.put_item(
            Item={
                "device_id": data["device_id"],
                "timestamp": str(int(time.time())),
                "heart_rate": data["heart_rate"],
                "bp": data["bp"]
            }
        )

    return {"status": "success"}

