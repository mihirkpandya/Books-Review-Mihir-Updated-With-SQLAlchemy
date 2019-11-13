import os
import requests

from flask import Flask, session, render_template, request, url_for, redirect
from flask_login import logout_user
from flask_session import Session
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/account" , methods = ["POST"])
def account():
	current_user = User(email = request.form.get("emailaddress"), 
		password = request.form.get("password"))
	# emailaddress = request.form.get("emailaddress")
	# password = request.form.get("password")
	if request.form['submit'] == 'register':
		user_found = User.query.filter(and_(User.email == current_user.email)).first()
		# user = db.execute("SELECT * FROM USERS WHERE EMAIl= :emailaddress",
		# 	{"emailaddress": emailaddress}).fetchone()
		if user_found is None:
			db.session.add(current_user)
			# db.execute("INSERT INTO USERS (email, password) VALUES (:emailaddress, crypt(:password, gen_salt('bf')))",
			# 	{"emailaddress":emailaddress, "password": password})
			db.session.commit()
			session['username'] = current_user.email
			return render_template("account.html", emailaddress= session['username'], 
				value="Account Created. Now you can search for books!")
		else:
			return render_template("index.html", message = "Email Address is Taken")
	elif request.form['submit'] == 'signin':
		user_found = User.query.filter(and_(User.email == current_user.email,
			User.password == current_user.password)).first()
		# user = db.execute("SELECT * FROM USERS WHERE email = :emailaddress AND password = crypt(:password, password)",
		# 	{"emailaddress": emailaddress, "password": password}).fetchone()
		if user_found is None:
			return render_template("index.html", message = "Wrong email or password")
		else:
			session['username'] = current_user.email
			return render_template("account.html", emailaddress= session['username'], 
				value="Welcome back to your account")

@app.route("/logout", methods = ["POST"])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route("/search", methods = ["POST", "GET"])
def search():
	if session.get('username') is None:
		return redirect(url_for('index'))

	searchquery = '%' + request.form.get("searchquery") + '%'
	results = Book.query.filter(or_(Book.isbn.like(searchquery), 
		Book.title.like(searchquery), Book.author.like(searchquery))).all()	
	# results = db.execute("SELECT * FROM BOOKS WHERE (isbn like :searchquery) OR (title like :searchquery) OR (author like :searchquery)", 
	# 	{"searchquery": searchquery}).fetchall()
	return render_template("account.html", emailaddress = session['username'], results = results)

@app.route("/book/<string:isbn>", methods = ["POST", "GET"])
def book(isbn):
	if session.get('username') is None:
		return redirect(url_for('index'))
	check_for_review = Review.query.filter(Review.book_isbn==isbn, 
		Review.user_email == session['username']).first()
	# check_for_review = db.execute("SELECT * FROM REVIEWS where book_isbn = :isbn AND user_email = :emailaddress", 
	# 	{"isbn": isbn, "emailaddress": session['username']}).fetchone()
	if check_for_review is None:
		reviewed = False
	else:
		reviewed = True
	if request.method == "POST":
		if reviewed == False:
			review = Review(rating = request.form.get("rating"), 
				review = request.form.get("review"), book_isbn = isbn, 
				user_email = session['username'])
			reviewed = True
			# rating = request.form.get("rating")
			# review = request.form.get("review")
			db.session.add(review)
			# db.execute("INSERT INTO REVIEWS(rating, review, book_isbn, user_email) VALUES (:rating, :review, :isbn, :emailaddress)",
			# 	{"rating":rating, "review":review, "isbn":isbn, "emailaddress": session['username']})
			db.session.commit()
			# db.commit()
	
	res = requests.get("https://www.goodreads.com/book/review_counts.json", 
		params={"key": "lU7QgX5713AaMvWBNqdcg", "isbns": isbn})


	result = Book.query.filter(Book.isbn==isbn).first()
	# result = db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn", 
	# 	{"isbn" : isbn}).fetchone()

	reviews = result.reviews
	# reviews = db.execute("SELECT * FROM REVIEWS WHERE book_isbn = :isbn AND user_email != :emailaddress", {
	# 	"isbn" : isbn, "emailaddress": session['username']}).fetchall() 
	return render_template("book.html", result = result , goodreads = res, 
		your_review = check_for_review, reviews = reviews, reviewed = reviewed, 
		emailaddress= session['username'])




