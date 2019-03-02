import json
import jsonify
import math
import httplib2

from flask import Flask, session, request, flash, redirect, url_for, render_template, Response
from flask import abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database_service import score_average, add_user, authenticate_user, count_reviews, search_books, find_book, add_review, get_reviews
from forms import RegistrationForm, LoginForm, ReviewForm
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
        print(email, password)
        # sure the credintials is right and create a login session
        user = authenticate_user(db, email, password)
        print(email + " has been logged in.")
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
    nr_of_pages = math.ceil(int((len(books) / PAGE_SIZE)))
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


@app.route("/book/<string:isbn>", methods=["post", "GET"])
@authenticate
def book(isbn):
    form = ReviewForm(csrf_enabled=False)
    if request.method == "POST":
        review = {
            "rating": form.rating.data,
            "review": form.review.data,
            "user_id": session["id"],
            "book_id": form.book_id.data
        }
        add = add_review(db, review)
        if add == True:
            flash("your review has been added...")
            return redirect(url_for("book", isbn=isbn))
        elif add == False:
            flash("Database Error..!, please Email: SaadElkheety@gmail.com")
            return redirect(url_for("book", isbn=isbn))
        else:
            flash(add)
            return redirect(url_for("book", isbn=isbn))
    if request.method == "GET":
        book = find_book(db, isbn)
        if book:
            reviews = get_reviews(db, book.id)
            try:
                url = f'https://www.goodreads.com/book/review_counts.json?key=fWW2DdoQzw82qH5DEIe4CQ&isbns={book.isbn}'
                h = httplib2.Http()
                result = h.request(url, 'GET')[1]
                result = json.loads(result)['books'][0]
                print(result)
                goodreads = result
            except:
                goodreads = None
        return render_template("book.html", book=book, reviews=reviews, goodreads=goodreads, form=form)


@app.route("/api/<string:isbn>")
@authenticate
def api(isbn):
    book = find_book(db, isbn)
    if not book:
        abort(404)
    review_count = count_reviews(db, book.id)
    average_score = round(score_average(db, book.id), 2)
    # return jsonify({
    #     "title": book.title,
    #     "author": book.author,
    #     "year": book.year,
    #     "isbn": book.isbn,
    #     "review_count": review_count,
    #     "average_score": average_score
    # })
    response = app.response_class(
        response=json.dumps({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": str(average_score)
        }),
        status = 200,
        mimetype = 'application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug = True)
