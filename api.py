from datetime import date, timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import Database
from book import Book
from member import Member
from borrowing import Borrowing


app = Flask(__name__)
CORS(app)


def get_db():
    return Database()


def book_to_dict(book: Book):
    return {
        "bookId": book.book_id,
        "title": book.title,
        "author": book.author,
        "pages": book.pages,
        "year": book.year_published,
        "status": book.status,
        "category": book.category,
    }


def member_to_dict(member: Member):
    return {
        "memberId": member.member_id,
        "name": member.name,
    }


@app.route("/api/stats/overview", methods=["GET"])
def stats_overview():
    db = get_db()
    total_books = db.fetch_one("SELECT COUNT(*) FROM books")[0]
    total_members = db.fetch_one("SELECT COUNT(*) FROM members")[0]
    borrowing_count = db.fetch_one(
        "SELECT COUNT(*) FROM borrowing WHERE return_date IS NULL"
    )[0]
    overdue_count = db.fetch_one(
        """
        SELECT COUNT(*)
        FROM borrowing
        WHERE return_date IS NULL AND due_date < %s
        """,
        (date.today(),),
    )[0]

    return jsonify(
        {
            "totalBooks": total_books,
            "totalMembers": total_members,
            "borrowingCount": borrowing_count,
            "overdueCount": overdue_count,
        }
    )


@app.route("/api/borrowings/recent", methods=["GET"])
def borrowings_recent():
    db = get_db()
    rows = db.fetch_all(
        """
        SELECT br.borrowing_id,
               m.name AS member_name,
               bk.title AS book_title,
               br.borrow_date
        FROM borrowing br
        JOIN members m ON m.member_id = br.member_id
        JOIN books bk ON bk.book_id = br.book_id
        ORDER BY br.borrow_date DESC
        LIMIT 10
        """
    )
    data = []
    for borrowing_id, member_name, title, borrow_date in rows:
        data.append(
            {
                "ticketCode": borrowing_id,
                "memberName": member_name,
                "bookTitle": title,
                "borrowDate": borrow_date.isoformat(),
            }
        )
    return jsonify(data)


@app.route("/api/borrowings/due-soon", methods=["GET"])
def borrowings_due_soon():
    db = get_db()
    today = date.today()
    limit_date = today + timedelta(days=7)
    rows = db.fetch_all(
        """
        SELECT br.borrowing_id,
               bk.title,
               br.due_date
        FROM borrowing br
        JOIN books bk ON bk.book_id = br.book_id
        WHERE br.return_date IS NULL AND br.due_date BETWEEN %s AND %s
        ORDER BY br.due_date ASC
        """,
        (today, limit_date),
    )

    data = []
    for borrowing_id, title, due_date in rows:
        status = "Quá hạn" if due_date < today else "Sắp đến hạn"
        data.append(
            {
                "ticketCode": borrowing_id,
                "bookTitle": title,
                "status": status,
            }
        )
    return jsonify(data)


@app.route("/api/books", methods=["GET", "POST"])
def books():
    db = get_db()
    if request.method == "POST":
        payload = request.get_json(force=True)
        title = (payload.get("title") or "").strip()
        author = (payload.get("author") or "").strip()
        category = (payload.get("category") or "").strip()
        pages = payload.get("pages")
        year = payload.get("year")

        try:
            pages = int(pages)
            year = int(year)
        except (TypeError, ValueError):
            return jsonify({"error": "Số trang và năm xuất bản phải là số nguyên."}), 400

        if not title or not author or not category:
            return (
                jsonify({"error": "Thiếu thông tin bắt buộc."}),
                400,
            )

        new_book = Book(None, title, author, pages, year, 0, category)
        new_book.add_book(db)
        return jsonify({"message": "Đã thêm sách thành công."}), 201

    keyword = request.args.get("q", "").strip()
    if keyword:
        books = Book.search_by_title_like(db, keyword)
    else:
        books = Book.get_all_books(db)

    data = []
    for book in books:
        info = book_to_dict(book)
        info["statusText"] = {0: "Có sẵn", 1: "Đang mượn", 2: "Khác"}.get(
            info["status"], "Không rõ"
        )
        data.append(info)
    return jsonify(data)


@app.route("/api/members", methods=["GET", "POST"])
def members():
    db = get_db()
    if request.method == "POST":
        payload = request.get_json(force=True)
        name = (payload.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Thiếu tên thành viên."}), 400
        Member(None, name).add_member(db)
        return jsonify({"message": "Đã thêm thành viên."}), 201

    members = Member.get_all_members(db)
    data = []
    for member in members:
        info = member_to_dict(member)
        info["email"] = ""
        info["status"] = ""
        data.append(info)
    return jsonify(data)

@app.route("/api/borrowings/borrow", methods=["POST"])
def borrow_book():
    db = get_db()
    payload = request.get_json(force=True)
    member_id = payload.get("memberId")
    book_id = payload.get("bookId")
    if not member_id or not book_id:
        return jsonify({"error": "Thiếu memberId hoặc bookId"}), 400
    today = date.today()
    due = today + timedelta(days=14)
    try:
        Borrowing(None, int(member_id), int(book_id), today, due).borrow_book(db)
        return jsonify({"message": "Mượn sách thành công.", "dueDate": due.isoformat()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/borrowings/current", methods=["GET"])
def borrowings_current():
    db = get_db()
    member_id = request.args.get("memberId", type=int)
    if not member_id:
        return jsonify([])
    rows = Borrowing.get_currently_borrowed_by_member(db, member_id)
    # rows: (book_id, title, author)
    data = [{"bookId": r[0], "title": r[1], "author": r[2]} for r in rows]
    return jsonify(data)

@app.route("/api/borrowings/return", methods=["POST"])
def return_book():
    db = get_db()
    payload = request.get_json(force=True)
    member_id = payload.get("memberId")
    book_id = payload.get("bookId")
    if not member_id or not book_id:
        return jsonify({"error": "Thiếu memberId hoặc bookId"}), 400
    try:
        Borrowing(None, int(member_id), int(book_id), None, None, return_date=date.today()).return_book(db)
        return jsonify({"message": "Trả sách thành công."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

