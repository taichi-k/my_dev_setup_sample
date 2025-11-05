from fastapi import FastAPI

from app.middleware.access_log import access_log_middleware


def setup_middlewares(app: FastAPI) -> None:
    """
    アプリケーションにmiddlewareを登録する

    Args:
        app: FastAPIアプリケーションインスタンス
    """
    # アクセスログmiddleware
    # 注意: middlewareは逆順で実行されるため、登録順序が重要
    app.middleware("http")(access_log_middleware)

    # 将来的に他のmiddlewareを追加する場合はここに記述
    # app.middleware("http")(error_handling_middleware)
    # app.middleware("http")(cors_middleware)
