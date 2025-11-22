#!/bin/bash
set -euo pipefail

ENV=${1:-dev}  # 第一引数で dev/stg/prod を指定

AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:? "AWS_ACCOUNT_ID is required"}
AWS_REGION=ap-northeast-1
ECR_BASE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
GIT_SHA=$(git rev-parse --short HEAD)

PROFILE=${AWS_PROFILE:-}
if [[ -n "$PROFILE" ]]; then
  AWS_CMD="aws --profile $PROFILE"
  echo "Using AWS profile: $PROFILE"
else
  AWS_CMD="aws"
  echo "Using default AWS credentials (no profile)"
fi

echo "ENV=${ENV}, GIT_SHA=${GIT_SHA}"

echo "🔐 Logging in to ECR..."
$AWS_CMD ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_BASE"


echo "📦 Building & pushing app..."
docker build -f app.Dockerfile -t test/app:"${GIT_SHA}" .
docker tag test/app:"${GIT_SHA}" "$ECR_BASE"/test/app:"${ENV}-${GIT_SHA}"
docker push "$ECR_BASE"/test/app:"${ENV}-${GIT_SHA}"

echo "📦 Building & pushing worker..."
docker build -f worker.Dockerfile -t test/worker:"${GIT_SHA}" .
docker tag test/worker:"${GIT_SHA}" "$ECR_BASE"/test/worker:"${ENV}-${GIT_SHA}"
docker push "$ECR_BASE"/test/worker:"${ENV}-${GIT_SHA}"

echo "📦 Building & pushing otel_collector..."
docker build -f otelcollector.Dockerfile -t test/otel_collector:latest .
docker tag test/otel_collector:latest $ECR_BASE/test/otel_collector:latest
docker push $ECR_BASE/test/otel_collector:latest

echo "✅ Pushed images for ENV=${ENV}, GIT_SHA=${GIT_SHA}"
