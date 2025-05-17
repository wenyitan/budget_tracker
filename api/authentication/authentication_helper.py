class AuthenticationHelper:
    def __init__(self, db):
        self.db = db

    def get_all_usernames(self):
        query = "select username from users;"
        results = self.db.fetch_all(query)
        return results

    def add_user(self, username, password_hash):
        query = "insert into users (username, password_hash) values (?,?)"
        self.db.execute(query, (username, password_hash))
        last_row_id = self.db.cursor.lastrowid
        return last_row_id

    def get_user_by_username(self, username):
        query = "select * from users where username=?"
        return self.db.fetch_one(query, (username,))

    def delete_user_by_username(self, username):
        query = "delete from users where username=?"
        self.db.execute(query, (username,))
        last_row_id = self.db.cursor.lastrowid
        return last_row_id