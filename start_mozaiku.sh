#!/bin/bash

# Mozaiku 自動モザイク処理アプリ - ワンクリック起動スクリプト (macOS)

echo "🎯 Mozaiku - 自動モザイク処理アプリを起動します"
echo "================================================"

# 現在のディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 仮想環境の確認・作成
if [ ! -d "venv" ]; then
    echo "📦 仮想環境を作成中..."
    python3 -m venv venv
fi

# 仮想環境を有効化
echo "🔧 仮想環境を有効化中..."
source venv/bin/activate

# 必要なパッケージをインストール
echo "📚 必要なライブラリをインストール中..."
pip install --upgrade pip
pip install fastapi uvicorn python-multipart opencv-python pillow numpy nudenet

# サーバーを起動（バックグラウンド）
echo "🚀 サーバーを起動中..."
echo "   URL: http://localhost:8002"
echo "   機能: 自動モザイク処理 + 手動モザイク処理"
echo ""
echo "💡 初回起動時はAIモデルのダウンロードで時間がかかります"
echo "   ブラウザが自動で開きます..."
echo ""

# サーバーをバックグラウンドで起動
python main.py &
SERVER_PID=$!

# 3秒待ってからブラウザを開く
sleep 3
open http://localhost:8002

echo "✅ Mozaikuが起動しました！"
echo ""
echo "🔴 終了するには:"
echo "   1. このターミナルウィンドウでCtrl+Cを押す"
echo "   2. または以下のコマンドを実行:"
echo "      kill $SERVER_PID"
echo ""

# サーバーの終了を待つ
wait $SERVER_PID