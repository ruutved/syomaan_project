import json

from flask import Flask, redirect, url_for, render_template, flash, request, jsonify, make_response
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user
from flask_mongoengine import MongoEngine
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'syomaan',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'syomaanapp'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Document, UserMixin):
    user_name = db.StringField(default=True)
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    registration_time = db.DateTimeField(default=datetime.now())


class Recipe(db.Document):
    recipe_name = db.StringField(default=True)
    ingredients = db.ListField(default=True)
    description = db.StringField(default=True)
    creator = db.StringField(default=True)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@app.route("/", methods=['GET'])
def home():
    recipes = Recipe.objects

    return render_template("home.html", recipes=recipes)


@app.route("/logged_in")
@login_required
def logged_in():
    return render_template('logged_in.html', name=current_user.user_name)


@app.route("/profile")
@login_required
def profile():
    email = current_user.email
    recipes = Recipe.objects

    user_recipes = 0

    for recipe in recipes:
        if recipe["creator"] == email:
            user_recipes += 1
        else:
            print("This recipe was created by another user")

    return render_template('profile.html', user_recipes=user_recipes, name=current_user.user_name)


@app.route("/plan")
@login_required
def plan():
    return render_template('plan.html', name=current_user.user_name)


@app.route("/add_recipe", methods=["POST", "PUT", "GET"])
@login_required
def add_recipe():

    global ingr_list
    if request.method == "PUT":
        ingr_list = request.get_json(force=True)
        res = make_response(jsonify({"message": "no niin"}))
        return res

    elif request.method == "POST":
        recipe_name = request.form.get("rec_name")
        ingredients = ingr_list
        description = request.form.get("instructions")
        creator = current_user.email

        new_recipe = Recipe(recipe_name=recipe_name,
                            ingredients=ingredients,
                            description=description,
                            creator=creator)

        new_recipe.save()
        return redirect(url_for('home'))

    else:
        return render_template("add_recipe.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        users = User.objects

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = users(email=email).first()

        if user:
            password_check = user['password']

            if check_password_hash(password_check, password):
                login_user(user, remember=remember)
                return redirect(url_for('logged_in'))

            else:
                if current_user.email:
                    return redirect(url_for('logged_in'))
                else:
                    flash('Väärä salasana')
                    return redirect(url_for('login'))
        else:
            flash('Käyttäjää ei löydy')
            return redirect(url_for('login'))

    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        users = User.objects
        user_name = request.form.get("name")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_found = users(email=email).first()

        if email_found:
            flash('Tämä sähköpostiosoite on jo rekisteröity!')
            return redirect(url_for('signup'))

        if password1 != password2:
            flash('Salasanat eivät täsmää!')
            return redirect(url_for('signup'))

        else:
            hashed_password = generate_password_hash(password2, method='sha256')
            user_input = User(user_name=user_name,
                              email=email,
                              password=hashed_password,
                              registration_time=datetime.now())

            user_input.save()

            return redirect(url_for('login'))

    else:
        return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/prep_delete/<recipe_name>", methods=["GET"])
@login_required
def prepare_delete(recipe_name):
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    if not recipe:
        flash('Reseptiä ei löydy, tarkista tiedot!')
        return redirect(url_for('home'))
    else:
        return render_template("prep_delete.html", recipe=recipe)


@app.route("/delete_recipe/<recipe_name>", methods=["GET"])
@login_required
def delete_recipe(recipe_name):

    recipe = Recipe.objects(recipe_name=recipe_name).first()

    if not recipe:
        return jsonify({"error": "data not found"})
    else:
        recipe.delete()
        return redirect(url_for("home"))


@app.route("/recipes/<recipe_name>", methods=["GET", "PUT"])
def modify(recipe_name):
    recipes = Recipe.objects
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    if request.method == "GET":
        if not recipe:
            return jsonify({"error": "data not found"})
        else:
            return render_template("modify.html", recipe=recipe)
    else:
        recipe = request.get_json(force=True)
        recipe.update()
        return render_template("home.html", recipes=recipes)


if __name__ == "__main__":
    db.app.run(debug=True)
