# Google Cloud Run デプロイ手順

## 🎯 Google Cloud Run の利点

✅ **無料枠が豊富**
- 月間 200万リクエスト
- 月間 40万GB秒のコンピュート時間
- 月間 1GB のネットワーク送信

✅ **自動モザイク処理対応**
- NudeNet AI検出
- OpenCV画像処理
- 大きなライブラリも使用可能

## 📋 事前準備

### 1. Google Cloudアカウント作成
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. Googleアカウントでログイン
3. 新しいプロジェクトを作成
4. **クレジットカード登録**（無料枠内なら課金されません）

### 2. Google Cloud SDK インストール
```bash
# macOS
brew install google-cloud-sdk

# Windows
# https://cloud.google.com/sdk/docs/install からダウンロード

# Linux
curl https://sdk.cloud.google.com | bash
```

### 3. 認証とプロジェクト設定
```bash
# Google Cloudにログイン
gcloud auth login

# プロジェクトIDを設定（your-project-idを実際のIDに変更）
gcloud config set project your-project-id

# Cloud Run APIを有効化
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## 🚀 デプロイ手順

### 1. プロジェクトIDを設定
`deploy-cloudrun.sh` ファイルの `PROJECT_ID` を変更：
```bash
PROJECT_ID="your-actual-project-id"  # ← ここを変更
```

### 2. デプロイ実行
```bash
./deploy-cloudrun.sh
```

### 3. 初回デプロイ時の確認事項
- リージョン選択: `asia-northeast1` (東京)
- 認証なしアクセス: `y` (一般公開)
- サービス名: `mozaiku-app`

## 📊 デプロイ後の確認

### アクセスURL
デプロイ完了後に表示されるURLでアクセス可能：
```
https://mozaiku-app-[hash]-asia-northeast1.a.run.app
```

### 機能確認
1. **自動モザイク処理**
   - 画像アップロード
   - 「物体検出を実行」ボタンクリック
   - AI検出結果の確認

2. **手動モザイク処理**
   - ブラシツールでの手動選択
   - 矩形選択ツール

## 💰 料金管理

### 無料枠の監視
```bash
# 使用量確認
gcloud logging read "resource.type=cloud_run_revision" --limit=10
```

### 予算アラート設定
1. Cloud Console → 請求 → 予算とアラート
2. 予算額: $1 (無料枠超過の早期検知)
3. アラート閾値: 50%, 90%, 100%

## 🔧 トラブルシューティング

### よくある問題

**Q: デプロイ時にメモリ不足エラー**
A: `deploy-cloudrun.sh` の `--memory` を `4Gi` に変更

**Q: 初回起動が遅い**
A: NudeNetモデルのダウンロードで1-2分かかります（初回のみ）

**Q: 画像処理がタイムアウト**
A: `--timeout` を `600` に変更（10分）

### ログ確認
```bash
# リアルタイムログ
gcloud run services logs tail mozaiku-app --region=asia-northeast1

# エラーログ確認
gcloud run services logs read mozaiku-app --region=asia-northeast1 --limit=50
```

## 🔄 更新・再デプロイ

コードを変更した場合：
```bash
# 再デプロイ
./deploy-cloudrun.sh

# または手動で
gcloud run deploy mozaiku-app --source . --region=asia-northeast1
```

## 🗑️ サービス削除

不要になった場合：
```bash
gcloud run services delete mozaiku-app --region=asia-northeast1
```

---

**これで自動モザイク処理機能付きのWebアプリが無料でデプロイできます！**