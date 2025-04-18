from App.database import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))  # produce, meat, dairy, etc.

    def __init__(self, name, category=None):
        self.name = name
        self.category = category

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category
        }