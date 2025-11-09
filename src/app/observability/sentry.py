import os

import sentry_sdk


def setup_sentry() -> None:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", ""),
        send_default_pii=True,
        traces_sample_rate=1.0,
        enable_logs=True,
    )
