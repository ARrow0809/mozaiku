#!/bin/bash

# Mozaiku Launcher - ダブルクリックで起動

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# ターミナルウィンドウのタイトルを設定
echo -ne "\033]0;Mozaiku - 自動モザイク処理アプリ\007"

# メイン起動スクリプトを実行
./start_mozaiku.sh