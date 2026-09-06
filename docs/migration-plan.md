# Modernization Status

## Completed

- Repository layout cleanup (`src/`, `models/`, `docs/`, `infra/terraform/`)
- Repository tooling standardized with `mise`, Ruff, pytest, and Lambda packaging
- ASK SDK dependencies upgraded and managed with pinned requirements files
- Lambda / IAM / Alexa invoke permission imported into Terraform
- Terraform remote state configured with a dedicated S3 backend and DynamoDB lock
- Lambda runtime, timeout, memory, environment, and code deployment managed by Terraform
- Lambda function migrated to `alexa-aws-iot`

## Current Decisions

- GitHub Actions は lightweight 運用（`terraform fmt` + Python quality checks）を継続
- 監視設定（CloudWatch Logs retention / alarms）は現時点では見送り

## Monitoring Backlog (recommended)

- CloudWatch Logs の保持期間を Terraform で明示管理
- Lambda エラー率 / Duration / Throttle のアラーム追加

