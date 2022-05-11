from flask import Blueprint
from application.controllers.auth_controllers import home, signup, login, logged_in, logout, profile


auth_bp = Blueprint('auth', __name__)
auth_bp.route('/', methods=['GET', 'PUT'])(home)
auth_bp.route('/signup', methods=['POST', 'GET'])(signup)
auth_bp.route('/login', methods=['POST', 'GET'])(login)
auth_bp.route('/logged_in', methods=['GET'])(logged_in)
auth_bp.route('/logout', methods=['GET'])(logout)
auth_bp.route('/profile', methods=['GET'])(profile)
