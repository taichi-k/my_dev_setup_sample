import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.access_log import access_log_middleware


def setup_middlewares(app: FastAPI) -> None:
    secret_key = os.getenv("SESSION_SECRET_KEY")
    if not secret_key:
        raise ValueError("SESSION_SECRET_KEY environment variable is not set")
    app.add_middleware(SessionMiddleware, secret_key=secret_key)

    # 注意: middlewareは逆順で実行されるため、登録順序が重要
    app.middleware("http")(access_log_middleware)

    # 将来的に他のmiddlewareを追加する場合はここに記述
    # app.middleware("http")(error_handling_middleware)
    # app.middleware("http")(cors_middleware)
