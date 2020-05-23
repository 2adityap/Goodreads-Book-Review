import os
from flask import Flask, render_template, request
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/welcome", methods = ["POST"])
def welcome():
    name = request.form.get("username")
    password = request.form.get("password")
    users = db.execute("SELECT * FROM users").fetchall()
    for user in users:
        if user.username == name and user.password == password:
            return render_template("welcome.html",name=name)
    return render_template("loginError.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/new_user", methods = ["POST"])
def new_user():
    username = request.form.get("username")
    password = request.form.get("password")
    users = db.execute("SELECT username FROM users").fetchall()
    for user in users:
        if user.username == username:
            return render_template("alreadyRegistered.html")
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
    db.commit()
    return render_template("successRegister.html")

@app.route("/search", methods = ["POST"])
def search():
    search = request.form.get("search")
    books = db.execute("SELECT * FROM books").fetchall()
    for book in books:
        if (book.title == search) or (book.isbn == search) or (book.author == search):
            ibn = book.isbn
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"CF3VCiRggrJxSHGXt1xfw","isbn": ibn })
            #data = res.json()
            #rating = data["books"][0]["average_rating"]
            #ratings = data["books"][0]["work_ratings_count"]
            rating = "Hi"
            ratings = 5
            return render_template("book.html",title=book.title,author=book.author,year=book.year,isbn=book.isbn, rating=rating, ratings=ratings)
    return render_template("bookNotExist.html")
