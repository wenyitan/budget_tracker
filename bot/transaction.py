class Transaction():
    def __init__(self, amount, person="", date="", description="", shared=None, id=None):
        self.id = id
        self.amount = amount
        self.person = person
        self.date = date
        self.description = description
        self.shared = shared