## Bộ Siêu Tham Số Đã Chọn và Lý Do (Kết Quả Bước 1)

Dựa trên quá trình thực nghiệm và theo dõi kết quả thông qua MLflow UI (các minh chứng hình ảnh được lưu tại thư mục `summit/`), tôi đã tiến hành chạy thử nghiệm mô hình `RandomForestClassifier` với 3 cấu hình siêu tham số (hyperparameters) khác nhau:

1. **Lần 1 (Mặc định):** `n_estimators: 100`, `max_depth: 5`, `min_samples_split: 2`
2. **Lần 2 (Mô hình nhỏ):** `n_estimators: 50`, `max_depth: 3`, `min_samples_split: 2`
3. **Lần 3 (Mô hình phức tạp):** `n_estimators: 200`, `max_depth: 10`, `min_samples_split: 5`

### 🏆 Bộ siêu tham số được chọn cuối cùng:
- `n_estimators` (Số lượng cây): **200**
- `max_depth` (Độ sâu tối đa của cây): **10**
- `min_samples_split` (Số mẫu tối thiểu để tách nút): **5**

### 💡 Lý do lựa chọn:
Thông qua việc phân tích và so sánh trực quan trên biểu đồ của MLflow UI (dựa trên các hình chụp `B1_gia_tri_...` và tính năng Compare), bộ tham số ở lần chạy thứ 3 đã chứng minh được hiệu năng tốt nhất với các lý do sau:

1. **Đạt chỉ số đo lường cao nhất:** Với cấu hình `n_estimators=200` và `max_depth=10`, biểu đồ metrics cho thấy cả hai chỉ số **Accuracy** và **F1-Score** đều đạt mức cao nhất trong cả 3 lần thử nghiệm.
2. **Khả năng học tốt hơn:** Việc tăng độ sâu của cây (`max_depth=10`) và số lượng cây (`n_estimators=200`) giúp mô hình học được các mối liên hệ phức tạp (non-linear) ẩn sâu trong tập dữ liệu mà cấu hình mặc định hoặc cấu hình nhỏ (`max_depth=3`) đã bỏ sót (underfitting).
3. **Kiểm soát Overfitting:** Mặc dù độ sâu của cây được tăng lên, nhưng việc chủ động tăng `min_samples_split` lên 5 (thay vì 2 như mặc định) đã tạo ra một "chốt chặn" hiệu quả, giúp các nhánh cây không bị chia nhỏ quá đà theo nhiễu của dữ liệu huấn luyện, từ đó đảm bảo mô hình giữ được sự tổng quát hóa tốt trên tập đánh giá (eval set).

Do đó, bộ tham số thứ 3 được lựa chọn làm cấu hình tốt nhất và đã được lưu vào file `params.yaml` để sử dụng làm chuẩn (baseline) cho các bước tiếp theo trong quy trình CI/CD.
