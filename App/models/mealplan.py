from App.database import db
from App.models.user import User
from App.models.recipe import Recipe
from App.models.ingredient import Ingredient

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    
    # Relationship
    recipe = db.relationship('Recipe', backref='meal_plans')

    def __init__(self, day, user_id, recipe_id):
        self.day = day
        self.user_id = user_id
        self.recipe_id = recipe_id

    def get_json(self):
        return {
            'id': self.id,
            'day': self.day,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id
        }