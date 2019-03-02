# book review website
this is a book review website. Users will be able to register for the website and then log in using their email and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. the website also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.

## the live version
https://elkheetybooks.herokuapp.com/

## requirements
check requirements.txt

## to run it:
- you can run it using python3 by command: "python3 application.py" after installing its requirements
by running command "pip3 install -r requirements.txt"
ps: make sure you are in the outer directory of the project

## application.py:
- it's the main file where the project starts and contains all routes which they are:
1. register:
  where the new users can register
2. login:
  where registered users can Login
3. logout:
  where the logged in users can logout
4. index("/"):
  where the user starts
5. search:
  Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well
6. Book:
  When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
  On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
  also display (if available) the average rating and number of ratings the work has received from Goodreads.
7. API:
  If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.

## database_service.py:
- it's the module contains all the functions deal directly with the database which they are:
1. add_user(db, user): adding the given user dict to the given db database.
2. authenticate_user(db, email, password): check the credentials passed within the passed db database.
3. add_book(db, book): to add book in the database.
4. search_books(db, search): find the books matches the search text in its isbn, title or author
5. find_book(db, isbn): find the book with a pecific ISBN
6. add_review(db, review): add a review
7. get_reviews(db, book_id): get a review for a specific book.
8. count_reviews(db, book_id): count the reviews for a specific book.
9. score_average(db, book_id): return the average rating for a specific book.

## decorators.py:
- it's the module contain the required decorators for the app which they are:
1. authenticate: to make sure there is a logged in user

## import.py:
a program that will take the books from CSV file and import them into the PostgreSQL database.
