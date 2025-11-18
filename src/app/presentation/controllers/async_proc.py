import json
import logging
import os
from datetime import datetime, timezone

import boto3
from fastapi import APIRouter

router = APIRouter()
log = logging.getLogger("app")


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
    dlq_resp = sqs.create_queue(QueueName=SQS_DLQ_NAME)
    dlq_url = dlq_resp["QueueUrl"]

    dlq_attrs = sqs.get_queue_attributes(
        QueueUrl=dlq_url,
        AttributeNames=["QueueArn"],
    )
    dlq_arn = dlq_attrs["Attributes"]["QueueArn"]

    # 2. メインキュー作成 + RedrivePolicy 設定
    redrive_policy = json.dumps(
        {
            "deadLetterTargetArn": dlq_arn,
            # この回数だけ受信しても delete されなかったら DLQ へ移動
            "maxReceiveCount": "2",
        }
    )

    main_resp = sqs.create_queue(
        QueueName=SQS_QUEUE_NAME,
        Attributes={
            "RedrivePolicy": redrive_policy,
        },
    )
    main_url = main_resp["QueueUrl"]

    return main_url, dlq_url


SQS_QUEUE_URL, SQS_DLQ_URL = setup_queues()


@router.get("/sqs")
async def async_proc() -> dict:
    requested_at = datetime.now(timezone.utc).isoformat()

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({"requested_at": requested_at}),
    )

    return {
        "status": "queued",
        "requested_at": requested_at,
        "queue_url": SQS_QUEUE_URL,
    }
