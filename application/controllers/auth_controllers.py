from datetime import datetime

from flask import request, render_template, make_response, flash, redirect, url_for, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from application.models.models import Recipe, User


def home():
    if request.method == 'GET':
        recipes = Recipe.objects
        return render_template("home.html", recipes=recipes)

    else:
        # Seuraava koodi muokkaa reseptiä:
        quantities = request.form.getlist(key="quantity")
        m_units = request.form.getlist(key="measuring_unit")
        ingredients = request.form.getlist(key="ingredient")

        modified_ingredients = []

        for j, k, x in zip(quantities, m_units, ingredients):
            ingr = {'quantity': j, 'measuring_unit': k, 'ingredient': x}
            modified_ingredients.append(ingr)

        recipe = Recipe.objects(id=request.form["recipe_id"]).first()

        recipe.update(recipe_name=request.form["rec_name"],
                      description=request.form["instructions"],
                      ingredients=modified_ingredients,
                      category=request.form["category"])
        res = make_response(jsonify({"message": "recipe updated"}))
        return res


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
            return redirect(url_for('auth.signup'))

        if password1 != password2:
            flash('Salasanat eivät täsmää!')
            return redirect(url_for('auth.signup'))

        else:
            hashed_password = generate_password_hash(password2, method='sha256')
            user_input = User(user_name=user_name,
                              email=email,
                              password=hashed_password,
                              registration_time=datetime.now())

            user_input.save()

            return redirect(url_for('auth.login'))

    else:
        return render_template("signup.html")


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
                return redirect(url_for('auth.logged_in'))

            else:
                if current_user.email:
                    return redirect(url_for('auth.logged_in'))
                else:
                    flash('Väärä salasana')
                    return redirect(url_for('auth.login'))
        else:
            flash('Käyttäjää ei löydy!')
            return redirect(url_for('auth.ogin'))

    else:
        return render_template("login.html")


@login_required
def logged_in():
    return render_template('logged_in.html', name=current_user.user_name)


@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))


@login_required
def profile():
    email = current_user.email
    recipes = Recipe.objects

    user_recipes = 0

    for recipe in recipes:
        if recipe["creator"] == email:
            user_recipes += 1
        else:
            pass

    return render_template('profile.html', user_recipes=user_recipes, name=current_user.user_name)

