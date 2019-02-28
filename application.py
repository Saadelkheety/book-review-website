import json
import jsonify

from flask import Flask, session, request, flash, redirect, url_for, render_template, Response
from flask import abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database_service import add_user, authenticate_user, search_books
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
    return render_template("index.html")

# registration route
@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if request.method == "GET":
        if session.get("email"):
            flash(
                f"you are alredy logged in as {session['first_name']} {session['last_name']}.")
            return redirect(url_for("index"))
        return render_template("register.html", form=form)
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
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(err)
        return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == "GET":
        if session.get("email"):
            flash(
                f"you are alredy logged in as {session['first_name']} {session['last_name']}.")
            return redirect(url_for("index"))
        return render_template("login.html", form=form)
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
            return render_template("login.html", form=form)

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


@app.route("/search", methods=["GET"])
@authenticate
def search():
    search_word = request.args.get("search").lower()
    books = search_books(db, search_word)
    # books = ','.join(map(str, books))
    PAGE_SIZE = 10
    page = request.args.get("page")
    if not page:
        page = 1
    nr_of_pages = int((len(books) / PAGE_SIZE))
    if len(books) == 0:
        flash("there are no results try another book or check the words you write.")
    if not nr_of_pages:
        nr_of_pages = 1
    print("this is the # of pages:   ", nr_of_pages)
    converted_page = int(page)
    if converted_page > nr_of_pages or converted_page < 0:
        print("this is the # of pages:   ", nr_of_pages,
              "but the requisted is:  ", converted_page)
        abort(404)

    from_idx = (converted_page - 1) * PAGE_SIZE
    stop_idx = from_idx + PAGE_SIZE
    books = books[from_idx:stop_idx]
    print(from_idx, stop_idx)
    print(books)
    return render_template("index.html", books=books, nr_of_pages=nr_of_pages, current_page=converted_page, search=search_word)
    # books = ','.join(map(str, books))
    # print(books)
    # return json.dumps(books)


if __name__ == '__main__':
    app.run(debug=True)
