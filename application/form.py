# Create a form class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

# Create a search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")

class UploadProfilePic(FlaskForm):
    profile_pic = FileField("Change Photo")
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Your full name", validators=[DataRequired()])
    username = StringField("Blogger name(How do you want others to see you?)", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = CKEditorField("Tell us something about yourself")
    phone = StringField("Phone")
    profession = StringField("What is your profession?")
    experience = StringField("How many years experience you have?")
    skills = StringField("Please methion the skills you have (each separated by a ',')")
    profile_pic = FileField("Add your profile pic", validators=[FileAllowed(["png", "jpg", "jpeg", "ico", "gif"], "Images only!")])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo("password_hash2", message="Passwords must match")])
    password_hash2 = PasswordField("Confirm passsword", validators=[DataRequired()])
    submit = SubmitField("Register now")

class NamerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    fav_color = StringField("Favourite colour")
    submit = SubmitField("Add user")

class UserUpdateForm(FlaskForm):
    name = StringField("Your full name", validators=[DataRequired()])
    username = StringField("Blogger name(How do you want others to see you?)", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = CKEditorField("Tell us something about yourself")
    phone = StringField("Phone")
    profession = StringField("What is your profession?")
    experience = StringField("How many years experience you have?")
    skills = StringField("Please methion the skills you have (each separated by a ',')")
    profile_pic = FileField("Update your profile pic", validators=[FileAllowed(["png", "jpeg", "jpg", "ico", "gif"], "Images only!")])
    password_hash = PasswordField("Password", validators=[DataRequired(),
                                                          EqualTo("password_hash2", message="Passwords must match")])
    password_hash2 = PasswordField("Confirm passsword", validators=[DataRequired()])
    submit = SubmitField("Update my profile")

class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Check")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author")
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserLogin(FlaskForm):
    username = StringField("Blogger name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")