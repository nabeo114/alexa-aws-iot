import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EnvMonitor:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb", region_name=os.environ["Region"])
        self.table = self.dynamodb.Table(os.environ["TableName"])

    def get_snapshot(self):
        # Read the latest sensor values from one fixed partition key/value pair.
        response = self.table.get_item(Key={os.environ["PartitionKey"]: os.environ["PartitionName"]})
        logger.info(response)
        item = response["Item"]
        return {
            "temperature": float(item["temperature"]),
            "humidity": float(item["humidity"]),
            "pressure": float(item["pressure"]),
        }
