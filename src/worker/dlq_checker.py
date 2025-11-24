import json
import os

import boto3
from mypy_boto3_sqs import SQSClient

AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
SQS_DLQ_NAME = os.getenv("SQS_DLQ_NAME", "async-queue-dlq")


def create_sqs_client() -> SQSClient:
    if AWS_ENDPOINT_URL:
        return boto3.client(
            "sqs",
            region_name=AWS_REGION,
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        )
    return boto3.client("sqs", region_name=AWS_REGION)


sqs = create_sqs_client()

dlq_url = sqs.get_queue_url(QueueName=SQS_DLQ_NAME)["QueueUrl"]

resp = sqs.receive_message(
    QueueUrl=dlq_url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=3,
)

for m in resp.get("Messages", []):
    print("[DLQ]", json.loads(m["Body"]))
