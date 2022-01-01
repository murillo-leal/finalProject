# Don Hermano
## Video Demo: <https://www.youtube.com/watch?v=0QWu7rF3h4M>
## Final project to CS50x
## Description: 

## Don Hermano WebStore 
Technologies used:
-Flask
-Python
-CSS
-Bootstrap
-WTForms
-Peewee
-Werkzeug

## How the webpage works?

It's a online web store, where you can buy the best mexican food.
Must be registered on the site to buy
with:
email
address
telephone
Name

Admin user can edit products details, price and storage.

## Routing
You can see the products but can't buy it without logged in, so some routes checks if the user is authenticated and if is administrator
I decided to made a simple web page, wich not much visual details. So user can come and buy it easily.


## Database
Database stores all users, orders, buy history and products. I used order as a foreign table to  User and Order. Now that's an MVP, but later i will implement some extra reports
to the administration
Admin's have all control to products storage and details.

## How to launch it
Requirements

Python 3
Pip (Python package manager)

Installation
pip install -r requirement.txt

python application.py




