
# 🐍 Python Selenium Unit Testing

## 🔧 Thiết lập môi trường

Để bắt đầu, bạn cần thiết lập một môi trường ảo và cài đặt các phụ thuộc cần thiết.

### 1. Tạo môi trường ảo

Chạy lệnh sau để tạo môi trường ảo:

```bash
python -m venv venv
```

### 2. Kích hoạt môi trường ảo

Kích hoạt môi trường ảo bằng lệnh sau:

- **Windows:**

```bash
.\venv\Scripts\activate 
```

- **Linux/MacOS:**

```bash
source venv/bin/activate
```

### 3. Cài đặt Selenium

Sau khi kích hoạt môi trường ảo, hãy cài đặt Selenium:

```bash
pip install selenium
```

### 4. Ngắt kết nối môi trường ảo

Khi bạn hoàn tất, bạn có thể ngắt kết nối môi trường ảo bằng lệnh sau:

```bash
deactivate
```

## 🧪 Chạy bài kiểm tra đơn vị

Để chạy các bài kiểm tra đơn vị, bạn cần kích hoạt môi trường ảo trước.

### 1. Kích hoạt môi trường ảo

```bash
.\venv\Scripts\activate   
```

### 2. Chạy tất cả bài kiểm tra

Chạy lệnh sau để chạy tất cả bài kiểm tra đơn vị:

```bash
python tests/test_add_account.py
```

## ⚡ Chạy một bài kiểm tra cụ thể

Nếu bạn chỉ muốn chạy một bài kiểm tra cụ thể, sử dụng lệnh sau:

### 1. Kích hoạt môi trường ảo

```bash
.\venv\Scripts\activate   
```

### 2. Chạy bài kiểm tra cụ thể

```bash
python -m unittest tests/test_add_account.py -k test_reset_functionality
```

---

### 👤 Tác giả

**Kenny Truong**

---

🎉 Chúc bạn thành công trong việc chạy các bài kiểm tra và phát triển dự án của mình!
