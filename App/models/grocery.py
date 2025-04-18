from App.database import db
from App.models.user import User
from App.models.ingredient import Ingredient

class GroceryList(db.Model):
    groceryID = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100), nullable=False)
    checked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, groceryID, ingredient_name, checked, user_id):
        self.groceryID = groceryID
        self.ingredient_name = ingredient_name
        self.checked= checked
        self.user_id = user_id

    def get_json(self):
        return {
            'groceryID': self.groceryID,
            'ingredient_name': self.ingredient_name,
            'checked': self.checked,
            'user_id': self.user_id
        }