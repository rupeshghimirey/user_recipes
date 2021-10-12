import re  
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.user import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data["date"]
        self.under_thirty_minutes = data["under_thirty_minutes"]
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if (len(form_data['name'])) < 4:
            flash("Name must be atleast 4 characters long!")
            is_valid = False;
        if (len(form_data['description'])) < 4:
            flash("Description must be atleast 4 characters long!")
            is_valid = False;
        if len(form_data['instructions']) < 4:
            flash("Please enter something the instructions for the recipe!")
            is_valid = False;
        if len(form_data['date']) < 10:
            flash("Please enter the date in the format")
            is_valid = False;
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, user_id, date, under_thirty_minutes, created_at, updated_at) VALUES(%(name)s,%(description)s,%(instructions)s, %(user_id)s,%(date)s,%(under_thirty_minutes)s, NOW(), NOW());"
        return connectToMySQL('users_recipes').query_db(query,data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('users_recipes').query_db(query)

        all_recipes = []

        for recipe in results:
            all_recipes.append(cls(recipe))
        
        return all_recipes;
    @classmethod
    def get_one_recipe_info_with_user(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s"
        result = connectToMySQL('users_recipes').query_db( query, data);

        recipe = cls(result[0])

        user_data = {
            "id" : result[0]["users.id"],
            "first_name"  : result[0]["first_name"],
            "last_name"   : result[0]["last_name"],
            "email"         : result[0]["email"],
            "password"         : result[0]["password"],
            "created_at"  : result[0]["users.created_at"],
            "updated_at"  : result[0]["users.updated_at"]
            }
        
        recipe.user = User(user_data)

        return recipe;

    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, user_id = %(user_id)s, date = %(date)s, under_thirty_minutes =  %(under_thirty_minutes)s WHERE id = %(recipe_id)s"
        # data is a dictionary that will be passed into the edit method from server.py
        connectToMySQL('users_recipes').query_db( query, data )

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s"
        # data is a dictionary that will be passed into the edit method from server.py
        connectToMySQL('users_recipes').query_db( query, data )
