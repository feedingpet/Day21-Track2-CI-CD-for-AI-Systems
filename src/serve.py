from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage
import joblib
import os

app = FastAPI()

# Đọc tên bucket từ biến môi trường (được đặt trong systemd service)
GCS_BUCKET = os.environ.get("GCS_BUCKET", "default-bucket-name-if-not-set")
GCS_MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = os.path.expanduser("~/models/model.pkl")


def download_model():
    """Tải file model.pkl từ GCS về máy khi server khởi động."""
    # Đảm bảo thư mục đích tồn tại
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # TODO 2.6.1: Tạo một storage.Client()
    client = storage.Client()
    
    # TODO 2.6.2: Lấy bucket bằng client.bucket(GCS_BUCKET)
    bucket = client.bucket(GCS_BUCKET)
    
    # TODO 2.6.3: Lấy blob bằng bucket.blob(GCS_MODEL_KEY)
    blob = bucket.blob(GCS_MODEL_KEY)
    
    # TODO 2.6.4: Tải file xuống bằng blob.download_to_filename(MODEL_PATH)
    blob.download_to_filename(MODEL_PATH)
    
    # TODO 2.6.5: In thông báo thành công
    print(f"✅ Tải model thành công từ gs://{GCS_BUCKET}/{GCS_MODEL_KEY} xuống {MODEL_PATH}")


# Gọi hàm này khi module được import (chạy khi server khởi động)
# Lưu ý: Khi chạy dưới local để dev mà chưa set biến môi trường hay file json thì hàm này sẽ báo lỗi.
# Nhưng khi chạy trên VM, systemd đã cấu hình đủ mọi thứ.
if os.environ.get("GCS_BUCKET"):
    download_model()
    model = joblib.load(MODEL_PATH)
else:
    print("⚠️ CẢNH BÁO: Không tìm thấy biến môi trường GCS_BUCKET, bỏ qua bước tải model (Dùng cho local dev).")
    # Khởi tạo model là None hoặc mock để không bị lỗi khi test local
    model = None


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    """Endpoint kiểm tra sức khỏe server. GitHub Actions dùng endpoint này để xác nhận deploy thành công."""
    # TODO 2.6.6: Trả về dict {"status": "ok"}
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    """
    Endpoint suy luận.

    Đầu vào: JSON {"features": [f1, f2, ..., f12]}
    Đầu ra:  JSON {"prediction": <0|1|2>, "label": <"thấp"|"trung_bình"|"cao">}
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded. Cannot serve prediction.")

    # TODO 2.6.7: Kiểm tra len(req.features) == 12.
    if len(req.features) != 12:
        raise HTTPException(status_code=400, detail="Expected 12 features (wine quality)")

    # TODO 2.6.8: Gọi model.predict([req.features]) để lấy kết quả dự đoán.
    # Hàm predict trả về 1 list/array, ta lấy phần tử đầu tiên
    pred_value = model.predict([req.features])[0]
    pred_int = int(pred_value) # Convert kiểu numpy sang kiểu int thuần của Python

    # TODO 2.6.9: Trả về dict chứa "prediction" (int) và "label" (string).
    label_map = {0: "thấp", 1: "trung_bình", 2: "cao"}
    label_str = label_map.get(pred_int, "không xác định")

    return {
        "prediction": pred_int,
        "label": label_str
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
