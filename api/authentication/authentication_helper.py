class AuthenticationHelper:
    def __init__(self, db):
        self.db = db
        self.users_collection = self.db.get_collection("users")

    def get_all_usernames(self):
        results = self.users_collection.find({})
        return results

    def add_user(self, username, password_hash):
        result = self.users_collection.insert_one({
            "username": username,
            "password_hash": password_hash
        })
        last_row_id = result.inserted_id
        return last_row_id

    def get_user_by_username(self, username):
        result = self.users_collection.find_one({"username": username})
        return result

    def delete_user_by_username(self, username):
        result = self.users_collection.delete_one({"username": username})
        return result.deleted_count