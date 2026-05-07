# Kế hoạch Triển khai Bước 2 & Bước 3

Dựa trên tài liệu hướng dẫn, đây là bản thiết kế kế hoạch chi tiết để hoàn thành hệ thống MLOps. Kế hoạch được chia thành các nhóm công việc: những việc bạn phải tự làm trên Cloud (vì liên quan đến tài khoản cá nhân) và những việc tôi (AI) có thể viết code thay bạn.

---

## BƯỚC 2: Xây dựng Pipeline CI/CD Tự Động

### Giai đoạn 2.1: Chuẩn bị Hạ tầng Cloud & DVC 👤 *(Bạn tự làm trên Terminal)*
1. **Tạo Bucket:** Mở GCP, tạo một Cloud Storage bucket để chứa dữ liệu và mô hình.
2. **Tạo Credentials:** Tạo Service Account, cấp quyền `objectAdmin` cho bucket, và tải file `sa-key.json` về máy.
3. **Cấu hình DVC:** Trỏ DVC đến bucket vừa tạo, nạp file `sa-key.json` cho DVC, dùng `dvc add` để theo dõi data và dùng lệnh `dvc push` để đẩy dữ liệu lên Cloud.
4. **Tạo Virtual Machine (VM):** Tạo 1 máy ảo Ubuntu trên Cloud, mở firewall cổng `8000`, và lấy địa chỉ IP Public.

### Giai đoạn 2.2: Lập trình API & Test 🤖 *(Tôi sẽ code giúp bạn)*
1. **Viết `src/serve.py`:** Code ứng dụng FastAPI để tải model từ GCS xuống và mở 2 endpoint (`/health`, `/predict`).
2. **Viết `tests/test_train.py`:** Code các hàm test tự động bằng `pytest` (giả lập dữ liệu, kiểm tra hàm train, kiểm tra các file output).

### Giai đoạn 2.3: Cấu hình Server & GitHub Secrets 👤 *(Bạn tự làm)*
1. **Setup VM:** SSH vào VM, cài đặt thư viện (`pip install fastapi uvicorn...`), copy file `sa-key.json` và `serve.py` lên VM.
2. **Setup Systemd:** Tạo service để VM giữ server luôn chạy.
3. **Tạo SSH Key:** Tạo file SSH Key trên máy cá nhân và copy public key lên VM.
4. **Cấu hình GitHub Secrets:** Lên repo GitHub, nhập 5 biến bí mật: `CLOUD_CREDENTIALS`, `CLOUD_BUCKET`, `VM_HOST`, `VM_USER`, `VM_SSH_KEY`.

### Giai đoạn 2.4: Viết CI/CD Workflow 🤖 *(Tôi sẽ code giúp bạn)*
1. **Viết `.github/workflows/mlops.yml`:** Lên kịch bản tự động cho GitHub Actions gồm 4 công đoạn:
   - `test`: Chạy Unit Test.
   - `train`: Kéo data từ cloud, chạy `train.py`, đẩy model lên bucket, lưu metrics.
   - `eval`: Đọc accuracy, nếu >= 0.70 thì cho đi tiếp, nếu nhỏ hơn thì đánh tạch pipeline.
   - `deploy`: SSH vào VM và restart lại service để chạy model mới.

### Giai đoạn 2.5: Triển khai lần đầu 👤 *(Bạn thao tác)*
1. Thêm file `__init__.py` vào `src/` và `tests/`.
2. Commit toàn bộ code và file `.dvc` (không commit file data thật).
3. `git push` lên GitHub và ngắm nhìn Actions chạy tự động.

---

## BƯỚC 3: Huấn Luyện Liên Tục (Continuous Training)

Bước này cực kỳ nhanh vì toàn bộ hệ thống đã tự động hóa.

1. **Sinh dữ liệu mới:** Chạy `python add_new_data.py`. 👤
2. **Báo cho DVC:** Chạy `dvc add data/train_phase1.csv`. 👤
3. **Commit Git:** Commit file `train_phase1.csv.dvc`. 👤
4. **Đẩy lên Cloud:** Chạy `dvc push`. 👤
5. **Kích hoạt CI/CD:** Chạy `git push` lên GitHub. Lúc này hệ thống tự nhận diện có data mới và sẽ lôi code cũ ra train lại trên lượng data bự hơn. 👤
6. **Báo cáo:** So sánh kết quả Accuracy giữa Bước 2 và Bước 3 và lưu vào báo cáo. 👤

---

## Open Questions
> [!IMPORTANT]
> Để bắt đầu, tôi đề xuất chúng ta sẽ xử lý các phần code Python và YAML trước (tức là Giai đoạn 2.2 và 2.4).
> 
> Bạn có muốn tôi tiến hành viết ngay mã nguồn cho các file **`src/serve.py`**, **`tests/test_train.py`** và **`.github/workflows/mlops.yml`** ngay bây giờ không?
