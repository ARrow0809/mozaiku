from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import io
from enum import Enum
from PIL import Image, ImageFilter
import json

app = FastAPI()

class ProcessType(str, Enum):
    mosaic = "mosaic"
    blur = "blur"
    white = "white"
    raw = "raw"

@app.get("/")
async def read_index():
    return FileResponse("../index.html")

@app.get("/test")
async def read_test():
    return FileResponse("test.html")

def apply_mosaic_pil(image, x, y, width, height, block_size=16):
    """PILを使用したモザイク処理"""
    # 指定領域を切り出し
    region = image.crop((x, y, x + width, y + height))
    
    # 小さくリサイズしてからもとのサイズに戻す（モザイク効果）
    small_width = max(1, width // block_size)
    small_height = max(1, height // block_size)
    
    # リサイズしてモザイク効果を作成
    small = region.resize((small_width, small_height), Image.NEAREST)
    mosaic = small.resize((width, height), Image.NEAREST)
    
    # 元画像に貼り付け
    image.paste(mosaic, (x, y))
    return image

def apply_blur_pil(image, x, y, width, height, blur_radius=10):
    """PILを使用したぼかし処理"""
    # 指定領域を切り出し
    region = image.crop((x, y, x + width, y + height))
    
    # ぼかし処理
    blurred = region.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # 元画像に貼り付け
    image.paste(blurred, (x, y))
    return image

def apply_white_pil(image, x, y, width, height):
    """PILを使用した白塗り処理"""
    # 白い矩形を作成
    white_region = Image.new('RGB', (width, height), (255, 255, 255))
    
    # 元画像に貼り付け
    image.paste(white_region, (x, y))
    return image

@app.post("/api/manual_mosaic")
async def manual_mosaic(
    file: UploadFile = File(...),
    mosaic_data: str = Form(...)
):
    """手動でモザイク範囲を指定して処理（PILベース）"""
    try:
        # JSON文字列をパース
        mosaic_areas = json.loads(mosaic_data)
    except json.JSONDecodeError:
        return {"error": "Invalid mosaic data format"}
    
    # 画像を読み込み
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # RGBモードに変換（必要に応じて）
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 各モザイク領域を処理
    for area in mosaic_areas:
        if 'size' in area:
            # ブラシストローク（円形）
            x = int(area['x'])
            y = int(area['y'])
            size = int(area['size'])
            process_type = area.get('process_type', 'mosaic')
            block_size = int(area.get('block_size', 16))
            blur_radius = int(area.get('blur_radius', 10))
            
            # 円形領域を矩形として近似処理
            radius = size // 2
            rect_x = max(0, x - radius)
            rect_y = max(0, y - radius)
            rect_width = min(image.width - rect_x, size)
            rect_height = min(image.height - rect_y, size)
            
            if process_type == 'mosaic':
                image = apply_mosaic_pil(image, rect_x, rect_y, rect_width, rect_height, block_size)
            elif process_type == 'blur':
                image = apply_blur_pil(image, rect_x, rect_y, rect_width, rect_height, blur_radius)
            elif process_type == 'white':
                image = apply_white_pil(image, rect_x, rect_y, rect_width, rect_height)
        else:
            # 矩形選択
            x = int(area['x'])
            y = int(area['y'])
            width = int(area['width'])
            height = int(area['height'])
            process_type = area.get('process_type', 'mosaic')
            block_size = int(area.get('block_size', 16))
            blur_radius = int(area.get('blur_radius', 10))
            
            # 座標が画像範囲内にあることを確認
            x = max(0, x)
            y = max(0, y)
            width = min(image.width - x, width)
            height = min(image.height - y, height)
            
            if width > 0 and height > 0:
                if process_type == 'mosaic':
                    image = apply_mosaic_pil(image, x, y, width, height, block_size)
                elif process_type == 'blur':
                    image = apply_blur_pil(image, x, y, width, height, blur_radius)
                elif process_type == 'white':
                    image = apply_white_pil(image, x, y, width, height)
    
    # 画像をJPEGとして出力
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=90)
    output.seek(0)
    
    return StreamingResponse(output, media_type="image/jpeg")

@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    confidence: float = Form(0.5),
    process_type: ProcessType = Form(ProcessType.raw),
    block_size: int = Form(16),
    blur_radius: int = Form(21)
):
    """基本的な画像処理（AI検出なし）"""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # RGBモードに変換
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # rawの場合はそのまま返す
    if process_type == ProcessType.raw:
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=90)
        output.seek(0)
        return StreamingResponse(output, media_type="image/jpeg")
    
    # AI検出機能は無効（Vercel制限のため）
    # 手動モザイク機能のみ提供
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=90)
    output.seek(0)
    return StreamingResponse(output, media_type="image/jpeg")

# Vercel用のハンドラー
def handler(request):
    return app(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)