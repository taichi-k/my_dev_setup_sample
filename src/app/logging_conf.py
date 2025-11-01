# app/logging_conf.py
import json
import logging
import sys

from opentelemetry import trace


class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
        }

        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            base["trace_id"] = format(ctx.trace_id, "032x")
            base["span_id"] = format(ctx.span_id, "016x")

        if hasattr(record, "extra") and isinstance(record.extra, dict):
            base.update(record.extra)
        return json.dumps(base, ensure_ascii=False)


def setup_logging():
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [h]
