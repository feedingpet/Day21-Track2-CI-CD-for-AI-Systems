# Hướng Dẫn Thu Thập Bằng Chứng Bonus 3, 4, 5

Tài liệu này hướng dẫn bạn cách thực hiện các thao tác và vị trí chụp ảnh để lấy trọn vẹn điểm cho các thử thách nâng cao.

---

## 🟢 Bonus 3: Báo Cáo Hiệu Suất Tự Động (4 điểm)

**Mục tiêu:** Chứng minh hệ thống tự tạo ra file báo cáo chi tiết (`report.txt`) sau mỗi lần huấn luyện.

### Thao tác:
1. Thực hiện `git push` code lên GitHub.
2. Đợi Pipeline chạy xong (tất cả các bước đều xanh).

### Bằng chứng cần chụp:
1. **Ảnh 1 (Vị trí Artifact):** Vào tab **Actions** -> Chọn lần chạy vừa xong -> Kéo xuống cuối trang phần **Artifacts**. Chụp màn hình thấy file `model-reports` đã được tải lên thành công.
2. **Ảnh 2 (Nội dung báo cáo):** Nhấn vào `model-reports` để tải về máy, giải nén và mở file `report.txt`. Chụp màn hình nội dung file (phải thấy bảng Classification Report và Confusion Matrix).

---

## 🟡 Bonus 4: Hoàn Trả Về Phiên Bản Trước - Safe Guard (4 điểm)

**Mục tiêu:** Chứng minh Pipeline sẽ **chặn (Fail)** nếu mô hình mới tệ hơn mô hình cũ.

### Thao tác:
1. Đảm bảo bạn đã có ít nhất một lần chạy thành công trước đó (để có mốc Accuracy lưu trên Cloud).
2. Mở file `params.yaml`, cố tình làm mô hình tệ đi (Ví dụ: với `random_forest`, hãy chỉnh `max_depth: 1` hoặc `n_estimators: 1`).
3. `git add`, `git commit`, `git push`.
4. Đợi Pipeline chạy đến bước **Eval**. Lúc này Pipeline sẽ bị **BÁO ĐỎ (FAIL)**.

### Bằng chứng cần chụp:
1. **Ảnh 1 (Pipeline bị chặn):** Chụp màn hình tổng quan Workflow thấy job **Eval** bị màu đỏ ❌.
2. **Ảnh 2 (Log so sánh):** Nhấn vào job **Eval** -> Mở phần `Check eval gate`. Chụp màn hình dòng log báo lỗi có nội dung tương tự:
   `❌ Accuracy 0.2500 is lower than previous 0.8500. Rollback/Abort deploy.`

---

## 🔵 Bonus 5: Cảnh Báo Lệch Lạc Dữ Liệu (4 điểm)

**Mục tiêu:** Chứng minh hệ thống có kiểm tra tỷ lệ các lớp dữ liệu trước khi huấn luyện.

### Thao tác:
1. Chạy Pipeline (bất kỳ lần nào thành công hoặc thất bại đều được).

### Bằng chứng cần chụp:
1. **Ảnh 1 (Log huấn luyện):** Vào tab **Actions** -> Chọn job **Train** -> Nhấn mở rộng bước **Train model**.
2. Tìm đoạn log có tiêu đề: `--- Kiem tra phan phoi nhan (Bonus 5) ---`.
3. Chụp màn hình đoạn đó, phải thấy được tỷ lệ % của các lớp 0, 1, 2 (Ví dụ: `Lop 0: 33.33%`, ...).

---

> [!TIP]
> Sau khi chụp xong, bạn hãy copy các ảnh này vào file báo cáo cuối cùng để nộp cho thầy cô nhé!
