# Mozaiku - YOLOv8 Object Detection Web App

**YOLOv8を使用したリアルタイム物体検出Webアプリケーション**

画像をアップロードするだけで、AI（YOLOv8）が自動的に物体を検出し、バウンディングボックスと信頼度スコアを表示します。

## 機能

- **画像アップロード**: ドラッグ&ドロップまたはクリックで画像を選択
- **AI物体検出**: YOLOv8モデルによる高精度な物体検出
- **視覚化**: 検出された物体をバウンディングボックスで表示
- **信頼度表示**: 各検出結果の信頼度スコアを表示
- **Webインターフェース**: 使いやすいモダンなUI

## クイックスタート

### 必要な環境
- Python 3.8以上
- pip

### インストール・起動方法

1. **リポジトリをクローン**
```bash
git clone https://github.com/ARrow0809/mozaiku.git
cd mozaiku
```

2. **仮想環境を作成・有効化**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **依存関係をインストール**
```bash
pip install -r requirements.txt
```

4. **アプリケーションを起動**
```bash
python main.py
```

5. **ブラウザでアクセス**
```
http://localhost:8000
```

## 使い方

1. **画像をアップロード**
   - ドラッグ&ドロップエリアに画像をドロップ
   - または「画像を選択」ボタンをクリックして画像を選択

2. **物体検出を実行**
   - 「物体検出を実行」ボタンをクリック
   - AIが自動的に画像内の物体を検出

3. **結果を確認**
   - 検出された物体がバウンディングボックスで囲まれて表示
   - 各物体のラベルと信頼度スコアが表示

## 技術スタック

- **バックエンド**: FastAPI (Python)
- **AI/ML**: YOLOv8 (Ultralytics)
- **フロントエンド**: HTML5, CSS3, JavaScript
- **画像処理**: OpenCV, PIL

## プロジェクト構成

```
mozaiku/
├── main.py              # FastAPIバックエンドサーバー
├── index.html           # フロントエンドUI
├── requirements.txt     # Python依存関係
├── README.md           # このファイル
├── LICENSE             # ライセンス
└── .gitignore          # Git除外設定
```

## 対応している物体クラス

YOLOv8は80種類の物体を検出できます：
- 人、動物（犬、猫、鳥など）
- 乗り物（車、バイク、飛行機など）
- 家具（椅子、テーブル、ソファなど）
- 電子機器（テレビ、ノートパソコン、携帯電話など）
- その他多数

## カスタマイズ

### ポート番号の変更
`main.py`の最後の行を編集：
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # ポート番号を変更
```

### 検出信頼度の調整
`main.py`の`detect_objects`関数内で調整：
```python
results = model(image, conf=0.5)  # 信頼度閾値を変更（0.0-1.0）
```

## 開発状況

**GitHubへのデプロイ完了** (2024年12月)
- ソースコードがGitHubリポジトリに正常にプッシュされました
- 他の環境でも簡単にクローン・起動が可能です

## コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## リンク

- **GitHub Repository**: https://github.com/ARrow0809/mozaiku.git
- **YOLOv8 Documentation**: https://docs.ultralytics.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

## トラブルシューティング

### よくある問題

**Q: モデルのダウンロードに時間がかかる**
A: 初回起動時にYOLOv8モデル（約6MB）が自動ダウンロードされます。インターネット接続を確認してください。

**Q: 画像がアップロードできない**
A: 対応形式（JPG, PNG, GIF, BMP, TIFF）の画像を使用してください。

**Q: ポートが使用中エラー**
A: 他のアプリケーションがポート8000を使用している可能性があります。ポート番号を変更するか、他のアプリケーションを停止してください。

---

**Mozaikuをお使いいただき、ありがとうございます！**