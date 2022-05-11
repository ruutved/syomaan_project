from itertools import repeat

from flask import render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user

from application.models.models import Recipe, User


@login_required
def prep_add_plan(recipe_name):

    recipe = Recipe.objects(recipe_name=recipe_name).first()
    recipe_id = recipe.id
    return render_template('add_to_plan.html', recipe=recipe, recipe_name=recipe_name, recipe_id=recipe_id)


@login_required
def added_to_plan(recipe_name):

    # Etsitään käyttäjä sähköpostiosoitteen perusteella, jotta
    # voidaan lisätä tälle resepti
    user = User.objects(email=current_user.email).first()
    recipe = Recipe.objects(recipe_name=recipe_name).first()

    user.recipes.append(recipe.id)
    user.save()

    return redirect(url_for("plan.plan"))


@login_required
def plan():

    recipes = current_user.recipes
    recipe_ids = []

    for item in recipes:
        recipe_ids.append(item["id"])


    # Tehdään uusi lista resepteistä siksi, että jos resepti lisätään viikkosuunnitelmaan
    # useammin kuin kerran, niin saadaan niistä kaikista yhteenlasketut ainekset ostoslistaan
    shortlist = []
    pre_shopping_list = []

    get_ingredients = Recipe.objects

    # Käydään läpi tietokannan reseptit:
    for item in get_ingredients:
        for r_id in recipe_ids:
            print(item["id"])
        # Jos reseptin nimi on sama kuin käyttäjän viikkosuunnitelman lisäämän reseptin:
            if item["id"] in recipes:
                print(item["id"])
            # Lasketaan, montako kertaa kukin resepti esiintyy viikkosuunnitelmassa:
            count = recipes.count(item["id"])
            # Lisätään kaikki reseptien nimet shortlistiin, myös ne jotka esiintyvät monta kertaa:
            shortlist.extend(repeat(item["id"], count))
            # Käydään läpi shortlist:
            for food in shortlist:
                # Jos id listalla on sama kuin minkä tahansa tietokannassa olevan reseptin:
                if food == item["id"]:
                    # Käydään läpi reseptin ainesosat tietokannassa:
                    for ingredient in item["ingredients"]:
                        # Vesi on sellainen ainesosa, jota ei tarvitse lisätä ostoslistaan, joten jätetään se pois:
                        if ingredient["ingredient"] != "vettä":
                        # Lisätään nyt kaikki muut tilapäiseen ostoslistaan:
                            pre_shopping_list.append(ingredient)

    # Suoritetaan tarvittavat yksikkömuunnokset, jotta saadaan ostoslistaan samat ainesosat yhdessä yksikössä.
    # Tässä tapauksessa kaikki ml, cl, l, rkl tai tl -muodossa olevat muutetaan desilitroiksi. Kilogrammat
    # muutetaan grammoiksi. Tämä ei ole kaikenkattava lista, mutta kattaa yleisimmät mitat.

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

    # Seuraava rakenne varmistaa sen, että useaan kertaan viikkosuunnitelmassa
    # esiintyvät ainesosat tulostuvat ostoslistaan kukin vain kerran, ja niiden kanssa
    # lopullinen tarvittava määrä. Esim. jos yhdessä reseptissä on 2 kananmunaa ja
    # toisessa 4, niin ostoslistaan tulostuu "6 kpl kananmunaa".

    final_list = {}
    for item in pre_shopping_list:
        key = (item["ingredient"])
        if key in final_list:
            final_list[key] = {"quantity": float(item["quantity"]) + float(final_list[key]["quantity"]),
                                "measuring_unit": item["measuring_unit"], "ingredient": item["ingredient"]}
        else:
            final_list[key] = {"quantity": float(item["quantity"]), "measuring_unit": item["measuring_unit"],
                               "ingredient": item["ingredient"]}

    return render_template('plan.html', name=current_user.user_name,
                           recipes=recipes, final_list=final_list)





@login_required
def delete_from_plan(recipe_name):

    user = User.objects(email=current_user.email).first()

    if recipe_name in user.recipes:
        user.recipes.remove(recipe_name)
        user.save()
        return redirect(url_for("plan.plan"))
    else:
        return jsonify({"error": "data not found"})


