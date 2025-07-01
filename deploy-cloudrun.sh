#!/bin/bash

# Google Cloud Run デプロイスクリプト
# 事前にGoogle Cloud SDKのインストールとログインが必要です

# プロジェクト設定（あなたのプロジェクトIDに変更してください）
PROJECT_ID="your-project-id"
SERVICE_NAME="mozaiku-app"
REGION="asia-northeast1"  # 東京リージョン

echo "Google Cloud Runにデプロイします..."
echo "プロジェクトID: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"

# main-cloudrun.pyをmain.pyにコピー
cp main-cloudrun.py main.py
cp requirements-cloudrun.txt requirements.txt

# Dockerイメージをビルドしてデプロイ
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10

echo "デプロイ完了！"
echo "アクセスURL: https://$SERVICE_NAME-[hash]-$REGION.a.run.app"