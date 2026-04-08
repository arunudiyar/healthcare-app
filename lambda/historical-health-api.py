import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table = boto3.resource('dynamodb').Table('health_data')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def lambda_handler(event, context):

    params = event.get("queryStringParameters") or {}
    device_id = params.get("device_id")

    if not device_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "device_id required"})
        }

    response = table.query(
        KeyConditionExpression=Key('device_id').eq(device_id)
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response["Items"], cls=DecimalEncoder)
    }
