## Link build model: https://colab.research.google.com/drive/1HnVuGjvwWL3Zk6otd895hso125S3Ry2Y?usp=sharing
## Result: toxic_comment_model.h5

# UI Demo - Phát hiện bình luận tiêu cực (Toxic Comments Detection)

Dự án này cung cấp một ứng dụng web tương tác sử dụng Streamlit để phát hiện bình luận độc hại (toxic comments) dựa trên mô hình deep learning đã được huấn luyện. Ứng dụng có thể phân loại bình luận thành 6 loại độc hại: `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`.

---

## 1. Cấu trúc dự án

```
Toxic-Comments-Detection-Demo/
├── ui_demo.py                    # Ứng dụng Streamlit chính
├── toxic_comment_model.h5        # Mô hình đã được huấn luyện
├── data/
│   ├── train/
│   │   └── train.csv            # Dữ liệu huấn luyện (Jigsaw dataset)
│   └── test/
│       ├── test.csv              # Dữ liệu test
│       └── test_demo.csv         # Dữ liệu demo
├── toxic_comments.csv            # Kết quả bình luận độc hại (tự động tạo)
└── non_toxic_comments.csv        # Kết quả bình luận không độc hại (tự động tạo)
```

---

## 2. Yêu cầu môi trường

Khuyến nghị sử dụng Python 3.10+ (Anaconda hoặc venv).

### Cài đặt các thư viện cần thiết:

```bash
pip install streamlit tensorflow pandas numpy
```

Hoặc tạo môi trường mới với conda:

```bash
conda create -n toxic-comments python=3.10 -y
conda activate toxic-comments
pip install streamlit tensorflow pandas numpy
```

---

## 3. Chuẩn bị dữ liệu

### Yêu cầu:
1. File `toxic_comment_model.h5`: Mô hình đã được huấn luyện (phải có trong thư mục gốc)
2. File `data/train/train.csv`: Dữ liệu huấn luyện để adapt TextVectorization
   - Phải có cột `comment_text` chứa các bình luận
   - Các cột nhãn: `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`

> **Lưu ý**: File `data/train/train.csv` có thể có dung lượng lớn (>50MB). Nếu không có sẵn, bạn cần tải về từ [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge) và đặt vào đúng đường dẫn.

---

## 4. Chạy ứng dụng UI Demo

### Bước 1: Mở terminal tại thư mục dự án

```bash
cd Toxic-Comments-Detection-Demo
```

### Bước 2: Kích hoạt môi trường (nếu dùng conda/venv)

```bash
conda activate toxic-comments  # hoặc source venv/bin/activate
```

### Bước 3: Chạy ứng dụng Streamlit

```bash
streamlit run ui_demo.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ `http://localhost:8501`

---

## 5. Hướng dẫn sử dụng

### 5.1. Kiểm tra bình luận đơn lẻ

1. Trong giao diện, chọn nút **"Enter comment"** (mặc định)
2. Nhập bình luận cần kiểm tra vào ô text area
3. Nhấn nút **"Submit"**
4. Kết quả sẽ hiển thị:
   - ✅ **Không độc hại**: Nếu bình luận không chứa nội dung độc hại
   - ❌ **Độc hại**: Hiển thị các loại độc hại được phát hiện (toxic, severe_toxic, obscene, threat, insult, identity_hate)

**Ví dụ:**
- Input: `"I hate you, you are stupid"`
- Output: `The comment is toxic! Types of toxicity: toxic, insult`

### 5.2. Kiểm tra hàng loạt từ file CSV

1. Chọn nút **"Insert from file"**
2. Upload file CSV có cột `comment_text` chứa các bình luận cần kiểm tra
3. Nhấn nút **"Submit"**
4. Ứng dụng sẽ:
   - Hiển thị kết quả cho từng bình luận trên giao diện
   - Tự động lưu kết quả vào 2 file:
     - `toxic_comments.csv`: Chứa các bình luận độc hại và loại độc hại
     - `non_toxic_comments.csv`: Chứa các bình luận không độc hại

**Định dạng file CSV đầu vào:**
```csv
comment_text
"This is a normal comment"
"I hate you"
"Great work!"
```

---

## 6. Cách hoạt động

### 6.1. Tiền xử lý văn bản

Ứng dụng tự động làm sạch văn bản trước khi đưa vào mô hình:
- Chuyển về chữ thường
- Xóa URL và liên kết
- Xóa emoji và ký tự đặc biệt
- Xóa số
- Chuẩn hóa khoảng trắng

### 6.2. Mô hình phân loại

- Sử dụng mô hình BiLSTM đã được huấn luyện trên dữ liệu Jigsaw
- TextVectorization với:
  - `max_tokens=200000`
  - `output_sequence_length=231`
- Ngưỡng phân loại: `0.5` (nếu xác suất > 0.5 thì được coi là độc hại)

### 6.3. 6 loại độc hại được phát hiện

1. **toxic**: Bình luận độc hại chung
2. **severe_toxic**: Bình luận cực kỳ độc hại
3. **obscene**: Bình luận tục tĩu
4. **threat**: Bình luận đe dọa
5. **insult**: Bình luận xúc phạm
6. **identity_hate**: Bình luận thù địch về danh tính

---

## 7. Xử lý lỗi thường gặp

### Lỗi: File không tìm thấy
- Đảm bảo file `toxic_comment_model.h5` có trong thư mục gốc
- Đảm bảo file `data/train/train.csv` tồn tại và có đúng cấu trúc

### Lỗi: Module không tìm thấy
- Kiểm tra đã cài đặt đầy đủ các thư viện: `streamlit`, `tensorflow`, `pandas`, `numpy`
- Kích hoạt đúng môi trường Python

### Lỗi: Memory error khi load dữ liệu
- File `train.csv` quá lớn, có thể giảm kích thước hoặc sử dụng sample nhỏ hơn để adapt vectorizer

---

## 8. Tùy chỉnh

### Thay đổi ngưỡng phân loại

Trong file `ui_demo.py`, hàm `score_comment()`, thay đổi giá trị `0.5`:

```python
if prediction[0][idx] > 0.5:  # Thay đổi 0.5 thành giá trị khác (0.0 - 1.0)
    toxic_list.append(col)
```

### Thay đổi tham số TextVectorization

Trong hàm `load_data_and_model()`, có thể điều chỉnh:
- `max_tokens`: Số lượng từ vựng tối đa
- `output_sequence_length`: Độ dài chuỗi đầu ra

---

## 9. Tác giả & Giấy phép

Dự án này được phát triển cho mục đích giáo dục và nghiên cứu.

---

## 10. Liên kết hữu ích

- [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
