from flask import Blueprint
from application.controllers.plan_controllers import prep_add_plan, plan, added_to_plan, delete_from_plan


plan_bp = Blueprint('plan', __name__)
plan_bp.route('/add_to_plan/<recipe_name>', methods=['GET'])(prep_add_plan)
plan_bp.route('/plan', methods=['GET'])(plan)
plan_bp.route('/added_to_plan/<recipe_name>', methods=['GET'])(added_to_plan)
plan_bp.route('/delete_from_plan/<recipe_name>', methods=['GET'])(delete_from_plan)
