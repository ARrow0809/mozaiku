#!/bin/bash

# Mozaiku 自動モザイク処理アプリ - ワンクリック起動スクリプト (macOS)

echo "🎯 Mozaiku - 自動モザイク処理アプリを起動します"
echo "================================================"

# 現在のディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PY="$SCRIPT_DIR/main.py"

echo "📁 作業ディレクトリ: $SCRIPT_DIR"

# Pythonコマンドの検出
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ エラー: Pythonが見つかりません"
    echo "   Python 3.7以上をインストールしてください"
    echo "   https://www.python.org/downloads/"
    read -p "Enterキーを押して終了..."
    exit 1
fi

echo "🐍 使用するPython: $PYTHON_CMD ($(${PYTHON_CMD} --version))"

# main.pyの存在確認
if [ ! -f "$MAIN_PY" ]; then
    echo "❌ エラー: main.py が見つかりません"
    echo "   場所: $MAIN_PY"
    echo "   Mozaikuのファイルが正しく配置されているか確認してください"
    read -p "Enterキーを押して終了..."
    exit 1
fi

cd "$SCRIPT_DIR"

# 仮想環境の確認・作成
if [ ! -d "venv" ]; then
    echo "📦 仮想環境を作成中..."
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ エラー: 仮想環境の作成に失敗しました"
        echo "   Pythonのvenvモジュールが利用できない可能性があります"
        read -p "Enterキーを押して終了..."
        exit 1
    fi
else
    echo "📦 既存の仮想環境を使用します"
fi

# 仮想環境を有効化
echo "🔧 仮想環境を有効化中..."
source venv/bin/activate

# 仮想環境のPythonが存在するか確認
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ エラー: 仮想環境のPythonが見つかりません"
    echo "   仮想環境の作成に失敗した可能性があります"
    echo "   venvフォルダを削除して再実行してください"
    read -p "Enterキーを押して終了..."
    exit 1
fi

echo "✅ 仮想環境が正常に有効化されました"

# 必要なパッケージをインストール
echo "📚 必要なライブラリをインストール中..."
pip install --upgrade pip
pip install fastapi uvicorn python-multipart opencv-python pillow numpy nudenet

# サーバーを起動（バックグラウンド）
echo "🚀 サーバーを起動中..."
echo "   URL: http://localhost:8003"
echo "   機能: 自動モザイク処理 + 手動モザイク処理"
echo ""
echo "💡 初回起動時はAIモデルのダウンロードで時間がかかります"
echo "   ブラウザが自動で開きます..."
echo ""

# サーバーをバックグラウンドで起動
# 仮想環境内のPythonを直接使用
"$SCRIPT_DIR/venv/bin/python" "$MAIN_PY" &
SERVER_PID=$!

# 3秒待ってからブラウザを開く
sleep 3
open http://localhost:8003

echo "✅ Mozaikuが起動しました！"
echo ""
echo "🔴 終了するには:"
echo "   1. このターミナルウィンドウでCtrl+Cを押す"
echo "   2. または以下のコマンドを実行:"
echo "      kill $SERVER_PID"
echo ""

# サーバーの終了を待つ
wait $SERVER_PID