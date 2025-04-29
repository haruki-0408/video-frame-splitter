## はじめに

このプロジェクトは、AWS SAM（Serverless Application Model）を使用して構築されたサーバレスアプリケーションです。  
動画ファイルを1秒ごとにフレーム（静止画）へ分割する処理を、LambdaとStep Functions Express Workflowsを使って実装しています。

---

## 使用環境

| 項目 | 内容 |
|:----|:-----|
| 言語 | Python 3.12 |
| デプロイ | AWS SAM CLI |
| ランタイム | Lambda (python3.12, x86_64アーキテクチャ) |
| メディアツール | [ffmpeg 7.0.2 amd64 static](https://johnvansickle.com/ffmpeg/) |
| Lambdaレイヤー | 上記ffmpegバイナリを含んだLayerを定義済み |
| ストレージ | Amazon S3（アップロード用／フレーム保存用） |
| 並列ワークフロー | Step Functions Express Workflow（Mapステートによる秒単位処理） |
| タイムアウト | Lambda関数: 最大240秒 |
| メモリ | Lambda関数: 4096MB |
| エフェメラルストレージ（/tmp） | Lambda関数: 4096MB（動画処理に必須） |

> ⚠️ **注意**  
> このプロジェクトに含まれる Lambda レイヤーには `ffmpeg-7.0.2-amd64-static` が含まれています。  
> 静的ビルド版で、Linux x86_64 向けに最適化されています。別アーキテクチャ環境で実行する場合は動作しない可能性があります。

---

## デプロイ手順

1. 必要な環境をインストール：

- [Python 3](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

2. 次のコマンドを実行：

```bash
sam build
sam deploy --guided
```

---

## S3バケット名について（重要）

`template.yaml` 内にハードコードされた以下のS3バケット名は、必ず**ご自身のAWSアカウントに合わせて一意な名前へ変更**してください。

```yaml
  SourceBucket:
    BucketName: video-frame-splitter-source-bucket

  FrameOutputBucket:
    BucketName: video-frame-splitter-output-bucket
```

変更しないままデプロイすると、バケット名の重複でエラーになります。

---

作成したリソースを削除したい場合は次のコマンドを実行してください：

```bash
sam delete
```

---

## 関連ドキュメント

- [AWS SAM 開発者ガイド](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/what-is-sam.html)
- [ffmpeg公式ビルドページ](https://johnvansickle.com/ffmpeg/)
- [Step Functions Express Workflows 概要](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-express.html)
