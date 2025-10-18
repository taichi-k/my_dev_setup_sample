FROM mcr.microsoft.com/devcontainers/python:3.12

# 必要ツール
RUN apt-get update \
    && apt-get -y install --no-install-recommends curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

# グローバル配置（/usr/local/bin）
RUN curl -LsSf https://astral.sh/uv/install.sh \
    | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

# 動作確認（ビルド時に失敗してくれた方がデバッグしやすい）
RUN which uv && uv --version

WORKDIR /workspace
