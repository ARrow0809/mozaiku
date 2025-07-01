#!/bin/bash

# Mozaiku 停止スクリプト

echo "🔴 Mozaikuサーバーを停止します..."

# Pythonプロセス（main.py）を検索して終了
pkill -f "python main.py"
pkill -f "python3 main.py"

# ポート8002を使用しているプロセスを終了
lsof -ti:8002 | xargs kill -9 2>/dev/null

echo "✅ Mozaikuサーバーを停止しました"
echo "   ブラウザタブも手動で閉じてください"