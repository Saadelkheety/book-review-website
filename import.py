import csv
from application import db
from database_service import add_book

with open('books.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count < 3947: # line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
            continue
        new_book = {
            "isbn": row[0],
            "title": row[1],
            "author": row[2],
            "year": row[3]
        }
        check = add_book(db, new_book)
        if check == True:
            print(f"line {line_count} added.")
            line_count += 1
        else:
            print(f"database error in line {line_count}")

    print(f'added {line_count} books.')
