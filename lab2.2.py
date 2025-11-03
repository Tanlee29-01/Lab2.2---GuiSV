from database import Database
from book import Book
from member import Member
from borrowing import Borrowing
from datetime import date, timedelta

#Hiển thị ds Book
def print_books(books):
    if not books:
        print("Không có sách phù hợp.")
    else:
        for b in books:
            print(" -", b)

#Hiển thị danh sách sinh viên
def print_members(members):
    if not members:
        print("Không có thành viên phù hợp.")
    else:
        for m in members:
            print(" -", m)


def main():
    db = Database()
    while True:
        print("==============Menu===============")
        print("HỆ THỐNG QUẢN LÝ THƯ VIỆN")
        print("1.  Thêm sách")
        print("2.  Sửa thông tin sách")
        print("3.  Xóa sách")
        print("4.  Tìm kiếm sách")
        print("5.  Hiển thị tất cả sách")
        print("6.  Thêm thành viên")
        print("7.  Sửa thông tin thành viên")
        print("8.  Xóa thành viên")
        print("9.  Tìm kiếm thành viên")
        print("10. Hiển thị tất cả thành viên")
        print("11. Mượn sách")
        print("12. Trả sách")
        print("13. Hiển thị sách quá hạn (kèm người mượn)")
        print("0.  Thoát")
        print("====================================")

        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            title = input("Tên sách: ").strip()
            author = input("Tác giả: ").strip()
            pages = int(input("Số trang: "))
            year = int(input("Năm xuất bản: "))
            category = input("Chủng loại: ").strip()
            status = int(input("Trạng thái (0: có sẵn, 1: đã mượn, 2: khác): "))
            Book(None, title, author, pages, year, status, category).add_book(db)
            print("Đã thêm sách.")

        elif choice == "2":
            book_id = int(input("ID sách cần sửa: "))
            check_book_id = Book.search_by_id(db, book_id)
            if not check_book_id:
                print("Không tìm thấy sách.")
            else:
                print("Hiện tại:", check_book_id)
                title = input("Tên mới: ")
                author = input("Tác giả mới: ")
                pages = int(input("Số trang mới: "))
                year = int(input("Năm XB mới: "))
                status = int(input("Trạng thái mới (0/1/2): "))
                category = input("Chủng loại mới: ")
                Book(book_id, title, author, pages, year, status, category).update_book(db)
                print("Đã cập nhật.")

        elif choice == "3":
            book_id = int(input("ID sách cần xóa: "))
            check_book_id = Book.search_by_id(db, book_id)
            if not check_book_id:
                print("Không tìm thấy sách.")
            else:
                Book(book_id, None, None, None, None, None, None).delete_book(db)
                print("Đã xóa sách.")

        elif choice == "4":
            print(" a) Theo ID")
            print(" b) Theo tiêu đề")
            choice = input("Chọn kiểu tìm: ").strip().lower()
            if choice == "a":
                book_id = int(input("Nhập ID: "))
                check_book_id = Book.search_by_id(db, book_id)
                print(check_book_id if check_book_id else "Không thấy.")
            elif choice == "b":
                title = input("Nhập tiêu đề chính xác: ").strip()
                check_book_id = Book.search_by_title(db, title)
                print(check_book_id if check_book_id else "Không thấy.")
            else:
                print("Lựa chọn không hợp lệ.")

        elif choice == "5":
            print_books(Book.get_all_books(db))

        elif choice == "6":
            name = input("Tên thành viên: ").strip()
            Member(None, name).add_member(db)
            print("Đã thêm thành viên.")

        elif choice == "7":
            member_id = int(input("ID thành viên cần sửa: "))
            check_member_id = Member.search_by_id(db, member_id)
            if not check_member_id:
                print("Không tìm thấy thành viên.")
            else:
                print("Hiện tại:", check_member_id)
                new_name = input("Tên mới: ").strip()
                Member(member_id, new_name).update_member_info(db)
                print("Đã cập nhật.")

        elif choice == "8":
            member_id = int(input("ID thành viên cần xóa: "))
            check_member_id = Member.search_by_id(db, member_id)
            if not check_member_id:
                print("Không tìm thấy thành viên.")
            else:
                Member(member_id, None).delete_member(db)
                print("Đã xóa thành viên.")

        elif choice == "9":
            print(" a) Theo ID")
            print(" b) Theo tên (từ khóa)")
            choice = input("Chọn kiểu tìm: ").strip().lower()
            if choice == "a":
                member_id = int(input("Nhập ID: "))
                check_member_id = Member.search_by_id(db, member_id)
                print(check_member_id if check_member_id else "Không thấy.")
            elif choice == "b":
                key_word = input("Nhập từ khóa tên: ").strip()
                check_member_id = Member.search_by_name_like(db, key_word)
                print_members(check_member_id)
            else:
                print("Lựa chọn không hợp lệ.")

        elif choice == "10":
            print_members(Member.get_all_members(db))

        elif choice == "11":
            member_id = int(input("ID thành viên: "))
            title = input("Tên sách (đúng chính tả): ").strip()
            check_book_id = Book.search_by_title(db, title)
            if not check_book_id:
                print("Không tìm thấy sách.")
                continue
            
            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=14)
            try:
                Borrowing(None, member_id, check_book_id.book_id, borrow_date, due_date).borrow_book(db)
                print(f"Mượn thành công. Hạn trả: {due_date:%Y-%m-%d}")
            except ValueError as Errorr:
                print(Errorr)

        elif choice == "12":
            member_id = int(input("ID thành viên: "))
            title = input("Tên sách (đúng chính tả): ").strip()
            check_book_title = Book.search_by_title(db, title)
            if not check_book_title:
                print("Không tìm thấy sách.")
                continue
            try:
                Borrowing(None, member_id, check_book_title.book_id, None, None, return_date=date.today()).return_book(db)
                print("Trả sách thành công.")
            except ValueError as e:
                print("Lỗi", e)

        elif choice == "13":
            rows = Borrowing.get_overdue_books(db)
            if not rows:
                print("Không có sách quá hạn.")
            else:
                print("== DANH SÁCH QUÁ HẠN ==")
                for member_id, name, book_id, title, borrow_date, due_date, days in rows:
                    print(f"- TV [{member_id}] {name} | Sách [{book_id}] {title} | Mượn {borrow_date} | Hạn {due_date} | Trễ {days} ngày")

        elif choice == "0":
            print("Tạm biệt")
            break

if __name__ == "__main__":
    main()
