class Transaction():
    def __init__(self, amount, person="", date="", description="", shared=None, id=None, category_id=None):
        self.id = id
        self.amount = amount
        self.person = person
        self.date = date
        self.description = description
        self.shared = shared
        self.category_id = category_id

    def get_query_placeholder(self):
        return [tup[1] for tup in self.__dict__.items() if tup[0] != 'id']