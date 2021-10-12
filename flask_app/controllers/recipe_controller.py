from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



# ==============================================
# adding new recipe page
# ==============================================
@app.route("/recipes/new")
def create_recipe():
    return render_template("create_recipe.html")

# ==============================================
# add/recipe route
# ==============================================

@app.route('/create_recipe', methods=["POST"])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
        
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions" : request.form["instructions"],
        #gives the id of a user stored in a session
        "user_id": session['user_id'],
        "date" : request.form["date"],
        "under_thirty_minutes" : request.form["under_thirty_minutes"],
        
    }
    Recipe.save(data)
    flash("New Recipe successfully added")
    return redirect("/dashboard")

@app.route("/view/instructions/<int:recipe_id>")
def recipe_instructions_page(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data_user = {
        "user_id" : session["user_id"]
    }
    user = User.get_user_info(data_user)
    data_recipe = {
        "recipe_id" : recipe_id
    }
    recipe_one = Recipe.get_one_recipe_info_with_user(data_recipe)
    return render_template("recipe_details.html", recipe_one = recipe_one, user = user)

@app.route("/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }

    one_recipe = Recipe.get_one_recipe_info_with_user(data);
    return render_template("edit_recipe.html", one_recipe = one_recipe)

@app.route('/edit/recipe/<int:recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "recipe_id": recipe_id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions" : request.form["instructions"],
        #gives the id of a user stored in a session
        "user_id": session['user_id'],
        "date" : request.form["date"],
        "under_thirty_minutes" : request.form["under_thirty_minutes"],
    }
    # We pass the data dictionary into the save method from the Friend class.
    Recipe.edit_recipe(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/dashboard')

@app.route("/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }

    Recipe.delete_recipe(data)

    return redirect("/dashboard")
    


