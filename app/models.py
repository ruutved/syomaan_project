'''from datetime import datetime
import db
from flask_login import UserMixin
import uuid


class User(db.Document, UserMixin):
    user_name = db.StringField(default=True)
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    timestamp = db.DateTimeField(default=datetime.now())
    user_id = uuid.uuid4().hex



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=None)
    ingredient = db.Column(db.String(100), nullable=None)
    #ingredients = db.relationship('Ingredient', backref='ingredient')
    description = db.Column(db.Text(3000))
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ing_name = db.Column(db.String(100), nullable=None)'''