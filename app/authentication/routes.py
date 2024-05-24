from flask import Blueprint, redirect, request, url_for, render_template, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from models import User, db, check_password_hash
from forms import NewUserForm, LoginUserForm

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    form = NewUserForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            user = User(first_name, last_name, email, password=password)
            db.session.add(user)
            db.session.commit()

            flash(f"LOG: You {first_name} {last_name} now has access to the api")
            return redirect(url_for("site.home"))
    except:
        raise Exception("ERROR: Sorry, invalid data form")
    
    print("opened")
    return render_template("signup.html", form=form)

@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    form = LoginUserForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("LOG: You are now logged in")
                return redirect(url_for("site.profile"))
            else:
                flash("ERROR: Access to api has been denied")
                return redirect(url_for("auth.signin"))
    except:
        raise Exception("ERROR: Sorry, invalid data form")
    
    return render_template("signin.html", form=form)

@auth.route("/logoff")
def logoff():
    logout_user()
    return redirect(url_for("site.logout"))