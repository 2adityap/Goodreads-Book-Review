import csv

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    count = 0
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
        print("ISBN: {0}, Title: {1}, Author: {2}, Year: {3}".format(isbn,title,author,year))
        count += 1
    db.commit()
    print("Count: {0}".format(count))

if __name__ == "__main__":
    main()
