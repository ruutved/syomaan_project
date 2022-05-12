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

    # Lisätään listaan reseptin id (referencefield Recipe-objektiin). Jos listaan lisättyä reseptiä
    # päivitetään myöhemmin, niin sen ainesosat päivittyvät myös ostoslistaan.
    user.recipes.append(recipe.id)
    user.save()

    return redirect(url_for("plan.plan"))


@login_required
def plan():
    recipes = current_user.recipes
    recipe_ids = []
    recipe_names = []

    # Lisätään reseptien id:t tarkasteltavassa muodossa listaan
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
        # Jos tietokannan reseptin id on sama kuin käyttäjän viikkosuunnitelmaan lisäämän reseptin id...
            if item["id"] == r_id:
            # ...lisätään kaikki reseptien id:t shortlistiin, jota tarvitaan seuraaviin vaiheisiin.
                shortlist.append(r_id)

    # Käydään läpi shortlist:
    # Jos id listalla on sama kuin minkä tahansa tietokannassa olevan reseptin, niin
    # lisätään sen reseptin nimi nimilistaan, jota tarvitaan viikkosuunnitelman tulostamiseen.
    # Tämä nimilista päivittyy aina plan-sivua ladatessa, eli jos reseptin nimi muuttuu, niin
    # se muuttuu myös viikkosuunnitelmassa.
    for item in get_ingredients:
        for food in shortlist:
            if food == item["id"]:
                recipe_names.append(item["recipe_name"])

                # Nyt varsinaiseen ostoslistaan.
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
    # toisessa 4, niin ostoslistaan tulostuu "6 kpl kananmunaa". Rajataan luvut kahteen desimaaliin.

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




