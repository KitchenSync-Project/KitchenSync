from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Email
from wtforms import DateField

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    image = FileField('Recipe Image')
    category = SelectField('Category', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert')
    ], validators=[DataRequired()])
    dietary = SelectField('Dietary Restrictions', choices=[
        ('', 'None'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('keto', 'Keto'),
        ('gluten-free', 'Gluten-Free'),
        ('diabetic', 'Diabetic')
    ])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    steps = TextAreaField('Steps', validators=[DataRequired()])
    suitable_for = StringField('Suitable For')
    submit = SubmitField('Add Recipe')

class PantryForm(FlaskForm):
    ingredient = StringField('Ingredient Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('produce', 'Produce'),
        ('meat', 'Meat'),
        ('dairy', 'Dairy'),
        ('grains', 'Grains'),
        ('seasonings', 'Seasonings')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Recipe')

class MealPlanForm(FlaskForm):
    day = SelectField('Day', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    recipe_id = SelectField('Recipe', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add to Meal Plan')

class PantryForm(FlaskForm):
    ingredient = StringField('Add Ingredient', validators=[DataRequired()])
    submit = SubmitField('Add')

class GroceryListForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    submit = SubmitField('Add Item')