# alexa-aws-iot

DynamoDB に記録された室内の温度・湿度・気圧を Alexa カスタムスキルで応答するサンプルです。

### Architecture

Alexa カスタムスキル → AWS Lambda → DynamoDB（センサー値の読み取り）

## Repository Layout

```text
.
|-- docs/              # 運用・移行ドキュメント
|-- infra/
|   `-- terraform/     # Terraform 定義（運用中）
|-- models/
|   `-- ja-JP.json     # Alexa対話モデル（開発者コンソール用）
|-- scripts/           # デプロイ補助スクリプト
|-- src/
|   |-- lambda_handler.py         # Lambda 実装本体
|   |-- env_monitor.py            # DynamoDB からのセンサー値取得
|   `-- env_monitor_document.json # APL ビジュアルドキュメント
`-- tests/             # pytest によるハンドラー単体テスト
```

## Lambda Handler

- 現在のハンドラー: `src.lambda_handler.lambda_handler`
- 依存関係(`ask-sdk-core` 等)は `requirements.txt` で管理し、パッケージング時に vendoring します。

## Packaging

Lambda デプロイ用アーティファクトは次のスクリプトで作成できます。

```bash
./scripts/package_lambda.sh
```

生成物:

- `dist/alexa-aws-iot-lambda.zip`

## Terraform (Operations)

日常運用の手順は次を参照してください。

- [infra/terraform/README.md](infra/terraform/README.md)

## Local development

ローカルでも CI と同じ Python 品質チェックを実行できるようにしています。

### 1. Tooling setup

```bash
brew install mise
mise install
```

### 2. Run checks

```bash
make setup
make check
```

この環境では Python 3.12 と Ruff を使用します。`make check` は pytest も実行します。

## Current Status

- Lambda 依存関係(`ask-sdk-core` 等)の pip 管理化・バージョン更新が完了
- Lambda / IAM ロール / Alexa 起動権限は Terraform 管理済み
- Lambda の runtime / timeout / memory_size / environment は Terraform 管理済み
- Terraform state は専用 S3 backend + DynamoDB lock で運用

残タスクは次を参照してください。

- [docs/migration-plan.md](docs/migration-plan.md)

## Alexa Developer Console

- `models/ja-JP.json` の対話モデルは Alexa Developer Console（または ASK CLI）側にも反映が必要です。
- APL ドキュメント(`src/env_monitor_document.json`)は Lambda 実行時に読み込まれるため、`src/` 配下で管理します。

### Setup and test

1. Alexa Developer Console で対象の Custom Skill を開き、`models/ja-JP.json` の内容を対象言語（日本語）へ反映して保存します。
2. `Custom > Endpoint` でサービスエンドポイントを `AWS Lambda ARN` にし、東京リージョンの Lambda ARN を設定します。現在の関数名は `alexa-aws-iot` です。
3. Lambda の Alexa Skills Kit トリガーに Skill ID を設定し、Skill ID verification を有効にします。
4. Console のテストシミュレーターでスキルを起動し、「室内環境」または「室内環境を教えて」と発話して、温度・湿度・気圧の応答を確認します。
5. APL 対応端末またはシミュレーターで、温度・湿度・気圧の画面表示も確認します。

Lambda ARN や Skill ID を変更した場合は、Terraform の `terraform.tfvars` も更新し、`terraform plan` で差分を確認します。

## Reference

- [カスタムスキルの概要](https://developer.amazon.com/ja-JP/docs/alexa/custom-skills/understanding-custom-skills.html)
- [カスタムスキルを AWS Lambda 関数としてホスティングする](https://developer.amazon.com/ja-JP/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html)
- [カスタムスキルの JSON インターフェースのリファレンス](https://developer.amazon.com/ja-JP/docs/alexa/custom-skills/request-and-response-json-reference.html)
- [Alexa Skills Kit SDK for Python](https://developer.amazon.com/ja-JP/docs/alexa/alexa-skills-kit-sdk-for-python/overview.html)
- [ASK SDK for Python GitHub リポジトリ](https://github.com/alexa/alexa-skills-kit-sdk-for-python)
- [Alexa Presentation Language（APL）](https://developer.amazon.com/ja-JP/docs/alexa/alexa-presentation-language/add-visuals-and-audio-to-your-skill.html)
