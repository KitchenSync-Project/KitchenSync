import click, pytest, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.models import User, Recipe, Ingredient, MealPlan, GroceryList, db
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from tabulate import tabulate 
from sqlalchemy.exc import IntegrityError
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

app = create_app()
migrate = get_migrate(app)


@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    # Create a user
    default_user = User(username='default_user', password=generate_password_hash('default_password'))
    db.session.add(default_user)
    db.session.commit()

    print('database initialized')


@app.cli.command("create-user", help="Creates a new user")
@click.argument("username")
@click.argument("password")
def create_user(username, password):
  
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        print(f"User created successfully.")
    except IntegrityError:
        db.session.rollback()
        print(f"Error: Username already exists.")


@app.cli.command("add-recipe", help="Adds a new recipe for a user")
@click.argument("username")
@click.argument("name")
@click.argument("ingredients_str") 
@click.argument("steps")
@click.option("--image", default=None, help="URL of the recipe image")
@click.option("--category", default="main", help="Category of the recipe (dinner, lunch, dessert, breakfast)")
@click.option("--dietary", default=None, help="Dietary restrictions (comma-separated: keto, diabetic, vegan, vegetarian)")
@click.option("--suitable_for", default=None, help="Suitable for dietary restrictions (comma-separated)")

def add_recipe(username, name, ingredients_str, steps, image, category, dietary, suitable_for):
    #Adds a new recipe to a user's profile.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    ingredients = [Ingredient(name=ing.strip()) for ing in ingredients_str.split(",")]
    recipe = Recipe(
        name=name,
        steps = steps,
        image=image,
        category=category,
        dietary_restrictions=dietary,
        suitable_for=suitable_for,
        user=user,
        ingredients=ingredients,
    )

    db.session.add(recipe)
    db.session.commit()
    print(f"Recipe '{name}' Recipe added.")


@app.cli.command("list-recipes", help="Lists all recipes for a user")
@click.argument("username")
def list_recipes(username):

    #Lists all recipes associated a username.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    recipes = user.recipes
    if not recipes:
        print(f"No recipes found for user.")
        return

    data = [[recipe.name, recipe.category, recipe.dietary_restrictions] for recipe in recipes]
    print(tabulate(data, headers=["Name", "Category", "Dietary Restrictions"]))


@app.cli.command("add-to-pantry", help="Adds an ingredient to the user's pantry")
@click.argument("username")
@click.argument("ingredient_name")
def add_to_pantry(username, ingredient_name):
    #Adds an ingredient to a user's pantry.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if not ingredient:
        ingredient = Ingredient(name=ingredient_name)  # Create if it doesn't exist

    user.pantry.append(ingredient)
    db.session.commit()
    print(f"{ingredient_name} added to pantry.")


@app.cli.command("view-pantry", help="View the user's pantry")
@click.argument("username")
def view_pantry(username):

    #View the ingredients in a user's pantry.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    if not user.pantry:
        print(f"Pantry is empty.")
        return

    ingredients = [item.name for item in user.pantry]
    print(f"Pantry: {', '.join(ingredients)}")


@app.cli.command("add-to-grocery-list", help="Adds an ingredient to the user's grocery list")
@click.argument("username")
@click.argument("ingredient_name")
def add_to_grocery_list(username, ingredient_name):

    #Adds an ingredient to a user's grocery list.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    grocery_item = GroceryList(ingredient_name=ingredient_name, user=user)
    db.session.add(grocery_item)
    db.session.commit()
    print(f"{ingredient_name} added to grocery list.")


@app.cli.command("view-grocery-list", help="View the user's grocery list")
@click.argument("username")
def view_grocery_list(username):
    #View the ingredients in a user's grocery list.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    grocery_list = user.grocery_list
    if not grocery_list:
        print(f"Grocery list is empty.")
        return

    items = [item.ingredient_name for item in grocery_list]
    print(f" Grocery List: {', '.join(items)}")


@app.cli.command("add-meal-plan", help="Adds a recipe to the user's meal plan for a specific day")
@click.argument("username")
@click.argument("recipe_name")
@click.argument("day")
def add_meal_plan(username, recipe_name, day):
    #Adds a recipe to a user's meal plan for a specific day.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    recipe = Recipe.query.filter_by(name=recipe_name, user_id=user.id).first()
    if not recipe:
        print(f"Recipe '{recipe_name}' not found.")
        return

    meal_plan = MealPlan(day=day, recipe=recipe, user=user)
    db.session.add(meal_plan)
    db.session.commit()
    print(f"{recipe_name} added to meal plan for {day}.")


@app.cli.command("view-meal-plan", help="View the user's meal plan")
@click.argument("username")
def view_meal_plan(username):
    #View the user's meal plan for the week.
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User not found.")
        return

    meal_plans = MealPlan.query.filter_by(user_id=user.id).all()
    if not meal_plans:
        print(f"No meal plans.")
        return

    data = [[plan.day, plan.recipe.name] for plan in meal_plans]
    print(tabulate(data, headers=["Day", "Recipe"]))
