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

# 3. 11/08/2025 Fix logic của book.py và member.py
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
```
