from flask_login import UserMixin
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_ckeditor import CKEditor
import json

#load the json data
file = open(r"application\config.json", "r")
data = json.load(file)
file.close()
# from .create_db import *

app = Flask(__name__)
# Add CKEditor to this application
ckeditor = CKEditor(app)

# Create the secret key
app.config["SECRET_KEY"] = "abcd@123"

# Let's configure the upload folder which tells our app where to store the uploaded files
UPLOAD_FOLDER = r"application/static/uploads/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Add database
# Old sqlite db
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# New PostGreSQL db

app.config["SQLALCHEMY_DATABASE_URI"] = data["postgresql_uri"]
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/users"
# create_db()

# Initialize the database
db = SQLAlchemy(app)
# Create a model for user

# Create an admin ID
admin_id = data["admin_id"]

#### There will be one to many relationship between User and Posts, i.e. a User can have many Posts, but a post can have only one User. ###

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    phone = db.Column(db.String(25))
    profile_pic = db.Column(db.String(200))
    profession = db.Column(db.String(150))
    experience = db.Column(db.String(3))
    skills = db.Column(db.String(500))
    about = db.Column(db.Text())

    date_added = db.Column(db.DateTime, default=datetime.now())
    # Do some password stuff
    password_hash = db.Column(db.String(200))

    # A user can have many posts
    posts = db.relationship("Posts", backref="poster") # It is upper case because it is referencing the class Posts, and not any table in the database. backref="poster" will create a sort of like a fake column in posts table and will keep track of each posts author name, thus if we want any post author name, we will refer to poster.username and so on...

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a string
    def __repr__(self):
        return "<Name %r>"%self.name


#Create a model for blog post
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    # author will be taken from the current logged in User only
    # Create a foreign key to link User, and this foreign key will refer to the primary key of the User.
    poster_id = db.Column(db.Integer, db.ForeignKey("user.id")) # It is lowercase u because it is referencing the table in database, which always starts with lower case

