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
    limit = int(params.get("limit", 20))
    start = params.get("start")
    end = params.get("end")
    last_key = params.get("lastKey")

    if not device_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "device_id required"})
        }

    # Base query
    if start and end:

        query = {
            "KeyConditionExpression":
                Key("device_id").eq(device_id)
                & Key("timestamp").between(start, end),
            "Limit": limit
        }

    else:

        query = {
            "KeyConditionExpression":
                Key("device_id").eq(device_id),
            "Limit": limit
        }

    # Pagination support
    if last_key:
        query["ExclusiveStartKey"] = {
            "device_id": device_id,
            "timestamp": last_key
        }

    response = table.query(**query)

    result = {
        "data": response.get("Items", [])
    }

    if "LastEvaluatedKey" in response:
        result["nextToken"] = response["LastEvaluatedKey"]["timestamp"]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, cls=DecimalEncoder)
    }
