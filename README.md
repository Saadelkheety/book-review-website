# book review website
this is a book review website. Users will be able to register for the website and then log in using their email and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. the website also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.

## the live version
https://elkheetybooks.herokuapp.com/

## requirements
check requirements.py

## to run it:
- you can run it using python3 by command: "python3 application.py" after installing its requirements
by running command "pip3 install -r requirements.txt"
ps: make sure you are in the outer directory of the project

## application.py:
- it's the main file where the project starts and contains all routs which they are:
1. register:
  where the new users can register
2. login:
  where registered users can Login
3. logout:
  where the logged in users can logout

## database_service.py:
- it's the module contains all the functions deal directly with the database which they are:
1. add_user(db, user): adding the given user dict to the given db database.
2. authenticate_user(db, email, password): check the credentials passed within the passed db database.


## decorators.py:
- it's the module contain the required decorators for the app which they are:
1. authenticate: to make sure there is a logged in user
