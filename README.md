Updated version of the Books-Review-Mihir.

This one uses SQLAlchemy and Python OOPS concept instead of just regular SQL queries. 

Commented out the older code to show the difference.

Website Informtion:

Registration: Users can register on the website, providing (at minimum) a username and password.


Login: Users, once registered, can log in to the website with their username and password.


Logout: Logged in users can log out of the site.


Import: Imported data from the file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one 
has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from web application, a program is written that takes the books and imports them into the PostgreSQL database. Table Structure is created in Models.py. Once the Tables are created I ran program by running python import.py to import the books into my database.


Search: Once a user has logged in, they are taken to a page where they can search for a book. Users can type in the ISBN number of a book, the title of a book, or the author of a book to make the search. After performing the search, website will display a list of possible matching results, or a message if there were no matches. If the user typed in only part of a title, ISBN, or author name, search page will find matches for those as well!


Book Page: When users click on a book from the results of the search page, they will be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.


Review Submission: On the book page, users can submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users cannot submit multiple reviews for the same book.


Goodreads Review Data: The book page also displays (if available) the average rating and number of ratings the work has received from Goodreads.


API Access: If users make a GET request to the website’s /api/books/<isbn> route, where <isbn> is an ISBN number, website will return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. 
