from datetime import datetime

class Transaction:
    def __init__(self, amount, category, description, person):
        self.amount = amount
        self.category = category
        self.description = description
        self.person = person
        self.date = datetime.now()

    def to_dict(self):
        return {
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "person": self.person,
            "date": self.date.strftime('%Y-%m-%d')
        }