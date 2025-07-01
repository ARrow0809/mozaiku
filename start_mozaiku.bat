@echo off
echo ========================================
echo    Mozaiku 自動モザイク処理アプリ
echo ========================================
echo.
echo 起動中...
echo.

REM 仮想環境をアクティベート
call venv\Scripts\activate

REM 必要なライブラリをインストール（初回のみ）
echo 依存関係をチェック中...
pip install fastapi uvicorn python-multipart opencv-python nudenet pillow numpy

REM サーバーを起動（バックグラウンド）
echo.
echo サーバーを起動中...
echo アクセスURL: http://localhost:8000
echo.
start /B python main.py

REM 3秒待ってからブラウザを開く
timeout /t 3 /nobreak >nul
start http://localhost:8000

echo.
echo ブラウザが開きました！
echo サーバーを停止するには、このウィンドウを閉じてください。
echo.
pause