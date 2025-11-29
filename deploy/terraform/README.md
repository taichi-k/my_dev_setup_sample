# Terraform - AWS インフラ構成管理

このディレクトリは、アプリケーションのAWSインフラをTerraformで管理するための設定です。
主にSSM Parameter StoreとVPCネットワークの構成を管理します。

## 📁 ディレクトリ構成

```
terraform/
├── README.md                    # このファイル
├── modules/                     # 再利用可能なモジュール
│   ├── network/                # VPCネットワーク構成
│   │   ├── main.tf
│   │   └── outputs.tf
│   └── ssm_parameters/         # SSMパラメータストア管理
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── stg/                        # ステージング環境
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars        # 環境変数（Git管理外）
│   └── terraform.tfvars.example
└── prd/                        # 本番環境
    └── main.tf
```

## 🎯 概要

以下のサービスの環境変数をSSM Parameter Storeに登録します：

- **app**: メインアプリケーション (22個の環境変数)
- **worker**: ワーカーサービス (7個の環境変数)
- **otel-collector**: OpenTelemetry Collector (2個の環境変数)

## 📝 命名規則

パラメータ名は以下の形式で管理されます：

```
/${project_name}/${environment}/{service}/{PARAMETER_NAME}
```

例：
- `/myproject/stg/app/SECRET_KEY_FOR_SESSION_MIDDLEWARE`
- `/myproject/stg/worker/DATABASE_URL`
- `/myproject/stg/otel-collector/LOKI_HOST`

## 🔐 パラメータタイプ

- **SecureString**: 機密情報（パスワード、APIキー、トークンなど）
- **String**: 非機密情報（URL、サービス名、ポート番号など）

## 🚀 使い方

### 1. 環境ディレクトリに移動

```bash
cd deploy/terraform/stg  # ステージング環境の場合
```

### 2. terraform.tfvarsを作成

`terraform.tfvars.example` をコピーして編集：

```bash
cp terraform.tfvars.example terraform.tfvars
# エディタで必要な値を設定
```

### 3. Terraform初期化

```bash
terraform init
```

### 4. プラン確認

```bash
terraform plan
```

### 5. 適用

```bash
terraform apply
```

## 📋 作成されるパラメータ一覧

### App Service (22個)
- `SECRET_KEY_FOR_SESSION_MIDDLEWARE` (SecureString)
- `GOOGLE_CLIENT_ID` (SecureString)
- `GOOGLE_CLIENT_SECRET` (SecureString)
- `GOOGLE_AUTH_REDIRECT_URL` (String)
- `DATABASE_URL` (SecureString)
- `DATABASE_URL_SYNC` (SecureString)
- `OTEL_EXPORTER_OTLP_ENDPOINT` (String)
- `OTEL_SERVICE_NAME` (String)
- `OTEL_SERVICE_VERSION` (String)
- `OTEL_SERVICE_NAMESPACE` (String)
- `OTEL_DEPLOYMENT_ENVIRONMENT` (String)
- `OTEL_LOGS_EXPORTER` (String)
- `OTEL_EXPORTER_OTLP_PROTOCOL` (String)
- `SENTRY_DSN` (SecureString)
- `AWS_REGION` (String)
- `SQS_QUEUE_NAME` (String)
- `SQS_DLQ_NAME` (String)
- `SQS_QUEUE_URL` (String)
- `SQS_DLQ_URL` (String)
- `REDIS_HOST` (String)
- `REDIS_PORT` (String)
- `REDIS_USE_TLS` (String)

### Worker Service (7個)
- `DATABASE_URL` (SecureString)
- `DATABASE_URL_SYNC` (SecureString)
- `AWS_REGION` (String)
- `SQS_QUEUE_NAME` (String)
- `SQS_DLQ_NAME` (String)
- `SQS_QUEUE_URL` (String)
- `SQS_DLQ_URL` (String)

### OTEL Collector (2個)
- `LOKI_HOST` (String)
- `LOKI_PORT` (String)

## ⚙️ カスタマイズ

### 環境を変更する場合

`terraform.tfvars` で `environment` を変更：

```hcl
environment = "prd"  # stg, prd など
```

### プロジェクト名を変更する場合

`terraform.tfvars` で `project_name` を変更：

```hcl
project_name = "your-app-name"
```

## 🏗️ バックエンド構成

Terraform の状態ファイルは S3 バケットで管理されます：

```hcl
backend "s3" {
  bucket = "771623671665-stg-test-terraform-state"
  key    = "terraform.tfstate"
  region = "ap-northeast-1"
}
```

初回実行前に、S3バケットが作成されていることを確認してください。

## 🔄 値の更新

Terraformで管理するパラメータの値を更新する場合：

1. 該当環境の `terraform.tfvars` を編集
2. `terraform plan` で変更内容を確認
3. `terraform apply` を実行

値が変更されると、SSM Parameter Storeの値も更新されます。

## ⚠️ 注意事項

- `terraform.tfvars` は機密情報を含むため `.gitignore` で除外されています
- AWS profileは `dev-setup-sample` を使用するように設定されています
- 実際の環境では、適切なIAM権限が必要です
- 各環境（stg, prd）ごとに異なる `terraform.tfvars` を設定してください

## 🔍 パラメータの確認

作成されたパラメータを確認：

```bash
# AWS CLIで確認
aws ssm get-parameters-by-path \
  --path "/myproject/stg/" \
  --recursive \
  --profile dev-setup-sample

# Terraformの出力を確認
terraform output
```

## 🧹 クリーンアップ

すべてのSSMパラメータを削除：

```bash
terraform destroy
```
