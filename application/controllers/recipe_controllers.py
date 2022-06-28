from flask import request, flash, redirect, render_template, url_for, jsonify
from flask_login import login_required, current_user

from application.models.models import Recipe, User


@login_required
def add_recipe():

    if request.method == "POST":

        recipe_name = request.form.get("rec_name")
        existing_recipe = Recipe.objects(recipe_name=recipe_name).first()

        if not existing_recipe:

            recipe_category = request.form.get("category")
            add_quantities = request.form.getlist(key="quantity")
            add_units = request.form.getlist(key="measuring_unit")
            add_ingredients = request.form.getlist(key="ingredient")

            added_ingredients = []

            for j, k, x in zip(add_quantities, add_units, add_ingredients):
                ingr = {'quantity': j, 'measuring_unit': k, 'ingredient': x}
                added_ingredients.append(ingr)

            description = request.form.get("instructions")
            creator = current_user.email

            new_recipe = Recipe(recipe_name=recipe_name,
                                ingredients=added_ingredients,
                                description=description,
                                category=recipe_category,
                                creator=creator)

            new_recipe.save()

        else:
            flash('Tämänniminen resepti on jo olemassa. Keksi jokin uusi nimi!')
            return redirect(url_for('recipe.add_recipe'))

        return redirect(url_for('auth.home'))

    else:
        return render_template("add_recipe.html")


@login_required
def modify(recipe_name):

    # This function only renders the page where a recipe is modified.
    # The modification itself is in the auth.home endpoint
    recipes = Recipe.objects
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    if request.method == "GET":
        if not recipe:
            return jsonify({"error": "data not found"})
        else:
            return render_template("modify.html", recipe=recipe)
    else:
        return render_template("home.html", recipes=recipes)


@login_required
def delete_ingredient(recipe_name):

    # Deleting an ingredient
    ingredient = request.args.get('ingredient')
    recipe = Recipe.objects(recipe_name=recipe_name).first()
    ingredients = recipe.ingredients

    for item in ingredients:
        if str(item) == str(ingredient):
            ingredients.remove(item)
            recipe.save()
        else:
            return jsonify({"error": ""})

    return redirect(url_for('recipe.modify', recipe_name=recipe_name))


@login_required
def prep_delete(recipe_name):
    # Rendering a recipe and making sure the user wants to delete it:
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    if not recipe:
        flash('Reseptiä ei löydy, tarkista tiedot!')  # No such recipe exists
        return redirect(url_for('auth.home'))
    else:
        return render_template("prep_delete.html", recipe=recipe)


@login_required
def delete_recipe(recipe_name):

    # Recipe can be deleted only if it's in just its creator's weekly plan
    recipe = Recipe.objects(recipe_name=recipe_name).first()
    all_users = User.objects
    recipe_id = recipe['id']

    action = 0

    if not recipe:
        return jsonify({"error": "data not found"})
    else:
        # Let's check if the recipe has been added to someone else's weekly plan (not the creator)
        # If yes, the recipe cannot be deleted.
        for user in all_users:
            if user["id"] != current_user.id:
                for item in user.recipes:
                    if recipe_id == item['id']:
                        action += 1
                        flash('Tätä reseptiä ei voi poistaa, sillä joku muu on lisännyt sen viikkosuunnitelmaansa!')
                        return render_template("prep_delete.html", recipe=recipe)
    # If the recipe isn't in anyone else's plan:
    if action == 0:
        # If it's in its creator's plan, let's first remove it from there and then entirely
        for item in current_user.recipes:
            if str(recipe_id) == str(item['id']):
                current_user.recipes.remove(item)
                current_user.save()
                recipe.delete()
                return redirect(url_for("auth.home"))
            else:
                recipe.delete()

    return redirect(url_for("auth.home"))
