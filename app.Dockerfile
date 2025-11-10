FROM mcr.microsoft.com/devcontainers/python:3.12

# 必要ツール
RUN apt-get update \
  && apt-get -y install --no-install-recommends curl git build-essential \
  && rm -rf /var/lib/apt/lists/*

# グローバル配置（/usr/local/bin）
RUN curl -LsSf https://astral.sh/uv/install.sh \
  | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

RUN which uv && uv --version

WORKDIR /workspace

COPY pyproject.toml uv.lock* ./

RUN uv sync --group dev

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--app-dir", "src", "--reload", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
