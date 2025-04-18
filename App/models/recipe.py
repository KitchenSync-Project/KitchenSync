from App.database import db
from App.models.user import User
from App.models.ingredient import Ingredient

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    steps = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200)) ##this might be a lil iffy 
    category = db.Column(db.String(50))  # breakfast, lunch, dinner, etc.
    dietary_restrictions = db.Column(db.String(200))
    suitable_for = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredient', lazy='subquery',
        backref=db.backref('recipes', lazy=True))

# Association table for Recipe-Ingredient
recipe_ingredient = db.Table('recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

    def __init__(self, name, steps, user_id, image=None, category='main', dietary=None, suitable_for=None):
        self.name = name
        self.steps = steps
        self.user_id = user_id
        self.image = image
        self.category = category
        self.dietary_restrictions = dietary
        self.suitable_for = suitable_for

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'dietary_restrictions': self.dietary_restrictions,
            'suitable_for': self.suitable_for,
            'user_id': self.user_id,
            'ingedients': self. ingedients
        }