import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


def add_user(db, user):
    check_email = db.execute("SELECT email FROM users WHERE email=:email", {"email":user["email"]}).fetchone()
    db.commit()
    if check_email:
        return f"{check_email[0]} is already used"
    cmd = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password);"
    try:
        new_user = db.execute(cmd, {"first_name": user["first_name"], "last_name": user["last_name"], "email": user["email"], "password": generate_password_hash(user["password"])})
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
    if check_password_hash(user.password, password):
        session["id"] = user.id
        session["email"] = user.email
        session["first_name"] = user.first_name
        session["last_name"] = user.last_name
        return dict(user)
    else:
        return False



if __name__ == "__main__":
    print(db)
