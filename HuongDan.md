# Hướng Dẫn Chạy Ứng Dụng Quản Lý Thư Viện

## 1. Chuẩn Bị Môi Trường
- Cài đặt **Python 3.13** (hoặc tối thiểu 3.10).
- Cài đặt **MySQL Server** và tạo cơ sở dữ liệu theo file `dbschema.sql`.  
  ```sql
  SOURCE path/to/dbschema.sql;
  ```
- Kiểm tra cấu hình trong `database.py` (host, user, password, database) khớp thông tin MySQL của bạn.

## 2. Cài Thư Viện Python
```bash
C:\path\to\python.exe -m pip install flask flask-cors mysql-connector-python
```
Khuyến nghị chạy lệnh bằng chính interpreter sẽ dùng cho server (ví dụ `C:\Users\<user>\AppData\Local\Programs\Python\Python313\python.exe`).

## 3. Khởi Động Backend (Flask API)
```bash
cd D:\Lab2.2---GuiSV
C:\Users\<user>\AppData\Local\Programs\Python\Python313\python.exe api.py
```
Server sẽ lắng nghe tại `http://127.0.0.1:5000`. Giữ cửa sổ này mở trong suốt quá trình sử dụng.

## 4. Mở Frontend
- Mở file `index.html` bằng trình duyệt (Edge, Chrome…).
- Các thành phần chính:
  - Dashboard thống kê (tổng sách, thành viên, đang mượn, trễ hạn).
  - Bảng “Sách mượn gần đây”, “Sắp đến hạn”, “Sách”, “Thành viên”.
  - Ô tìm kiếm sách (lọc theo tiêu đề) và nút “+ Thêm Sách” (prompt nhập dữ liệu).

## 5. Vận Hành
- **Tìm sách**: nhập từ khóa → dữ liệu bảng “Sách” tự động lọc.
- **Thêm sách**: nhấn “+ Thêm Sách” → điền thông tin trong các hộp thoại → sách mới được lưu vào MySQL.
- Các bảng còn lại lấy dữ liệu từ các endpoint tương ứng (`/borrowings/recent`, `/borrowings/due-soon`, `/members`, …).

## 6. Kiểm Tra Và Khắc Phục
- Nếu giao diện báo lỗi “Không thể tải…”, kiểm tra log ở cửa sổ chạy Flask hoặc xem `flask.log` (nếu chạy bằng lệnh `python -u api.py > flask.log 2>&1`).
- Đảm bảo MySQL chạy và thông tin kết nối đúng.
- Khi thay đổi cấu trúc CSDL hoặc chỉnh sửa mã nguồn backend, khởi động lại Flask server.

## 7. Thoát Ứng Dụng
- Đóng tab trình duyệt.
- Bấm `Ctrl+C` trong cửa sổ Flask để tắt server.

