# books_app
-----------------------------------------------------------------

Simple API that enables users to manage the books they've read.

User can add, delete,retrieve and list books created by them.


Requirements
-----------------------------------------------------------------
- Docker
	https://docs.docker.com/compose/install/
- MySql
	https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/

As in Dockerfile:
- virtualenv
	$ pip install virtualenv
	$ source ./env/bin/activate

- Requirements file: requiremets.txt
	$ pip install -r requirements.txt


Setup
-----------------------------------------------------------------
Run Docker:

$ docker build -t books_app .
$ docker-compose up --build
$ docker-compose up
	> $ docker-compose up db -> start db container
	> $ docker-compose up web -> start books_app container

Run App (no Docker):
$ python3 manage.py runserver


Usage
-----------------------------------------------------------------
UserProfile views:
(Screenshots included in this same directory.)
- List:
	/books_app/users/
	> Lists all users.
- Retrieve:
    /books_app/books/<pk>/
    > Retrieves user record where pk is primary key for a user.
- Delete:
	/books_app/user/<pk>/
	> Delete user where pk is primary key for a user.

Books views:
(Screenshots included in this same directory.)
- List:
	/books_app/books/
	> Lists all books
	/books_app/books/?days_ago=<int>
	> List all books added by user within last <int> number of days
- Retrieve:
    /books_app/books/<pk>/
    > Retrieves book record where pk is primary key for a book.
- Delete:
	/books_app/books/<pk>/
	> Delete book where pk is primary key for a book.  
