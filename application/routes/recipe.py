from flask import Blueprint
from application.controllers.recipe_controllers import add_recipe, \
    modify, delete_ingredient, prep_delete, delete_recipe

recipe_bp = Blueprint('recipe', __name__)
recipe_bp.route('/add_recipe', methods=['GET', 'POST'])(add_recipe)
recipe_bp.route('/recipes/<recipe_name>', methods=['GET', 'PUT'])(modify)
recipe_bp.route('/delete_ingredient/<recipe_name>', methods=['GET'])(delete_ingredient)
recipe_bp.route('/prep_delete/<recipe_name>', methods=['GET'])(prep_delete)
recipe_bp.route('/delete_recipe/<recipe_name>', methods=['GET'])(delete_recipe)
