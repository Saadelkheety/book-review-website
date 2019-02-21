import json

from flask import Flask, session, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database_service import add_user, authenticate_user
from forms import RegistrationForm, LoginForm
from decorators import authenticate

app = Flask(__name__)
app.config['DATABASE_URL'] = 'postgres://pnmtgllgpxpljn:c61804a0547643ba8d629d9093c880841c30bbea40e359114cb1aca21f3aa2fc@ec2-23-21-171-25.compute-1.amazonaws.com:5432/d66gugrpbq4r0k'
app.config['secret_key'] = b'_5#y2L"F4Q8z\n\xec]/'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(app.config['DATABASE_URL'])
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@authenticate
def index():
    return f"Hi, ya3am {session['first_name']} {session['last_name']}"

# registration route
@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if request.method == "GET":
        return "this is the registration template. C'MON just imagine"
    elif form.validate_on_submit():
        new_user = {
        "first_name": form.first_name.data,
        "last_name": form.last_name.data,
        "email": form.email.data,
        "password": form.password.data
        }
        check = add_user(db, new_user)
        # if the user added without errors then login the user
        if check == True:
            user = authenticate_user(db, form.email.data, form.password.data)
            if user:
                return redirect(url_for("index"))
            else:
                return "authentication error"
        # if the email already in the database
        elif check == False:
            flash("this email is already registerd")
            return redirect(url_for("register"))
        # if there are any other errors just flash it
        else:
            flash(check, 'danger')
            return redirect(url_for("register"))
    # if the validation raise errorMessages then flash it
    elif form.errors.items():
        err_str = ""
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                err_str = err_str + err +"\n"
        flash(err_str, 'danger')
        return redirect(url_for("register"))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == "GET":
        return "this is the login template. C'MON just imagine"
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        # sure the credintials is right and create a login session
        user = authenticate_user(db, email, password)
        print(user.get("email") + " has been logged in.")
        if user:
            return redirect(url_for("index"))
        else:
            flash("the credintials are wrong please correct eamil or password", 'danger')
            return "this is the login template. C'MON just imagine"

# to log out using POST request
@app.route("/logout", methods=["POST"])
def logout():
    if not session.get("email"):
        flash("you are alredy logged out")
        return redirect(url_for("login"))
    session.clear()
    flash("logged out")
    print(session, "is empty?")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug = True)
