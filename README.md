# my_dev_setup_sample

新規サービスを作成する時のテンプレ

## 事前準備

```
brew install go-task
task setup
```

## アプリの起動

Webアプリを起動
```
task up
```

Observability系のコンテナを使う場合
```
task up:obs
```

## 非同期処理サンプル（Kafka）

Kafka + ワーカーを使った非同期処理のサンプルを追加しています。

1. `task up` でアプリと Kafka（`kafka:9092`/`localhost:9094`）を立ち上げる。
2. 別ターミナルでワーカーを起動する。
   ```
   docker compose exec app uv run python -m app.workers.async_print_worker
   ```
   ※ローカルで直接実行する場合は `KAFKA_BOOTSTRAP_SERVERS=localhost:9094` を設定してください。
3. `GET http://localhost:8080/async_proc` にアクセス（例: `curl http://localhost:8080/async_proc`）。
4. リクエスト時刻が Kafka 経由でワーカーに配送され、ワーカー側のログに `timestamp=...` が `print` されます。
