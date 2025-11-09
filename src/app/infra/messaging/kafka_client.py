from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Any

from kafka import KafkaProducer
from kafka.errors import KafkaError

log = logging.getLogger("app")


def _parse_bootstrap_servers(raw_servers: str | None) -> list[str]:
    if not raw_servers:
        return ["kafka:9092"]
    return [server.strip() for server in raw_servers.split(",") if server.strip()]


def _serialize(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload).encode("utf-8")


class AsyncJobPublisher:
    def __init__(self, topic: str | None = None, bootstrap_servers: str | None = None) -> None:
        self.topic = topic or os.getenv("ASYNC_PROC_TOPIC", "async_proc")
        self._producer = KafkaProducer(
            bootstrap_servers=_parse_bootstrap_servers(
                bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS")
            ),
            value_serializer=_serialize,
        )

    def publish_timestamp(self, timestamp: str) -> None:
        payload = {"timestamp": timestamp}
        try:
            future = self._producer.send(self.topic, payload)
            future.get(timeout=10)
        except KafkaError as exc:
            log.error(
                "Failed to send async job to Kafka topic %s: %s",
                self.topic,
                exc,
                extra={"extra": {"service": "app", "event": "async_job_publish_error"}},
            )
            raise RuntimeError("Kafka publish failed") from exc


@lru_cache
def get_async_job_publisher() -> AsyncJobPublisher:
    return AsyncJobPublisher()
