# Terraform - SSM Parameter Store 管理

このディレクトリは、アプリケーションの環境変数をAWS Systems Manager Parameter Storeに登録するためのTerraform設定です。

## 📁 ディレクトリ構成

```
terraform/
├── main.tf                      # プロバイダー設定
├── variables.tf                 # 変数定義
├── ssm_parameters.tf            # SSMパラメータリソース定義
├── outputs.tf                   # 出力設定
├── terraform.tfvars.example     # tfvarsのサンプル
├── .gitignore                   # Git除外設定
├── scripts/
│   └── generate_tfvars.py      # .env → tfvars 変換スクリプト
└── README.md                    # このファイル
```

## 🎯 概要

以下のサービスの環境変数をSSM Parameter Storeに登録します：

- **app**: メインアプリケーション (19個の環境変数)
- **worker**: ワーカーサービス (8個の環境変数)
- **otel-collector**: OpenTelemetry Collector (2個の環境変数)

## 📝 命名規則

パラメータ名は以下の形式で管理されます：

```
/${project_name}/${environment}/{service}/{PARAMETER_NAME}
```

例：
- `/test/dev/app/SECRET_KEY_FOR_SESSION_MIDDLEWARE`
- `/test/dev/worker/DATABASE_URL`
- `/test/dev/otel-collector/LOKI_HOST`

## 🔐 パラメータタイプ

- **SecureString**: 機密情報（パスワード、APIキー、トークンなど）
- **String**: 非機密情報（URL、サービス名、ポート番号など）

## 🚀 使い方

### 1. .envファイルからterraform.tfvarsを生成

プロジェクトルートの `.env` ファイルから `terraform.tfvars` を自動生成します：

```bash
# プロジェクトルートで実行
python3 terraform/scripts/generate_tfvars.py
```

または手動で `terraform.tfvars` を作成：

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# エディタで編集
```

### 2. Terraform初期化

```bash
cd terraform
terraform init
```

### 3. プラン確認

```bash
terraform plan
```

### 4. 適用

```bash
terraform apply
```

## 📋 作成されるパラメータ一覧

### App Service (19個)
- `SECRET_KEY_FOR_SESSION_MIDDLEWARE` (SecureString)
- `GOOGLE_CLIENT_ID` (SecureString)
- `GOOGLE_CLIENT_SECRET` (SecureString)
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
- `AWS_ACCESS_KEY_ID` (SecureString)
- `AWS_SECRET_ACCESS_KEY` (SecureString)
- `AWS_ENDPOINT_URL` (String)
- `SQS_QUEUE_NAME` (String)
- `SQS_DLQ_NAME` (String)

### Worker Service (8個)
- `DATABASE_URL` (SecureString)
- `DATABASE_URL_SYNC` (SecureString)
- `AWS_REGION` (String)
- `AWS_ACCESS_KEY_ID` (SecureString)
- `AWS_SECRET_ACCESS_KEY` (SecureString)
- `AWS_ENDPOINT_URL` (String)
- `SQS_QUEUE_NAME` (String)
- `SQS_DLQ_NAME` (String)

### OTEL Collector (2個)
- `LOKI_HOST` (String)
- `LOKI_PORT` (String)

## ⚙️ カスタマイズ

### 環境を変更する場合

`terraform.tfvars` で `environment` を変更：

```hcl
environment = "prod"  # dev, staging, prod など
```

### プロジェクト名を変更する場合

`terraform.tfvars` で `project_name` を変更：

```hcl
project_name = "your-app-name"
```

## 🔄 値の更新

Terraformで管理するパラメータの値を更新する場合：

1. `terraform.tfvars` を編集
2. `terraform apply` を実行

値が変更されると、SSM Parameter Storeの値も更新されます。

## ⚠️ 注意事項

- `terraform.tfvars` は機密情報を含むため `.gitignore` で除外されています
- AWS profileは `dev-setup-sample` を使用するように設定されています
- 実際の環境では、適切なIAM権限が必要です

## 🔍 パラメータの確認

作成されたパラメータを確認：

```bash
# AWS CLIで確認
aws ssm get-parameters-by-path \
  --path "/test/dev/" \
  --recursive \
  --profile dev-setup-sample

# Terraformの出力を確認
terraform output ssm_parameters_created
```

## 🧹 クリーンアップ

すべてのSSMパラメータを削除：

```bash
terraform destroy
```
