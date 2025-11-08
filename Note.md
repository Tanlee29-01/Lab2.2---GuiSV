# 03/11/2025
# 1. Xây dụng đầu vào chặt chẽ:
```bash
def get_safe_input(prompt):
    """
    Mục đích sử dụng khi người dùng nhập sai infor ta sẽ bắt họ nhập lại
    Code sẽ lặp lại tới khi nào đúng mới thôi
    """
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
            return value
        except ValueError:
            print("Lỗi: vui lòng chỉ nhập một số nguyên.")
```
# 2. Gặp 1 số lỗi: 
      2.1 Input số hết thì chức năng thêm sách vẫn nhận(Output rác)
      2.2 Input string nhập rác vẫn nhận
