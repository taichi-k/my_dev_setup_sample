import json
import os
import random
import time
from datetime import datetime, timezone

import boto3

AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "async-queue")
SQS_DLQ_NAME = os.getenv("SQS_DLQ_NAME", "async-queue-dlq")

sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)


def setup_queues() -> tuple[str, str]:
    # FastAPI側と同じロジック（複数回呼ばれても冪等）
    dlq_resp = sqs.create_queue(QueueName=SQS_DLQ_NAME)
    dlq_url = dlq_resp["QueueUrl"]

    dlq_attrs = sqs.get_queue_attributes(
        QueueUrl=dlq_url,
        AttributeNames=["QueueArn"],
    )
    dlq_arn = dlq_attrs["Attributes"]["QueueArn"]

    redrive_policy = json.dumps(
        {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": "2",
        }
    )

    main_resp = sqs.create_queue(
        QueueName=SQS_QUEUE_NAME,
        Attributes={"RedrivePolicy": redrive_policy},
    )
    main_url = main_resp["QueueUrl"]

    return main_url, dlq_url


SQS_QUEUE_URL, SQS_DLQ_URL = setup_queues()


def process_message(body: dict) -> None:
    requested_at = body.get("requested_at")
    processed_at = datetime.now(timezone.utc).isoformat()

    if random.choice([True, True, False]):
        raise RuntimeError("processing failed")

    print(f"[WORKER] OK requested_at={requested_at}, processed_at={processed_at}")


def main() -> None:
    print("[WORKER] started. waiting for messages...")

    while True:
        resp = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
            VisibilityTimeout=30,
        )

        messages = resp.get("Messages", [])
        if not messages:
            continue
        for m in messages:
            body = json.loads(m["Body"])
            try:
                process_message(body)
            except Exception as e:
                # ❌ ここで delete しない：SQS が再配信 → 規定回数超えたらDLQへ
                print(f"[WORKER] ERROR processing message: {e}")
            else:
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=m["ReceiptHandle"],
                )
        time.sleep(1)


if __name__ == "__main__":
    main()
