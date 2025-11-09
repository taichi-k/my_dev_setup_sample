# my_dev_setup_sample

新規サービスを作成する時のテンプレ

## 事前準備

```
brew install go-task
task setup
```

`task setup` では `uv sync --group dev` に加えて `uv tool install pre-commit` を実行し、ローカルに永続的な `pre-commit` コマンドを用意します。必要なら `export PATH="$HOME/.local/bin:$PATH"` や `uv tool update-shell` で PATH を通してください。各ワークツリーで `uv run pre-commit install` を実行すると一時ディレクトリを指すフックが毎回生成されるため、hooks が壊れてしまう場合があります。`pre-commit` が見つからないときは以下を再実行してください。

```
uv tool install pre-commit
pre-commit install
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
