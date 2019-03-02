import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, make_response


def add_user(db, user):
    check_email = db.execute("SELECT email FROM users WHERE email=:email", {
                             "email": user["email"]}).fetchone()
    db.commit()
    if check_email:
        return f"{check_email[0]} is already used"
    cmd = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password);"
    try:
        new_user = db.execute(cmd, {"first_name": user["first_name"], "last_name": user["last_name"],
                                    "email": user["email"], "password": generate_password_hash(user["password"])})
        db.commit()
        return True
    except:
        return False
    # user_check = db.execute("SELECT * FROM users WHERE email = :email", {"email": user["email"]}).fetchone()
    # db.commit()
    return "database error"


def authenticate_user(db, email, password):
    cmd = "SELECT * FROM users WHERE email = :email"
    user = db.execute(cmd, {"email": email}).fetchone()
    if not user:
        return False
    elif check_password_hash(user.password, password):
        session["id"] = user.id
        session["email"] = user.email
        session["first_name"] = user.first_name
        session["last_name"] = user.last_name
        return dict(user)
    else:
        return False


def add_book(db, book):
    check_isbn = db.execute("SELECT isbn FROM books WHERE isbn=:isbn", {
        "isbn": book["isbn"]}).fetchone()
    db.commit()
    if check_isbn:
        return f"{check_isbn[0]} is already used"
    cmd = "INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year);"
    try:
        new_book = db.execute(cmd, {"isbn": book["isbn"], "title": book["title"],
                                    "author": book["author"], "year": book["year"]})
        db.commit()
        return True
    except:
        return False
    # user_check = db.execute("SELECT * FROM users WHERE email = :email", {"email": user["email"]}).fetchone()
    # db.commit()
    return "database error"


def search_books(db, search):
    books = db.execute("SELECT * FROM books WHERE isbn LIKE :search or title LIKE :search or author LIKE :search ORDER BY TITLE;", {
        "search": "%" + search + "%"}).fetchall()
    return books


def find_book(db, isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:search;", {
        "search": isbn}).fetchone()
    if book:
        return book
    else:
        return None


def add_review(db, review):
    check_review = db.execute("SELECT * FROM reviews WHERE user_id=:user_id AND book_id=:book_id", {
        "user_id": review["user_id"], "book_id": review["book_id"]}).fetchone()
    db.commit()
    if check_review:
        return f"you already added a review to this book"
    cmd = "INSERT INTO reviews (rating, review, user_id, book_id) VALUES (:rating, :review, :user_id, :book_id);"
    try:
        new_review = db.execute(cmd, {"rating": review["rating"], "review": review.get("review"),
                                      "user_id": review["user_id"], "book_id": review["book_id"]})
        db.commit()
        return True
    except:
        return False
    # user_check = db.execute("SELECT * FROM users WHERE email = :email", {"email": user["email"]}).fetchone()
    # db.commit()
    return "database error"


def get_reviews(db, book_id):
    reviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id", {
        "book_id": book_id}).fetchall()
    db.commit()
    if reviews:
        return reviews
    else:
        return None


def count_reviews(db, book_id):
    review_count = db.execute("SELECT count(*) FROM reviews WHERE book_id=:book_id", {
        "book_id": book_id}).fetchone()[0]
    db.commit()
    return review_count


def score_average(db, book_id):
    average_score = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id=:book_id", {
        "book_id": book_id}).fetchone()[0]
    db.commit()
    return average_score


if __name__ == "__main__":
    print(db)
