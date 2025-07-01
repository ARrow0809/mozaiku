#!/bin/bash

# デスクトップにMozaikuのショートカットを作成

echo "🖥️ デスクトップにMozaikuのショートカットを作成します..."

# 現在のディレクトリを取得
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER_PATH="$CURRENT_DIR/mozaiku_launcher.command"

# デスクトップパスを取得
DESKTOP_PATH="$HOME/Desktop"

# ショートカット名
SHORTCUT_NAME="🎯 Mozaiku - 自動モザイク処理.command"

# デスクトップにエイリアスを作成
if [ -f "$LAUNCHER_PATH" ]; then
    # シンボリックリンクを作成
    ln -sf "$LAUNCHER_PATH" "$DESKTOP_PATH/$SHORTCUT_NAME"
    
    echo "✅ デスクトップショートカットを作成しました！"
    echo "   ファイル名: $SHORTCUT_NAME"
    echo "   場所: $DESKTOP_PATH"
    echo ""
    echo "💡 使い方:"
    echo "   1. デスクトップの「🎯 Mozaiku - 自動モザイク処理.command」をダブルクリック"
    echo "   2. ブラウザが自動で開きます"
    echo "   3. 画像をアップロードして自動モザイク処理を実行"
else
    echo "❌ エラー: mozaiku_launcher.command が見つかりません"
    echo "   このスクリプトをMozaikuフォルダ内で実行してください"
fi