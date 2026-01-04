# Hướng dẫn Deploy lên Streamlit Cloud

## Yêu cầu trước khi deploy

1. **File `requirements.txt`**: Đã được tạo với các dependencies cần thiết
2. **File mô hình**: `toxic_comment_model.h5` phải có trong repository
3. **File dữ liệu**: Cần ít nhất một trong các file sau:
   - `data/train/train.csv` (hoặc sample nhỏ)
   - `data/test/test_demo.csv` (fallback)

## Các bước deploy

### 1. Đảm bảo các file cần thiết có trong repository

```bash
# Kiểm tra các file quan trọng
ls -lh toxic_comment_model.h5
ls -lh data/train/train.csv  # hoặc data/test/test_demo.csv
ls -lh requirements.txt
ls -lh ui_demo.py
```

### 2. Push code lên GitHub

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 3. Deploy trên Streamlit Cloud

1. Truy cập [Streamlit Cloud](https://streamlit.io/cloud)
2. Đăng nhập bằng GitHub account
3. Click "New app"
4. Chọn repository: `ncuong0704/UI_demo_toxic_comments_detection`
5. Chọn branch: `main`
6. Main file path: `ui_demo.py`
7. Click "Deploy"

## Xử lý lỗi thường gặp

### Lỗi: ModuleNotFoundError

**Nguyên nhân**: Thiếu dependencies trong `requirements.txt`

**Giải pháp**: 
- Kiểm tra file `requirements.txt` có đầy đủ các thư viện
- Đảm bảo các version tương thích

### Lỗi: File not found

**Nguyên nhân**: Thiếu file mô hình hoặc dữ liệu

**Giải pháp**:
- Đảm bảo `toxic_comment_model.h5` có trong repository
- Đảm bảo có ít nhất `data/test/test_demo.csv` hoặc `data/train/train.csv`

### Lỗi: File quá lớn (>50MB)

**Nguyên nhân**: GitHub không cho phép file >50MB

**Giải pháp**:
1. Sử dụng Git LFS:
```bash
git lfs install
git lfs track "*.h5"
git lfs track "data/train/train.csv"
git add .gitattributes
git add toxic_comment_model.h5
git commit -m "Add large files with LFS"
git push origin main
```

2. Hoặc sử dụng sample nhỏ hơn:
   - Code đã được tối ưu để chỉ đọc 10000 dòng đầu của train.csv
   - Có thể tạo file sample nhỏ hơn và thay thế

### Lỗi: Memory limit exceeded

**Nguyên nhân**: App sử dụng quá nhiều bộ nhớ

**Giải pháp**:
- Code đã được tối ưu để chỉ load sample nhỏ (10000 dòng)
- Có thể giảm `nrows=10000` xuống nhỏ hơn nếu cần

## Lưu ý quan trọng

1. **File size**: Streamlit Cloud có giới hạn về kích thước repository
2. **Memory**: App sẽ cache model và vectorizer để tối ưu hiệu suất
3. **Timeout**: Lần đầu load model có thể mất thời gian, hãy kiên nhẫn

## Kiểm tra sau khi deploy

Sau khi deploy thành công, kiểm tra:
- ✅ App load được không?
- ✅ Có thể nhập comment và nhận kết quả?
- ✅ Upload file CSV có hoạt động không?
- ✅ Kết quả được hiển thị đúng không?

## Tối ưu hóa

Code đã được tối ưu với:
- `@st.cache_resource`: Cache model và vectorizer
- Chỉ đọc sample nhỏ để adapt vectorizer
- `verbose=0` trong model.predict để giảm log
- Error handling tốt hơn

