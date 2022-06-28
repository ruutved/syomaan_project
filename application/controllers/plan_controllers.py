from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from application.models.models import Recipe, User


@login_required
def prep_add_plan(recipe_name):
    # Recipe will be rendered on the page and the user is asked if
    # they want to add it to the weekly plan:
    recipe = Recipe.objects(recipe_name=recipe_name).first()
    recipe_id = recipe.id
    return render_template('add_to_plan.html', recipe=recipe, recipe_name=recipe_name, recipe_id=recipe_id)


@login_required
def added_to_plan(recipe_name):
    # The user is identified by their email address so the recipe can be
    # added to the weekly plan:
    user = User.objects(email=current_user.email).first()
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    # Adding the recipe id to the user's recipe list (a reference field to the Recipe
    # object). So if the added recipe is updated later, its ingredients etc. are
    # updated in the shopping list as well.
    user.recipes.append(recipe.id)
    user.save()

    return redirect(url_for("plan.plan"))


@login_required
def plan():

    # Rendering the weekly plan:

    # Retrieving the current user's recipes:
    recipes = current_user.recipes

    # Let's create two empty lists. One is for recipe ids and the other
    # will later on take the recipes' names.

    recipe_ids = []
    recipe_names = []

    # Now we add the recipe ids to the above list. This has to be done - if we just
    # loop through current_user.recipes, we print a string "Recipe object" (this could be
    # described as a kind of foreign key to the recipe).
    # So we have to retrieve all the ids with a temporary variable item["id"], as the data type ObjectID
    # cannot be handled as such.

    for item in recipes:
        recipe_ids.append(item["id"])

    # Let's now create a list for the ingredients:
    pre_shopping_list = []

    # Retrieving all the recipes in the database to have a reference to the ingredients:
    get_ingredients = Recipe.objects

    # Next, we loop through the recipe_ids list together with all the recipes in the database.
    # If an id on the recipe_ids list is identical to any recipe in the database (which we expect to be the case),
    # we add that recipe's name to the name list.
    # This name list is always updated and retrieved when loading the "plan" page - so in case of any
    # changes, the changes are reflected in the weekly plan.
    for item in get_ingredients:
        for food in recipe_ids:
            if food == item["id"]:
                recipe_names.append(item["recipe_name"])

                # Now we create the shopping list.
                # Looping through the ingredients:
                for ingredient in item["ingredients"]:
                    # One doesn't usually have to buy water for cooking so let's exclude it:
                    if ingredient["ingredient"] != "vettä":
                        # Now adding everything else to a temporary shopping list:
                        pre_shopping_list.append(ingredient)

    # Measurement conversions are up next, so the same ingredients will be in the same units of measurement.
    # I have chosen to convert all the ml, cl, l, tbsp or tsp (rkl and tl in Finnish, respectively) to desiliters (dl).
    # Kilograms are converted to grams.
    # Obviously this list is NOT exhaustive and won't solve all the problems!
    # It's rather an example of what can be done:

    for item in pre_shopping_list:
        if item["measuring_unit"].strip() == "ml" or item["measuring_unit"].strip() == "millilitraa":
            item["quantity"] = float(item["quantity"]) * 0.01
            item["measuring_unit"] = "dl"
        elif item["measuring_unit"].strip() == "cl" or item["measuring_unit"].strip() == "senttilitraa":
            item["quantity"] = float(item["quantity"]) * 0.1
            item["measuring_unit"] = "dl"
        elif item["measuring_unit"].strip() == "l" or item["measuring_unit"].strip() == "litraa":
            item["quantity"] = float(item["quantity"]) * 10
            item["measuring_unit"] = "dl"
        elif item["measuring_unit"].strip() == "rkl" or item["measuring_unit"].strip() == "ruokalusikallista":
            item["quantity"] = float(item["quantity"]) * 0.15
            item["measuring_unit"] = "dl"
        elif item["measuring_unit"].strip() == "tl" or item["measuring_unit"].strip() == "teelusikallista":
            item["quantity"] = float(item["quantity"]) * 0.05
            item["measuring_unit"] = "dl"
        elif item["measuring_unit"].strip() == "kg" or item["measuring_unit"].strip() == "kilogrammaa":
            item["quantity"] = float(item["quantity"]) * 1000
            item["measuring_unit"] = "g"
        elif item["measuring_unit"].strip() == "gr":
            item["measuring_unit"] = "g"
        else:
            pass

    # The next structure makes sure that any duplicate ingredients from many recipes are printed in the
    # shopping list only once, with the total amount needed for all the recipes.
    # For example, if one recipe has 2 eggs and another 4 eggs, then the shopping list will have 6 eggs.
    # Amounts are rounded to 2 decimals.
    # This program won't take into account typing errors or ingredients written in different forms!
    # So this also should be treated as an example of a feature.

    final_list = {}
    for item in pre_shopping_list:
        key = (item["ingredient"])
        if key in final_list:
            final_list[key] = {"quantity": round(float(item["quantity"]) + float(final_list[key]["quantity"]), 2),
                                "measuring_unit": item["measuring_unit"], "ingredient": item["ingredient"]}
        else:
            final_list[key] = {"quantity": round(float(item["quantity"]), 2), "measuring_unit": item["measuring_unit"],
                               "ingredient": item["ingredient"]}

    return render_template('plan.html', name=current_user.user_name,
                           recipes=recipe_names, final_list=final_list)


@login_required
def delete_from_plan(recipe_name):

    # Retrieving recipe name and id, so it can be deleted from the weekly plan:
    recipe = Recipe.objects(recipe_name=recipe_name).first()
    recipe_id = recipe.id

    for item in current_user.recipes:
        if str(recipe_id) == str(item['id']):
            current_user.recipes.remove(item)
            current_user.save()
            return redirect(url_for("plan.plan"))

        else:
            pass

    return redirect(url_for("plan.plan"))




