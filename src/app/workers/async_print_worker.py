from __future__ import annotations

import json
import os
from typing import Any

from kafka import KafkaConsumer


def _parse_servers(raw_servers: str) -> list[str]:
    return [server.strip() for server in raw_servers.split(",") if server.strip()]


def _deserialize(raw_value: bytes) -> dict[str, Any]:
    if not raw_value:
        return {}
    return json.loads(raw_value.decode("utf-8"))


def main() -> None:
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9094")
    topic = os.getenv("ASYNC_PROC_TOPIC", "async_proc")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=_parse_servers(bootstrap),
        value_deserializer=_deserialize,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        group_id="async_proc_worker",
    )

    print(
        f"[async-worker] Listening for messages on topic '{topic}' via {bootstrap}",
        flush=True,
    )

    try:
        for message in consumer:
            payload = message.value or {}
            timestamp = payload.get("timestamp", "unknown")
            print(f"[async-worker] received timestamp={timestamp}", flush=True)
    except KeyboardInterrupt:
        print("[async-worker] Interrupted, shutting down...", flush=True)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
