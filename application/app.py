from flask import Flask
from flask_login import LoginManager

from application.models.models import db, User
from application.routes.auth import auth_bp
from application.routes.plan import plan_bp
from application.routes.recipe import recipe_bp

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'syomaan',
    'host': 'localhost',
    'port': 27017
}


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


app.config['SECRET_KEY'] = 'syomaanapp'

app.register_blueprint(auth_bp, url_prefix='')
app.register_blueprint(recipe_bp, url_prefix='')
app.register_blueprint(plan_bp, url_prefix='')

if __name__ == "__main__":
    db.app.run(debug=True)
