import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List
import cv2
import numpy as np
import io
from enum import Enum
from nudenet.nudenet import NudeDetector # NudeNetをインポート
from PIL import Image # PILをインポート
import tempfile # 一時ファイル作成用
import os # ファイル削除用

app = FastAPI()

# NudeNetモデルのロード
# 初回実行時にモデルがダウンロードされます
detector = NudeDetector()

def apply_block_processing(img, mask, process_type, block_size, blur_radius):
    """マスクされた領域にブロック単位で処理を適用する共通関数"""
    h, w = img.shape[:2]
    
    if process_type == 'mosaic':
        # ブロック単位でモザイク処理
        for block_y in range(0, h, block_size):
            for block_x in range(0, w, block_size):
                block_y2 = min(block_y + block_size, h)
                block_x2 = min(block_x + block_size, w)
                
                # ブロック内にマスクされたピクセルがあるかチェック
                block_mask = mask[block_y:block_y2, block_x:block_x2]
                if np.any(block_mask > 0):
                    # ブロック全体をモザイク処理（平均色で塗りつぶし）
                    block_roi = img[block_y:block_y2, block_x:block_x2]
                    if block_roi.size > 0:
                        avg_color = np.mean(block_roi.reshape(-1, 3), axis=0)
                        img[block_y:block_y2, block_x:block_x2] = avg_color
                        
    elif process_type == 'blur':
        # 全体をぼかし処理
        radius_blur = blur_radius if blur_radius % 2 != 0 else blur_radius + 1
        blurred = cv2.GaussianBlur(img, (radius_blur, radius_blur), 0)
        
        # ブロック単位で適用
        for block_y in range(0, h, block_size):
            for block_x in range(0, w, block_size):
                block_y2 = min(block_y + block_size, h)
                block_x2 = min(block_x + block_size, w)
                
                # ブロック内にマスクされたピクセルがあるかチェック
                block_mask = mask[block_y:block_y2, block_x:block_x2]
                if np.any(block_mask > 0):
                    # ブロック全体をぼかし処理で置き換え
                    img[block_y:block_y2, block_x:block_x2] = blurred[block_y:block_y2, block_x:block_x2]
                    
    elif process_type == 'white':
        # ブロック単位で白塗り
        for block_y in range(0, h, block_size):
            for block_x in range(0, w, block_size):
                block_y2 = min(block_y + block_size, h)
                block_x2 = min(block_x + block_size, w)
                
                # ブロック内にマスクされたピクセルがあるかチェック
                block_mask = mask[block_y:block_y2, block_x:block_x2]
                if np.any(block_mask > 0):
                    # ブロック全体を白で塗りつぶし
                    img[block_y:block_y2, block_x:block_x2] = 255

class ProcessType(str, Enum):
    mosaic = "mosaic"
    blur = "blur"
    white = "white"
    raw = "raw"

class ManualMosaicRequest(BaseModel):
    x: int
    y: int
    width: int
    height: int
    process_type: ProcessType = ProcessType.mosaic
    block_size: int = 16
    blur_radius: int = 21

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    confidence: float = Form(0.5),
    process_type: ProcessType = Form(ProcessType.mosaic),
    block_size: int = Form(16),
    blur_radius: int = Form(21) # Must be odd
):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if process_type == ProcessType.raw:
        _, encoded_img = cv2.imencode(".jpg", img)
        return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")

    # OpenCV画像をPIL Imageに変換し、一時ファイルに保存
    # NudeNetはNumPy配列を直接受け取らないため
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            pil_img.save(temp_file.name)
            temp_file_path = temp_file.name

        # NudeNetで局部を検出
        # NudeNetは検出されたクラスとバウンディングボックスを返します
        detections = detector.detect(temp_file_path)
        
        # デバッグ: 検出されたラベルをログ出力
        print(f"検出されたラベル: {[det['class'] for det in detections]}")
        print(f"検出詳細: {detections}")
        
        # 局部のみを対象とするラベルを定義（NudeNetの実際のラベル名）
        # 一般的なNudeNetのラベル名を試す（男性の睾丸も含む）
        target_labels = [
            'EXPOSED_GENITALIA_F', 'COVERED_GENITALIA_F',
            'EXPOSED_GENITALIA_M', 'COVERED_GENITALIA_M', 
            'EXPOSED_ANUS', 'COVERED_ANUS',
            'GENITALIA_COVERED', 'GENITALIA_EXPOSED',
            'ANUS_COVERED', 'ANUS_EXPOSED',
            'VAGINA_COVERED', 'VAGINA_EXPOSED',
            'PENIS_COVERED', 'PENIS_EXPOSED',
            'TESTICLES_COVERED', 'TESTICLES_EXPOSED',
            'SCROTUM_COVERED', 'SCROTUM_EXPOSED'
        ]
        
        # 検出されたバウンディングボックスにモザイク処理
        for det in detections:
            # 一時的にすべてのラベルを処理対象にしてデバッグ
            if det['score'] >= confidence:
                print(f"処理中のラベル: {det['class']}, 信頼度: {det['score']}")
                # 局部関連のラベルのみを処理（より柔軟な条件、睾丸も含む）
                label_lower = det['class'].lower()
                is_genital = any(keyword in label_lower for keyword in ['genital', 'penis', 'vagina', 'anus', 'pussy', 'testicle', 'scrotum', 'ball'])
                if not is_genital:
                    print(f"スキップ: {det['class']} (局部ではない)")
                    continue
                
                x1, y1, w, h = det['box'] # NudeDetectorはx, y, w, hで返す
                x2, y2 = x1 + w, y1 + h
                
                # バウンディングボックスの座標を整数に変換
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # 座標が画像範囲内にあることを確認
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(img.shape[1], x2)
                y2 = min(img.shape[0], y2)

                # ROI (Region of Interest)
                roi = img[y1:y2, x1:x2]
                h, w, _ = roi.shape

                if h > 0 and w > 0:
                    if process_type == ProcessType.mosaic:
                        b_h = max(1, h // block_size)
                        b_w = max(1, w // block_size)
                        small = cv2.resize(roi, (b_w, b_h), interpolation=cv2.INTER_LINEAR)
                        processed_roi = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
                    elif process_type == ProcessType.blur:
                        radius = blur_radius if blur_radius % 2 != 0 else blur_radius + 1
                        processed_roi = cv2.GaussianBlur(roi, (radius, radius), 0)
                    elif process_type == ProcessType.white:
                        processed_roi = np.full((h, w, 3), 255, dtype=np.uint8)
                    
                    img[y1:y2, x1:x2] = processed_roi
    except Exception as e:
        print(f"Error during NudeNet processing: {e}")
        # エラーが発生した場合でも、元の画像を返すか、エラー画像を返すか選択
        # 今回は元の画像を返す
        _, encoded_img = cv2.imencode(".jpg", img)
        return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path) # 一時ファイルを削除

    _, encoded_img = cv2.imencode(".jpg", img)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")

@app.post("/api/manual_mosaic")
async def manual_mosaic(
    file: UploadFile = File(...),
    mosaic_data: str = Form(...)  # JSON文字列として受け取る
):
    """手動でモザイク範囲を指定して処理"""
    import json
    
    # JSON文字列をパース
    try:
        mosaic_areas = json.loads(mosaic_data)
    except json.JSONDecodeError:
        return {"error": "Invalid mosaic data format"}
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # ブラシストロークと矩形選択を分離して処理
    brush_areas = [area for area in mosaic_areas if 'size' in area]
    rect_areas = [area for area in mosaic_areas if 'size' not in area]
    
    # ブラシストロークがある場合、統合マスクを作成して一括処理
    if brush_areas:
        # 処理タイプごとにグループ化
        brush_groups = {}
        for area in brush_areas:
            process_type = area.get('process_type', 'mosaic')
            block_size = int(area.get('block_size', 16))
            blur_radius = int(area.get('blur_radius', 21))
            
            key = (process_type, block_size, blur_radius)
            if key not in brush_groups:
                brush_groups[key] = []
            brush_groups[key].append(area)
        
        # 各グループごとに統合マスクを作成して処理
        for (process_type, block_size, blur_radius), areas in brush_groups.items():
            # 統合マスクを作成
            combined_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
            
            for area in areas:
                x = int(area['x'])
                y = int(area['y'])
                size = int(area['size'])
                radius = size // 2
                cv2.circle(combined_mask, (x, y), radius, 255, -1)
            
            # 統合マスクに対してブロック単位で処理を適用
            apply_block_processing(img, combined_mask, process_type, block_size, blur_radius)
    
    # 矩形選択を処理
    for area in rect_areas:
        # 矩形選択
        x = int(area['x'])
        y = int(area['y'])
        width = int(area['width'])
        height = int(area['height'])
        process_type = area.get('process_type', 'mosaic')
        block_size = int(area.get('block_size', 16))
        blur_radius = int(area.get('blur_radius', 21))
        
        # 座標が画像範囲内にあることを確認
        x = max(0, x)
        y = max(0, y)
        x2 = min(img.shape[1], x + width)
        y2 = min(img.shape[0], y + height)
        
        if x2 > x and y2 > y:
            # ROI (Region of Interest)
            roi = img[y:y2, x:x2]
            h, w, _ = roi.shape
            
            if h > 0 and w > 0:
                if process_type == 'mosaic':
                    b_h = max(1, h // block_size)
                    b_w = max(1, w // block_size)
                    small = cv2.resize(roi, (b_w, b_h), interpolation=cv2.INTER_LINEAR)
                    processed_roi = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
                elif process_type == 'blur':
                    radius = blur_radius if blur_radius % 2 != 0 else blur_radius + 1
                    processed_roi = cv2.GaussianBlur(roi, (radius, radius), 0)
                elif process_type == 'white':
                    processed_roi = np.full((h, w, 3), 255, dtype=np.uint8)
                else:
                    processed_roi = roi  # 処理しない
                
                img[y:y2, x:x2] = processed_roi
    
    _, encoded_img = cv2.imencode(".jpg", img)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    # Cloud Runはポート8080を使用
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)