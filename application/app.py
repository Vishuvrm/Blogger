from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_manager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid # Unique User ID numbers
import os
from .form import *
from .table_models import *
from datetime import datetime
from .create_db import create_db
from .create_table import create_table

# Create tables if not exists
create_table("user", app.config["SQLALCHEMY_DATABASE_URI"], db)
create_table("posts", app.config["SQLALCHEMY_DATABASE_URI"], db)

# Migrate our app with the database db
migrate = Migrate(app, db)

# Login stuff
login_manager = LoginManager() # Instantiate flask login thing
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login form
@app.route("/login", methods=["GET", "POST"])
def login():
    form = UserLogin()
    # Validate form submission
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            # Check the hash
            pw_hash = user.password_hash
            pw_to_check = form.password.data
            if check_password_hash(pw_hash, pw_to_check):
                login_user(user) # Login the user
                if current_user.id == admin_id:
                    flash(f"Welcome {current_user.name}! You are logged in as admin")
                return redirect(f"/dashboard")
            else:
                flash("Incorrect password!")
                form.password.data = ""
        else:
            flash("User not valid!")
            form.username.data = ""

    return render_template("login.html", form=form)

# Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = User.query.filter_by(id=current_user.id).first()
    form = UserUpdateForm()
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted.desc())
    num_posts = len(Posts.query.filter_by(poster_id=current_user.id).all())
    if current_user.skills:
        skills_list = [skill.strip() for skill in (current_user.skills).split(",")]
    else:
        skills_list = []
    # Check if that user alerady exists
    user_to_find = form.username.data
    if User.query.filter_by(username=user_to_find).first() and user_to_find != current_user.username:
        flash(f"Sorry! Blogger name {user_to_find} already taken :(")
    else:
        # if form.validate_on_submit():
        if request.method == "POST":
            user.name = form.name.data
            user.username = form.username.data
            user.email = form.email.data
            user.about = form.about.data
            user.phone = form.phone.data
            user.profession = form.profession.data
            user.experience = form.experience.data
            user.skills = form.skills.data

            profile_image = form.profile_pic.data
            if profile_image:
                # Grab image name
                profile_pic_name = secure_filename(profile_image.filename)
                # set uuid
                pic_name = f"{(uuid.uuid1())}_{profile_pic_name}"
                # Save that image and delete the previous one
                if user.profile_pic:
                    os.remove(os.path.join((app.config["UPLOAD_FOLDER"]), user.profile_pic))
                profile_image.save(os.path.join(app.config["UPLOAD_FOLDER"]), pic_name)
                # save the name to the database
                user.profile_pic = pic_name

            user.date_added = datetime.now()
            try:
                db.session.commit()
                flash(f"Your profile updated!")
                return redirect("/dashboard")
            except Exception:
                flash(f"Couldn't update for {user.name}")
                return redirect("/dashboard")

    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.about.data = user.about
    form.phone.data = user.phone
    form.profession.data = user.profession
    form.experience.data = user.experience
    # form.skills.data = ", ".join(user.skills)
    form.skills.data = user.skills
    form.profile_pic.data = user.profile_pic

    return render_template("dashboard.html", user=user, form=form, posts=posts, num_posts=num_posts, skills_list = skills_list, admin_id=admin_id)

# Create logout function
@app.route("/logout", methods=["GET", "POST"])
@login_required  # We can logout only when we are logged in.
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect("/")

@app.route("/posts")
def posts():
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted.desc())
    num_posts = len(Posts.query.filter_by().all())
    return render_template("posts.html", posts=posts, num_posts = num_posts, admin_id=admin_id)

# See the post
@app.route("/posts/<int:id>/<string:slug>")
def view_post(id,slug):
    # post = Posts.query.filter_by(id=id).first()
    post = Posts.query.get_or_404(id)
    return render_template("view_post.html", post=post, admin_id=admin_id)

# Add posts page
@app.route("/add/post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        title = form.title.data
        slug = title.replace(" ", "-").lower()
        content = form.content.data

        post = Posts(title=title, slug=slug, content=content, date_posted=datetime.now(), poster_id=poster)

        # Add post to the database table posts
        db.session.add(post)
        db.session.commit()

        # Clear the form
        form.title.data = ""
        form.content.data = ""
        flash("Your post submitted!")
        return redirect(f"/posts/{post.id}/{post.slug}")

    return render_template("add_post.html", form=form, admin_id=admin_id)

@app.route("/posts/edit/<int:id>/<string:slug>", methods=["GET", "POST"])
@login_required
def edit_post(id, slug):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        slug = title.replace(" ", "-").lower()
        content = form.content.data

        # Edit post into database table posts
        post.title = title
        post.author = author
        post.slug = slug
        post.content = content

        db.session.commit()

        # Clear the form
        form.title.data = ""
        form.author.data = ""
        form.content.data = ""
        flash("Your post edited!")
        return redirect(f"/posts/{post.id}/{post.slug}")

    form.title.data = post.title
    form.content.data = post.content

    return render_template("edit_post.html", form=form, post=post)

# delete posts
@app.route("/posts/delete/<int:id>/<string:slug>")
@login_required
def delete_post(id, slug):
    try:
        Posts.query.filter_by(id=id).delete()
        db.session.commit()
        flash(f"Post Deleted!")
    except Exception:
        flash(f"Couldn't delete post")

    return redirect("/dashboard")

# delete all posts for a user
@app.route("/<int:id>/delete-all-posts")
@login_required
def delete_all_posts(id):
    try:
        Posts.query.filter_by(poster_id=id).delete()
        db.session.commit()
        flash(f"All posts Deleted!")
    except Exception:
        flash(f"Couldn't delete all posts")

    return redirect("/dashboard")

# Pass stuff to extended files like base.html -> navbar.html
@app.context_processor # It will pass stuff to the base file(extended files)
def base():
    form = SearchForm()
    return dict(form = form)

# Create search function
@app.route("/search-results", methods=["POST"])
def search():
    form = SearchForm()
    if request.method == "POST":
        searched = form.searched.data
        searched_posts = Posts.query.filter(Posts.content.like(f"%{searched}%")).order_by(Posts.title).all()
        all_posts = Posts.query.filter().order_by(Posts.title).all()

        num_searched_posts = len(searched_posts)
        num_posts = len(all_posts)
        return render_template("search_results.html", admin_id=admin_id, form=form, searched=searched, searched_posts=searched_posts, num_searched_posts=num_searched_posts, all_posts=all_posts, num_posts=num_posts)


# Create admin page
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.id == admin_id:
        our_users = User.query.order_by(User.date_added).all()
        num_users = len(our_users)
        return render_template("admin.html", our_users=our_users, num_users=num_users, admin_id=admin_id)
    else:
        flash("Sorry! You are not an admin")
        return redirect("/dashboard")

# View anyone's post as admin
@app.route("/<int:id>/<string:username>/posts")
@login_required
def view_posts_as_admin(id, username):
    user = User.query.get_or_404(id)
    posts = Posts.query.filter_by(poster_id=id).all()
    skills_list = [skill.strip() for skill in (user.skills).split(",")]
    return render_template("view_posts_as_admin.html", user=user, posts=posts, admin_id=admin_id, name=user.name, skills_list=skills_list)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    username = None
    email = None
    form = UserForm()
    # Validate form submission
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        about = form.about.data
        phone = form.phone.data
        profession = form.profession.data
        experience = form.experience.data
        # skills = [skill.strip() for skill in (form.skills.data).split(",")]
        skills = form.skills.data
        profile_pic = form.profile_pic.data
        password = form.password_hash.data
        hashed_pass = generate_password_hash(password, "sha256")
        user_as_username = User.query.filter_by(username=username).first()
        user_as_email = User.query.filter_by(email=email).first()
        if user_as_username is not None:
            flash(f"Username {username} already taken :(")
            # return redirect("/user/add")
        elif user_as_email is not None:
            flash("Email already exists")
            # return redirect("/user/add")
        else:
            form.name.data = ""
            form.username.data = ""
            form.email.data = ""
            form.profession.data = ""
            form.experience.data = ""
            form.skills.data = ""
            form.phone.data = ""
            form.about.data = ""

            form.password_hash.data = ""

            user = User(name=name, username=username, email=email, about=about, phone=phone, profession=profession, experience=experience, skills=skills, profile_pic=profile_pic, date_added=datetime.now(), password_hash=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash(f"Hi {name}! You are now registered!")
            return redirect("/login")

    return render_template("add_user.html", email=email, name=name, form=form)

# Update database record
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    user = User.query.filter_by(id=id).first()
    form = UserUpdateForm()
    if request.method == "POST":
        # user.name = request.form.get("name")
        # user.email = request.form.get("email")
        # OR
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
        user.date_added = datetime.now()
        try:
            db.session.commit()
            flash(f"Updated your profile!")
            return redirect("/dashboard")
        except Exception:
            flash(f"Couldn't update for {user.name}")


    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username

    return render_template("update_record.html", user=user, form=form)

# Update database record
@app.route("/user/delete")
@login_required
def delete_user():
    try:
        if current_user.id == admin_id:
            flash("Can't delete admin!")
            return redirect("/dashboard")
        else:
            id = current_user.id
            user = User.query.filter_by(id=id).first()
            User.query.filter_by(id=id).delete()
            db.session.commit()
            flash(f"Your account removed! Thankyou for being with us so long..")
    except Exception as e:
        if current_user.id != admin_id:
            flash(f"Couldn't delete {user.name}..Try deleting all your posts first before we say goodbye...")
        return redirect("/dashboard")
    return redirect("/")

@app.route("/admin/user/<int:id>/delete")
@login_required
def admin_delete_user(id):
    try:
        if id != admin_id:
            user = User.query.filter_by(id=id).first()
            User.query.filter_by(id=id).delete()
            db.session.commit()
            flash(f"Removed account for {user.name}(User-ID: {user.id})!")
        else:
            flash("Can't delete admin!")
    except Exception:
        flash(f"Couldn't delete {user.name}..Try deleting all the posts first before deleting this user...")
        return redirect("/admin")
    return redirect("/admin")

@app.route("/")
def index():
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted.desc())
    num_posts = len(Posts.query.filter_by().all())
    return render_template("index.html", posts=posts, num_posts=num_posts, admin_id=admin_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

