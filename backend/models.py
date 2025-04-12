class Transaction:
    def __init__(self, amount, category, description, person, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.person = person
        self.date = date # YYYY-MM-DD

    def to_dict(self):
        return {
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "person": self.person,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)