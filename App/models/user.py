from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    dietary_specs = db.Column(db.String(200)) #not sure if to leave this here or not
    
    # Relationships
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    pantry = db.relationship('Ingredient', secondary='user_pantry', lazy='subquery',
        backref=db.backref('users', lazy=True))
    grocery_list = db.relationship('GroceryList', backref='user', lazy=True)
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True)

# Association table for User-Ingredient (Pantry)
user_pantry = db.Table('user_pantry',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'dietary_specs': self.dietary_specs #not sure as well
