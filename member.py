class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def __str__(self):
        return f"[{self.member_id}] {self.name}"

    # CREATE
    def add_member(self, db):
        query = "INSERT INTO members(name) VALUES(%s)"
        db.execute_query(query, (self.name,))

    # UPDATE
    def update_member_info(self, db):
        query = "UPDATE members SET name=%s WHERE member_id=%s"
        db.execute_query(query, (self.name, self.member_id))

    # DELETE
    def delete_member(self, db):
        query = "DELETE FROM members WHERE member_id=%s"
        db.execute_query(query, (self.member_id,))

    # READ / SEARCH
    @staticmethod
    def get_all_members(db):
        query = "SELECT * FROM members"
        return [Member(*row) for row in db.fetch_all(query)]

    @staticmethod
    def search_by_id(db, member_id):
        query = "SELECT * FROM members WHERE member_id=%s"
        row = db.fetch_one(query, (member_id,))
        return Member(*row) if row else None

    @staticmethod
    def search_by_name_like(db, keyword):
        query = "SELECT * FROM members WHERE name LIKE %s"
        rows = db.fetch_all(query, (f"%{keyword}%",))
        return [Member(*r) for r in rows]
