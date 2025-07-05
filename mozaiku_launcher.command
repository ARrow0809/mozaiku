#!/bin/bash

# Mozaiku Launcher - ダブルクリックで起動

# スクリプトの絶対パスを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_SCRIPT="$SCRIPT_DIR/start_mozaiku.sh"

# ターミナルウィンドウのタイトルを設定
echo -ne "\033]0;Mozaiku - 自動モザイク処理アプリ\007"

echo "🎯 Mozaiku Launcher"
echo "スクリプト場所: $SCRIPT_DIR"

# start_mozaiku.shの存在確認
if [ ! -f "$START_SCRIPT" ]; then
    echo "❌ エラー: start_mozaiku.sh が見つかりません"
    echo "   場所: $START_SCRIPT"
    echo "   Mozaikuのファイルが正しく配置されているか確認してください"
    read -p "Enterキーを押して終了..."
    exit 1
fi

# 実行権限の確認と設定
if [ ! -x "$START_SCRIPT" ]; then
    echo "🔧 実行権限を設定中..."
    chmod +x "$START_SCRIPT"
fi

# スクリプトのディレクトリに移動
cd "$SCRIPT_DIR"

# メイン起動スクリプトを実行
echo "🚀 Mozaikuを起動中..."
"$START_SCRIPT"