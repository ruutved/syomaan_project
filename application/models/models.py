from datetime import datetime
from flask_login import UserMixin
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Recipe(db.Document):
    recipe_name = db.StringField(default=True)
    ingredients = db.ListField(default=True)
    description = db.StringField(default=True)
    category = db.StringField(default=True)
    creator = db.StringField(default=True)


class User(db.Document, UserMixin):
    user_name = db.StringField(default=True)
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    registration_time = db.DateTimeField(default=datetime.now())
    recipes = db.ListField(db.ReferenceField(Recipe), default=[])
