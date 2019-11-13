import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
	__tablename__ = "books"
	isbn = db.Column(db.String, primary_key = True, nullable = False)
	title =  db.Column(db.String, nullable=False)
	author = db.Column(db.String, nullable=False)
	year = db.Column(db.Integer, nullable=False)
	reviews = db.relationship("Review", backref = "Book", lazy = True)

class User(db.Model):
	__tablename__ = "users"
	email = db.Column(db.String, primary_key=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	review = db.relationship("Review", backref = "User", lazy=True)

class Review(db.Model):
	__tablename__ = "reviews"
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer, nullable=False)
	review = db.Column(db.String)
	book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
	user_email = db.Column(db.String, db.ForeignKey("users.email"), nullable=False)