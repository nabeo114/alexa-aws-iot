# Terraform

このディレクトリは、Alexa custom skill 用 Lambda の実運用を Terraform で管理するための定義です。

## Scope

- Include:
  - Lambda function
  - Lambda 実行ロールと IAM ポリシー/attachment
  - Alexa Skills Kit からの起動権限（`aws_lambda_permission`）
- Exclude:
  - DynamoDB リソース
  - Alexa スキル自体（対話モデル・APLドキュメントなど、開発者コンソール/ASK CLI側で管理）

## Files

- `versions.tf`: Terraform / provider バージョン
- `provider.tf`: AWS provider
- `variables.tf`: 入力変数
- `main.tf`: Lambda / IAM / Alexa 起動権限
- `outputs.tf`: 出力値
- `terraform.tfvars.example`: 変数例

## Prerequisites (one-time)

1. Terraform がインストール済み
2. AWS 認証情報が利用可能
3. Terraform backend 用の専用 S3 バケットと lock 用 DynamoDB テーブル

初回セットアップ:

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
cp backend.hcl.example backend.hcl
terraform init -backend-config=backend.hcl
```

`backend.hcl` の `bucket` はこのプロジェクト専用バケットを指定します。

## Daily Operation

### 1) Lambda コードのデプロイ

```bash
cd ../..
./scripts/package_lambda.sh
cd infra/terraform
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

### 2) 設定値変更（runtime / timeout / memory / env）

1. `terraform.tfvars` を編集
2. `terraform plan -var-file=terraform.tfvars`
3. `terraform apply -var-file=terraform.tfvars`

## GitHub Actions (Lightweight)

`.github/workflows/ci.yml` では次を実行します。

- `terraform fmt -check -recursive`
- Python の lint / format / test チェック（`ruff check`, `ruff format --check`, `pytest`）

Terraform backend や AWS 認証は不要です。

## Managed Lambda Environment

Terraform で管理する Lambda 環境変数:

- `Region`
- `TableName`
- `PartitionKey`
- `PartitionName`

## Notes

- `alexa_skill_id` が空の場合、Alexa 起動権限（`aws_lambda_permission.alexa_invoke`）は作成されません。
  スキルIDが判明したら `terraform.tfvars` に設定してください。
