# Python 3.9 slim image
FROM python:3.9-slim

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txtをコピーして依存関係をインストール
COPY requirements-cloudrun.txt .
RUN pip install --no-cache-dir -r requirements-cloudrun.txt

# アプリケーションファイルをコピー
COPY main.py .
COPY index.html .

# ポート8080を公開（Cloud Runのデフォルト）
EXPOSE 8080

# アプリケーションを起動
CMD ["python", "main.py"]