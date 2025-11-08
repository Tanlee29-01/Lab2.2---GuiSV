# 03/11/2025
# 1. Xây dụng đầu vào chặt chẽ:
```bash
______________________________________________________________________________________
Lab2.2.py
#Hàm trợ giúp để nhập chuỗi không rỗng
def get_string_input(prompt, min_length=2):
    """
    Hiển thị 'prompt' và yêu cầu người dùng nhập.
    Lặp lại cho đến khi người dùng nhập một chuỗi
    1. Không rỗng
    2. Có độ dài ít nhất min_length
    3. Không chỉ chứa số
    4. Phải bắt đầu bằng một chữ cái (THÊM MỚI)
    """
    while True:
        user_input = input(prompt).strip()
        
        if not user_input: # 1. Kiểm tra rỗng
            print("Lỗi: Thông tin này không được để trống. Vui lòng nhập lại.")
            continue 

        if len(user_input) < min_length: # 2. Kiểm tra độ dài tối thiểu
            print(f"Lỗi: Phải có ít nhất {min_length} ký tự. Vui lòng nhập lại.")
            continue 
        
        if user_input.isdigit(): # 3. Kiểm tra chỉ chứa số
            print("Lỗi: Thông tin này không thể chỉ chứa số. Vui lòng nhập lại.")
            continue
            
        # 4. KIỂM TRA MỚI: Ký tự đầu tiên phải là chữ cái
        # (isalpha() hoạt động tốt với cả tiếng Việt có dấu)
        if not user_input[0].isalpha():
            print("Lỗi: Thông tin này phải bắt đầu bằng một chữ cái. Vui lòng nhập lại.")
            continue

        return user_input # Trả về nếu mọi thứ đều ổn

#Hàm bổ trợ cho người dùng nhập int
def get_safe_int_input(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
            return value
        except ValueError:
            print("Lỗi: vui lòng chỉ nhập một số nguyên.")

# Thêm hàm này vào khu vực hàm trợ giúp
def get_integer_in_range(prompt, valid_options):
    """
    Yêu cầu người dùng nhập một số nguyên cho đến khi
    số đó nằm trong 'valid_options' (một list).
    """
    while True:
        # Dùng lại hàm get_safe_int_input bạn đã viết
        value = get_safe_int_input(prompt) 
        
        if value in valid_options:
            return value # Trả về nếu số nằm trong danh sách
        else:
            # Số hợp lệ, nhưng không nằm trong phạm vi
            print(f"Lỗi: Vui lòng chỉ chọn một trong các giá trị: {valid_options}")


def get_integer_with_min_max(prompt, min_val=None, max_val=None):
    """
    Hiển thị 'prompt' và yêu cầu người dùng nhập một số nguyên.
    Lặp lại cho đến khi số đó nằm trong khoảng [min_val, max_val].
    """
    while True:
        # Chúng ta dùng lại hàm get_integer_input cũ để lấy số
        value = get_safe_int_input(prompt) 
        
        # Kiểm tra giới hạn dưới
        if min_val is not None and value < min_val:
            print(f"Lỗi: Giá trị phải lớn hơn hoặc bằng {min_val}.")
            continue # Yêu cầu nhập lại

        # Kiểm tra giới hạn trên
        if max_val is not None and value > max_val:
            print(f"Lỗi: Giá trị phải nhỏ hơn hoặc bằng {max_val}.")
            continue # Yêu cầu nhập lại
        
        return value 
______________________________________________________________________________________
```
# 2. Gặp 1 số lỗi: 
      2.1 Input số hết thì chức năng thêm sách vẫn nhận(Output rác)
      2.2 Input string nhập rác vẫn nhận
    => Đã xử lý xong 08/11/2025✅

# 3. 11/08/2025 Fix logic của book.py và member.py:
```bash
__________________________________________________________________________________
member.py
    # DELETE
    def delete_member(self, db):
        # 1. KIỂM TRA MỚI: Kiểm tra xem thành viên có đang mượn sách không
        check_query = """
            SELECT 1 FROM borrowing 
            WHERE member_id = %s AND return_date IS NULL 
            LIMIT 1
        """

        is_borrowing = db.fetch_one(check_query, (self.member_id,)) 
        if is_borrowing:
            raise ValueError("Không thể xóa. Thành viên này đang mượn sách.")
        
        query = "DELETE FROM members WHERE member_id=%s"
        db.execute_query(query, (self.member_id,))

Lab2.2.py(choice 8)

        elif choice == "8":
            member_id = get_integer_with_min_max("ID thành viên cần xóa: ")
            check_member_id = Member.search_by_id(db, member_id)
            if not check_member_id:
                print("Không tìm thấy thành viên.")
            else:
                try:
                    Member(member_id, None).delete_member(db)
                    print("Đã xóa thành viên.")
                except ValueError as e:
                    print(f"Lỗi{e}")
__________________________________________________________________________________
book.py
 # DELETE
    def delete_book(self, db):
        checK_query = "DELETE FROM books WHERE book_id=%s"
        row = db.execute_query(checK_query, (self.book_id,))
        
        if not row:
            raise ValueError("Sách không tồn tại để xóa")
        
        if row[0] == 1:
            raise ValueError("Không thể xóa. Sách này đang được mượn.")
        
        query = "DELETE FROM books WHERE book_id = %s"
        db.execute_query(query,(self.book_id,))

Lab2.2.py(choice 3)
        elif choice == "3":
            book_id = get_safe_int_input("ID sách cần xóa: ")
            check_book_id = Book.search_by_id(db, book_id)
            try:
                book_to_delete = Book(book_id, None, None, None, None, None, None)
                book_to_delete.delete_book(db)
                print("Đã xóa sách.")
            except ValueError as e:
                    print(f"Lỗi {e}")
__________________________________________________________________________________

Lab2.2.py(choice 9)
elif choice == "9":
            # ... (phần code 'a)' )
            if choice == "a":
                member_id = get_safe_int_input("Nhập ID: ") # SỬA Ở ĐÂY
                check_member_id = Member.search_by_id(db, member_id)
                print(check_member_id if check_member_id else "Không thấy.")
            # ...
______________________________________________________________________________________
```
# 4. Nâng cấp choice 11(Mượn sách) và choice 12(Trả sách) 08/11/2025:
```bash
elif choice == "11": 
            member_id = get_safe_int_input("ID thành viên: ")
            
            keyword = get_string_input("Nhập từ khóa tên sách cần mượn: ")
            available_books = Book.search_available_by_title_like(db, keyword)
            
            if not available_books:
                print("Không tìm thấy sách nào 'có sẵn' khớp với từ khóa.")
                continue

            print("== Các sách 'có sẵn' tìm thấy: ==")
            valid_book_ids = [] 
            for book in available_books:
                print(f" - [{book.book_id}] {book.title} - {book.author}")
                valid_book_ids.append(book.book_id)

            book_id_to_borrow = get_safe_int_input("Nhập ID sách bạn muốn mượn: ")
            

            if book_id_to_borrow not in valid_book_ids:
                print("Lỗi: ID sách không hợp lệ.")
                continue
                

            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=14)
            try:
                Borrowing(None, member_id, book_id_to_borrow, borrow_date, due_date).borrow_book(db)
                print(f"Mượn thành công. Hạn trả: {due_date:%Y-%m-%d}")
            except ValueError as Errorr:
                print(Errorr)
______________________________________________________________________________________
        elif choice == "12":
            member_id = get_safe_int_input("ID thành viên: ")
            borrowed_books = Borrowing.get_currently_borrowed_by_member(db, member_id)
            
            if not borrowed_books:
                print("Thành viên này không có sách nào đang mượn.")
                continue


            print("== Các sách bạn đang mượn: ==")
            valid_book_ids = [] 
            for book_id, title, author in borrowed_books:
                print(f" - [{book_id}] {title} - {author}")
                valid_book_ids.append(book_id)

            book_id_to_return = get_safe_int_input("Nhập ID sách bạn muốn trả: ")
            
            if book_id_to_return not in valid_book_ids:
                print("Lỗi: Bạn không mượn sách có ID này.")
                continue

            try:
                Borrowing(None, member_id, book_id_to_return, None, None, return_date=date.today()).return_book(db)
                print("Trả sách thành công.")
            except ValueError as e:
                print("Lỗi", e)
```
______________________________________________________________________________________
# 5. Thêm 3 chức năng 14, 15, 16 09/11/2025:
```bash
- 14. Tìm kiếm sách theo tên
- 15. Xem lịch sử mượn sách
- 16. Báo cáo sách đang được mượn
```
