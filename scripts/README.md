# Scripts

このディレクトリには、Lambda パッケージングやデプロイ補助のスクリプトを配置します。

## package_lambda.sh

Lambda デプロイ用 zip を作成します。`requirements.txt` の依存関係(ask-sdk-core 等)を
`src/` と同じディレクトリ階層にインストールしてからパッケージングします。

- 入力
	- `src/`
	- `requirements.txt`
- 出力
	- `dist/alexa-aws-iot-lambda.zip`

実行例:

```bash
./scripts/package_lambda.sh
```
