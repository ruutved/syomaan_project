import os

from flask import Flask, request, make_response, jsonify, url_for, redirect, session, render_template
from flask_mongoengine import MongoEngine
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = pymongo.MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client.get_database('syomaan_app')
users = db.users



''' class Recipes(db.Document):
    Name = db.StringField(required=True)
    Ingredients = db.ListField(required=True)
    Description = db.StringField(required=True) '''


@app.route("/", methods=['GET'])
def home():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    else:
        return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = users.find_one({"name": name})
        email_found = users.find_one({"email": email})

        if user_found:
            message = "Käyttäjänimi on jo olemassa!"
            return render_template("home.html", message=message)
        if email_found:
            message = "Tällä sähköpostiosoitteella on jo käyttäjänimi!"
            return render_template("home.html", message=message)

        if password1 != password2:
            message = 'Salasanat eivät täsmää!'
            return render_template("home.html", message=message)

        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {"name": name, "email": email, "password": hashed}
            users.insert_one(user_input)

            user_data = users.find_one({"email": email})
            new_email = user_data["email"]

            return render_template("logged_in.html", email=new_email)

    else:
        return render_template("signup.html")


@app.route("/logged_in")
def logged_in():
    if "name" in session:
        name = session["name"]
        return render_template("logged_in.html", name=name)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
